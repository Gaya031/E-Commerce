import api from "./axios";

export const getWallet = () => {
  return api.get("/wallet/");
};

export const addToWallet = (data) => {
  return api.post("/wallet/add", data);
};

