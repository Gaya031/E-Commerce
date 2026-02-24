import { useState, useEffect } from "react";
import Navbar from "../../components/navbar/Navbar";
import Footer from "../../components/footer/Footer";
import { useAuthStore } from "../../store/auth.store";
import { Truck, Package, MapPin, Phone, CheckCircle, Clock } from "lucide-react";

export default function DeliveryDeliveries() {
  const user = useAuthStore((s) => s.user);
  const [deliveries, setDeliveries] = useState([]);
  const [loading, setLoading] = useState(true);

  // Mock data for demonstration
  const mockDeliveries = [
    {
      id: 1,
      orderId: "12345",
      status: "pending",
      pickup: "Store A - Main Street",
      drop: "Customer - 123 Main St",
      customer: "John Doe",
      phone: "9876543210",
      amount: 250,
    },
    {
      id: 2,
      orderId: "12346",
      status: "in_transit",
      pickup: "Store B - Market Road",
      drop: "Customer - 456 Oak Ave",
      customer: "Jane Smith",
      phone: "9876543211",
      amount: 180,
    },
  ];

  useEffect(() => {
    // Simulate loading
    setTimeout(() => {
      setDeliveries(mockDeliveries);
      setLoading(false);
    }, 500);
  }, []);

  const getStatusColor = (status) => {
    switch (status) {
      case "delivered":
        return "bg-green-100 text-green-800";
      case "in_transit":
        return "bg-blue-100 text-blue-800";
      default:
        return "bg-yellow-100 text-yellow-800";
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      
      <div className="max-w-7xl mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-2xl font-bold">Delivery Dashboard</h1>
          <p className="text-gray-500">Welcome back, {user?.name}</p>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
          <div className="bg-white rounded-xl shadow p-6">
            <div className="flex items-center justify-between mb-4">
              <div className="w-12 h-12 bg-yellow-100 rounded-lg flex items-center justify-center">
                <Clock className="w-6 h-6 text-yellow-600" />
              </div>
            </div>
            <p className="text-2xl font-bold">
              {deliveries.filter(d => d.status === "pending").length}
            </p>
            <p className="text-gray-500 text-sm">Pending</p>
          </div>

          <div className="bg-white rounded-xl shadow p-6">
            <div className="flex items-center justify-between mb-4">
              <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                <Truck className="w-6 h-6 text-blue-600" />
              </div>
            </div>
            <p className="text-2xl font-bold">
              {deliveries.filter(d => d.status === "in_transit").length}
            </p>
            <p className="text-gray-500 text-sm">In Transit</p>
          </div>

          <div className="bg-white rounded-xl shadow p-6">
            <div className="flex items-center justify-between mb-4">
              <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
                <CheckCircle className="w-6 h-6 text-green-600" />
              </div>
            </div>
            <p className="text-2xl font-bold">
              {deliveries.filter(d => d.status === "delivered").length}
            </p>
            <p className="text-gray-500 text-sm">Delivered Today</p>
          </div>
        </div>

        {/* Deliveries List */}
        <h2 className="text-lg font-semibold mb-4">Today's Deliveries</h2>
        
        {loading ? (
          <div className="flex items-center justify-center h-48">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-600"></div>
          </div>
        ) : deliveries.length === 0 ? (
          <div className="bg-white rounded-lg shadow p-8 text-center">
            <Truck className="w-16 h-16 mx-auto text-gray-400 mb-4" />
            <h2 className="text-xl font-semibold mb-2">No deliveries assigned</h2>
            <p className="text-gray-500">Check back later for new deliveries.</p>
          </div>
        ) : (
          <div className="space-y-4">
            {deliveries.map((delivery) => (
              <div key={delivery.id} className="bg-white rounded-lg shadow p-4">
                <div className="flex items-center justify-between mb-4">
                  <div className="flex items-center gap-2">
                    <Package className="w-5 h-5 text-gray-500" />
                    <span className="font-semibold">Order #{delivery.orderId}</span>
                  </div>
                  <span className={`px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(delivery.status)}`}>
                    {delivery.status.replace("_", " ").toUpperCase()}
                  </span>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                  <div className="flex items-start gap-2">
                    <MapPin className="w-4 h-4 text-green-600 mt-1" />
                    <div>
                      <p className="text-xs text-gray-500">Pickup</p>
                      <p className="text-sm">{delivery.pickup}</p>
                    </div>
                  </div>
                  <div className="flex items-start gap-2">
                    <MapPin className="w-4 h-4 text-red-600 mt-1" />
                    <div>
                      <p className="text-xs text-gray-500">Drop</p>
                      <p className="text-sm">{delivery.drop}</p>
                    </div>
                  </div>
                </div>

                <div className="flex items-center justify-between border-t pt-4">
                  <div className="flex items-center gap-2">
                    <Phone className="w-4 h-4 text-gray-500" />
                    <span className="text-sm">{delivery.customer} - {delivery.phone}</span>
                  </div>
                  <div className="flex items-center gap-3">
                    <span className="font-semibold">₹{delivery.amount}</span>
                    <button className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700">
                      {delivery.status === "pending" ? "Accept" : "Update Status"}
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      <Footer />
    </div>
  );
}

