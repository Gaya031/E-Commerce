import CheckoutHeader from "../../components/checkout/CheckoutHeader";
import AddressSection from "../../components/checkout/AddressSection";
import DeliverySchedule from "../../components/checkout/DeliverySchedule";
import PaymentMethod from "../../components/checkout/PaymentMethod";
import OrderSummary from "../../components/checkout/OrderSummary";

export default function CheckoutPage() {
  return (
    <div className="max-w-7xl mx-auto px-6 py-8">
      <CheckoutHeader />

      <div className="grid grid-cols-12 gap-8 mt-6">
        <div className="col-span-8 space-y-6">
          <AddressSection />
          <DeliverySchedule />
          <PaymentMethod />
        </div>

        <div className="col-span-4">
          <OrderSummary />
        </div>
      </div>
    </div>
  );
}