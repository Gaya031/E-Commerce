import { getNearbyStores } from '@/api/store.api';
import { useLocationStore } from '@/store/location.store'
import { useEffect, useState } from 'react'
import { Swiper, SwiperSlide } from 'swiper/react';
import StoreCard from './StoreCard';
import "swiper/css";

const NearbyStores = () => {
  const { lat, lng } = useLocationStore(s => s.location);
  const [stores, setStores] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getNearbyStores({ lat, lng })
      .then(res => setStores(res.data))
      .catch(err => console.error(err))
      .finally(() => setLoading(false))
  }, [lat, lng]);

  if (loading) return <p className='px-4'>Loading stores...</p>;
  if (!stores.length) return <p className='px-4'>No stores nearby</p>;
  return (
    <section className='max-w-7xl mx-auto px-4 mt-12'>
      <h3 className='font-semibold mb-4'>Stores Near You</h3>
      <Swiper slidesPerView={3} spaceBetween={16}>
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