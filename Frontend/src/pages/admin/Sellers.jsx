import { useState, useEffect } from "react";
import { getSellers, approveSeller, blockUser } from "../../api/admin.api";
import { Users, CheckCircle, XCircle, Shield } from "lucide-react";
import RoleDashboardLayout from "../../components/layouts/RoleDashboardLayout";

export default function AdminSellers() {
  const [sellers, setSellers] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchSellers();
  }, []);

  const fetchSellers = async () => {
    try {
      const response = await getSellers();
      setSellers(response.data || []);
    } catch (err) {
      console.error("Error fetching sellers:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleApprove = async (sellerId, approved) => {
    try {
      await approveSeller(sellerId, { approved, commission_percent: 10 });
      fetchSellers();
    } catch (err) {
      console.error("Error approving seller:", err);
    }
  };

  const handleBlock = async (userId, blocked) => {
    try {
      await blockUser(userId, { blocked });
      fetchSellers();
    } catch (err) {
      console.error("Error blocking user:", err);
    }
  };

  if (loading) {
    return (
      <RoleDashboardLayout role="admin" title="Seller Management">
        <div className="flex items-center justify-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-600"></div>
        </div>
      </RoleDashboardLayout>
    );
  }

  return (
    <RoleDashboardLayout role="admin" title="Seller Management">
        <div className="flex items-center gap-2 mb-6">
          <Shield className="w-8 h-8 text-purple-600" />
        </div>

        {sellers.length === 0 ? (
          <div className="bg-white rounded-lg shadow p-8 text-center">
            <Users className="w-16 h-16 mx-auto text-gray-400 mb-4" />
            <h2 className="text-xl font-semibold mb-2">No sellers yet</h2>
          </div>
        ) : (
          <div className="bg-white rounded-lg shadow overflow-hidden">
            <table className="w-full">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Seller</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Store Name</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Commission</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {sellers.map((seller) => (
                  <tr key={seller.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4">
                      <div>
                        <p className="font-medium">{seller.user?.name}</p>
                        <p className="text-sm text-gray-500">{seller.user?.email}</p>
                      </div>
                    </td>
                    <td className="px-6 py-4">{seller.store_name}</td>
                    <td className="px-6 py-4">
                      <span className={`px-3 py-1 rounded-full text-xs font-medium ${
                        seller.is_approved 
                          ? "bg-green-100 text-green-800" 
                          : "bg-yellow-100 text-yellow-800"
                      }`}>
                        {seller.is_approved ? "Approved" : "Pending"}
                      </span>
                    </td>
                    <td className="px-6 py-4">{seller.commission_percent || 0}%</td>
                    <td className="px-6 py-4">
                      <div className="flex gap-2">
                        {!seller.is_approved && (
                          <>
                            <button
                              onClick={() => handleApprove(seller.id, true)}
                              className="p-2 text-green-600 hover:bg-green-50 rounded"
                              title="Approve"
                            >
                              <CheckCircle className="w-5 h-5" />
                            </button>
                            <button
                              onClick={() => handleApprove(seller.id, false)}
                              className="p-2 text-red-600 hover:bg-red-50 rounded"
                              title="Reject"
                            >
                              <XCircle className="w-5 h-5" />
                            </button>
                          </>
                        )}
                        {seller.user && (
                          <button
                            onClick={() => handleBlock(seller.user.id, !seller.user.is_blocked)}
                            className={`p-2 rounded ${
                              seller.user.is_blocked 
                                ? "text-green-600 hover:bg-green-50" 
                                : "text-red-600 hover:bg-red-50"
                            }`}
                            title={seller.user.is_blocked ? "Unblock" : "Block"}
                          >
                            <Shield className="w-5 h-5" />
                          </button>
                        )}
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
    </RoleDashboardLayout>
  );
}
