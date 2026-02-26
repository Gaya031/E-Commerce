import { useEffect, useState } from "react";
import { getDeliveryEarningsSummary } from "../../api/delivery.api";
import RoleDashboardLayout from "../../components/layouts/RoleDashboardLayout";

export default function DeliveryEarningsSummary() {
  const [data, setData] = useState(null);
  useEffect(() => {
    getDeliveryEarningsSummary().then((res) => setData(res.data));
  }, []);

  return (
    <RoleDashboardLayout role="delivery" title="Delivery Earnings Summary">
      <div className="max-w-3xl">
        {!data ? (
          <p>Loading...</p>
        ) : (
          <div className="bg-white rounded-xl shadow p-6">
            <p>Completed Deliveries: <b>{data.completed_deliveries}</b></p>
            <p>Total Earnings: <b>₹{data.total_earnings}</b></p>
          </div>
        )}
      </div>
    </RoleDashboardLayout>
  );
}
