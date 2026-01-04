import { Swiper, SwiperSlide } from "swiper/react";
import "swiper/css";
import StoreCard from "./StoreCard";

export default function NearbyStores() {
  return (
    <section className="max-w-7xl mx-auto px-4 mt-12">
      <h3 className="font-semibold mb-4">Stores Near You</h3>

      <Swiper slidesPerView={3} spaceBetween={16}>
        {[1, 2, 3].map(i => (
          <SwiperSlide key={i}>
            <StoreCard />
          </SwiperSlide>
        ))}
      </Swiper>
    </section>
  );
}
