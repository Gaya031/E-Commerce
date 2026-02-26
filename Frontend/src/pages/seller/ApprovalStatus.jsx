import { useEffect, useState } from "react";
import { getSellerApprovalStatus } from "../../api/seller.api";
import RoleDashboardLayout from "../../components/layouts/RoleDashboardLayout";

export default function SellerApprovalStatus() {
  const [data, setData] = useState(null);
  useEffect(() => {
    getSellerApprovalStatus().then((res) => setData(res.data));
  }, []);

  return (
    <RoleDashboardLayout role="seller" title="Approval Status">
      <div className="max-w-2xl">
        {!data ? (
          <p>Loading status...</p>
        ) : (
          <div className="bg-white rounded-xl shadow p-6">
            <p>Approved: <b>{String(data.approved)}</b></p>
            <p>KYC Status: <b>{String(data.kyc_status)}</b></p>
          </div>
        )}
      </div>
    </RoleDashboardLayout>
  );
}
