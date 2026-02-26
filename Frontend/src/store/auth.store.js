import { create } from "zustand";
import { createJSONStorage, persist } from "zustand/middleware";

export const useAuthStore = create(
  persist(
    (set) => ({
      user: null,
      accessToken: null,
      refreshToken: null,
      cart: { storeId: null, items: [] },
      setAuth: (user, accessToken, refreshToken = null) =>
        set((state) => ({
          user: user ?? state.user,
          accessToken: accessToken ?? state.accessToken,
          refreshToken: refreshToken ?? state.refreshToken,
        })),
      setAccessToken: (accessToken) => set({ accessToken }),
      setCart: (cart) => set({ cart }),
      clearAuth: () =>
        set({
          user: null,
          accessToken: null,
          refreshToken: null,
          cart: { storeId: null, items: [] },
        }),
    }),
    {
      name: "rushcart_auth",
      storage: createJSONStorage(() => localStorage),
      partialize: (state) => ({
        user: state.user,
        accessToken: state.accessToken,
        refreshToken: state.refreshToken,
      }),
    }
  )
);
