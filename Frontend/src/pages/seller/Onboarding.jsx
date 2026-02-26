import { useEffect, useState } from "react";

import RoleDashboardLayout from "../../components/layouts/RoleDashboardLayout";
import { createSellerProfile, getSellerProfile, updateSellerProfile } from "../../api/seller.api";

const initialForm = {
  store_name: "",
  description: "",
  address: "",
  city: "",
  pincode: "",
  latitude: "",
  longitude: "",
  logo_url: "",
  cover_image: "",
  delivery_radius_km: "5",
};

export default function SellerOnboarding() {
  const [form, setForm] = useState(initialForm);
  const [hasProfile, setHasProfile] = useState(false);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState("");

  useEffect(() => {
    getSellerProfile()
      .then((res) => {
        const p = res.data;
        setHasProfile(true);
        setForm({
          store_name: p.store_name || "",
          description: p.description || "",
          address: p.address || "",
          city: p.city || "",
          pincode: p.pincode || "",
          latitude: p.latitude || "",
          longitude: p.longitude || "",
          logo_url: p.logo_url || "",
          cover_image: p.cover_image || "",
          delivery_radius_km: String(p.delivery_radius_km || 5),
        });
      })
      .catch(() => {
        setHasProfile(false);
      })
      .finally(() => setLoading(false));
  }, []);

  const submit = async (e) => {
    e.preventDefault();
    setMessage("");
    try {
      const payload = {
        ...form,
        latitude: form.latitude ? Number(form.latitude) : undefined,
        longitude: form.longitude ? Number(form.longitude) : undefined,
        delivery_radius_km: Number(form.delivery_radius_km || 5),
      };
      if (hasProfile) {
        await updateSellerProfile(payload);
        setMessage("Seller profile updated.");
      } else {
        await createSellerProfile(payload);
        setMessage("Seller onboarding submitted.");
        setHasProfile(true);
      }
    } catch (err) {
      setMessage(err?.response?.data?.detail || "Failed to save seller profile");
    }
  };

  return (
    <RoleDashboardLayout role="seller" title="Seller Onboarding">
      <div className="max-w-2xl">
        {loading ? (
          <p>Loading...</p>
        ) : (
          <form onSubmit={submit} className="bg-white p-6 rounded-xl shadow space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <input
                className="w-full border rounded px-3 py-2"
                placeholder="Store name"
                value={form.store_name}
                onChange={(e) => setForm({ ...form, store_name: e.target.value })}
                required
              />
              <input
                className="w-full border rounded px-3 py-2"
                placeholder="City"
                value={form.city}
                onChange={(e) => setForm({ ...form, city: e.target.value })}
              />
            </div>
            <textarea
              className="w-full border rounded px-3 py-2 min-h-[90px]"
              placeholder="Description"
              value={form.description}
              onChange={(e) => setForm({ ...form, description: e.target.value })}
            />
            <input
              className="w-full border rounded px-3 py-2"
              placeholder="Address"
              value={form.address}
              onChange={(e) => setForm({ ...form, address: e.target.value })}
            />
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <input
                className="w-full border rounded px-3 py-2"
                placeholder="Pincode"
                value={form.pincode}
                onChange={(e) => setForm({ ...form, pincode: e.target.value })}
              />
              <input
                className="w-full border rounded px-3 py-2"
                placeholder="Latitude"
                value={form.latitude}
                onChange={(e) => setForm({ ...form, latitude: e.target.value })}
              />
              <input
                className="w-full border rounded px-3 py-2"
                placeholder="Longitude"
                value={form.longitude}
                onChange={(e) => setForm({ ...form, longitude: e.target.value })}
              />
            </div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <input
                className="w-full border rounded px-3 py-2"
                placeholder="Logo URL"
                value={form.logo_url}
                onChange={(e) => setForm({ ...form, logo_url: e.target.value })}
              />
              <input
                className="w-full border rounded px-3 py-2"
                placeholder="Cover Image URL"
                value={form.cover_image}
                onChange={(e) => setForm({ ...form, cover_image: e.target.value })}
              />
              <input
                type="number"
                min={1}
                max={50}
                className="w-full border rounded px-3 py-2"
                placeholder="Delivery radius (km)"
                value={form.delivery_radius_km}
                onChange={(e) => setForm({ ...form, delivery_radius_km: e.target.value })}
              />
            </div>
            <button className="w-full bg-green-600 text-white py-2 rounded">
              {hasProfile ? "Update Seller Profile" : "Submit Onboarding"}
            </button>
            {message && <p className="text-sm">{message}</p>}
          </form>
        )}
      </div>
    </RoleDashboardLayout>
  );
}
