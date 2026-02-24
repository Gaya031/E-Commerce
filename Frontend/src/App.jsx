import { BrowserRouter, Routes, Route } from "react-router-dom";
import { useAuth } from "./hooks/useAuth";

import ProtectedRoute from "./routes/ProtectedRoute";
import RoleRoute from "./routes/RoleRoute";

import Login from "./pages/auth/Login";
import Home from "./pages/buyer/Home";
import Register from "./pages/auth/Register";
import StoreLayout from "./pages/store/StoreLayout";
import Products from "./pages/store/Products";
import Review from "./pages/store/Review";
import Promotions from "./pages/store/Promotions";
import About from "./pages/store/About";

// Buyer Pages
import CartPage from "./pages/cart/CartPage";
import CheckoutPage from "./pages/checkout/CheckoutPage";
import OrderSuccess from "./pages/order/OrderSuccess";
import BuyerOrders from "./pages/buyer/Orders";
import BuyerWallet from "./pages/buyer/Wallet";
import BuyerCart from "./pages/buyer/Cart";

// Seller Pages
import SellerDashboard from "./pages/seller/Dashboard";
import SellerProducts from "./pages/seller/Products";
import SellerOrders from "./pages/seller/Orders";

// Admin Pages
import AdminDashboard from "./pages/admin/Dashboard";
import AdminSellers from "./pages/admin/Sellers";
import AdminOrders from "./pages/admin/Orders";
import AdminPayouts from "./pages/admin/Payouts";

// Delivery Pages
import DeliveryDeliveries from "./pages/delivery/Deliveries";

function App() {
  useAuth();

  return (
    <BrowserRouter>
      <Routes>
        {/* Public Routes */}
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/" element={<Home />} />

        {/* Store Routes */}
        <Route path="/store/:storeId" element={<StoreLayout />}>
          <Route index element={<Products />} />
          <Route path="reviews" element={<Review />} />
          <Route path="promotions" element={<Promotions />} />
          <Route path="about" element={<About />} />
        </Route>

        {/* Cart & Checkout - Protected */}
        <Route
          path="/cart"
          element={
            <ProtectedRoute>
              <CartPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/checkout"
          element={
            <ProtectedRoute>
              <CheckoutPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/order/success"
          element={
            <ProtectedRoute>
              <OrderSuccess />
            </ProtectedRoute>
          }
        />

        {/* Buyer Routes */}
        <Route
          path="/buyer"
          element={
            <ProtectedRoute>
              <RoleRoute role="buyer" />
            </ProtectedRoute>
          }
        />
        <Route
          path="/buyer/orders"
          element={
            <ProtectedRoute>
              <BuyerOrders />
            </ProtectedRoute>
          }
        />
        <Route
          path="/buyer/wallet"
          element={
            <ProtectedRoute>
              <BuyerWallet />
            </ProtectedRoute>
          }
        />

        {/* Seller Routes */}
        <Route
          path="/seller"
          element={
            <ProtectedRoute>
              <RoleRoute role="seller">
                <SellerDashboard />
              </RoleRoute>
            </ProtectedRoute>
          }
        />
        <Route
          path="/seller/products"
          element={
            <ProtectedRoute>
              <RoleRoute role="seller">
                <SellerProducts />
              </RoleRoute>
            </ProtectedRoute>
          }
        />
        <Route
          path="/seller/orders"
          element={
            <ProtectedRoute>
              <RoleRoute role="seller">
                <SellerOrders />
              </RoleRoute>
            </ProtectedRoute>
          }
        />

        {/* Admin Routes */}
        <Route
          path="/admin"
          element={
            <ProtectedRoute>
              <RoleRoute role="admin">
                <AdminDashboard />
              </RoleRoute>
            </ProtectedRoute>
          }
        />
        <Route
          path="/admin/sellers"
          element={
            <ProtectedRoute>
              <RoleRoute role="admin">
                <AdminSellers />
              </RoleRoute>
            </ProtectedRoute>
          }
        />
        <Route
          path="/admin/orders"
          element={
            <ProtectedRoute>
              <RoleRoute role="admin">
                <AdminOrders />
              </RoleRoute>
            </ProtectedRoute>
          }
        />
        <Route
          path="/admin/payouts"
          element={
            <ProtectedRoute>
              <RoleRoute role="admin">
                <AdminPayouts />
              </RoleRoute>
            </ProtectedRoute>
          }
        />

        {/* Delivery Partner Routes */}
        <Route
          path="/delivery"
          element={
            <ProtectedRoute>
              <RoleRoute role="delivery">
                <DeliveryDeliveries />
              </RoleRoute>
            </ProtectedRoute>
          }
        />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
