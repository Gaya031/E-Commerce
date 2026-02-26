import { useState } from "react";
import { updateCommissionConfig } from "../../api/admin.api";
import RoleDashboardLayout from "../../components/layouts/RoleDashboardLayout";

export default function AdminCommissionConfig() {
  const [sellerId, setSellerId] = useState("");
  const [percent, setPercent] = useState("10");
  const [message, setMessage] = useState("");

  const submit = async (e) => {
    e.preventDefault();
    try {
      const res = await updateCommissionConfig(Number(sellerId), Number(percent));
      setMessage(JSON.stringify(res.data));
    } catch (err) {
      setMessage(err?.response?.data?.detail || "Update failed");
    }
  };

  return (
    <RoleDashboardLayout role="admin" title="Commission Configuration">
      <div className="max-w-xl">
        <form onSubmit={submit} className="bg-white rounded-xl shadow p-6 space-y-4">
          <input className="w-full border rounded px-3 py-2" placeholder="Seller ID" value={sellerId} onChange={(e)=>setSellerId(e.target.value)} required />
          <input className="w-full border rounded px-3 py-2" placeholder="Commission %" value={percent} onChange={(e)=>setPercent(e.target.value)} required />
          <button className="w-full bg-gray-900 text-white py-2 rounded">Update</button>
          {message && <p className="text-sm">{message}</p>}
        </form>
      </div>
    </RoleDashboardLayout>
  );
}
