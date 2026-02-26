import { create } from "zustand";
import { getUserProfile, updateUserLocation } from "../api/location.api";
import { useAuthStore } from "./auth.store";

const DEFAULT_LOCATION = {
  lat: 28.6292,
  lng: 77.3725,
  label: "Sector C, Indrapuri",
};

const STORAGE_KEY = "rushcart_guest_location";
const LOCATION_CACHE_TTL_MS = 5 * 60 * 1000;

const loadGuestLocation = () => {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return null;
    const parsed = JSON.parse(raw);
    return parsed && typeof parsed === "object" ? parsed : null;
  } catch {
    return null;
  }
};

const persistGuestLocation = (payload) => {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(payload));
  } catch {
    // noop
  }
};

const toLocationState = (payload = {}) => {
  const latitude = payload.latitude !== undefined && payload.latitude !== null ? String(payload.latitude) : null;
  const longitude = payload.longitude !== undefined && payload.longitude !== null ? String(payload.longitude) : null;

  return {
    location: {
      lat: parseFloat(latitude) || DEFAULT_LOCATION.lat,
      lng: parseFloat(longitude) || DEFAULT_LOCATION.lng,
      label: payload.address || payload.city || "Current Location",
    },
    address: payload.address || null,
    city: payload.city || null,
    state: payload.state || null,
    pincode: payload.pincode || null,
    latitude,
    longitude,
  };
};

export const useLocationStore = create((set, get) => ({
    location: DEFAULT_LOCATION,
    address: null,
    city: null,
    state: null,
    pincode: null,
    latitude: null,
    longitude: null,
    locationLoadedFor: null,
    locationLastFetchedAt: 0,
    locationFetchInFlight: null,
    
    setLocation: (location) => set({ location }),
    
    // Fetch location for logged-in users from backend, fallback to guest local storage
    fetchLocation: async ({ force = false } = {}) => {
        const user = useAuthStore.getState().user;
        const now = Date.now();
        const { locationLoadedFor, locationLastFetchedAt, locationFetchInFlight } = get();

        if (!user) {
            const guest = loadGuestLocation();
            if (guest) {
                set({
                    ...toLocationState(guest),
                    locationLoadedFor: "guest",
                    locationLastFetchedAt: now,
                });
            }
            return;
        }

        const cacheKey = `user:${user.id}`;
        const cacheFresh =
          locationLoadedFor === cacheKey &&
          now - locationLastFetchedAt < LOCATION_CACHE_TTL_MS;

        if (!force && cacheFresh) {
          return;
        }

        if (!force && locationFetchInFlight) {
          return locationFetchInFlight;
        }

        const userHasLocation =
          !!user.address || !!user.city || !!user.state || !!user.pincode || !!user.latitude || !!user.longitude;

        if (!force && userHasLocation && locationLoadedFor !== cacheKey) {
          set({
            ...toLocationState(user),
            locationLoadedFor: cacheKey,
            locationLastFetchedAt: now,
          });
          return;
        }

        const request = getUserProfile()
          .then((response) => {
            const profile = response.data;
            if (!profile) return;
            set({
              ...toLocationState(profile),
              locationLoadedFor: cacheKey,
              locationLastFetchedAt: Date.now(),
            });
          })
          .catch((error) => {
            console.error("Error fetching location:", error);
          })
          .finally(() => {
            if (get().locationFetchInFlight === request) {
              set({ locationFetchInFlight: null });
            }
          });

        set({ locationFetchInFlight: request });
        return request;
    },
    
    // Update location for logged-in users in backend; guests in local storage
    saveLocation: async (locationData) => {
        const user = useAuthStore.getState().user;
        if (!user) {
            const payload = {
                ...locationData,
                latitude: locationData.latitude ? String(locationData.latitude) : null,
                longitude: locationData.longitude ? String(locationData.longitude) : null,
            };
            persistGuestLocation(payload);
            set({
                ...toLocationState(payload),
                locationLoadedFor: "guest",
                locationLastFetchedAt: Date.now(),
            });
            return true;
        }

        try {
            const response = await updateUserLocation(locationData);
            const profile = response.data;
            if (profile) {
                set({
                    ...toLocationState({
                      ...locationData,
                      ...profile,
                    }),
                    locationLoadedFor: `user:${user.id}`,
                    locationLastFetchedAt: Date.now(),
                });
            }
            return true;
        } catch (error) {
            console.error("Error saving location:", error);
            return false;
        }
    }
}));
