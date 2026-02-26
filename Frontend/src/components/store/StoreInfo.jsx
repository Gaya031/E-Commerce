import React from 'react'
import { useOutletContext } from 'react-router-dom'

const StoreInfo = () => {
    const {store} = useOutletContext();
  return (
    <div className="mt-4 text-sm text-gray-600">
        <p><b>Address:</b> {store.address || "Not provided"}</p>
        <p className='mt-1'>
            <b>City:</b> {store.city || "Not provided"}
        </p>
        <p className='mt-1'>
            <b>Rating:</b> {store.average_rating || 0} / 5
        </p>
    </div>
  );
}

export default StoreInfo
