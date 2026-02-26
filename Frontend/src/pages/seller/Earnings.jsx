import { useEffect, useState } from "react";
import { getSellerEarningsSummary } from "../../api/seller.api";
import RoleDashboardLayout from "../../components/layouts/RoleDashboardLayout";

export default function SellerEarnings() {
  const [data, setData] = useState(null);
  useEffect(() => {
    getSellerEarningsSummary().then((res) => setData(res.data));
  }, []);

  return (
    <RoleDashboardLayout role="seller" title="Seller Earnings Summary">
      <div className="max-w-3xl">
        {!data ? (
          <p>Loading...</p>
        ) : (
          <div className="bg-white rounded-xl shadow p-6">
            <p>Completed Orders: <b>{data.completed_orders}</b></p>
            <p>Gross Revenue: <b>₹{data.gross_revenue}</b></p>
          </div>
        )}
      </div>
    </RoleDashboardLayout>
  );
}
