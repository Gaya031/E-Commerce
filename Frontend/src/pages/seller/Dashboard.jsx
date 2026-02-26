import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { ArrowRight, DollarSign, Package, ShoppingBag, TrendingUp } from "lucide-react";

import RoleDashboardLayout from "../../components/layouts/RoleDashboardLayout";
import { getSellerDashboardStats } from "../../api/seller.api";
import { useAuthStore } from "../../store/auth.store";

export default function SellerDashboard() {
  const user = useAuthStore((s) => s.user);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    getSellerDashboardStats()
      .then((res) => setStats(res.data))
      .catch((err) => setError(err?.response?.data?.detail || "Failed to load dashboard stats"))
      .finally(() => setLoading(false));
  }, []);

  return (
    <RoleDashboardLayout role="seller" title="Seller Dashboard">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-2xl font-bold">Seller Dashboard</h1>
          <p className="text-gray-500">Welcome back, {user?.name}</p>
        </div>
        <Link
          to="/seller/products"
          className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 flex items-center gap-2"
        >
          Add Product <ArrowRight className="w-4 h-4" />
        </Link>
      </div>

      {error && <p className="text-sm text-red-600 mb-4">{error}</p>}
      {loading ? (
        <p>Loading dashboard...</p>
      ) : (
        <>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
            <div className="bg-white rounded-xl shadow p-6">
              <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
                <Package className="w-6 h-6 text-blue-600" />
              </div>
              <p className="text-2xl font-bold">{stats?.total_items_sold || 0}</p>
              <p className="text-gray-500 text-sm">Items Sold</p>
            </div>
            <div className="bg-white rounded-xl shadow p-6">
              <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mb-4">
                <ShoppingBag className="w-6 h-6 text-purple-600" />
              </div>
              <p className="text-2xl font-bold">{stats?.total_orders || 0}</p>
              <p className="text-gray-500 text-sm">Total Orders</p>
            </div>
            <div className="bg-white rounded-xl shadow p-6">
              <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mb-4">
                <DollarSign className="w-6 h-6 text-green-600" />
              </div>
              <p className="text-2xl font-bold">₹{Number(stats?.total_revenue || 0).toLocaleString()}</p>
              <p className="text-gray-500 text-sm">Total Revenue</p>
            </div>
            <div className="bg-white rounded-xl shadow p-6">
              <div className="w-12 h-12 bg-yellow-100 rounded-lg flex items-center justify-center mb-4">
                <TrendingUp className="w-6 h-6 text-yellow-600" />
              </div>
              <p className="text-2xl font-bold">{stats?.pending_orders || 0}</p>
              <p className="text-gray-500 text-sm">Pending Orders</p>
            </div>
          </div>

          <div className="bg-white rounded-xl shadow p-6">
            <h2 className="text-lg font-semibold mb-4">Recent Orders</h2>
            {!stats?.latest_orders?.length ? (
              <p className="text-sm text-gray-500">No recent orders</p>
            ) : (
              <div className="space-y-3">
                {stats.latest_orders.map((order) => (
                  <div key={order.id} className="flex items-center justify-between border rounded p-3">
                    <div>
                      <p className="font-medium">Order #{order.id}</p>
                      <p className="text-sm text-gray-500">
                        {order.items_count} items • {order.status}
                      </p>
                    </div>
                    <p className="font-semibold">₹{order.total_amount}</p>
                  </div>
                ))}
              </div>
            )}
          </div>
        </>
      )}
    </RoleDashboardLayout>
  );
}
