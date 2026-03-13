import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import Navbar from "../../components/navbar/Navbar";
import Footer from "../../components/footer/Footer";
import { cancelOrder, getOrderById } from "../../api/order.api";
import { pushToast } from "../../store/toast.store";

export default function OrderDetail() {
  const { orderId } = useParams();
  const [order, setOrder] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [cancelling, setCancelling] = useState(false);

  useEffect(() => {
    const load = async () => {
      try {
        const res = await getOrderById(orderId);
        setOrder(res.data);
      } catch (err) {
        setError(err?.response?.data?.detail || "Failed to load order");
      } finally {
        setLoading(false);
      }
    };
    load();
  }, [orderId]);

  const canCancel = (status) => {
    const normalized = String(status || "").toLowerCase();
    return normalized === "placed" || normalized === "packed";
  };

  const onCancelOrder = async () => {
    if (!order || !canCancel(order.status)) return;
    if (!window.confirm("Cancel this order?")) return;

    setCancelling(true);
    try {
      const response = await cancelOrder(order.id);
      const refundStatus = response?.data?.refund_status;
      setOrder((prev) => (prev ? { ...prev, status: "cancelled", can_cancel: false } : prev));
      const refundMessage =
        refundStatus === "initiated"
          ? " Refund has been initiated."
          : refundStatus === "failed"
            ? " Refund initiation failed and will be handled manually."
            : "";
      pushToast({ type: "success", message: `Order cancelled successfully.${refundMessage}` });
    } catch (err) {
      pushToast({ type: "error", message: err?.response?.data?.detail || "Failed to cancel order." });
    } finally {
      setCancelling(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <div className="max-w-4xl mx-auto px-4 py-8">
        {loading && <p>Loading order...</p>}
        {!loading && error && <p className="text-red-600">{error}</p>}
        {!loading && order && (
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-start justify-between gap-4 mb-4">
              <h1 className="text-2xl font-bold">Order #{order.id}</h1>
              {canCancel(order.status) && (
                <button
                  type="button"
                  onClick={onCancelOrder}
                  disabled={cancelling}
                  className="px-3 py-2 rounded-lg border border-red-300 text-red-700 hover:bg-red-50 disabled:opacity-60"
                >
                  {cancelling ? "Cancelling..." : "Cancel Order"}
                </button>
              )}
            </div>
            <p className="mb-2">Status: <b>{order.status}</b></p>
            <p className="mb-4">Total: <b>₹{order.total_amount}</b></p>
            <h2 className="font-semibold mb-2">Items</h2>
            <div className="space-y-2">
              {order.items?.map((item, idx) => (
                <div key={idx} className="flex justify-between border-b pb-2">
                  <span>Product #{item.product_id} x {item.quantity}</span>
                  <span>₹{item.price * item.quantity}</span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
      <Footer />
    </div>
  );
}
