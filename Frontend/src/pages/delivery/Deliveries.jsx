import { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { useAuthStore } from "../../store/auth.store";
import { Truck, Package, CheckCircle, Clock, ArrowRight } from "lucide-react";
import RoleDashboardLayout from "../../components/layouts/RoleDashboardLayout";
import { getAssignedDeliveries } from "../../api/delivery.api";

export default function DeliveryDeliveries() {
  const user = useAuthStore((s) => s.user);
  const [deliveries, setDeliveries] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    let mounted = true;

    const load = async () => {
      try {
        const res = await getAssignedDeliveries();
        if (!mounted) return;
        setDeliveries(Array.isArray(res.data) ? res.data : []);
      } catch (err) {
        if (!mounted) return;
        setError(err?.response?.data?.detail || "Failed to fetch deliveries");
      } finally {
        if (mounted) setLoading(false);
      }
    };

    load();

    return () => {
      mounted = false;
    };
  }, []);

  const stats = useMemo(() => {
    const pending = deliveries.filter((d) => d.status === "assigned").length;
    const inTransit = deliveries.filter((d) => d.status === "picked").length;
    const delivered = deliveries.filter((d) => d.status === "delivered").length;
    return { pending, inTransit, delivered };
  }, [deliveries]);

  return (
    <RoleDashboardLayout role="delivery" title="Delivery Dashboard">
      <div className="mb-8">
        <p className="text-gray-500">Welcome back, {user?.name}</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
        <div className="bg-white rounded-xl shadow p-6">
          <div className="w-12 h-12 bg-yellow-100 rounded-lg flex items-center justify-center mb-4">
            <Clock className="w-6 h-6 text-yellow-600" />
          </div>
          <p className="text-2xl font-bold">{loading ? "..." : stats.pending}</p>
          <p className="text-gray-500 text-sm">Assigned</p>
        </div>

        <div className="bg-white rounded-xl shadow p-6">
          <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
            <Truck className="w-6 h-6 text-blue-600" />
          </div>
          <p className="text-2xl font-bold">{loading ? "..." : stats.inTransit}</p>
          <p className="text-gray-500 text-sm">Picked</p>
        </div>

        <div className="bg-white rounded-xl shadow p-6">
          <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mb-4">
            <CheckCircle className="w-6 h-6 text-green-600" />
          </div>
          <p className="text-2xl font-bold">{loading ? "..." : stats.delivered}</p>
          <p className="text-gray-500 text-sm">Delivered</p>
        </div>
      </div>

      <h2 className="text-lg font-semibold mb-4">Latest Deliveries</h2>

      {error && <p className="text-sm text-red-600 mb-3">{error}</p>}

      {loading ? (
        <div className="flex items-center justify-center h-40">
          <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-green-600"></div>
        </div>
      ) : deliveries.length === 0 ? (
        <div className="bg-white rounded-lg shadow p-8 text-center">
          <Package className="w-16 h-16 mx-auto text-gray-400 mb-4" />
          <h2 className="text-xl font-semibold mb-2">No deliveries assigned</h2>
          <p className="text-gray-500">Check back later for new deliveries.</p>
        </div>
      ) : (
        <div className="space-y-3">
          {deliveries.slice(0, 6).map((delivery) => (
            <div key={delivery.id} className="bg-white rounded-lg shadow p-4 flex items-center justify-between">
              <div>
                <p className="font-semibold">Delivery #{delivery.id}</p>
                <p className="text-sm text-gray-500">Order #{delivery.order_id}</p>
              </div>
              <div className="flex items-center gap-3">
                <span className="text-xs px-2 py-1 rounded bg-gray-100 capitalize">{delivery.status}</span>
                <Link
                  to={`/delivery/map?deliveryId=${delivery.id}`}
                  className="text-sm text-green-700 hover:text-green-800 flex items-center gap-1"
                >
                  Open Map <ArrowRight className="w-4 h-4" />
                </Link>
              </div>
            </div>
          ))}
        </div>
      )}
    </RoleDashboardLayout>
  );
}
