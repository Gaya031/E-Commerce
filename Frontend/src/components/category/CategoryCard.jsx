export default function CategoryCard({ title }) {
  return (
    <div className="text-center cursor-pointer">
      <div className="w-20 h-20 rounded-full bg-green-100 mx-auto" />
      <p className="mt-2 text-sm">{title}</p>
    </div>
  );
}
