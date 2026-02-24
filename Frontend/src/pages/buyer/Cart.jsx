import React from 'react'
import { useCartStore } from "../../store/cart.store";
import { Button } from "@/components/ui/button";

const Cart = () => {
  const items = useCartStore(s => s.items);
  const updateQuantity = useCartStore(s => s.updateQuantity);
  const total = useCartStore(s => s.totalAmount);

  if (!items.length)
    return <p className="p-6">Cart is empty</p>;

  return (
    <div className="max-w-4xl mx-auto p-6">
      <h2 className="text-xl font-bold mb-6">Your Cart</h2>

      {items.map(i => (
        <div
          key={i.productId}
          className="flex justify-between items-center mb-4"
        >
          <div>
            <p>{i.title}</p>
            <p className="text-sm text-gray-500">
              ₹{i.price}
            </p>
          </div>

          <div className="flex gap-2 items-center">
            <Button
              size="sm"
              onClick={() =>
                updateQuantity(i.productId, i.quantity - 1)
              }
            >
              -
            </Button>
            <span>{i.quantity}</span>
            <Button
              size="sm"
              onClick={() =>
                updateQuantity(i.productId, i.quantity + 1)
              }
            >
              +
            </Button>
          </div>
        </div>
      ))}

      <div className="mt-6 font-semibold">
        Total: ₹{total()}
      </div>

      <Button className="mt-4 w-full">
        Proceed to Checkout
      </Button>
    </div>
  );
}

export default Cart