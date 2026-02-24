import React from 'react'
import { useOutletContext } from 'react-router-dom'

const StoreInfo = () => {
    const {store} = useOutletContext();
  return (
    <div className="mt-4 text-sm trxt-gray-600">
        <p><b>Address:</b> {store.address || "Sector 62, Noida"}</p>
        <p className='mt-1'>
            <b>Delivery:</b> {store.eta_min} mins
        </p>
        <p className='mt-1'>
            <b>Open:</b> {store.is_open ? "Yes" : "No"}
        </p>
    </div>
  );
}

export default StoreInfo