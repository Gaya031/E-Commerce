const getApiOrigin = () => {
  const apiUrl = import.meta.env.VITE_API_URL || "";
  try {
    const parsed = new URL(apiUrl, window.location.origin);
    return parsed.origin;
  } catch {
    return window.location.origin;
  }
};

const isLikelyImageFilename = (value) =>
  /^[A-Za-z0-9._-]+\.(jpg|jpeg|png|webp|gif|heic|heif|avif)$/i.test(value || "");

export const resolveMediaUrl = (value, fallback = "") => {
  const raw = String(value || "").trim();
  if (!raw) return fallback;

  if (raw.startsWith("data:") || raw.startsWith("blob:")) {
    return raw;
  }

  if (/^https?:\/\//i.test(raw)) {
    return raw;
  }

  if (raw.startsWith("//")) {
    return `${window.location.protocol}${raw}`;
  }

  if (raw.startsWith("/uploads/")) {
    return `${getApiOrigin()}${raw}`;
  }

  if (raw.startsWith("uploads/")) {
    return `${getApiOrigin()}/${raw}`;
  }

  if (raw.startsWith("/")) {
    return raw;
  }

  if (isLikelyImageFilename(raw)) {
    return `${getApiOrigin()}/uploads/products/${raw}`;
  }

  return `${getApiOrigin()}/${raw}`;
};

export const getProductImage = (product, fallback = "/product.jpg") => {
  if (!product) return fallback;
  const firstImage = Array.isArray(product.images) ? product.images[0] : product.images;
  return resolveMediaUrl(product.image || product.image_url || firstImage, fallback);
};
