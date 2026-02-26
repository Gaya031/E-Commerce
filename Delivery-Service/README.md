# Delivery Service (Node.js + Socket.IO Microservice)

Delivery microservice for map/navigation and live driver tracking.

## Run

```bash
cd Delivery-Service
npm install
npm run dev
```

## Endpoints

- `GET /health`
- `GET /map/route?from_lat=&from_lng=&to_lat=&to_lng=`
- `POST /tracking/location`
- `GET /tracking/delivery/:deliveryId`
- `GET /tracking/order/:orderId`

## Socket Events

- Client -> server:
  - `join_delivery` `{ delivery_id }`
  - `join_order` `{ order_id }`
  - `driver_location` `{ delivery_id, order_id, lat, lng, heading?, speed?, status? }`
- Server -> client:
  - `tracking:update` `{ delivery_id, order_id, lat, lng, heading, speed, status, updated_at }`
