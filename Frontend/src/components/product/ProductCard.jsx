import { Button } from "@/components/ui/button";
import { useCartStore } from "@/store/cart.store";
import { useParams } from "react-router-dom";

export default function ProductCard({ product }) {
  const { storeId } = useParams();
  const addItem = useCartStore((s) => s.addItem);
  return (
    <div className="bg-white p-3 rounded-xl">
      <img src={product.image || "/product.jpg"} alt={product.title} />

      <h4 className="text-sm font-medium mt-2">{product.title}</h4>

      <p className="text-green-600 font-semibold">₹{product.price}</p>

      <Button
        size="sm"
        className="mt-2 w-full"
        onClick={() => addItem(Number(storeId), product)}
      >
        + Add
      </Button>
    </div>
  );
}
