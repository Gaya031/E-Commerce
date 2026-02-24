import { useState, useEffect } from "react";
import Navbar from "../../components/navbar/Navbar";
import Footer from "../../components/footer/Footer";
import { getWallet } from "../../api/wallet.api";
import { Wallet as WalletIcon, ArrowUpRight, ArrowDownLeft, CreditCard } from "lucide-react";

export default function BuyerWallet() {
  const [wallet, setWallet] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchWallet();
  }, []);

  const fetchWallet = async () => {
    try {
      const response = await getWallet();
      setWallet(response.data);
    } catch (err) {
      console.error("Error fetching wallet:", err);
      setError("Failed to load wallet");
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString("en-IN", {
      year: "numeric",
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Navbar />
        <div className="flex items-center justify-center h-96">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-600"></div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      
      <div className="max-w-4xl mx-auto px-4 py-8">
        <h1 className="text-2xl font-bold mb-6">My Wallet</h1>

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded mb-4">
            {error}
          </div>
        )}

        {/* Wallet Balance Card */}
        <div className="bg-gradient-to-r from-green-600 to-green-500 rounded-xl p-6 text-white mb-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-green-100 text-sm mb-1">Available Balance</p>
              <p className="text-4xl font-bold">₹{wallet?.balance || 0}</p>
            </div>
            <div className="w-16 h-16 bg-white/20 rounded-full flex items-center justify-center">
              <WalletIcon className="w-8 h-8" />
            </div>
          </div>
          
          <div className="flex gap-3 mt-6">
            <button className="flex-1 bg-white text-green-600 py-2 rounded-lg font-medium hover:bg-green-50">
              Add Money
            </button>
            <button className="flex-1 bg-white/20 text-white py-2 rounded-lg font-medium hover:bg-white/30">
              Send Money
            </button>
          </div>
        </div>

        {/* Transaction History */}
        <div className="bg-white rounded-lg shadow">
          <div className="p-4 border-b">
            <h2 className="text-lg font-semibold">Transaction History</h2>
          </div>

          {wallet?.transactions?.length === 0 ? (
            <div className="p-8 text-center text-gray-500">
              <CreditCard className="w-12 h-12 mx-auto mb-3 text-gray-400" />
              <p>No transactions yet</p>
            </div>
          ) : (
            <div className="divide-y">
              {wallet?.transactions?.map((txn, index) => (
                <div key={index} className="p-4 flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className={`w-10 h-10 rounded-full flex items-center justify-center ${
                      txn.type === "credit" ? "bg-green-100" : "bg-red-100"
                    }`}>
                      {txn.type === "credit" ? (
                        <ArrowDownLeft className="w-5 h-5 text-green-600" />
                      ) : (
                        <ArrowUpRight className="w-5 h-5 text-red-600" />
                      )}
                    </div>
                    <div>
                      <p className="font-medium">{txn.description || txn.type}</p>
                      <p className="text-sm text-gray-500">{formatDate(txn.created_at)}</p>
                    </div>
                  </div>
                  <p className={`font-semibold ${
                    txn.type === "credit" ? "text-green-600" : "text-red-600"
                  }`}>
                    {txn.type === "credit" ? "+" : "-"}₹{txn.amount}
                  </p>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      <Footer />
    </div>
  );
}

