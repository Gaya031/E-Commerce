import api from "./axios";

export const initiatePayment = (orderId) => {
  return api.post("/payments/initiate", { order_id: orderId });
};

export const confirmPayment = (payload) => {
  return api.post("/payments/confirm", payload);
};

export const verifyPaymentWebhook = (payload, signature) => {
  return api.post("/payments/webhook", payload, {
    headers: { "x-razorpay-signature": signature },
  });
};
