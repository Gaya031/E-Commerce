import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { getStoreDetails } from "../../api/store.api";

export default function ProfileVariant3() {
  const { storeId } = useParams();
  const [store, setStore] = useState(null);
  useEffect(() => {
    getStoreDetails(storeId).then((res) => setStore(res.data));
  }, [storeId]);
  if (!store) return <p className="p-6">Loading...</p>;
  return (
    <div className="p-6 border-2 border-dashed border-green-600 rounded-xl bg-white">
      <h2 className="text-xl font-semibold">{store.store_name}</h2>
      <p className="italic text-gray-700">{store.description}</p>
      <p className="mt-3 text-sm">Delivery radius: {store.delivery_radius_km} km</p>
    </div>
  );
}
