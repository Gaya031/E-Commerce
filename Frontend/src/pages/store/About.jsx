import { useOutletContext } from "react-router-dom";

export default function About() {
  const { store } = useOutletContext();

  return (
    <div className="bg-white rounded-xl p-5 space-y-3">
      <h3 className="text-lg font-semibold">About {store.store_name}</h3>
      <p className="text-gray-700">{store.description || "No description provided by the store."}</p>
      <div className="text-sm text-gray-600 space-y-1">
        <p>
          <span className="font-medium">Address:</span> {store.address || "Not provided"}
        </p>
        <p>
          <span className="font-medium">City:</span> {store.city || "Not provided"}
        </p>
        <p>
          <span className="font-medium">Pincode:</span> {store.pincode || "Not provided"}
        </p>
        <p>
          <span className="font-medium">Delivery Radius:</span> {store.delivery_radius_km || 0} km
        </p>
        <p>
          <span className="font-medium">Rating:</span> {store.average_rating || 0} ({store.total_reviews || 0} reviews)
        </p>
      </div>
    </div>
  );
}
