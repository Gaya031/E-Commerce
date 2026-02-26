import { create } from "zustand";
import { pushToast } from "./toast.store";
import { useAuthStore } from "./auth.store";
import { clearServerCart, getServerCart, replaceServerCart, syncServerCart } from "../api/cart.api";

const CART_KEY = "rushcart_cart";

const getEmptyCart = () => ({
  storeId: null,
  items: [],
});

const normalizeCart = (cart) => {
  const storeId = cart?.storeId ?? cart?.store_id ?? null;
  const items = Array.isArray(cart?.items) ? cart.items : [];

  return {
    storeId,
    items: items.map((i) => ({
      productId: i.productId ?? i.product_id,
      title: i.title,
      price: Number(i.price) || 0,
      image: i.image || "/product.jpg",
      quantity: Number(i.quantity) || 1,
    })),
  };
};

const loadCart = () => {
  try {
    const raw = localStorage.getItem(CART_KEY);
    if (!raw) return getEmptyCart();
    return normalizeCart(JSON.parse(raw));
  } catch {
    return getEmptyCart();
  }
};

const persistLocal = (cart) => {
  localStorage.setItem(CART_KEY, JSON.stringify(cart));
};

const toServerPayload = (cart) => ({
  store_id: cart.storeId,
  items: cart.items.map((i) => ({
    product_id: i.productId,
    title: i.title,
    price: i.price,
    image: i.image,
    quantity: i.quantity,
  })),
});

export const useCartStore = create((set, get) => ({
  ...loadCart(),

  setCart: (cart) => {
    const normalized = normalizeCart(cart);
    persistLocal(normalized);
    set(normalized);
  },

  persistServer: async (cart) => {
    const user = useAuthStore.getState().user;
    const accessToken = useAuthStore.getState().accessToken;
    if (!user || !accessToken) return;

    try {
      await replaceServerCart(toServerPayload(cart || get()));
    } catch {
      // keep local cart as source of truth if network fails
    }
  },

  hydrateFromServer: async () => {
    const user = useAuthStore.getState().user;
    const accessToken = useAuthStore.getState().accessToken;
    if (!user || !accessToken) return;

    try {
      const res = await getServerCart();
      const normalized = normalizeCart(res.data);
      persistLocal(normalized);
      set(normalized);
    } catch {
      // keep existing local cart
    }
  },

  syncGuestCartToServer: async () => {
    const user = useAuthStore.getState().user;
    const accessToken = useAuthStore.getState().accessToken;
    if (!user || !accessToken) return;

    const localCart = loadCart();

    try {
      const res = await syncServerCart(toServerPayload(localCart));
      const merged = normalizeCart(res.data);
      persistLocal(merged);
      set(merged);
    } catch {
      // if sync endpoint fails, at least attempt full replace
      try {
        await get().persistServer(localCart);
        const refreshed = await getServerCart();
        const normalized = normalizeCart(refreshed.data);
        persistLocal(normalized);
        set(normalized);
      } catch {
        pushToast({ type: "warning", message: "Cart sync failed. Using local cart only." });
      }
    }
  },

  addItem: (storeId, product) => {
    const cart = get();

    if (cart.storeId && cart.storeId !== storeId) {
      pushToast({ type: "warning", message: "Your cart contains items from another store." });
      return;
    }

    const existing = cart.items.find((i) => i.productId === product.id);
    const items = existing
      ? cart.items.map((i) =>
          i.productId === product.id ? { ...i, quantity: i.quantity + 1 } : i
        )
      : [
          ...cart.items,
          {
            productId: product.id,
            title: product.title,
            price: Number(product.price) || 0,
            image: product.image || product.images?.[0] || "/product.jpg",
            quantity: 1,
          },
        ];

    const updatedCart = { storeId, items };
    persistLocal(updatedCart);
    set(updatedCart);
    void get().persistServer(updatedCart);
  },

  updateQuantity: (productId, quantity) => {
    const items = get()
      .items.map((i) => (i.productId === productId ? { ...i, quantity } : i))
      .filter((i) => i.quantity > 0);

    const updatedCart = {
      storeId: items.length ? get().storeId : null,
      items,
    };

    persistLocal(updatedCart);
    set(updatedCart);
    void get().persistServer(updatedCart);
  },

  clearCart: () => {
    localStorage.removeItem(CART_KEY);
    set(getEmptyCart());
    const user = useAuthStore.getState().user;
    const accessToken = useAuthStore.getState().accessToken;
    if (user && accessToken) {
      void clearServerCart();
    }
  },

  mergeCart: (incomingCart) => {
    if (!incomingCart || !incomingCart.items?.length) return;

    const current = get();
    if (!current.items.length) {
      persistLocal(incomingCart);
      set(normalizeCart(incomingCart));
      return;
    }

    if (current.storeId && incomingCart.storeId && current.storeId !== incomingCart.storeId) {
      return;
    }

    const mergedItems = [...current.items];
    incomingCart.items.forEach((item) => {
      const existing = mergedItems.find((i) => i.productId === item.productId);
      if (existing) {
        existing.quantity += item.quantity;
      } else {
        mergedItems.push(item);
      }
    });

    const mergedCart = {
      storeId: current.storeId || incomingCart.storeId,
      items: mergedItems,
    };

    persistLocal(mergedCart);
    set(mergedCart);
    void get().persistServer(mergedCart);
  },

  totalAmount: () => get().items.reduce((sum, i) => sum + i.price * i.quantity, 0),
}));
