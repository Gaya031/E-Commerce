import { getNearbyStores } from '@/api/store.api';
import { useLocationStore } from '@/store/location.store'
import { useEffect, useState } from 'react'
import { Swiper, SwiperSlide } from 'swiper/react';
import StoreCard from './StoreCard';
import "swiper/css";

const NearbyStores = () => {
  const { lat, lng } = useLocationStore(s => s.location);
  const hasCoordinates = typeof lat === "number" && typeof lng === "number";
  const [stores, setStores] = useState([]);
  const [loading, setLoading] = useState(hasCoordinates);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!hasCoordinates) {
      return;
    }
    let alive = true;
    const loadStores = async () => {
      setLoading(true);
      try {
        const res = await getNearbyStores({ lat, lng });
        if (!alive) return;
        const rows = Array.isArray(res?.data) ? res.data : [];
        setStores(rows);
        setError("");
      } catch (err) {
        if (!alive) return;
        console.error(err);
        setError(err?.response?.data?.detail || "Failed to load nearby stores.");
      } finally {
        if (alive) {
          setLoading(false);
        }
      }
    };
    loadStores();
    return () => {
      alive = false;
    };
  }, [hasCoordinates, lat, lng]);

  if (!hasCoordinates) return <p className='px-4'>Enable location to view nearby stores.</p>;
  if (loading) return <p className='px-4'>Loading stores...</p>;
  if (error) return <p className='px-4 text-sm text-red-600'>{error}</p>;
  if (!stores.length) return <p className='px-4'>No stores nearby</p>;
  return (
    <section className='max-w-7xl mx-auto px-4 mt-12'>
      <h3 className='font-semibold mb-4'>Stores Near You</h3>
      <Swiper
        slidesPerView={1.2}
        spaceBetween={16}
        breakpoints={{
          640: { slidesPerView: 2.1 },
          1024: { slidesPerView: 3 },
        }}
      >
        {stores.map(store => (
          <SwiperSlide key={store.id}>
            <StoreCard store={store} />
          </SwiperSlide>
        ))}
      </Swiper>
    </section>
  )
}

export default NearbyStores;
