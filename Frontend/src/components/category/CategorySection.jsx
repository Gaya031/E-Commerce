import CategoryCard from "./CategoryCard";

const categories = [
  "Vegetables",
  "Fruits",
  "Dairy",
  "Bakery",
  "Care",
  "Home",
  "Snacks",
];

export default function CategorySection() {
  return (
    <section className="max-w-7xl mx-auto px-4 mt-10">
      <h3 className="font-semibold mb-4">Shop by Category</h3>
      <div className="flex gap-6">
        {categories.map(c => (
          <CategoryCard key={c} title={c} />
        ))}
      </div>
    </section>
  );
}
