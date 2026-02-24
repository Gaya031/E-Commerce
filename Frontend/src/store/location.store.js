import { create } from "zustand";
import { getUserProfile, updateUserLocation } from "../api/location.api";

export const useLocationStore = create((set, get) => ({
    location: {
        lat: 28.6292,
        lng: 77.3725,
        label: "Sector C, Indrapuri"
    },
    address: null,
    city: null,
    state: null,
    pincode: null,
    
    setLocation: (location) => set({ location }),
    
    // Fetch location from backend user profile
    fetchLocation: async () => {
        try {
            const response = await getUserProfile();
            const user = response.data;
            if (user) {
                const location = {
                    lat: parseFloat(user.latitude) || 28.6292,
                    lng: parseFloat(user.longitude) || 77.3725,
                    label: user.address || "Current Location"
                };
                set({
                    location,
                    address: user.address,
                    city: user.city,
                    state: user.state,
                    pincode: user.pincode
                });
            }
        } catch (error) {
            console.error("Error fetching location:", error);
        }
    },
    
    // Update location in backend and local store
    saveLocation: async (locationData) => {
        try {
            const response = await updateUserLocation(locationData);
            const user = response.data;
            if (user) {
                const location = {
                    lat: parseFloat(user.latitude) || locationData.latitude || 28.6292,
                    lng: parseFloat(user.longitude) || locationData.longitude || 77.3725,
                    label: user.address || locationData.address || "Current Location"
                };
                set({
                    location,
                    address: user.address,
                    city: user.city,
                    state: user.state,
                    pincode: user.pincode
                });
            }
            return true;
        } catch (error) {
            console.error("Error saving location:", error);
            return false;
        }
    }
}));
