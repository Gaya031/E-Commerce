import React from 'react'

const CheckoutHeader = () => {
  return (
    <div className="flex justify-between items-center">
      <div>
        <p className="text-sm text-gray-500">
          Cart &gt; <span className="text-green-600">Checkout</span> &gt; Confirmation
        </p>
        <h1 className="text-2xl font-bold mt-1">Secure Checkout</h1>
        <p className="text-gray-600">
          Complete your order details below to get your fresh goods.
        </p>
      </div>

      <div className="text-green-600 font-medium flex items-center gap-2">
        🔒 100% Secure Checkout
      </div>
    </div>
  );
}

export default CheckoutHeader