import React, { useEffect, useMemo } from 'react'
import { useLocationStore } from '../../store/location.store';
import { MapPin } from 'lucide-react';

const AddressSection = ({ onAddressSelect }) => {
  const { address, city, state, pincode, latitude, longitude, fetchLocation } = useLocationStore();
  
  // Single saved address from user profile
  const savedAddress = useMemo(() => (
    address
      ? {
          id: 1,
          label: "Home",
          name: "Customer",
          address: address,
          city: city,
          state: state,
          pincode: pincode,
          latitude: latitude,
          longitude: longitude,
          default: true,
        }
      : null
  ), [address, city, state, pincode, latitude, longitude]);

  useEffect(() => {
    fetchLocation();
  }, [fetchLocation]);

  useEffect(() => {
    if (savedAddress) {
      onAddressSelect?.(savedAddress);
    }
  }, [savedAddress, onAddressSelect]);

  return (
    <div className="bg-white p-6 rounded-xl">
      <div className="flex justify-between mb-4">
        <h2 className="font-semibold">1. Shipping Address</h2>
        <button 
          onClick={() => window.dispatchEvent(new CustomEvent('openLocationSelector'))}
          className="text-green-600 text-sm flex items-center gap-1"
        >
          <MapPin className="w-4 h-4" />
          Change Address
        </button>
      </div>

      {savedAddress ? (
        <div 
          onClick={() => onAddressSelect?.(savedAddress)}
          className={`border rounded-xl p-4 cursor-pointer ${
            savedAddress
              ? "border-green-500 bg-green-50"
              : "border-gray-200"
          }`}
        >
          <div className="flex justify-between">
            <p className="font-medium">{savedAddress.label}</p>
            {savedAddress.default && (
              <span className="text-xs bg-green-500 text-white px-2 py-1 rounded">
                Default
              </span>
            )}
          </div>
          <p className="text-sm mt-1">{savedAddress.name}</p>
          <p className="text-sm">{savedAddress.address}</p>
          <p className="text-sm">
            {savedAddress.city}
            {savedAddress.state && `, ${savedAddress.state}`}
            {savedAddress.pincode && ` - ${savedAddress.pincode}`}
          </p>
          {savedAddress.latitude && savedAddress.longitude && (
            <div className="mt-2 text-xs text-gray-500 flex items-center gap-1">
              <MapPin className="w-3 h-3" />
              📍 {savedAddress.latitude}, {savedAddress.longitude}
            </div>
          )}
        </div>
      ) : (
        <div className="text-center py-8 text-gray-500">
          <MapPin className="w-12 h-12 mx-auto mb-2 text-gray-300" />
          <p>No address saved</p>
          <p className="text-sm">Please add your delivery address</p>
          <button 
            onClick={() => window.dispatchEvent(new CustomEvent('openLocationSelector'))}
            className="mt-2 text-green-600 text-sm"
          >
            Add Address
          </button>
        </div>
      )}
    </div>
  );
}

export default AddressSection
