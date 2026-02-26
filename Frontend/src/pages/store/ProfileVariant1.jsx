import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { getStoreDetails } from "../../api/store.api";

export default function ProfileVariant1() {
  const { storeId } = useParams();
  const [store, setStore] = useState(null);
  useEffect(() => {
    getStoreDetails(storeId).then((res) => setStore(res.data));
  }, [storeId]);
  if (!store) return <p className="p-6">Loading...</p>;
  return (
    <div className="p-6 bg-white rounded-xl shadow">
      <h2 className="text-xl font-bold">{store.store_name}</h2>
      <p className="text-gray-600">{store.description}</p>
      <p className="mt-2 text-sm">City: {store.city}</p>
    </div>
  );
}
