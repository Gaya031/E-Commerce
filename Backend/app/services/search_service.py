from __future__ import annotations

from typing import Any

import httpx
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.logging import logger
from app.models.product_model import Product
from app.models.seller_model import Seller
from app.utils.simple_cache import cache_get, cache_set

_es_client: httpx.AsyncClient | None = None


def _base_url() -> str:
    return settings.ELASTICSEARCH_URL.rstrip("/")


def _get_es_client() -> httpx.AsyncClient:
    global _es_client
    if _es_client is None:
        timeout = httpx.Timeout(settings.ELASTICSEARCH_TIMEOUT_SECONDS)
        _es_client = httpx.AsyncClient(timeout=timeout)
    return _es_client


async def close_search_client() -> None:
    global _es_client
    if _es_client is not None:
        await _es_client.aclose()
        _es_client = None


async def _es_request(method: str, path: str, **kwargs) -> httpx.Response | None:
    url = f"{_base_url()}{path}"
    try:
        client = _get_es_client()
        return await client.request(method, url, **kwargs)
    except Exception as exc:
        logger.warning("Elasticsearch request failed (%s %s): %s", method, path, str(exc))
        return None


async def ensure_search_indices() -> None:
    product_mapping = {
        "mappings": {
            "properties": {
                "id": {"type": "integer"},
                "seller_id": {"type": "integer"},
                "title": {"type": "text"},
                "description": {"type": "text"},
                "category": {"type": "text"},
                "price": {"type": "integer"},
                "image_url": {"type": "keyword"},
                "store_name": {"type": "text"},
                "is_active": {"type": "boolean"},
            }
        }
    }
    store_mapping = {
        "mappings": {
            "properties": {
                "id": {"type": "integer"},
                "store_name": {"type": "text"},
                "description": {"type": "text"},
                "logo_url": {"type": "keyword"},
                "banner_url": {"type": "keyword"},
                "city": {"type": "text"},
                "address": {"type": "text"},
                "approved": {"type": "boolean"},
                "rating": {"type": "float"},
                "total_reviews": {"type": "integer"},
            }
        }
    }

    for index_name, mapping in (
        (settings.ELASTICSEARCH_PRODUCTS_INDEX, product_mapping),
        (settings.ELASTICSEARCH_STORES_INDEX, store_mapping),
    ):
        head = await _es_request("HEAD", f"/{index_name}")
        if head is None:
            continue
        if head.status_code == 200:
            continue

        put = await _es_request("PUT", f"/{index_name}", json=mapping)
        if put is None:
            continue
        if put.status_code not in (200, 201):
            logger.warning("Failed to create Elasticsearch index '%s': %s", index_name, put.text)


async def _upsert_document(index: str, doc_id: int, payload: dict[str, Any]) -> None:
    response = await _es_request("PUT", f"/{index}/_doc/{doc_id}", json=payload)
    if response is None:
        return

    if response.status_code in (200, 201):
        return

    # If index is missing, create it once and retry.
    if response.status_code == 404:
        await ensure_search_indices()
        retry = await _es_request("PUT", f"/{index}/_doc/{doc_id}", json=payload)
        if retry is None:
            return
        if retry.status_code in (200, 201):
            return
        logger.warning("Elasticsearch upsert retry failed for %s/%s: %s", index, doc_id, retry.text)
        return

    logger.warning("Elasticsearch upsert failed for %s/%s: %s", index, doc_id, response.text)


async def _delete_document(index: str, doc_id: int) -> None:
    response = await _es_request("DELETE", f"/{index}/_doc/{doc_id}")
    if response is None:
        return
    if response.status_code in (200, 202, 404):
        return
    logger.warning("Elasticsearch delete failed for %s/%s: %s", index, doc_id, response.text)


