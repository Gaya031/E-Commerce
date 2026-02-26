import { Button } from "@/components/ui/button";
import { useCartStore } from "@/store/cart.store";
import { useParams, Link } from "react-router-dom";

export default function ProductCard({ product }) {
  const { storeId } = useParams();
  const addItem = useCartStore((s) => s.addItem);
  
  const handleAddToCart = (e) => {
    e.preventDefault();
    e.stopPropagation();
    addItem(Number(storeId || product.seller_id), {
      ...product,
      image: product.image || product.images?.[0] || "/product.jpg",
    });
  };
  
  return (
    <Link to={`/product/${product.id}`} className="block bg-white p-3 rounded-xl hover:shadow-md transition-shadow">
      <img src={product.image || product.images?.[0] || "/product.jpg"} alt={product.title} className="w-full h-40 object-cover rounded-lg" />

      <h4 className="text-sm font-medium mt-2 line-clamp-2">{product.title}</h4>

      <p className="text-green-600 font-semibold">₹{product.price}</p>

      <Button
        size="sm"
        className="mt-2 w-full"
        onClick={handleAddToCart}
      >
        + Add
      </Button>
    </Link>
  );
}
