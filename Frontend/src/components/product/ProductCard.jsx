import { Button } from "@/components/ui/button";

export default function ProductCard() {
  return (
    <div className="bg-white p-3 rounded-xl">
      <img src="/product.jpg" alt="product" />
      <h4 className="text-sm font-medium mt-2">
        Fresh Milk 1L
      </h4>
      <p className="text-green-600 font-semibold">₹60</p>
      <Button size="sm" className="mt-2 w-full">
        + Add
      </Button>
    </div>
  );
}
