import { useState, useEffect } from "react";
import { MapPin } from "lucide-react";
import { useLocationStore } from "../../store/location.store";

export default function LocationSelector() {
  const { location, address, city, fetchLocation } = useLocationStore();
  const [showModal, setShowModal] = useState(false);
  const [formData, setFormData] = useState({
    address: "",
    city: "",
    state: "",
    pincode: "",
    latitude: "",
    longitude: ""
  });

  useEffect(() => {
    fetchLocation();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const { saveLocation } = useLocationStore.getState();
    await saveLocation(formData);
    setShowModal(false);
  };

  const displayLocation = address || city 
    ? `${address || ""} ${city ? `, ${city}` : ""}`.trim() 
    : location?.label || "Select Location";

  return (
    <>
      <div 
        className="text-sm text-gray-600 cursor-pointer hover:text-gray-900 flex items-center gap-1"
        onClick={() => setShowModal(true)}
      >
        <MapPin className="w-4 h-4" />
        <span className="hidden md:inline">
          Delivering to <b>{displayLocation}</b>
        </span>
        <span className="md:hidden">
          <b>{city || "Location"}</b>
        </span>
      </div>

      {showModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md">
            <h2 className="text-xl font-bold mb-4">Update Delivery Location</h2>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-1">Address</label>
                <input
                  type="text"
                  value={formData.address}
                  onChange={(e) => setFormData({ ...formData, address: e.target.value })}
                  className="w-full px-3 py-2 border rounded-lg"
                  placeholder="Enter your address"
                  required
                />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium mb-1">City</label>
                  <input
                    type="text"
                    value={formData.city}
                    onChange={(e) => setFormData({ ...formData, city: e.target.value })}
                    className="w-full px-3 py-2 border rounded-lg"
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-1">State</label>
                  <input
                    type="text"
                    value={formData.state}
                    onChange={(e) => setFormData({ ...formData, state: e.target.value })}
                    className="w-full px-3 py-2 border rounded-lg"
                  />
                </div>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium mb-1">Pincode</label>
                  <input
                    type="text"
                    value={formData.pincode}
                    onChange={(e) => setFormData({ ...formData, pincode: e.target.value })}
                    className="w-full px-3 py-2 border rounded-lg"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-1">Latitude</label>
                  <input
                    type="text"
                    value={formData.latitude}
                    onChange={(e) => setFormData({ ...formData, latitude: e.target.value })}
                    className="w-full px-3 py-2 border rounded-lg"
                    placeholder="e.g., 28.6292"
                  />
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Longitude</label>
                <input
                  type="text"
                  value={formData.longitude}
                  onChange={(e) => setFormData({ ...formData, longitude: e.target.value })}
                  className="w-full px-3 py-2 border rounded-lg"
                  placeholder="e.g., 77.3725"
                />
              </div>
              <div className="flex gap-3 pt-4">
                <button
                  type="button"
                  onClick={() => setShowModal(false)}
                  className="flex-1 px-4 py-2 border rounded-lg hover:bg-gray-50"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="flex-1 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700"
                >
                  Save Location
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </>
  );
}
