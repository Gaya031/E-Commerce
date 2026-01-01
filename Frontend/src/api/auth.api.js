import api from "./axios";

export const login = (data) => {
    return api.post("/auth/auth/login", data);
};

export const register = data =>
  api.post("/auth/auth/register", data);

export const getMe = () =>
  api.get("/users/me");

// export const logout = () =>
//   api.post("/auth/logout");
