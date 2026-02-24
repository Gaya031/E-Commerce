import CartHeader from "../../components/cart/CartHeader";
import FreeDeliveryProgress from "../../components/cart/FreeDeliveryProgress";
import CartList from "../../components/cart/CartList";
import OrderSummary from "../../components/cart/OrderSummary";
import SuggestedProducts from "../../components/cart/SuggestedProducts";

const CartPage = () => {
  return (
    <div className='max-w-7xl mx-auto px-6 py-8'>
        <CartHeader /> 
        <div className="grid grid-cols-12 gap-8 mt-6">
        <div className="col-span-8 space-y-6">
          <FreeDeliveryProgress />
          <CartList />
        </div>

        <div className="col-span-4">
          <OrderSummary />
        </div>
      </div>

      <SuggestedProducts />
    </div>
  )
}

export default CartPage