def _product_to_doc(product: Product, seller: Seller | None) -> dict[str, Any]:
    image_url = product.images[0] if isinstance(product.images, list) and product.images else None
    return {
        "id": product.id,
        "seller_id": product.seller_id,
        "title": product.title,
        "description": product.description,
        "category": product.category,
        "price": int(product.price),
        "image_url": image_url,
        "store_name": seller.store_name if seller else None,
        "is_active": bool(product.is_active),
    }


def _seller_to_doc(seller: Seller) -> dict[str, Any]:
    return {
        "id": seller.id,
        "store_name": seller.store_name,
        "description": seller.description,
        "logo_url": seller.logo_url,
        "banner_url": seller.cover_image,
        "city": seller.city,
        "address": seller.address,
        "approved": bool(seller.approved),
        "rating": float(seller.average_rating or 0),
        "total_reviews": int(seller.total_reviews or 0),
    }


async def upsert_product_document(db: AsyncSession, product_id: int) -> None:
    product = await db.get(Product, product_id)
    if not product:
        await _delete_document(settings.ELASTICSEARCH_PRODUCTS_INDEX, product_id)
        return

    if not product.is_active:
        await _delete_document(settings.ELASTICSEARCH_PRODUCTS_INDEX, product_id)
        return

    seller = await db.get(Seller, product.seller_id)
    await _upsert_document(
        settings.ELASTICSEARCH_PRODUCTS_INDEX,
        product_id,
        _product_to_doc(product, seller),
    )


async def upsert_store_document(db: AsyncSession, seller_id: int) -> None:
    seller = await db.get(Seller, seller_id)
    if not seller:
        await _delete_document(settings.ELASTICSEARCH_STORES_INDEX, seller_id)
        return

    await _upsert_document(settings.ELASTICSEARCH_STORES_INDEX, seller_id, _seller_to_doc(seller))


async def _search_es(index: str, query: dict[str, Any]) -> list[dict[str, Any]] | None:
    response = await _es_request("POST", f"/{index}/_search", json=query)
    if response is None:
        return None
    if response.status_code != 200:
        logger.warning("Elasticsearch search failed for %s: %s", index, response.text)
        return None

    try:
        body = response.json()
        hits = body.get("hits", {}).get("hits", [])
        return [h.get("_source", {}) for h in hits]
    except Exception as exc:
        logger.warning("Failed parsing Elasticsearch response for %s: %s", index, str(exc))
        return None


def _product_brief(source: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": source.get("id"),
        "name": source.get("title"),
        "price": source.get("price"),
        "image_url": source.get("image_url"),
    }


def _product_full(source: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": source.get("id"),
        "seller_id": source.get("seller_id"),
        "name": source.get("title"),
        "description": source.get("description"),
        "price": source.get("price"),
        "original_price": source.get("price"),
        "image_url": source.get("image_url"),
        "rating": 0,
        "review_count": 0,
    }


def _store_full(source: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": source.get("id"),
        "store_name": source.get("store_name"),
        "description": source.get("description"),
        "logo_url": source.get("logo_url"),
        "banner_url": source.get("banner_url"),
        "rating": source.get("rating") or 0,
        "total_reviews": source.get("total_reviews") or 0,
    }


async def _search_products_db(db: AsyncSession, q: str, page: int, size: int) -> list[dict[str, Any]]:
    offset = (page - 1) * size
    result = await db.execute(
        select(Product)
        .where(
            Product.is_active == True,
            or_(
                Product.title.ilike(f"%{q}%"),
                Product.description.ilike(f"%{q}%"),
                Product.category.ilike(f"%{q}%"),
            ),
        )
        .offset(offset)
        .limit(size)
    )
    products = result.scalars().all()

    rows: list[dict[str, Any]] = []
    for p in products:
        image_url = p.images[0] if isinstance(p.images, list) and p.images else None
        rows.append(
            {
                "id": p.id,
                "seller_id": p.seller_id,
                "name": p.title,
                "description": p.description,
                "price": p.price,
                "original_price": p.price,
                "image_url": image_url,
                "rating": p.average_rating,
                "review_count": 0,
            }
        )
    return rows


