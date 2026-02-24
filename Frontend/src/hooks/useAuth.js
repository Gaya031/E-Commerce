import { useEffect } from "react";
import { useAuthStore } from "../store/auth.store";
import { getMe } from "../api/auth.api";

export const useAuth = () => {
  const setAuth = useAuthStore((s) => s.setAuth);
  const clearAuth = useAuthStore((s) => s.clearAuth);
  const token = useAuthStore((s) => s.accessToken);

  useEffect(() => {
    if (!token) return;

    getMe()
      .then((res) => {
        setAuth(res.data, token);
      })
      .catch(() => {
        clearAuth();
      });
  }, [token]);
};
