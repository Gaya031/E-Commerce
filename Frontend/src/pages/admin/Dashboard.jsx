import { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { useAuthStore } from "../../store/auth.store";
import { Users, ShoppingBag, DollarSign, Package, ArrowRight } from "lucide-react";
import RoleDashboardLayout from "../../components/layouts/RoleDashboardLayout";
import { getRevenueAnalytics } from "../../api/admin.api";

export default function AdminDashboard() {
  const user = useAuthStore((s) => s.user);
  const [stats, setStats] = useState({
    totalSellers: 0,
    totalOrders: 0,
    totalRevenue: 0,
    activeUsers: 0,
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const loadStats = async () => {
      try {
        const res = await getRevenueAnalytics();
        const data = res?.data || {};
        setStats({
          totalSellers: Number(data.total_sellers || 0),
          totalOrders: Number(data.total_orders || 0),
          totalRevenue: Number(data.total_revenue ?? data.gross_revenue ?? 0),
          activeUsers: Number(data.active_users || 0),
        });
        setError("");
      } catch (err) {
        setError(err?.response?.data?.detail || "Failed to load dashboard metrics.");
      } finally {
        setLoading(false);
      }
    };
    loadStats();
  }, []);

  const formattedRevenue = useMemo(() => `₹${stats.totalRevenue.toLocaleString()}`, [stats.totalRevenue]);

  return (
    <RoleDashboardLayout role="admin" title="Admin Dashboard">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-2xl font-bold">Admin Dashboard</h1>
          <p className="text-gray-500">Welcome back, {user?.name}</p>
          {error && <p className="text-sm text-red-600 mt-2">{error}</p>}
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
          <div className="bg-white rounded-xl shadow p-6">
            <div className="flex items-center justify-between mb-4">
              <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                <Users className="w-6 h-6 text-blue-600" />
              </div>
            </div>
            <p className="text-2xl font-bold">{loading ? "..." : stats.totalSellers}</p>
            <p className="text-gray-500 text-sm">Total Sellers</p>
          </div>

          <div className="bg-white rounded-xl shadow p-6">
            <div className="flex items-center justify-between mb-4">
              <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center">
                <ShoppingBag className="w-6 h-6 text-purple-600" />
              </div>
            </div>
            <p className="text-2xl font-bold">{loading ? "..." : stats.totalOrders}</p>
            <p className="text-gray-500 text-sm">Total Orders</p>
          </div>

          <div className="bg-white rounded-xl shadow p-6">
            <div className="flex items-center justify-between mb-4">
              <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
                <DollarSign className="w-6 h-6 text-green-600" />
              </div>
            </div>
            <p className="text-2xl font-bold">{loading ? "..." : formattedRevenue}</p>
            <p className="text-gray-500 text-sm">Total Revenue</p>
          </div>

          <div className="bg-white rounded-xl shadow p-6">
            <div className="flex items-center justify-between mb-4">
              <div className="w-12 h-12 bg-yellow-100 rounded-lg flex items-center justify-center">
                <Users className="w-6 h-6 text-yellow-600" />
              </div>
            </div>
            <p className="text-2xl font-bold">{loading ? "..." : stats.activeUsers}</p>
            <p className="text-gray-500 text-sm">Active Users</p>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="bg-white rounded-xl shadow p-6">
            <h2 className="text-lg font-semibold mb-4">Quick Actions</h2>
            <div className="space-y-3">
              <Link 
                to="/admin/sellers" 
                className="flex items-center justify-between p-3 bg-gray-50 rounded-lg hover:bg-gray-100"
              >
                <span className="flex items-center gap-3">
                  <Users className="w-5 h-5 text-gray-600" />
                  Manage Sellers
                </span>
                <ArrowRight className="w-4 h-4 text-gray-400" />
              </Link>
              <Link 
                to="/admin/orders" 
                className="flex items-center justify-between p-3 bg-gray-50 rounded-lg hover:bg-gray-100"
              >
                <span className="flex items-center gap-3">
                  <ShoppingBag className="w-5 h-5 text-gray-600" />
                  Manage Orders
                </span>
                <ArrowRight className="w-4 h-4 text-gray-400" />
              </Link>
              <Link 
                to="/admin/users" 
                className="flex items-center justify-between p-3 bg-gray-50 rounded-lg hover:bg-gray-100"
              >
                <span className="flex items-center gap-3">
                  <Package className="w-5 h-5 text-gray-600" />
                  Manage Users
                </span>
                <ArrowRight className="w-4 h-4 text-gray-400" />
              </Link>
            </div>
          </div>

          <div className="bg-white rounded-xl shadow p-6">
            <h2 className="text-lg font-semibold mb-4">Recent Activity</h2>
            <div className="text-center py-8 text-gray-500">
              <Package className="w-12 h-12 mx-auto mb-3 text-gray-400" />
              <p>No recent activity</p>
            </div>
          </div>
        </div>
    </RoleDashboardLayout>
  );
}
