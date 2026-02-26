import axios from "axios";
import { useAuthStore } from "../store/auth.store";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  withCredentials: true,
});

api.interceptors.request.use(config => {
  const token = useAuthStore.getState().accessToken;
  if(token){
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
});

api.interceptors.response.use(
  response => response,
  async error => {
    const originalRequest = error.config || {};
    if (originalRequest.url?.includes("/auth/refresh")) {
      useAuthStore.getState().clearAuth();
      window.location.href = "/login";
      return Promise.reject(error);
    }
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      try {
        const { refreshToken, setAccessToken } = useAuthStore.getState();
        if (!refreshToken) {
          throw new Error("No refresh token");
        }
        const res = await api.post("/auth/refresh", { refresh_token: refreshToken });
        const newAccess = res?.data?.access_token;
        const newRefresh = res?.data?.refresh_token;
        if (!newAccess) {
          throw new Error("Missing access token in refresh response");
        }
        setAccessToken(newAccess);
        if (newRefresh) {
          useAuthStore.getState().setAuth(null, newAccess, newRefresh);
        }
        originalRequest.headers = originalRequest.headers || {};
        originalRequest.headers.Authorization = `Bearer ${newAccess}`;
        return api(originalRequest);
      } catch {
        useAuthStore.getState().clearAuth();
        window.location.href = "/login";
      }
    }
    return Promise.reject(error);
  }
);

export default api;
