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

export const getAdminUsers = () => {
  return api.get("/admin/users");
};

export const getPendingReturns = () => {
  return api.get("/admin/returns");
};

export const getRefundQueue = () => {
  return api.get("/admin/refunds");
};

export const updateCommissionConfig = (sellerId, commissionPercent) => {
  return api.patch("/admin/commission/config", null, {
    params: { seller_id: sellerId, commission_percent: commissionPercent },
  });
};

export const getRevenueAnalytics = () => {
  return api.get("/admin/analytics/revenue");
};

export const exportReports = () => {
  return api.get("/admin/reports/export");
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
