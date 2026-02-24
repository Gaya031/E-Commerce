import React from 'react'

const PaymentMethod = () => {
  const [method, setMethod] = useState("upi");

  return (
    <div className="bg-white p-6 rounded-xl">
      <h2 className="font-semibold mb-4">3. Payment Method</h2>

      {[
        { id: "upi", label: "UPI", desc: "Google Pay, PhonePe, Paytm" },
        { id: "card", label: "Credit / Debit Card" },
        { id: "cod", label: "Cash on Delivery" },
      ].map(opt => (
        <div
          key={opt.id}
          onClick={() => setMethod(opt.id)}
          className={`border p-4 rounded-xl mb-3 cursor-pointer ${
            method === opt.id
              ? "border-green-500 bg-green-50"
              : "border-gray-200"
          }`}
        >
          <b>{opt.label}</b>
          <p className="text-sm text-gray-600">{opt.desc}</p>
        </div>
      ))}
    </div>
  );
}

export default PaymentMethod