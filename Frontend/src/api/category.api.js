import api from "./axios";

// Get all categories
export const getAllCategories = () => {
    return api.get("/categories/");
};

// Get category by ID
export const getCategory = (categoryId) => {
    return api.get(`/categories/${categoryId}`);
};

// Get category by slug
export const getCategoryBySlug = (slug) => {
    return api.get(`/categories/slug/${slug}`);
};

// Get category products
export const getCategoryProducts = (categoryId, params) => {
    return api.get(`/categories/${categoryId}/products`, { params });
};
