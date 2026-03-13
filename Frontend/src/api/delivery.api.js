import api from "./axios";

export const getAvailableDeliveries = () => api.get("/delivery/available");
export const getAssignedDeliveries = (includeDelivered = false) =>
  api.get("/delivery/assigned", {
    params: includeDelivered ? { include_delivered: true } : {},
  });
export const claimDelivery = (orderId) => api.post(`/delivery/claim/${orderId}`);
export const getDeliveryRouteContext = (deliveryId) => api.get(`/delivery/${deliveryId}/route-context`);
export const confirmPickup = (deliveryId) => api.post(`/delivery/${deliveryId}/pickup-confirmation`);
export const confirmDelivery = (deliveryId) => api.post(`/delivery/${deliveryId}/delivery-confirmation`);
export const updateDeliveryStatus = (deliveryId, status) =>
  api.patch(`/delivery/${deliveryId}/status`, { status });
export const getDeliveryEarningsSummary = () => api.get("/delivery/earnings-summary");

const deliveryServiceBase = (import.meta.env.VITE_DELIVERY_SERVICE_URL || "").trim();
const DELIVERY_TIMEOUT_MS = 3500;
const REALTIME_CACHE_TTL_MS = 30000;
let realtimeHealthCache = { checkedAt: 0, available: false };

export const getDeliveryServiceBase = () => deliveryServiceBase;
const isDeliveryServiceConfigured = () => Boolean(deliveryServiceBase);

const fetchWithTimeout = async (url, options = {}) => {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), DELIVERY_TIMEOUT_MS);
  try {
    return await fetch(url, { ...options, signal: controller.signal });
  } finally {
    clearTimeout(timeoutId);
  }
};

export const isDeliveryRealtimeAvailable = async (forceCheck = false) => {
  if (!isDeliveryServiceConfigured()) return false;
  const now = Date.now();
  if (!forceCheck && now - realtimeHealthCache.checkedAt < REALTIME_CACHE_TTL_MS) {
    return realtimeHealthCache.available;
  }
  try {
    const res = await fetchWithTimeout(`${deliveryServiceBase}/health`);
    realtimeHealthCache = {
      checkedAt: now,
      available: res.ok,
    };
    return res.ok;
  } catch {
    realtimeHealthCache = {
      checkedAt: now,
      available: false,
    };
    return false;
  }
};

export const getDeliveryMapRoute = async ({ fromLat, fromLng, toLat, toLng }) => {
  const params = new URLSearchParams({
    from_lat: String(fromLat),
    from_lng: String(fromLng),
    to_lat: String(toLat),
    to_lng: String(toLng),
  });

  if (await isDeliveryRealtimeAvailable()) {
    try {
      const res = await fetchWithTimeout(`${deliveryServiceBase}/map/route?${params.toString()}`);
      if (res.ok) return res.json();
      realtimeHealthCache.available = false;
    } catch {
      realtimeHealthCache.available = false;
    }
  }

  const response = await api.get("/delivery/map/route", {
    params: {
      from_lat: fromLat,
      from_lng: fromLng,
      to_lat: toLat,
      to_lng: toLng,
    },
  });
  return response.data;
};

export const postDeliveryLocation = async (payload) => {
  if (await isDeliveryRealtimeAvailable()) {
    try {
      const res = await fetchWithTimeout(`${deliveryServiceBase}/tracking/location`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      if (res.ok) return res.json();
      realtimeHealthCache.available = false;
    } catch {
      realtimeHealthCache.available = false;
    }
  }
  const response = await api.post("/delivery/tracking/location", payload);
  return response.data;
};

export const getDeliveryTrackingByOrder = async (orderId) => {
  if (await isDeliveryRealtimeAvailable()) {
    try {
      const res = await fetchWithTimeout(`${deliveryServiceBase}/tracking/order/${orderId}`);
      if (res.ok) return res.json();
      realtimeHealthCache.available = false;
    } catch {
      realtimeHealthCache.available = false;
    }
  }

  try {
    const response = await api.get(`/delivery/tracking/order/${orderId}`);
    return response.data;
  } catch {
    return null;
  }
};
