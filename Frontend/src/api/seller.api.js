import api from "./axios";

// Seller - Products
export const createProduct = (data) => {
  return api.post("/products/", data);
};

export const updateProduct = (productId, data) => {
  return api.put(`/products/${productId}`, data);
};

export const updateStock = (productId, data) => {
  return api.patch(`/products/${productId}/stock`, data);
};

export const deleteProduct = (productId) => {
  return api.delete(`/products/${productId}`);
};

export const getSellerProducts = () => {
  return api.get("/products/mine");
};

// Seller - Profile
export const createSellerProfile = (data) => {
  return api.post("/sellers/", data);
};

export const updateSellerProfile = (data) => {
  return api.put("/sellers/me", data);
};

export const updateSellerKYC = (sellerId, data) => {
  return api.put(`/sellers/${sellerId}/kyc`, data);
};

export const updateMySellerKYC = (data) => {
  return api.put("/sellers/me/kyc", data);
};

export const getSellerProfile = () => {
  return api.get("/sellers/me");
};

export const getSellerApprovalStatus = () => {
  return api.get("/sellers/me/approval-status");
};

export const getSellerOrders = () => {
  return api.get("/sellers/me/orders");
};

export const getSellerEarningsSummary = () => {
  return api.get("/sellers/me/earnings-summary");
};

export const getSellerCommissionDetails = () => {
  return api.get("/sellers/me/commission-details");
};

export const getSellerSubscriptionStatus = () => {
  return api.get("/sellers/me/subscription-status");
};

export const getSellerDashboardStats = () => {
  return api.get("/sellers/me/dashboard-stats");
};

export const updateSellerOrderStatus = (orderId, status) => {
  return api.patch(`/sellers/me/orders/${orderId}/status`, null, { params: { status } });
};
