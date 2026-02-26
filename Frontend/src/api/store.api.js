import api from "./axios";

export const getNearbyStores = ({lat, lng}) => {
    return api.get("/stores/nearby", {
        params: {lat, lng}
    });
};

export const getStoreDetails = storeId => {
    return api.get(`/stores/${storeId}`);
};

export const getStoreProducts = (storeId, params) => {
    return api.get(`/stores/${storeId}/products`, { params });
};

export const getStoreBestSellers = (storeId, params) => api.get(`/stores/${storeId}/bestsellers`, { params });
