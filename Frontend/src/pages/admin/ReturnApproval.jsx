import { useEffect, useState } from "react";
import { decideReturn, getPendingReturns } from "../../api/admin.api";
import RoleDashboardLayout from "../../components/layouts/RoleDashboardLayout";

export default function AdminReturnApproval() {
  const [rows, setRows] = useState([]);
  const load = () => getPendingReturns().then((res) => setRows(res.data || []));
  useEffect(load, []);

  const decide = async (id, approved) => {
    await decideReturn(id, { approved });
    load();
  };

  return (
    <RoleDashboardLayout role="admin" title="Return Approval">
      <div className="max-w-5xl">
        <div className="bg-white rounded-xl shadow p-4 space-y-3">
          {rows.map((r) => (
            <div key={r.id} className="border rounded p-3 flex justify-between items-center">
              <p>Order #{r.id}</p>
              <div className="space-x-2">
                <button className="px-3 py-1 bg-green-600 text-white rounded" onClick={() => decide(r.id, true)}>Approve</button>
                <button className="px-3 py-1 bg-red-600 text-white rounded" onClick={() => decide(r.id, false)}>Reject</button>
              </div>
            </div>
          ))}
          {!rows.length && <p>No pending returns.</p>}
        </div>
      </div>
    </RoleDashboardLayout>
  );
}
