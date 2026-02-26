import http from "http";

import cors from "cors";
import express from "express";
import { Server as SocketIOServer } from "socket.io";

const app = express();
app.disable("x-powered-by");

const allowedOrigins = (process.env.ALLOWED_ORIGINS || "http://localhost:5173")
  .split(",")
  .map((o) => o.trim())
  .filter(Boolean);

app.use(
  cors({
    origin: (origin, callback) => {
      if (!origin || allowedOrigins.includes(origin)) {
        callback(null, true);
        return;
      }
      callback(new Error("Origin not allowed by CORS"));
    },
    methods: ["GET", "POST"],
  })
);
app.use(express.json({ limit: "100kb" }));

const server = http.createServer(app);
const io = new SocketIOServer(server, {
  cors: {
    origin: allowedOrigins,
    methods: ["GET", "POST"],
  },
});

const toNum = (val) => {
  const num = Number(val);
  return Number.isFinite(num) ? num : null;
};

const toLatLng = (coords = []) => coords.map(([lng, lat]) => [lat, lng]);

const trackingByDelivery = new Map();
const historyByDelivery = new Map();

const upsertTracking = (payload) => {
  const deliveryId = String(payload.delivery_id);
  const orderId = payload.order_id ? String(payload.order_id) : null;
  const lat = toNum(payload.lat);
  const lng = toNum(payload.lng);
  if (lat === null || lng === null || !deliveryId) {
    return null;
  }

  const row = {
    delivery_id: deliveryId,
    order_id: orderId,
    lat,
    lng,
    heading: toNum(payload.heading),
    speed: toNum(payload.speed),
    status: payload.status || null,
    updated_at: new Date().toISOString(),
  };

  trackingByDelivery.set(deliveryId, row);

  const history = historyByDelivery.get(deliveryId) || [];
  history.push({ lat: row.lat, lng: row.lng, updated_at: row.updated_at });
  if (history.length > 200) history.shift();
  historyByDelivery.set(deliveryId, history);

  return row;
};

const broadcastTracking = (tracking) => {
  io.to(`delivery:${tracking.delivery_id}`).emit("tracking:update", tracking);
  if (tracking.order_id) {
    io.to(`order:${tracking.order_id}`).emit("tracking:update", tracking);
  }
};

io.on("connection", (socket) => {
  socket.on("join_delivery", ({ delivery_id }) => {
    if (delivery_id) socket.join(`delivery:${delivery_id}`);
  });

  socket.on("join_order", ({ order_id }) => {
    if (order_id) socket.join(`order:${order_id}`);
  });

  socket.on("leave_delivery", ({ delivery_id }) => {
    if (delivery_id) socket.leave(`delivery:${delivery_id}`);
  });

  socket.on("leave_order", ({ order_id }) => {
    if (order_id) socket.leave(`order:${order_id}`);
  });

  socket.on("driver_location", (payload = {}) => {
    const tracking = upsertTracking(payload);
    if (tracking) broadcastTracking(tracking);
  });
});

app.get("/health", (_, res) => {
  res.json({ ok: true, service: "delivery-service", socketio: true });
});

app.get("/map/route", async (req, res) => {
  const fromLat = toNum(req.query.from_lat);
  const fromLng = toNum(req.query.from_lng);
  const toLat = toNum(req.query.to_lat);
  const toLng = toNum(req.query.to_lng);

  if ([fromLat, fromLng, toLat, toLng].some((v) => v === null)) {
    res.status(400).json({ message: "from_lat, from_lng, to_lat, to_lng are required numbers" });
    return;
  }

  try {
    const osrmUrl = `https://router.project-osrm.org/route/v1/driving/${fromLng},${fromLat};${toLng},${toLat}?overview=full&geometries=geojson`;
    const routeRes = await fetch(osrmUrl);
    if (!routeRes.ok) throw new Error(`OSRM request failed with status ${routeRes.status}`);

    const data = await routeRes.json();
    const route = Array.isArray(data.routes) ? data.routes[0] : null;
    if (!route) throw new Error("No route found");

    res.json({
      distance_km: Number(route.distance || 0) / 1000,
      eta_minutes: Math.round(Number(route.duration || 0) / 60),
      polyline: toLatLng(route.geometry?.coordinates || []),
    });
  } catch (err) {
    res.status(502).json({ message: err.message || "Failed to generate route" });
  }
});

app.post("/tracking/location", (req, res) => {
  const tracking = upsertTracking(req.body || {});
  if (!tracking) {
    res.status(400).json({ message: "delivery_id, lat and lng are required" });
    return;
  }
  broadcastTracking(tracking);
  res.json({ ok: true, tracking });
});

app.get("/tracking/delivery/:deliveryId", (req, res) => {
  const deliveryId = String(req.params.deliveryId);
  const tracking = trackingByDelivery.get(deliveryId);
  if (!tracking) {
    res.status(404).json({ message: "Tracking not found" });
    return;
  }
  res.json({
    tracking,
    history: historyByDelivery.get(deliveryId) || [],
  });
});

app.get("/tracking/order/:orderId", (req, res) => {
  const orderId = String(req.params.orderId);
  for (const row of trackingByDelivery.values()) {
    if (row.order_id === orderId) {
      res.json({ tracking: row });
      return;
    }
  }
  res.status(404).json({ message: "Tracking not found" });
});

const port = process.env.PORT || 4001;
server.listen(port, () => {
  console.log(`Delivery service running on port ${port}`);
});
