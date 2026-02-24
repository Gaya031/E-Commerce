import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import Navbar from "../../components/navbar/Navbar";
import Footer from "../../components/footer/Footer";
import { useAuthStore } from "../../store/auth.store";
import { Users, ShoppingBag, DollarSign, Package, ArrowRight } from "lucide-react";

export default function AdminDashboard() {
  const user = useAuthStore((s) => s.user);
  const [stats] = useState({
    totalSellers: 0,
    totalOrders: 0,
    totalRevenue: 0,
    activeUsers: 0,
  });

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      
      <div className="max-w-7xl mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-2xl font-bold">Admin Dashboard</h1>
          <p className="text-gray-500">Welcome back, {user?.name}</p>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
          <div className="bg-white rounded-xl shadow p-6">
            <div className="flex items-center justify-between mb-4">
              <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                <Users className="w-6 h-6 text-blue-600" />
              </div>
            </div>
            <p className="text-2xl font-bold">{stats.totalSellers}</p>
            <p className="text-gray-500 text-sm">Total Sellers</p>
          </div>

          <div className="bg-white rounded-xl shadow p-6">
            <div className="flex items-center justify-between mb-4">
              <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center">
                <ShoppingBag className="w-6 h-6 text-purple-600" />
              </div>
            </div>
            <p className="text-2xl font-bold">{stats.totalOrders}</p>
            <p className="text-gray-500 text-sm">Total Orders</p>
          </div>

          <div className="bg-white rounded-xl shadow p-6">
            <div className="flex items-center justify-between mb-4">
              <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
                <DollarSign className="w-6 h-6 text-green-600" />
              </div>
            </div>
            <p className="text-2xl font-bold">₹{stats.totalRevenue.toLocaleString()}</p>
            <p className="text-gray-500 text-sm">Total Revenue</p>
          </div>

          <div className="bg-white rounded-xl shadow p-6">
            <div className="flex items-center justify-between mb-4">
              <div className="w-12 h-12 bg-yellow-100 rounded-lg flex items-center justify-center">
                <Users className="w-6 h-6 text-yellow-600" />
              </div>
            </div>
            <p className="text-2xl font-bold">{stats.activeUsers}</p>
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
                to="/admin/products" 
                className="flex items-center justify-between p-3 bg-gray-50 rounded-lg hover:bg-gray-100"
              >
                <span className="flex items-center gap-3">
                  <Package className="w-5 h-5 text-gray-600" />
                  Manage Products
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
      </div>

      <Footer />
    </div>
  );
}

