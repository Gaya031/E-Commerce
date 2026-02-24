import { useState, useEffect } from "react";
import Navbar from "../../components/navbar/Navbar";
import Footer from "../../components/footer/Footer";
import { getAllOrders, refundOrder, decideReturn } from "../../api/admin.api";
import { ShoppingBag, CheckCircle, XCircle, RefreshCw } from "lucide-react";

export default function AdminOrders() {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState("all");

  useEffect(() => {
    fetchOrders();
  }, []);

  const fetchOrders = async () => {
    try {
      const response = await getAllOrders();
      setOrders(response.data || []);
    } catch (err) {
      console.error("Error fetching orders:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleRefund = async (orderId) => {
    try {
      await refundOrder(orderId);
      fetchOrders();
    } catch (err) {
      console.error("Error refunding order:", err);
    }
  };

  const handleReturnDecision = async (orderId, approved) => {
    try {
      await decideReturn(orderId, { approved });
      fetchOrders();
    } catch (err) {
      console.error("Error deciding return:", err);
    }
  };

  const getStatusColor = (status) => {
    switch (status?.toLowerCase()) {
      case "delivered":
        return "bg-green-100 text-green-800";
      case "cancelled":
        return "bg-red-100 text-red-800";
      case "refunded":
        return "bg-gray-100 text-gray-800";
      default:
        return "bg-yellow-100 text-yellow-800";
    }
  };

  const filteredOrders = filter === "all" 
    ? orders 
    : orders.filter(o => o.status?.toLowerCase() === filter);

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Navbar />
        <div className="flex items-center justify-center h-96">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-600"></div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      
      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="flex items-center gap-2 mb-6">
          <ShoppingBag className="w-8 h-8 text-purple-600" />
          <h1 className="text-2xl font-bold">Order Management</h1>
        </div>

        {/* Filter */}
        <div className="flex gap-2 mb-6">
          {["all", "processing", "shipped", "delivered", "cancelled", "refunded"].map((status) => (
            <button
              key={status}
              onClick={() => setFilter(status)}
              className={`px-4 py-2 rounded-lg capitalize ${
                filter === status 
                  ? "bg-green-600 text-white" 
                  : "bg-white text-gray-600 hover:bg-gray-100"
              }`}
            >
              {status}
            </button>
          ))}
        </div>

        {filteredOrders.length === 0 ? (
          <div className="bg-white rounded-lg shadow p-8 text-center">
            <ShoppingBag className="w-16 h-16 mx-auto text-gray-400 mb-4" />
            <h2 className="text-xl font-semibold mb-2">No orders found</h2>
          </div>
        ) : (
          <div className="space-y-4">
            {filteredOrders.map((order) => (
              <div key={order.id} className="bg-white rounded-lg shadow p-4">
                <div className="flex items-center justify-between mb-4">
                  <div>
                    <p className="text-sm text-gray-500">Order ID</p>
                    <p className="font-semibold">#{order.id}</p>
                  </div>
                  <span className={`px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(order.status)}`}>
                    {order.status || "Processing"}
                  </span>
                </div>

                <div className="border-t pt-4">
                  <p className="text-sm text-gray-500 mb-2">Items</p>
                  <div className="space-y-2">
                    {order.items?.map((item, idx) => (
                      <div key={idx} className="flex justify-between text-sm">
                        <span>{item.title} x {item.quantity}</span>
                        <span className="font-medium">₹{item.price * item.quantity}</span>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="border-t pt-4 mt-4 flex justify-between items-center">
                  <p className="text-xl font-bold">₹{order.total_amount || order.total}</p>
                  <div className="flex gap-2">
                    {order.status === "paid" && (
                      <button 
                        onClick={() => handleRefund(order.id)}
                        className="flex items-center gap-1 px-3 py-1 bg-red-100 text-red-700 rounded hover:bg-red-200"
                      >
                        <RefreshCw className="w-4 h-4" /> Refund
                      </button>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      <Footer />
    </div>
  );
}

