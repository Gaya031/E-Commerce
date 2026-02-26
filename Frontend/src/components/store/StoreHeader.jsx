import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"

const StoreHeader = ({ store }) => {
  return (
    <div className="bg-white border-b">
      {/* Banner */}
      <div className="relative h-56 bg-gray-200">
        <img src={store.cover_image || "/store-banner.jpg"}
          alt={store.store_name}
          className="w-full h-full object-cover" />
      </div>

      {/* Store info */}
      <div className="max-w-7xl mx-auto px-4 py-6 flex gap-6">
        {/* logo */}
        <div className="w-20 h-20 bg-white rounded-xl shadow flex items-center justify-center">
          <img src={store.logo || "/store-logo.png"}
            alt="logo"
            className="w-12 h-12"
          />
        </div>

        {/* Meta */}
        <div className="flex-1">
          <div className="flex items-center gap-3">
            <h1 className="text-2xl font-bold">{store.store_name}</h1>
            {store.approved && <Badge>Open Now</Badge>}
          </div>

          <p className="text-sm text-gray-600 mt-1">
            ⭐ {store.average_rating} ({store.total_reviews} reviews)
          </p>

          <p className="text-sm text-gray-500 mt-1">
            {store.description}
          </p>
        </div>

        {/* Actions */}
        <div className="flex gap-3">
          <Button variant="outline">♡ Follow</Button>
          <Button>Contact Seller</Button>
        </div>
      </div>
    </div>
  )
}

export default StoreHeader
