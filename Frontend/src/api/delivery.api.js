import api from "./axios";

export const getAvailableDeliveries = () => api.get("/delivery/available");
export const getAssignedDeliveries = () => api.get("/delivery/assigned");
export const getDeliveryRouteContext = (deliveryId) => api.get(`/delivery/${deliveryId}/route-context`);
export const confirmPickup = (deliveryId) => api.post(`/delivery/${deliveryId}/pickup-confirmation`);
export const confirmDelivery = (deliveryId) => api.post(`/delivery/${deliveryId}/delivery-confirmation`);
export const updateDeliveryStatus = (deliveryId, status) =>
  api.patch(`/delivery/${deliveryId}/status`, { status });
export const getDeliveryEarningsSummary = () => api.get("/delivery/earnings-summary");

const deliveryServiceBase = import.meta.env.VITE_DELIVERY_SERVICE_URL || "http://localhost:4001";

export const getDeliveryServiceBase = () => deliveryServiceBase;

export const getDeliveryMapRoute = async ({ fromLat, fromLng, toLat, toLng }) => {
  const params = new URLSearchParams({
    from_lat: String(fromLat),
    from_lng: String(fromLng),
    to_lat: String(toLat),
    to_lng: String(toLng),
  });

  const res = await fetch(`${deliveryServiceBase}/map/route?${params.toString()}`);
  if (!res.ok) {
    throw new Error("Failed to fetch route");
  }
  return res.json();
};

export const postDeliveryLocation = async (payload) => {
  const res = await fetch(`${deliveryServiceBase}/tracking/location`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error("Failed to post delivery location");
  return res.json();
};

export const getDeliveryTrackingByOrder = async (orderId) => {
  const res = await fetch(`${deliveryServiceBase}/tracking/order/${orderId}`);
  if (!res.ok) return null;
  return res.json();
};
