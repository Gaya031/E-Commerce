import { create } from "zustand";

const CART_KEY = "rushcart_cart";

const getEmptyCart = () => ({
  storeId: null,
  items: [],
});

const loadCart = () => {
  try {
    const raw = localStorage.getItem(CART_KEY);
    if (!raw) return getEmptyCart();
    const parsed = JSON.parse(raw);

    // basic shape validation
    if (!parsed.items || !Array.isArray(parsed.items)) {
      return getEmptyCart();
    }
    return parsed;
  } catch {
    return getEmptyCart();
  }
};

export const useCartStore = create((set, get) => ({
  ...loadCart(),

  /* ---------------- ADD ITEM ---------------- */
  addItem: (storeId, product) => {
    const cart = get();

    // one-store-only rule
    if (cart.storeId && cart.storeId !== storeId) {
      alert("Your cart contains items from another store");
      return;
    }

    const existing = cart.items.find(
      (i) => i.productId === product.id
    );

    let items;

    if (existing) {
      items = cart.items.map((i) =>
        i.productId === product.id
          ? { ...i, quantity: i.quantity + 1 }
          : i
      );
    } else {
      items = [
        ...cart.items,
        {
          productId: product.id,
          title: product.title,
          price: product.price,
          image: product.image,
          quantity: 1,
        },
      ];
    }

    const updatedCart = { storeId, items };
    localStorage.setItem(CART_KEY, JSON.stringify(updatedCart));
    set(updatedCart);
  },

  /* ---------------- UPDATE QUANTITY ---------------- */
  updateQuantity: (productId, quantity) => {
    const items = get()
      .items.map((i) =>
        i.productId === productId
          ? { ...i, quantity }
          : i
      )
      .filter((i) => i.quantity > 0);

    const updatedCart = {
      storeId: items.length ? get().storeId : null,
      items,
    };

    localStorage.setItem(CART_KEY, JSON.stringify(updatedCart));
    set(updatedCart);
  },

  /* ---------------- CLEAR CART ---------------- */
  clearCart: () => {
    localStorage.removeItem(CART_KEY);
    set(getEmptyCart());
  },

  /* ---------------- MERGE CART (ON LOGIN) ---------------- */
  mergeCart: (incomingCart) => {
    if (!incomingCart || !incomingCart.items?.length) return;

    const current = get();

    // if current cart empty → replace
    if (!current.items.length) {
      localStorage.setItem(CART_KEY, JSON.stringify(incomingCart));
      set(incomingCart);
      return;
    }

    // store mismatch → do nothing (safe default)
    if (
      current.storeId &&
      incomingCart.storeId &&
      current.storeId !== incomingCart.storeId
    ) {
      return;
    }

    const mergedItems = [...current.items];

    incomingCart.items.forEach((item) => {
      const existing = mergedItems.find(
        (i) => i.productId === item.productId
      );

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

    localStorage.setItem(CART_KEY, JSON.stringify(mergedCart));
    set(mergedCart);
  },

  /* ---------------- TOTAL ---------------- */
  totalAmount: () =>
    get().items.reduce(
      (sum, i) => sum + i.price * i.quantity,
      0
    ),
}));