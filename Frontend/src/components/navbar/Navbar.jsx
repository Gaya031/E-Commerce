import { Link, useNavigate } from "react-router-dom";
import LocationSelector from "./LocationsSelector";
import SearchBar from "./SearchBar";
import ProfileDropdown from "./ProfileDropdown";
import { Button } from "@/components/ui/button";
import { useAuthStore } from "../../store/auth.store";
import { ShoppingCart } from "lucide-react";

export default function Navbar() {
  const user = useAuthStore((s) => s.user);
  const cart = useAuthStore((s) => s.cart);
  const navigate = useNavigate();

  // Calculate cart count
  const cartCount = cart?.items?.length || 0;

  return (
    <header className="sticky top-0 z-50 bg-white border-b">
      <div className="max-w-7xl mx-auto px-4 py-3 flex items-center gap-4">
        <Link to="/" className="text-xl font-bold text-green-600 hover:text-green-700">
          SahuMart
        </Link>

        <LocationSelector />
        <SearchBar />

        <div className="ml-auto flex items-center gap-3">
          <Button 
            variant="outline" 
            onClick={() => navigate("/seller")}
          >
            Become a Seller
          </Button>

          {!user ? (
            <>
              <Button 
                variant="ghost" 
                onClick={() => navigate("/login")}
              >
                Login
              </Button>
              <Button onClick={() => navigate("/register")}>
                Register
              </Button>
            </>
          ) : (
            <>
              <Link to="/cart" className="relative p-2 hover:bg-gray-100 rounded-full">
                <ShoppingCart className="w-5 h-5" />
                {cartCount > 0 && (
                  <span className="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">
                    {cartCount}
                  </span>
                )}
              </Link>
              <ProfileDropdown />
            </>
          )}
        </div>
      </div>
    </header>
  );
}
