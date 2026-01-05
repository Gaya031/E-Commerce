import { Badge } from '@/components/ui/badge';
import React from 'react'

const StoreCard = ({ store }) => {
  return (
    <div className='bg-white p-4 rounded-xl shadow-sm cursor-pointer'>
      <img
        src={store.image || "/store.jpg"}
        className='rounded-lg'
        alt={store.name}
      />
      <h4 className='font-semibold mt-2'>{store.name}</h4>
      <p className='text-sm text-gray-500'>
        {store.distance_km} km • {store.eta_mins} mins
      </p>
      {store.is_open && (
        <Badge className='mt-2'>Open Now</Badge>
      )}
    </div>
  )
}

export default StoreCard