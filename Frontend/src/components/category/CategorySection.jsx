import { useEffect, useState } from "react";
import CategoryCard from "./CategoryCard";
import { getAllCategories } from "@/api/category.api";

const slugify = (name) =>
  String(name || "")
    .trim()
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "");

export default function CategorySection() {
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getAllCategories()
      .then(res => {
        const rows = Array.isArray(res?.data) ? res.data : [];
        const normalized = rows.filter((row) => Boolean(row?.name));
        setCategories(normalized);
      })
      .catch(err => console.error("Error fetching categories:", err))
      .finally(() => setLoading(false));
  }, []);

  return (
    <section className="max-w-7xl mx-auto px-4 mt-10">
      <h3 className="font-semibold mb-4">Shop by Category</h3>
      {loading && <p className="text-sm text-gray-500">Loading categories...</p>}
      {!loading && categories.length === 0 && (
        <p className="text-sm text-gray-500">No categories available right now.</p>
      )}
      <div className="flex gap-6 overflow-x-auto pb-2">
        {categories.map(c => (
          <CategoryCard 
            key={c.id || c} 
            title={c.name || c}
            slug={c.slug || slugify(c.name || c)}
            image={c.image_url || c.image}
          />
        ))}
      </div>
    </section>
  );
}
