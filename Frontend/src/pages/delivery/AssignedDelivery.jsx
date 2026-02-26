import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { getAssignedDeliveries } from "../../api/delivery.api";
import RoleDashboardLayout from "../../components/layouts/RoleDashboardLayout";

export default function AssignedDelivery() {
  const [rows, setRows] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  useEffect(() => {
    getAssignedDeliveries()
      .then((res) => setRows(res.data || []))
      .catch((err) => setError(err?.response?.data?.detail || "Failed to fetch assigned deliveries"))
      .finally(() => setLoading(false));
  }, []);

  return (
    <RoleDashboardLayout role="delivery" title="Assigned Deliveries">
      <div className="max-w-4xl">
        <div className="bg-white rounded-xl shadow p-4 space-y-3">
          {error && <p className="text-sm text-red-600">{error}</p>}
          {loading && <p>Loading...</p>}
          {rows.map((r) => (
            <div key={r.id} className="border rounded p-3">
              <p>Delivery #{r.id}</p>
              <p className="text-sm">Order #{r.order_id} • {r.status}</p>
              <div className="flex gap-3 text-sm mt-1">
                <Link to={`/delivery/map?deliveryId=${r.id}`} className="text-green-700 hover:text-green-800">
                  Open Navigation
                </Link>
                <Link to={`/delivery/${r.id}/pickup`} className="text-blue-700 hover:text-blue-800">
                  Pickup
                </Link>
                <Link to={`/delivery/${r.id}/confirm`} className="text-purple-700 hover:text-purple-800">
                  Confirm Delivery
                </Link>
              </div>
            </div>
          ))}
          {!loading && !rows.length && <p>No assigned deliveries.</p>}
        </div>
      </div>
    </RoleDashboardLayout>
  );
}
