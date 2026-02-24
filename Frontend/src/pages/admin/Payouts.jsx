import { useState, useEffect } from "react";
import Navbar from "../../components/navbar/Navbar";
import Footer from "../../components/footer/Footer";
import { payoutSeller, payoutDeliveryPartner } from "../../api/admin.api";
import { DollarSign, CheckCircle, Truck } from "lucide-react";

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
      alert("Payout initiated successfully!");
    } catch (err) {
      console.error("Error initiating payout:", err);
      alert("Failed to initiate payout");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      
      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="flex items-center gap-2 mb-6">
          <DollarSign className="w-8 h-8 text-purple-600" />
          <h1 className="text-2xl font-bold">Payout Management</h1>
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
              disabled={loading}
              className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50"
            >
              {loading ? "Processing..." : "Process Delivery Payouts"}
            </button>
          </div>
        </div>
      </div>

      <Footer />
    </div>
  );
}

