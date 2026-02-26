import { useEffect, useState } from "react";
import { getRevenueAnalytics } from "../../api/admin.api";
import RoleDashboardLayout from "../../components/layouts/RoleDashboardLayout";

export default function AdminRevenueAnalytics() {
  const [data, setData] = useState(null);
  useEffect(() => {
    getRevenueAnalytics().then((res) => setData(res.data));
  }, []);

  return (
    <RoleDashboardLayout role="admin" title="Revenue Analytics">
      <div className="max-w-4xl">
        {!data ? (
          <p>Loading analytics...</p>
        ) : (
          <div className="grid md:grid-cols-2 gap-4">
            <div className="bg-white rounded-xl shadow p-6">Total Orders: <b>{data.total_orders}</b></div>
            <div className="bg-white rounded-xl shadow p-6">Delivered Orders: <b>{data.delivered_orders}</b></div>
            <div className="bg-white rounded-xl shadow p-6">Gross Revenue: <b>₹{data.gross_revenue}</b></div>
            <div className="bg-white rounded-xl shadow p-6">Platform Commission: <b>₹{data.platform_commission}</b></div>
          </div>
        )}
      </div>
    </RoleDashboardLayout>
  );
}
