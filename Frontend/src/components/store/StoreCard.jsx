import { Badge } from '@/components/ui/badge';
import React from 'react'
import { Link } from 'react-router-dom';
import { resolveMediaUrl } from '@/utils/media';

const StoreCard = ({ store }) => {
  const storeName = store?.store_name || store?.name || "Store";
  const storeImage = resolveMediaUrl(store?.logo_url || store?.image, "/store.jpg");
  const eta = store?.delivery_time_minutes ?? store?.eta_mins;
  const distance = store?.distance_km;

  return (
    <Link to={`/store/${store?.id}`} className='bg-white p-4 rounded-xl shadow-sm cursor-pointer block'>
      <img
        src={storeImage}
        className='rounded-lg h-28 w-full object-cover'
        alt={storeName}
      />
      <h4 className='font-semibold mt-2'>{storeName}</h4>
      <p className='text-sm text-gray-500'>
        {typeof distance === "number" ? `${distance} km` : "Nearby"} • {eta ? `${eta} mins` : "Fast delivery"}
      </p>
      {store?.average_rating > 0 && (
        <p className='text-xs text-gray-500 mt-1'>⭐ {Number(store.average_rating).toFixed(1)} ({store.total_reviews || 0})</p>
      )}
      {store?.is_open && (
        <Badge className='mt-2'>Open Now</Badge>
      )}
    </Link>
  )
}

export default StoreCard
