import React from 'react'
import { useCartStore } from "../../store/cart.store";
import { Button } from "@/components/ui/button";

const PLATFORM_FEE = 1;
const TAX = 0.5;

const OrderSummary = () => {
  const items = useCartStore(s => s.items);
  const subtotal = useCartStore(s => s.totalAmount)();

  const total = subtotal + PLATFORM_FEE + TAX;

  return (
    <div className="bg-white p-6 rounded-xl sticky top-28">
      <h3 className="font-semibold mb-4">Your Order</h3>

      <div className="space-y-3 text-sm">
        {items.map(i => (
          <div key={i.productId} className="flex justify-between">
            <span>{i.title} × {i.quantity}</span>
            <span>${i.price * i.quantity}</span>
          </div>
        ))}
      </div>

      <hr className="my-4" />

      <div className="text-sm space-y-2">
        <div className="flex justify-between">
          <span>Item Total</span>
          <span>${subtotal}</span>
        </div>
        <div className="flex justify-between">
          <span>Delivery Fee</span>
          <span className="text-green-600">FREE</span>
        </div>
        <div className="flex justify-between">
          <span>Platform Fee</span>
          <span>${PLATFORM_FEE}</span>
        </div>
        <div className="flex justify-between">
          <span>Taxes</span>
          <span>${TAX}</span>
        </div>
      </div>

      <div className="flex justify-between font-bold text-lg mt-4">
        <span>To Pay</span>
        <span className="text-green-600">${total}</span>
      </div>

      <Button className="w-full mt-6">
        Place Order ${total}
      </Button>

      <p className="text-xs text-center text-gray-500 mt-2">
        Secure payments by Razorpay
      </p>
    </div>
  );
}

export default OrderSummary