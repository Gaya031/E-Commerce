import api from "./axios";

// Get all products
export const getAllProducts = (params) => {
    return api.get("/products/", { params });
};

// Get featured products
export const getFeaturedProducts = () => {
    return api.get("/products/featured");
};

// Get single product
export const getProduct = (productId) => {
    return api.get(`/products/${productId}`);
};

// Create product (seller only)
export const createProduct = (data) => {
    return api.post("/products/", data);
};

// Update product (seller only)
export const updateProduct = (productId, data) => {
    return api.put(`/products/${productId}`, data);
};

// Update stock (seller only)
export const updateStock = (productId, stock) => {
    return api.patch(`/products/${productId}/stock`, { stock });
};

// Search products
export const searchProducts = (query) => {
    return api.get("/products/search", { params: { q: query } });
};
