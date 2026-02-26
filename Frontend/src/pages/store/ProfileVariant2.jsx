import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { getStoreDetails } from "../../api/store.api";

export default function ProfileVariant2() {
  const { storeId } = useParams();
  const [store, setStore] = useState(null);
  useEffect(() => {
    getStoreDetails(storeId).then((res) => setStore(res.data));
  }, [storeId]);
  if (!store) return <p className="p-6">Loading...</p>;
  return (
    <div className="p-6 rounded-xl bg-gradient-to-r from-green-50 to-emerald-100">
      <h2 className="text-2xl font-black">{store.store_name}</h2>
      <p className="mt-3">{store.description}</p>
      <div className="mt-4 text-sm">Rating: {store.average_rating} / Reviews: {store.total_reviews}</div>
    </div>
  );
}
