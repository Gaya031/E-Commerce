from __future__ import annotations

from datetime import datetime, timezone

import httpx
from fastapi import APIRouter, Depends
from fastapi.responses import PlainTextResponse
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.observability import request_metrics
from app.db.postgres import get_db
from app.db.redis import get_redis

router = APIRouter(prefix="/system", tags=["system"])


@router.get("/health/live")
async def liveness() -> dict:
    return {
        "status": "ok",
        "service": settings.APP_NAME,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@router.get("/health/ready")
async def readiness(db: AsyncSession = Depends(get_db)) -> dict:
    checks = {
        "database": False,
        "redis": False,
        "elasticsearch": False,
    }

    try:
        await db.execute(text("SELECT 1"))
        checks["database"] = True
    except Exception:
        checks["database"] = False

    try:
        redis = await get_redis()
        checks["redis"] = bool(await redis.ping())
    except Exception:
        checks["redis"] = False

    try:
        timeout = httpx.Timeout(2.5)
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.get(settings.ELASTICSEARCH_URL.rstrip("/"))
        checks["elasticsearch"] = response.status_code < 500
    except Exception:
        checks["elasticsearch"] = False

    overall = "ready" if checks["database"] and checks["redis"] else "degraded"
    return {
        "status": overall,
        "service": settings.APP_NAME,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "checks": checks,
    }


@router.get("/metrics")
async def metrics() -> dict:
    return request_metrics.snapshot()


@router.get("/metrics/prometheus", response_class=PlainTextResponse)
async def metrics_prometheus() -> str:
    return request_metrics.prometheus_text()


@router.get("/alerts")
async def alerts() -> dict:
    snap = request_metrics.snapshot()
    alerts_list: list[dict] = []

    if snap["error_rate"] >= settings.ALERT_ERROR_RATE_THRESHOLD:
        alerts_list.append(
            {
                "severity": "high",
                "code": "HIGH_ERROR_RATE",
                "message": (
                    f"Error rate {snap['error_rate']:.2%} is above threshold "
                    f"{settings.ALERT_ERROR_RATE_THRESHOLD:.2%}"
                ),
            }
        )

    if snap["p95_duration_ms"] >= settings.ALERT_P95_MS_THRESHOLD:
        alerts_list.append(
            {
                "severity": "medium",
                "code": "HIGH_P95_LATENCY",
                "message": (
                    f"p95 latency {snap['p95_duration_ms']}ms is above threshold "
                    f"{settings.ALERT_P95_MS_THRESHOLD}ms"
                ),
            }
        )

    if snap["inflight_requests"] >= settings.ALERT_INFLIGHT_THRESHOLD:
        alerts_list.append(
            {
                "severity": "medium",
                "code": "HIGH_INFLIGHT_REQUESTS",
                "message": (
                    f"Inflight requests {snap['inflight_requests']} is above threshold "
                    f"{settings.ALERT_INFLIGHT_THRESHOLD}"
                ),
            }
        )

    return {
        "status": "alerting" if alerts_list else "ok",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "thresholds": {
            "error_rate": settings.ALERT_ERROR_RATE_THRESHOLD,
            "p95_duration_ms": settings.ALERT_P95_MS_THRESHOLD,
            "inflight_requests": settings.ALERT_INFLIGHT_THRESHOLD,
        },
        "alerts": alerts_list,
    }
