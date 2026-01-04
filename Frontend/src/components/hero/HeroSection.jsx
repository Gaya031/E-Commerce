import { Swiper, SwiperSlide } from "swiper/react";
import "swiper/css";
import PromoSlide from "./PromoSlide";

export default function HeroSection() {
  return (
    <div className="max-w-7xl mx-auto px-4 mt-6">
      <Swiper autoplay>
        <SwiperSlide>
          <PromoSlide />
        </SwiperSlide>
        <SwiperSlide>
          <PromoSlide />
        </SwiperSlide>
      </Swiper>
    </div>
  );
}
