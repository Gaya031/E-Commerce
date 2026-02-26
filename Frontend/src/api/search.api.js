import api from "./axios";

export const searchAll = (query) => {
    return api.get("/search/", {
        params: { q: query }
    });
};

export const searchProducts = (query) => {
    return api.get("/search/products", {
        params: { q: query }
    });
};

export const searchStores = (query) => {
    return api.get("/search/stores", {
        params: { q: query }
    });
};
