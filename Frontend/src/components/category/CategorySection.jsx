import { useEffect, useState } from "react";
import CategoryCard from "./CategoryCard";
import { getAllCategories } from "@/api/category.api";

const defaultCategories = [
  "Vegetables",
  "Fruits",
  "Dairy",
  "Bakery",
  "Care",
  "Home",
  "Snacks",
];

const slugify = (name) =>
  String(name || "")
    .trim()
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "");

export default function CategorySection() {
  const [categories, setCategories] = useState(defaultCategories);

  useEffect(() => {
    getAllCategories()
      .then(res => {
        if (res.data && res.data.length > 0) {
          setCategories(res.data);
        }
      })
      .catch(err => console.error("Error fetching categories:", err));
  }, []);

  return (
    <section className="max-w-7xl mx-auto px-4 mt-10">
      <h3 className="font-semibold mb-4">Shop by Category</h3>
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
