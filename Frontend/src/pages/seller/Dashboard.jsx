import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import Navbar from "../../components/navbar/Navbar";
import Footer from "../../components/footer/Footer";
import { useAuthStore } from "../../store/auth.store";
import { Package, ShoppingBag, DollarSign, TrendingUp, ArrowRight } from "lucide-react";

export default function SellerDashboard() {
  const user = useAuthStore((s) => s.user);
  const [stats] = useState({
    totalProducts: 0,
    totalOrders: 0,
    totalRevenue: 0,
    pendingOrders: 0,
  });

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      
      <div className="max-w-7xl mx-auto px-4 py-8">
        {/* Header */}
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

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
          <div className="bg-white rounded-xl shadow p-6">
            <div className="flex items-center justify-between mb-4">
              <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                <Package className="w-6 h-6 text-blue-600" />
              </div>
              <span className="text-green-500 text-sm flex items-center gap-1">
                <TrendingUp className="w-3 h-3" /> +12%
              </span>
            </div>
            <p className="text-2xl font-bold">{stats.totalProducts}</p>
            <p className="text-gray-500 text-sm">Total Products</p>
          </div>

          <div className="bg-white rounded-xl shadow p-6">
            <div className="flex items-center justify-between mb-4">
              <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center">
                <ShoppingBag className="w-6 h-6 text-purple-600" />
              </div>
              <span className="text-green-500 text-sm flex items-center gap-1">
                <TrendingUp className="w-3 h-3" /> +8%
              </span>
            </div>
            <p className="text-2xl font-bold">{stats.totalOrders}</p>
            <p className="text-gray-500 text-sm">Total Orders</p>
          </div>

          <div className="bg-white rounded-xl shadow p-6">
            <div className="flex items-center justify-between mb-4">
              <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
                <DollarSign className="w-6 h-6 text-green-600" />
              </div>
              <span className="text-green-500 text-sm flex items-center gap-1">
                <TrendingUp className="w-3 h-3" /> +15%
              </span>
            </div>
            <p className="text-2xl font-bold">₹{stats.totalRevenue.toLocaleString()}</p>
            <p className="text-gray-500 text-sm">Total Revenue</p>
          </div>

          <div className="bg-white rounded-xl shadow p-6">
            <div className="flex items-center justify-between mb-4">
              <div className="w-12 h-12 bg-yellow-100 rounded-lg flex items-center justify-center">
                <ShoppingBag className="w-6 h-6 text-yellow-600" />
              </div>
            </div>
            <p className="text-2xl font-bold">{stats.pendingOrders}</p>
            <p className="text-gray-500 text-sm">Pending Orders</p>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="bg-white rounded-xl shadow p-6">
            <h2 className="text-lg font-semibold mb-4">Quick Actions</h2>
            <div className="space-y-3">
              <Link 
                to="/seller/products" 
                className="flex items-center justify-between p-3 bg-gray-50 rounded-lg hover:bg-gray-100"
              >
                <span className="flex items-center gap-3">
                  <Package className="w-5 h-5 text-gray-600" />
                  Manage Products
                </span>
                <ArrowRight className="w-4 h-4 text-gray-400" />
              </Link>
              <Link 
                to="/seller/orders" 
                className="flex items-center justify-between p-3 bg-gray-50 rounded-lg hover:bg-gray-100"
              >
                <span className="flex items-center gap-3">
                  <ShoppingBag className="w-5 h-5 text-gray-600" />
                  View Orders
                </span>
                <ArrowRight className="w-4 h-4 text-gray-400" />
              </Link>
            </div>
          </div>

          <div className="bg-white rounded-xl shadow p-6">
            <h2 className="text-lg font-semibold mb-4">Recent Orders</h2>
            <div className="text-center py-8 text-gray-500">
              <ShoppingBag className="w-12 h-12 mx-auto mb-3 text-gray-400" />
              <p>No recent orders</p>
            </div>
          </div>
        </div>
      </div>

      <Footer />
    </div>
  );
}

