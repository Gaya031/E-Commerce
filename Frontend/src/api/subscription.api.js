import api from "./axios";

export const getSubscriptionPlans = () => api.get("/subscriptions/");