async def _search_stores_db(db: AsyncSession, q: str, page: int, size: int) -> list[dict[str, Any]]:
    offset = (page - 1) * size
    result = await db.execute(
        select(Seller)
        .where(
            Seller.approved == True,
            or_(
                Seller.store_name.ilike(f"%{q}%"),
                Seller.description.ilike(f"%{q}%"),
                Seller.city.ilike(f"%{q}%"),
            ),
        )
        .offset(offset)
        .limit(size)
    )
    stores = result.scalars().all()

    return [
        {
            "id": s.id,
            "store_name": s.store_name,
            "description": s.description,
            "logo_url": s.logo_url,
            "banner_url": s.cover_image,
            "rating": s.average_rating,
            "total_reviews": s.total_reviews,
        }
        for s in stores
    ]


async def search_products(db: AsyncSession, q: str, page: int = 1, size: int = 20) -> dict[str, Any]:
    cache_key = f"search:products:{q.strip().lower()}:{page}:{size}"
    cached = await cache_get(cache_key)
    if cached is not None:
        return cached

    offset = (page - 1) * size
    query = {
        "from": offset,
        "size": size,
        "query": {
            "bool": {
                "must": [
                    {
                        "multi_match": {
                            "query": q,
                            "fields": ["title^3", "description", "category", "store_name^2"],
                            "fuzziness": "AUTO",
                        }
                    }
                ],
                "filter": [{"term": {"is_active": True}}],
            }
        },
    }
    hits = await _search_es(settings.ELASTICSEARCH_PRODUCTS_INDEX, query)
    if hits:
        payload = {"products": [_product_full(h) for h in hits]}
        await cache_set(cache_key, payload, ttl_seconds=30)
        return payload

    payload = {"products": await _search_products_db(db, q, page, size)}
    await cache_set(cache_key, payload, ttl_seconds=30)
    return payload


async def search_stores(db: AsyncSession, q: str, page: int = 1, size: int = 20) -> dict[str, Any]:
    cache_key = f"search:stores:{q.strip().lower()}:{page}:{size}"
    cached = await cache_get(cache_key)
    if cached is not None:
        return cached

    offset = (page - 1) * size
    query = {
        "from": offset,
        "size": size,
        "query": {
            "bool": {
                "must": [
                    {
                        "multi_match": {
                            "query": q,
                            "fields": ["store_name^3", "description", "city", "address"],
                            "fuzziness": "AUTO",
                        }
                    }
                ],
                "filter": [{"term": {"approved": True}}],
            }
        },
    }
    hits = await _search_es(settings.ELASTICSEARCH_STORES_INDEX, query)
    if hits:
        payload = {"stores": [_store_full(h) for h in hits]}
        await cache_set(cache_key, payload, ttl_seconds=30)
        return payload

    payload = {"stores": await _search_stores_db(db, q, page, size)}
    await cache_set(cache_key, payload, ttl_seconds=30)
    return payload


async def global_search(db: AsyncSession, q: str) -> dict[str, Any]:
    cache_key = f"search:global:{q.strip().lower()}"
    cached = await cache_get(cache_key)
    if cached is not None:
        return cached

    products = await search_products(db=db, q=q, page=1, size=10)
    stores = await search_stores(db=db, q=q, page=1, size=10)

    payload = {
        "products": [
            {
                "id": p.get("id"),
                "name": p.get("name"),
                "price": p.get("price"),
                "image_url": p.get("image_url"),
            }
            for p in products.get("products", [])
        ],
        "stores": [
            {
                "id": s.get("id"),
                "store_name": s.get("store_name"),
                "logo_url": s.get("logo_url"),
            }
            for s in stores.get("stores", [])
        ],
    }
    await cache_set(cache_key, payload, ttl_seconds=20)
    return payload
