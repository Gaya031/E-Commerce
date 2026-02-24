import React from 'react'
import { Button } from "@/components/ui/button";
import { useCartStore } from "../../store/cart.store";
import { useNavigate } from "react-router-dom";

const DELIVERY_FEE = 20;
const TAX = 5;
const FREE_DELIVERY_THRESHOLD = 200;
const OrderSummary = () => {
  const total = useCartStore(s => s.totalAmount)();
  const navigate = useNavigate();

  const delivery =
    total >= FREE_DELIVERY_THRESHOLD ? 0 : DELIVERY_FEE;

  const finalTotal = total + delivery + TAX;

  return (
    <div className="bg-white p-6 rounded-xl sticky top-28">
      <h3 className="font-semibold mb-4">Order Summary</h3>

      <div className="space-y-2 text-sm">
        <div className="flex justify-between">
          <span>Subtotal</span>
          <span>₹{total}</span>
        </div>
        <div className="flex justify-between">
          <span>Delivery Fee</span>
          <span>₹{delivery}</span>
        </div>
        <div className="flex justify-between">
          <span>Taxes & Fees</span>
          <span>₹{TAX}</span>
        </div>
      </div>

      <div className="flex justify-between font-bold mt-4">
        <span>Total</span>
        <span>₹{finalTotal}</span>
      </div>

      <Button
        className="w-full mt-6"
        onClick={() => navigate("/checkout")}
      >
        Proceed to Checkout →
      </Button>
    </div>
  );
}

export default OrderSummary