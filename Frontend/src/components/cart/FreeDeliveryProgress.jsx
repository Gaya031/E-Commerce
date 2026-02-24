import React from 'react'
import { useCartStore } from "../../store/cart.store";

const FREE_DELIVERY_THRESHOLD = 200;

const FreeDeliveryProgress = () => {
  const total = useCartStore(s => s.totalAmount)();
  const remaining = Math.max(FREE_DELIVERY_THRESHOLD - total, 0);
  const percent = Math.min((total / FREE_DELIVERY_THRESHOLD) * 100, 100);

  return (
    <div className="bg-green-50 p-4 rounded-xl">
      <p className="text-sm mb-2">
        {remaining > 0
          ? `Spend ₹${remaining} more for free delivery`
          : "You have unlocked free delivery 🎉"}
      </p>

      <div className="w-full bg-green-100 h-2 rounded">
        <div
          className="bg-green-500 h-2 rounded"
          style={{ width: `${percent}%` }}
        />
      </div>
    </div>
  );
}

export default FreeDeliveryProgress