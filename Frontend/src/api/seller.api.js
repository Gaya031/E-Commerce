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

export const getSellerProducts = () => {
  return api.get("/products/");
};

// Seller - Profile
export const createSellerProfile = (data) => {
  return api.post("/sellers/", data);
};

export const updateSellerKYC = (sellerId, data) => {
  return api.put(`/sellers/${sellerId}/kyc`, data);
};

export const getSellerProfile = () => {
  return api.get("/sellers/me");
};

