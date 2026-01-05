import { useEffect, useState } from "react";
import { Swiper, SwiperSlide } from "swiper/react";
import "swiper/css";

import ProductCard from "./ProductCard";
import { getFeaturedProducts } from "../../api/product.api";

export default function FeaturedProducts() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getFeaturedProducts()
      .then(res => setProducts(res.data))
      .catch(err => console.error(err))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <p className="px-4">Loading products...</p>;
  if (!products.length) return <p className="px-4">No products found</p>;

  return (
    <section className="max-w-7xl mx-auto px-4 mt-12">
      <h3 className="font-semibold mb-4">
        Best Selling Products
      </h3>

      <Swiper slidesPerView={5} spaceBetween={16}>
        {products.map(product => (
          <SwiperSlide key={product.id}>
            <ProductCard product={product} />
          </SwiperSlide>
        ))}
      </Swiper>
    </section>
  );
}
