import { Button } from "@/components/ui/button";
import { useNavigate } from "react-router-dom";

export default function PromoSlide() {
  const navigate = useNavigate();

  return (
    <div className="bg-white rounded-xl p-10 grid grid-cols-2 gap-6">
      <div>
        <span className="text-green-500 font-semibold">
          ⚡ Super Fast Delivery
        </span>
        <h2 className="text-4xl font-bold mt-4">
          Fresh Groceries in 20 mins
        </h2>
        <p className="text-gray-600 mt-2">
          Daily essentials from nearby stores
        </p>

        <div className="mt-6 flex gap-4">
          <Button onClick={() => navigate("/products")}>Shop Now</Button>
          <Button variant="outline" onClick={() => navigate("/products?offers=1")}>View Offers</Button>
        </div>
      </div>

      <img
        src="/hero.png"
        className="rounded-xl"
        alt="Groceries"
      />
    </div>
  );
}
