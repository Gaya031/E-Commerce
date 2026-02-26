import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { getAvailableDeliveries } from "../../api/delivery.api";
import RoleDashboardLayout from "../../components/layouts/RoleDashboardLayout";

export default function AvailableDeliveries() {
  const [rows, setRows] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    getAvailableDeliveries()
      .then((res) => setRows(res.data || []))
      .catch((err) => setError(err?.response?.data?.detail || "Failed to fetch available deliveries"))
      .finally(() => setLoading(false));
  }, []);

  return (
    <RoleDashboardLayout role="delivery" title="Available Deliveries">
      <div className="max-w-4xl">
        <div className="bg-white rounded-xl shadow p-4 space-y-3">
          {error && <p className="text-sm text-red-600">{error}</p>}
          {loading && <p>Loading...</p>}
          {rows.map((r) => (
            <div key={r.id} className="border rounded p-3">
              <p>Delivery #{r.id}</p>
              <p className="text-sm">Order #{r.order_id} • {r.status}</p>
              <Link to={`/delivery/map?deliveryId=${r.id}`} className="text-sm text-green-700 hover:text-green-800">
                Open Navigation
              </Link>
            </div>
          ))}
          {!loading && !rows.length && <p>No available deliveries.</p>}
        </div>
      </div>
    </RoleDashboardLayout>
  );
}
