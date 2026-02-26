import { useEffect, useState } from "react";
import { getRefundQueue, refundOrder } from "../../api/admin.api";
import RoleDashboardLayout from "../../components/layouts/RoleDashboardLayout";

export default function AdminRefundControl() {
  const [rows, setRows] = useState([]);
  const load = () => getRefundQueue().then((res) => setRows(res.data || []));
  useEffect(load, []);

  const refund = async (orderId) => {
    await refundOrder(orderId);
    load();
  };

  return (
    <RoleDashboardLayout role="admin" title="Refund Control">
      <div className="max-w-5xl">
        <div className="bg-white rounded-xl shadow p-4 space-y-3">
          {rows.map((r) => (
            <div key={r.id} className="border rounded p-3 flex justify-between items-center">
              <p>Order #{r.id}</p>
              <button className="px-3 py-1 bg-purple-600 text-white rounded" onClick={() => refund(r.id)}>
                Initiate Refund
              </button>
            </div>
          ))}
          {!rows.length && <p>No refunds pending.</p>}
        </div>
      </div>
    </RoleDashboardLayout>
  );
}
