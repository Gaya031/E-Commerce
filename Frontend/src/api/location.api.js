import api from "./axios";

export const getUserProfile = () => {
  return api.get("/users/me");
};

export const updateUserLocation = (data) => {
  return api.put("/users/me/location", data);
};

