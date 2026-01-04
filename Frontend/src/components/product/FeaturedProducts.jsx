import { Swiper, SwiperSlide } from "swiper/react";
import ProductCard from "./ProductCard";
import "swiper/css";

export default function FeaturedProducts() {
  return (
    <section className="max-w-7xl mx-auto px-4 mt-12">
      <h3 className="font-semibold mb-4">
        Featured Products
      </h3>

      <Swiper slidesPerView={5} spaceBetween={16}>
        {[1, 2, 3, 4, 5].map(i => (
          <SwiperSlide key={i}>
            <ProductCard />
          </SwiperSlide>
        ))}
      </Swiper>
    </section>
  );
}
