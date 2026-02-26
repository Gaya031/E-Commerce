import { useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { confirmDelivery } from "../../api/delivery.api";
import RoleDashboardLayout from "../../components/layouts/RoleDashboardLayout";

export default function DeliveryConfirmationPage() {
  const { deliveryId } = useParams();
  const [msg, setMsg] = useState("");
  const navigate = useNavigate();

  const confirm = async () => {
    try {
      await confirmDelivery(deliveryId);
      setMsg("Delivery confirmed.");
      setTimeout(() => navigate("/delivery/earnings"), 700);
    } catch (err) {
      setMsg(err?.response?.data?.detail || "Delivery confirmation failed");
    }
  };

  return (
    <RoleDashboardLayout role="delivery" title="Delivery Confirmation">
      <div className="max-w-xl">
        <div className="bg-white rounded-xl shadow p-6">
          <p className="mb-4">Delivery ID: {deliveryId}</p>
          <button onClick={confirm} className="bg-blue-600 text-white px-4 py-2 rounded">
            Confirm Delivered
          </button>
          {msg && <p className="mt-3 text-sm">{msg}</p>}
        </div>
      </div>
    </RoleDashboardLayout>
  );
}
