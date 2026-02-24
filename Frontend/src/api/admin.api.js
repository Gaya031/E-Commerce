import api from "./axios";

// Admin - Sellers
export const getSellers = () => {
  return api.get("/admin/sellers");
};

export const approveSeller = (sellerId, data) => {
  return api.post(`/admin/sellers/${sellerId}/decision`, data);
};

export const blockUser = (userId, data) => {
  return api.patch(`/admin/users/${userId}`, data);
};

// Admin - Orders
export const getAllOrders = () => {
  return api.get("/admin/orders");
};

export const refundOrder = (orderId) => {
  return api.post(`/admin/orders/${orderId}/refund`);
};

export const decideReturn = (orderId, data) => {
  return api.post(`/admin/orders/${orderId}/return-decision`, data);
};

// Admin - Payouts
export const payoutSeller = (sellerId) => {
  return api.post(`/payouts/seller/${sellerId}`);
};

export const payoutDeliveryPartner = (partnerId) => {
  return api.post(`/payouts/delivery/${partnerId}`);
};

// Commissions
export const calculateCommission = (orderId) => {
  return api.post(`/commissions/calculate/${orderId}`);
};

