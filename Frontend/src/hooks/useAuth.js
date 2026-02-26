import { useEffect } from "react";
import { useAuthStore } from "../store/auth.store";
import { getMe } from "../api/auth.api";
import { useCartStore } from "../store/cart.store";

export const useAuth = () => {
  const setAuth = useAuthStore((s) => s.setAuth);
  const clearAuth = useAuthStore((s) => s.clearAuth);
  const token = useAuthStore((s) => s.accessToken);
  const refreshToken = useAuthStore((s) => s.refreshToken);
  const hydrateFromServer = useCartStore((s) => s.hydrateFromServer);

  useEffect(() => {
    if (!token) return;

    getMe()
      .then((res) => {
        setAuth(res.data, token, refreshToken);
        return hydrateFromServer();
      })
      .catch(() => {
        clearAuth();
      });
  }, [token, refreshToken, setAuth, clearAuth, hydrateFromServer]);
};
