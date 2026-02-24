import api from "./axios";

export const createOrder = (data) => {
  return api.post("/orders/", data);
};

export const getOrders = () => {
  return api.get("/orders/");
};

export const getOrderById = (orderId) => {
  return api.get(`/orders/${orderId}`);
};

export const cancelOrder = (orderId) => {
  return api.post(`/orders/${orderId}/cancel`);
};

export const returnOrder = (orderId, data) => {
  return api.post(`/orders/${orderId}/return`, data);
};

