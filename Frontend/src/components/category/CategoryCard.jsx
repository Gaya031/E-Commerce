import { Link } from "react-router-dom";

export default function CategoryCard({ title, slug, image }) {
  return (
    <Link to={`/category/${slug}`} className="text-center cursor-pointer block min-w-[88px]">
      {image ? (
        <img src={image} alt={title} className="w-20 h-20 rounded-full object-cover mx-auto border border-green-100" />
      ) : (
        <div className="w-20 h-20 rounded-full bg-green-100 mx-auto" />
      )}
      <p className="mt-2 text-sm">{title}</p>
    </Link>
  );
}
