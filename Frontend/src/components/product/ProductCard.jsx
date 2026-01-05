import { Button } from "@/components/ui/button";

export default function ProductCard({ product }) {
  return (
    <div className="bg-white p-3 rounded-xl">
      <img
        src={product.image || "/product.jpg"}
        alt={product.title}
      />

      <h4 className="text-sm font-medium mt-2">
        {product.title}
      </h4>

      <p className="text-green-600 font-semibold">
        ₹{product.price}
      </p>

      <Button size="sm" className="mt-2 w-full">
        + Add
      </Button>
    </div>
  );
}
