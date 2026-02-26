import api from "./axios";

export const createReview = (data) => {
    return api.post("/reviews/", data);
};

export const getProductReviews = (productId, params) => {
    return api.get(`/reviews/product/${productId}`, { params });
};

export const getStoreReviews = (storeId, params) => {
    return api.get(`/reviews/store/${storeId}`, { params });
};

export const getProductReviewSummary = (productId) => {
    return api.get(`/reviews/product/${productId}/summary`);
};

export const getStoreReviewSummary = (storeId) => {
    return api.get(`/reviews/store/${storeId}/summary`);
};

export const deleteReview = (reviewId) => {
    return api.delete(`/reviews/${reviewId}`);
};
