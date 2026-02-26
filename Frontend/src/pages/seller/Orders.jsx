import { useState, useEffect } from "react";
import { getSellerOrders, updateSellerOrderStatus } from "../../api/seller.api";
import { Package, Clock, CheckCircle, XCircle } from "lucide-react";
import RoleDashboardLayout from "../../components/layouts/RoleDashboardLayout";

export default function SellerOrders() {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState("all");
  const [message, setMessage] = useState("");

  useEffect(() => {
    fetchOrders();
  }, []);

  const fetchOrders = async () => {
    try {
      const response = await getSellerOrders();
      setOrders(response.data || []);
      setMessage("");
    } catch (err) {
      setMessage(err?.response?.data?.detail || "Error fetching orders");
    } finally {
      setLoading(false);
    }
  };

  const updateStatus = async (orderId, status) => {
    try {
      await updateSellerOrderStatus(orderId, status);
      fetchOrders();
    } catch (err) {
      setMessage(err?.response?.data?.detail || "Failed to update order status");
    }
  };

  const getStatusIcon = (status) => {
    switch (status?.toLowerCase()) {
      case "delivered":
        return <CheckCircle className="w-5 h-5 text-green-500" />;
      case "cancelled":
        return <XCircle className="w-5 h-5 text-red-500" />;
      default:
        return <Clock className="w-5 h-5 text-yellow-500" />;
    }
  };

  const getStatusColor = (status) => {
    switch (status?.toLowerCase()) {
      case "delivered":
        return "bg-green-100 text-green-800";
      case "cancelled":
        return "bg-red-100 text-red-800";
      case "packed":
      case "shipped":
        return "bg-blue-100 text-blue-800";
      case "placed":
      default:
        return "bg-yellow-100 text-yellow-800";
    }
  };

  const filteredOrders = filter === "all" 
    ? orders 
    : orders.filter(o => o.status?.toLowerCase() === filter);

  if (loading) {
    return (
      <RoleDashboardLayout role="seller" title="Order Management">
        <div className="flex items-center justify-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-600"></div>
        </div>
      </RoleDashboardLayout>
    );
  }

  return (
    <RoleDashboardLayout role="seller" title="Order Management">

        {/* Filter */}
        <div className="flex gap-2 mb-6">
          {["all", "placed", "packed", "shipped", "delivered", "cancelled"].map((status) => (
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
        {message && <p className="text-sm text-red-600 mb-3">{message}</p>}

        {filteredOrders.length === 0 ? (
          <div className="bg-white rounded-lg shadow p-8 text-center">
            <Package className="w-16 h-16 mx-auto text-gray-400 mb-4" />
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
                  <div className="flex items-center gap-2">
                    {getStatusIcon(order.status)}
                    <span className={`px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(order.status)}`}>
                      {order.status || "Processing"}
                    </span>
                  </div>
                </div>

                <div className="border-t pt-4">
                  <p className="text-sm text-gray-500 mb-2">Items</p>
                  <div className="space-y-2">
                    {order.items?.map((item, idx) => (
                      <div key={idx} className="flex justify-between text-sm">
                        <span>Product #{item.product_id} x {item.quantity}</span>
                        <span className="font-medium">₹{item.price * item.quantity}</span>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="border-t pt-4 mt-4">
                  <p className="text-xl font-bold text-right">₹{order.total_amount || order.total}</p>
                </div>
                {order.status !== "delivered" && order.status !== "cancelled" && (
                  <div className="border-t pt-3 mt-3 flex gap-2 justify-end">
                    {order.status === "placed" && (
                      <button
                        onClick={() => updateStatus(order.id, "packed")}
                        className="px-3 py-1 text-sm rounded bg-blue-600 text-white"
                      >
                        Mark Packed
                      </button>
                    )}
                    {(order.status === "placed" || order.status === "packed") && (
                      <button
                        onClick={() => updateStatus(order.id, "shipped")}
                        className="px-3 py-1 text-sm rounded bg-green-600 text-white"
                      >
                        Mark Shipped
                      </button>
                    )}
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
    </RoleDashboardLayout>
  );
}
