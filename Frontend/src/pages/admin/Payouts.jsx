import { useState } from "react";
import { payoutSeller, payoutDeliveryPartner } from "../../api/admin.api";
import { DollarSign, CheckCircle, Truck } from "lucide-react";
import RoleDashboardLayout from "../../components/layouts/RoleDashboardLayout";
import { pushToast } from "../../store/toast.store";

export default function AdminPayouts() {
  const [loading, setLoading] = useState(false);

  const handlePayout = async (type, id) => {
    setLoading(true);
    try {
      if (type === "seller") {
        await payoutSeller(id);
      } else {
        await payoutDeliveryPartner(id);
      }
      pushToast({ type: "success", message: "Payout initiated successfully." });
    } catch (err) {
      console.error("Error initiating payout:", err);
      pushToast({ type: "error", message: "Failed to initiate payout." });
    } finally {
      setLoading(false);
    }
  };

  return (
    <RoleDashboardLayout role="admin" title="Payout Management">
        <div className="flex items-center gap-2 mb-6">
          <DollarSign className="w-8 h-8 text-purple-600" />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Seller Payouts */}
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center gap-2 mb-4">
              <CheckCircle className="w-6 h-6 text-green-600" />
              <h2 className="text-lg font-semibold">Seller Payouts</h2>
            </div>
            <p className="text-gray-500 mb-4">
              Process payouts to sellers after deducting platform commission.
            </p>
            <button 
              onClick={() => handlePayout("seller", 1)}
              disabled={loading}
              className="w-full bg-green-600 text-white py-2 rounded-lg hover:bg-green-700 disabled:opacity-50"
            >
              {loading ? "Processing..." : "Process Seller Payouts"}
            </button>
          </div>

          {/* Delivery Partner Payouts */}
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center gap-2 mb-4">
              <Truck className="w-6 h-6 text-blue-600" />
              <h2 className="text-lg font-semibold">Delivery Partner Payouts</h2>
            </div>
            <p className="text-gray-500 mb-4">
              Process payouts to delivery partners for completed deliveries.
            </p>
            <button 
              onClick={() => handlePayout("delivery", 1)}
              disabled={loading}
              className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50"
            >
              {loading ? "Processing..." : "Process Delivery Payouts"}
            </button>
          </div>
        </div>
    </RoleDashboardLayout>
  );
}
