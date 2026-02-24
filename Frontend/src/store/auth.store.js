import { create } from "zustand";

export const useAuthStore = create((set) => ({
  user: null,
  accessToken: null,
  cart: { storeId: null, items: [] },
  setAuth: (user, token) => set({ user, accessToken: token }),
  setCart: (cart) => set({ cart }),
  clearAuth: () => set({ user: null, accessToken: null, cart: { storeId: null, items: [] } }),
}));
