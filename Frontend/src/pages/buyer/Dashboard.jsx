import { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { ShoppingBag, Wallet, Clock3, CheckCircle2, ArrowRight } from "lucide-react";
import { useAuthStore } from "../../store/auth.store";
import { getOrderSummary } from "../../api/order.api";
import { getWallet } from "../../api/wallet.api";
import RoleDashboardLayout from "../../components/layouts/RoleDashboardLayout";

export default function BuyerDashboard() {
  const user = useAuthStore((s) => s.user);
  const [summary, setSummary] = useState({
    total_orders: 0,
    active_orders: 0,
    delivered_orders: 0,
    recent_orders: [],
  });
  const [walletBalance, setWalletBalance] = useState(0);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let mounted = true;

    const loadData = async () => {
      try {
        const [summaryRes, walletRes] = await Promise.allSettled([getOrderSummary(), getWallet()]);

        if (!mounted) return;

        if (summaryRes.status === "fulfilled") {
          setSummary({
            total_orders: Number(summaryRes.value?.data?.total_orders ?? 0),
            active_orders: Number(summaryRes.value?.data?.active_orders ?? 0),
            delivered_orders: Number(summaryRes.value?.data?.delivered_orders ?? 0),
            recent_orders: Array.isArray(summaryRes.value?.data?.recent_orders) ? summaryRes.value.data.recent_orders : [],
          });
        }

        if (walletRes.status === "fulfilled") {
          const nextBalance = Number(walletRes.value?.data?.balance ?? walletRes.value?.data?.wallet_balance ?? 0);
          setWalletBalance(Number.isFinite(nextBalance) ? nextBalance : 0);
        }
      } finally {
        if (mounted) setLoading(false);
      }
    };

    loadData();

    return () => {
      mounted = false;
    };
  }, []);

  const stats = useMemo(
    () => ({
      totalOrders: Number(summary.total_orders || 0),
      activeOrders: Number(summary.active_orders || 0),
      deliveredOrders: Number(summary.delivered_orders || 0),
    }),
    [summary]
  );

  return (
    <RoleDashboardLayout role="buyer" title="Buyer Dashboard">
      <div className="mb-8">
        <h1 className="text-2xl font-bold">Buyer Dashboard</h1>
        <p className="text-gray-500">Welcome back, {user?.name}</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        <div className="bg-white rounded-xl shadow p-6">
          <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
            <ShoppingBag className="w-6 h-6 text-blue-600" />
          </div>
          <p className="text-2xl font-bold">{loading ? "..." : stats.totalOrders}</p>
          <p className="text-gray-500 text-sm">Total Orders</p>
        </div>

        <div className="bg-white rounded-xl shadow p-6">
          <div className="w-12 h-12 bg-yellow-100 rounded-lg flex items-center justify-center mb-4">
            <Clock3 className="w-6 h-6 text-yellow-600" />
          </div>
          <p className="text-2xl font-bold">{loading ? "..." : stats.activeOrders}</p>
          <p className="text-gray-500 text-sm">Active Orders</p>
        </div>

        <div className="bg-white rounded-xl shadow p-6">
          <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mb-4">
            <CheckCircle2 className="w-6 h-6 text-green-600" />
          </div>
          <p className="text-2xl font-bold">{loading ? "..." : stats.deliveredOrders}</p>
          <p className="text-gray-500 text-sm">Delivered Orders</p>
        </div>

        <div className="bg-white rounded-xl shadow p-6">
          <div className="w-12 h-12 bg-emerald-100 rounded-lg flex items-center justify-center mb-4">
            <Wallet className="w-6 h-6 text-emerald-700" />
          </div>
          <p className="text-2xl font-bold">₹{loading ? "..." : walletBalance}</p>
          <p className="text-gray-500 text-sm">Wallet Balance</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white rounded-xl shadow p-6">
          <h2 className="text-lg font-semibold mb-4">Quick Actions</h2>
          <div className="space-y-3">
            <Link to="/buyer/orders" className="flex items-center justify-between p-3 bg-gray-50 rounded-lg hover:bg-gray-100">
              <span className="flex items-center gap-3">
                <ShoppingBag className="w-5 h-5 text-gray-600" />
                View My Orders
              </span>
              <ArrowRight className="w-4 h-4 text-gray-400" />
            </Link>
            <Link to="/buyer/wallet" className="flex items-center justify-between p-3 bg-gray-50 rounded-lg hover:bg-gray-100">
              <span className="flex items-center gap-3">
                <Wallet className="w-5 h-5 text-gray-600" />
                Open Wallet
              </span>
              <ArrowRight className="w-4 h-4 text-gray-400" />
            </Link>
            <Link to="/products" className="flex items-center justify-between p-3 bg-gray-50 rounded-lg hover:bg-gray-100">
              <span className="flex items-center gap-3">
                <ShoppingBag className="w-5 h-5 text-gray-600" />
                Continue Shopping
              </span>
              <ArrowRight className="w-4 h-4 text-gray-400" />
            </Link>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow p-6">
          <h2 className="text-lg font-semibold mb-4">Recent Order Snapshot</h2>
          {loading ? (
            <p className="text-gray-500">Loading orders...</p>
          ) : summary.recent_orders.length === 0 ? (
            <p className="text-gray-500">No orders yet. Place your first order from nearby stores.</p>
          ) : (
            <div className="space-y-2">
              {summary.recent_orders.map((order) => (
                <div key={order.id} className="flex items-center justify-between text-sm border rounded-lg px-3 py-2">
                  <span>Order #{order.id}</span>
                  <span className="capitalize text-gray-600">{order.status || "placed"}</span>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </RoleDashboardLayout>
  );
}
