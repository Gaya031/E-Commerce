import React from 'react'
import { useEffect } from "react";
import { useSearchParams, useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { useCartStore } from "../../store/cart.store";

const OrderSuccess = () => {
  const [params] = useSearchParams();
  const navigate = useNavigate();
  const clearCart = useCartStore((s) => s.clearCart);

  const orderId = params.get("orderId");

  // Clear cart ONCE when page loads
  useEffect(() => {
    clearCart();
  }, [clearCart]);

  if (!orderId) {
    return (
      <div className="max-w-3xl mx-auto p-8 text-center">
        <h1 className="text-xl font-semibold">Invalid Order</h1>
        <Button className="mt-4" onClick={() => navigate("/")}>
          Go Home
        </Button>
      </div>
    );
  }

  return (
    <div className="max-w-3xl mx-auto px-6 py-16 text-center">
      {/* Success Icon */}
      <div className="w-20 h-20 mx-auto rounded-full bg-green-100 flex items-center justify-center text-green-600 text-3xl">
        ✓
      </div>

      <h1 className="text-2xl font-bold mt-6">
        Order Placed Successfully!
      </h1>

      <p className="text-gray-600 mt-2">
        Thank you for shopping with RushCart. Your order has been confirmed.
      </p>

      {/* Order Details */}
      <div className="bg-white rounded-xl shadow-sm p-6 mt-8 text-left">
        <div className="flex justify-between mb-2">
          <span className="text-gray-500">Order ID</span>
          <span className="font-medium">#{orderId}</span>
        </div>

        <div className="flex justify-between mb-2">
          <span className="text-gray-500">Delivery</span>
          <span className="font-medium">30–45 minutes</span>
        </div>

        <div className="flex justify-between">
          <span className="text-gray-500">Payment</span>
          <span className="font-medium">Confirmed</span>
        </div>
      </div>
    {/* Actions */}
      <div className="flex justify-center gap-4 mt-10">
        <Button
          variant="outline"
          onClick={() => navigate("/buyer/orders")}
        >
          View Orders
        </Button>

        <Button onClick={() => navigate("/")}>
          Continue Shopping
        </Button>
      </div>

      {/* Footer hint */}
      <p className="text-sm text-gray-500 mt-6">
        You will receive order updates via notification.
      </p>
    </div>
  );
}

export default OrderSuccess
