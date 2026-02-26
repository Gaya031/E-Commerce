import { useEffect, useState } from "react";
import { getSellerCommissionDetails } from "../../api/seller.api";
import RoleDashboardLayout from "../../components/layouts/RoleDashboardLayout";

export default function SellerCommission() {
  const [data, setData] = useState(null);
  useEffect(() => {
    getSellerCommissionDetails().then((res) => setData(res.data));
  }, []);

  return (
    <RoleDashboardLayout role="seller" title="Commission Details">
      <div className="max-w-4xl">
        {!data ? (
          <p>Loading...</p>
        ) : (
          <div className="bg-white rounded-xl shadow p-6 space-y-2">
            <p>Current Commission %: <b>{data.current_commission_percent}</b></p>
            <p>Total Platform Commission: <b>₹{data.total_platform_commission}</b></p>
            <p>Total Seller Earnings: <b>₹{data.total_seller_earnings}</b></p>
          </div>
        )}
      </div>
    </RoleDashboardLayout>
  );
}
