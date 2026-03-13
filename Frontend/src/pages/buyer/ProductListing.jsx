import { useEffect, useMemo, useState } from "react";
import { useSearchParams } from "react-router-dom";
import Navbar from "../../components/navbar/Navbar";
import Footer from "../../components/footer/Footer";
import ProductCard from "../../components/product/ProductCard";
import { getAllProducts } from "../../api/product.api";
import { searchProducts as searchProductsApi } from "../../api/search.api";

export default function ProductListing() {
  const [searchParams] = useSearchParams();
  const query = (searchParams.get("q") || "").trim();
  const offersOnly = searchParams.get("offers") === "1";

  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    let mounted = true;
    setLoading(true);
    setError("");

    const load = async () => {
      try {
        if (query) {
          const res = await searchProductsApi(query);
          if (!mounted) return;
          const rows = Array.isArray(res.data?.products) ? res.data.products : [];
          setProducts(
            rows.map((p) => ({
              id: p.id,
              seller_id: p.seller_id,
              title: p.name,
              description: p.description,
              price: p.price,
              image: p.image_url,
            }))
          );
          return;
        }

        const res = await getAllProducts();
        if (!mounted) return;
        const rows = Array.isArray(res.data) ? res.data : [];
        if (offersOnly) {
          const sorted = [...rows].sort((a, b) => Number(a.price || 0) - Number(b.price || 0));
          setProducts(sorted.slice(0, 20));
          return;
        }
        setProducts(rows);
      } catch (err) {
        if (!mounted) return;
        setError(err?.response?.data?.detail || "Failed to load products");
      } finally {
        if (mounted) setLoading(false);
      }
    };

    load();

    return () => {
      mounted = false;
    };
  }, [offersOnly, query]);

  const title = useMemo(() => {
    if (query) return `Search results for "${query}"`;
    if (offersOnly) return "Best Offers";
    return "All Products";
  }, [offersOnly, query]);

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <div className="max-w-7xl mx-auto px-4 py-8">
        <h1 className="text-2xl font-bold mb-6">{title}</h1>
        {error && <p className="text-sm text-red-600 mb-3">{error}</p>}

        {loading ? (
          <p>Loading products...</p>
        ) : products.length === 0 ? (
          <p className="text-gray-600">No products found.</p>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {products.map((p) => (
              <ProductCard key={p.id} product={p} />
            ))}
          </div>
        )}
      </div>
      <Footer />
    </div>
  );
}
