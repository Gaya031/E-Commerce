import { useEffect, useState } from "react";

import RoleDashboardLayout from "../../components/layouts/RoleDashboardLayout";
import { getSellerProfile, updateMySellerKYC } from "../../api/seller.api";

export default function SellerKYCUpload() {
  const [hasProfile, setHasProfile] = useState(false);
  const [form, setForm] = useState({ aadhar: "", pan: "", gst: "", business_proof: "" });
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getSellerProfile()
      .then((res) => {
        setHasProfile(true);
        const docs = res.data?.kyc_docs || {};
        setForm({
          aadhar: docs.aadhar || "",
          pan: docs.pan || "",
          gst: docs.gst || "",
          business_proof: docs.business_proof || "",
        });
      })
      .catch(() => setHasProfile(false))
      .finally(() => setLoading(false));
  }, []);

  const submit = async (e) => {
    e.preventDefault();
    setMessage("");
    try {
      await updateMySellerKYC(form);
      setMessage("KYC uploaded successfully.");
    } catch (err) {
      setMessage(err?.response?.data?.detail || "KYC upload failed");
    }
  };

  return (
    <RoleDashboardLayout role="seller" title="Seller KYC Upload">
      <div className="max-w-xl">
        {loading ? (
          <p>Loading...</p>
        ) : !hasProfile ? (
          <div className="bg-white p-6 rounded-xl shadow">
            <p className="text-sm text-gray-700">Create your seller profile first from onboarding page.</p>
          </div>
        ) : (
          <form onSubmit={submit} className="bg-white p-6 rounded-xl shadow space-y-4">
            <input
              className="w-full border rounded px-3 py-2"
              placeholder="Aadhar"
              value={form.aadhar}
              onChange={(e) => setForm({ ...form, aadhar: e.target.value })}
            />
            <input
              className="w-full border rounded px-3 py-2"
              placeholder="PAN"
              value={form.pan}
              onChange={(e) => setForm({ ...form, pan: e.target.value })}
            />
            <input
              className="w-full border rounded px-3 py-2"
              placeholder="GST"
              value={form.gst}
              onChange={(e) => setForm({ ...form, gst: e.target.value })}
            />
            <input
              className="w-full border rounded px-3 py-2"
              placeholder="Business proof URL"
              value={form.business_proof}
              onChange={(e) => setForm({ ...form, business_proof: e.target.value })}
            />
            <button className="w-full bg-blue-600 text-white py-2 rounded">Upload KYC</button>
            {message && <p className="text-sm">{message}</p>}
          </form>
        )}
      </div>
    </RoleDashboardLayout>
  );
}
