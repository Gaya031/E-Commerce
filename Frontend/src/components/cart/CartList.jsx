import React from 'react'
import { useCartStore } from "../../store/cart.store";
import CartItem from "./CartItem";

const CartList = () => {
  const items = useCartStore(s => s.items);

  if (!items.length) {
    return (
      <div className="bg-white p-6 rounded-xl text-center">
        Your cart is empty
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {items.map(item => (
        <CartItem key={item.productId} item={item} />
      ))}
    </div>
  );
}

export default CartList