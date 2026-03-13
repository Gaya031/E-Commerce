import api from "./axios";

export const getSubscriptionPlans = () => api.get("/subscriptions/");
export const activateSubscriptionPlan = (planId) => api.post(`/subscriptions/activate/${planId}`);
