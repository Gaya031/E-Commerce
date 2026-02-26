import React, { useState, useEffect } from 'react'
import { CreditCard, Smartphone, Banknote } from 'lucide-react';

const PaymentMethod = ({ onMethodSelect }) => {
  const [method, setMethod] = useState("prepaid");

  useEffect(() => {
    onMethodSelect?.(method);
  }, [method, onMethodSelect]);

  const paymentOptions = [
    { 
      id: "prepaid", 
      label: "Prepaid (UPI/Card/Wallet)", 
      icon: CreditCard,
      desc: "Pay now and get exclusive discounts"
    },
    { 
      id: "cod", 
      label: "Cash on Delivery", 
      icon: Banknote,
      desc: "Pay when you receive the order"
    },
  ];

  return (
    <div className="bg-white p-6 rounded-xl">
      <h2 className="font-semibold mb-4">3. Payment Method</h2>

      <div className="space-y-3">
        {paymentOptions.map(opt => {
          const Icon = opt.icon;
          return (
            <div
              key={opt.id}
              onClick={() => setMethod(opt.id)}
              className={`border p-4 rounded-xl cursor-pointer transition-all ${
                method === opt.id
                  ? "border-green-500 bg-green-50"
                  : "border-gray-200 hover:border-gray-300"
              }`}
            >
              <div className="flex items-center gap-3">
                <Icon className={`w-5 h-5 ${method === opt.id ? "text-green-600" : "text-gray-400"}`} />
                <div>
                  <b className={method === opt.id ? "text-green-700" : ""}>{opt.label}</b>
                  <p className="text-sm text-gray-500">{opt.desc}</p>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {method === "prepaid" && (
        <div className="mt-4 p-4 bg-amber-50 border border-amber-200 rounded-lg">
          <div className="flex items-center gap-2 text-amber-800">
            <Smartphone className="w-5 h-5" />
            <span className="font-medium">Save ₹25 on this order!</span>
          </div>
          <p className="text-sm text-amber-700 mt-1">
            Prepaid orders get free delivery + exclusive discounts
          </p>
        </div>
      )}
    </div>
  );
}

export default PaymentMethod
