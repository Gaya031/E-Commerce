import Navbar from "../../components/navbar/Navbar";
import HeroSection from "../../components/hero/HeroSection";
import CategorySection from "../../components/category/CategorySection";
import NearbyStores from "../../components/store/NearbyStores";
import FeaturedProducts from "../../components/product/FeaturedProducts";
import Footer from "../../components/footer/Footer";

export default function Home() {
  return (
    <div className="rc-shell">
      <Navbar />
      <HeroSection />
      <CategorySection />
      <NearbyStores />
      <FeaturedProducts />
      <Footer />
    </div>
  );
}
