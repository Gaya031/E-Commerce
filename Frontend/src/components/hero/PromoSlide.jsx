import { Button } from "@/components/ui/button";
import { useNavigate } from "react-router-dom";
import { resolveMediaUrl } from "@/utils/media";

export default function PromoSlide({ banner }) {
  const navigate = useNavigate();
  const title = banner?.title || "Fresh Groceries in 20 mins";
  const subtitle = banner?.subtitle || "Daily essentials from nearby stores";
  const imageUrl = resolveMediaUrl(banner?.image_url, "/hero.png");
  const primaryLabel = banner?.cta_primary_label || "Shop Now";
  const primaryLink = banner?.cta_primary_link || "/products";
  const secondaryLabel = banner?.cta_secondary_label || "View Offers";
  const secondaryLink = banner?.cta_secondary_link || "/products?offers=1";
  const showSecondary = Boolean(secondaryLabel);

  return (
    <div className="bg-white rounded-xl p-10 grid grid-cols-2 gap-6">
      <div>
        <span className="text-green-500 font-semibold">
          ⚡ Super Fast Delivery
        </span>
        <h2 className="text-4xl font-bold mt-4">
          {title}
        </h2>
        <p className="text-gray-600 mt-2">
          {subtitle}
        </p>

        <div className="mt-6 flex gap-4">
          <Button onClick={() => navigate(primaryLink)}>{primaryLabel}</Button>
          {showSecondary && (
            <Button variant="outline" onClick={() => navigate(secondaryLink)}>
              {secondaryLabel}
            </Button>
          )}
        </div>
      </div>

      <img
        src={imageUrl}
        className="rounded-xl"
        alt="Groceries"
      />
    </div>
  );
}
