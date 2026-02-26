import api from "./axios";

export const getServerCart = () => api.get("/cart/");

export const replaceServerCart = (data) => api.put("/cart/", data);

export const syncServerCart = (data) => api.post("/cart/sync", data);

export const clearServerCart = () => api.delete("/cart/");
