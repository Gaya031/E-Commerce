import { useEffect, useState } from "react";
import { getSellerSubscriptionStatus } from "../../api/seller.api";
import { getSubscriptionPlans } from "../../api/subscription.api";
import RoleDashboardLayout from "../../components/layouts/RoleDashboardLayout";

export default function SellerSubscriptionStatus() {
  const [status, setStatus] = useState(null);
  const [plans, setPlans] = useState([]);

  useEffect(() => {
    getSellerSubscriptionStatus().then((res) => setStatus(res.data));
    getSubscriptionPlans().then((res) => setPlans(res.data || []));
  }, []);

  return (
    <RoleDashboardLayout role="seller" title="Subscription Status">
      <div className="max-w-4xl">
        <div className="grid md:grid-cols-2 gap-4">
          <div className="bg-white rounded-xl shadow p-6">
            {!status ? (
              <p>Loading status...</p>
            ) : (
              <>
                <p>Plan ID: <b>{status.subscription_plan_id || "None"}</b></p>
                <p>Expiry: <b>{status.subscription_expiry || "N/A"}</b></p>
                <p>Approved: <b>{String(status.approved)}</b></p>
              </>
            )}
          </div>
          <div className="bg-white rounded-xl shadow p-6">
            <h2 className="font-semibold mb-2">Available Plans</h2>
            {plans.length ? plans.map((p) => (
              <div key={p.id} className="border-b py-2">
                <p className="font-medium">{p.plan_name}</p>
                <p className="text-sm text-gray-500">₹{p.price}</p>
              </div>
            )) : <p>No plans available</p>}
          </div>
        </div>
      </div>
    </RoleDashboardLayout>
  );
}
