import { Link, useLocation } from "react-router-dom";
import Navbar from "../navbar/Navbar";

const navByRole = {
  buyer: [
    ["/buyer", "Dashboard"],
    ["/buyer/orders", "My Orders"],
    ["/buyer/wallet", "Wallet"],
    ["/products", "Browse Products"],
  ],
  seller: [
    ["/seller", "Dashboard"],
    ["/seller/onboarding", "Onboarding"],
    ["/seller/kyc", "KYC Upload"],
    ["/seller/approval-status", "Approval Status"],
    ["/seller/products", "Product Management"],
    ["/seller/orders", "Order Management"],
    ["/seller/earnings", "Earnings Summary"],
    ["/seller/commission", "Commission Details"],
    ["/seller/subscription", "Subscription Status"],
  ],
  admin: [
    ["/admin", "Dashboard"],
    ["/admin/sellers", "Seller Approval & KYC"],
    ["/admin/users", "User Management"],
    ["/admin/orders", "Order Monitoring"],
    ["/admin/returns", "Return Approval"],
    ["/admin/refunds", "Refund Control"],
    ["/admin/commission-config", "Commission Config"],
    ["/admin/revenue-analytics", "Revenue Analytics"],
    ["/admin/reports", "Reports & Exports"],
    ["/admin/payouts", "Payouts"],
  ],
  delivery: [
    ["/delivery", "Dashboard"],
    ["/delivery/available", "Available Deliveries"],
    ["/delivery/assigned", "Assigned Delivery"],
    ["/delivery/map", "Navigation Map"],
    ["/delivery/earnings", "Earnings Summary"],
  ],
};

export default function RoleDashboardLayout({ role, title, children }) {
  const location = useLocation();
  const links = navByRole[role] || [];

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <div className="max-w-7xl mx-auto px-4 py-6 grid grid-cols-12 gap-6">
        <aside className="col-span-12 lg:col-span-3">
          <div className="bg-white rounded-xl shadow p-4 sticky top-24">
            <h2 className="font-semibold mb-3 capitalize">{role} Panel</h2>
            <div className="space-y-1">
              {links.map(([to, label]) => {
                const active = location.pathname === to || location.pathname.startsWith(`${to}/`);
                return (
                  <Link
                    key={to}
                    to={to}
                    className={`block px-3 py-2 rounded-lg text-sm ${
                      active ? "bg-green-100 text-green-700 font-medium" : "hover:bg-gray-100 text-gray-700"
                    }`}
                  >
                    {label}
                  </Link>
                );
              })}
            </div>
          </div>
        </aside>
        <main className="col-span-12 lg:col-span-9">
          {title && <h1 className="text-2xl font-bold mb-4">{title}</h1>}
          {children}
        </main>
      </div>
    </div>
  );
}
