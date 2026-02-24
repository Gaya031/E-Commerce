import React from 'react'
import { useCartStore } from "../../store/cart.store";

const CartHeader = () => {
  const items = useCartStore(s => s.items);
  const count = items.reduce((sum, i) => sum + i.quantity, 0);

  return (
    <div>
      <p className="text-sm text-gray-500">Home / Cart</p>
      <h1 className="text-2xl font-bold mt-1">
        Your Shopping Cart ({count} items)
      </h1>
    </div>
  );
}

export default CartHeader