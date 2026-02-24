import api from "./axios";

export const getFeaturedProducts = () => {
    return api.get("/products/featured");
};