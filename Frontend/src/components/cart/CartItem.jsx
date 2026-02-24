import React from "react";
import { Button } from "@/components/ui/button";
import { useCartStore } from "../../store/cart.store";

const CartItem = () => {
  const updateQuantity = useCartStore((s) => s.updateQuantity);

  return (
    <div className="bg-white p-4 rounded-xl flex gap-4">
      <img
        src={item.image}
        alt={item.title}
        className="w-20 h-20 object-cover rounded"
      />

      <div className="flex-1">
        <h3 className="font-semibold">{item.title}</h3>
        <p className="text-sm text-gray-500">₹{item.price}</p>

        <div className="flex gap-4 mt-2 text-sm text-gray-600">
          <button
            className="text-red-500"
            onClick={() => updateQuantity(item.productId, 0)}
          >
            Remove
          </button>
          <button className="text-green-600">Save for later</button>
        </div>
      </div>

      <div className="flex items-center gap-2">
        <Button
          size="sm"
          onClick={() => updateQuantity(item.productId, item.quantity - 1)}
        >
          -
        </Button>
        <span>{item.quantity}</span>
        <Button
          size="sm"
          onClick={() => updateQuantity(item.productId, item.quantity + 1)}
        >
          +
        </Button>
      </div>
    </div>
  );
};

export default CartItem;
