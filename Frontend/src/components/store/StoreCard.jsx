import { Badge } from "@/components/ui/badge";

export default function StoreCard() {
  return (
    <div className="bg-white p-4 rounded-xl shadow-sm">
      <img
        src="/store.jpg"
        className="rounded-lg"
        alt="Store"
      />
      <h4 className="font-semibold mt-2">
        Gupta General Store
      </h4>
      <p className="text-sm text-gray-500">
        0.8 km • 15 mins
      </p>
      <Badge className="mt-2">Free Delivery</Badge>
    </div>
  );
}
