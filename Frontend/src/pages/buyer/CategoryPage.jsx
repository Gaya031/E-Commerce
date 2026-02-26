import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

import Footer from "../../components/footer/Footer";
import Navbar from "../../components/navbar/Navbar";
import ProductCard from "../../components/product/ProductCard";
import { getCategoryBySlug, getCategoryProducts } from "../../api/category.api";

export default function CategoryPage() {
  const { slug } = useParams();
  const [category, setCategory] = useState(null);
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    let mounted = true;
    const load = async () => {
      setLoading(true);
      setError("");
      try {
        const categoryRes = await getCategoryBySlug(slug);
        if (!mounted) return;
        setCategory(categoryRes.data);

        const productsRes = await getCategoryProducts(categoryRes.data.id);
        if (!mounted) return;
        setProducts(Array.isArray(productsRes.data) ? productsRes.data : []);
      } catch (err) {
        if (!mounted) return;
        setError(err?.response?.data?.detail || "Failed to load category");
      } finally {
        if (mounted) setLoading(false);
      }
    };

    load();
    return () => {
      mounted = false;
    };
  }, [slug]);

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <div className="max-w-7xl mx-auto px-4 py-8">
        {loading ? (
          <p>Loading category...</p>
        ) : error ? (
          <p className="text-red-600 text-sm">{error}</p>
        ) : (
          <>
            <h1 className="text-2xl font-bold mb-2">{category?.name}</h1>
            {category?.description && <p className="text-gray-600 mb-6">{category.description}</p>}
            {products.length === 0 ? (
              <p className="text-gray-600">No products available in this category.</p>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                {products.map((p) => (
                  <ProductCard key={p.id} product={p} />
                ))}
              </div>
            )}
          </>
        )}
      </div>
      <Footer />
    </div>
  );
}
