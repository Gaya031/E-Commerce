import { create } from "zustand";

export const useLocationStore = create(set => ({
    location:{
        lat: 28.6292,
        lng: 77.3725,
        label: "Sector C, Indrapuri"
    },
    setLocation: location => set({location})
}));