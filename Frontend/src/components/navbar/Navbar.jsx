import LocationSelector from "./LocationsSelector";
import SearchBar from "./SearchBar";
import ProfileDropdown from "./ProfileDropdown";
import { Button } from "@/components/ui/button";
import { useAuthStore } from "../../store/auth.store";
import { ShoppingCart } from "lucide-react";

export default function Navbar() {
  const user = useAuthStore(s => s.user);

  return (
    <header className="sticky top-0 z-50 bg-white border-b">
      <div className="max-w-7xl mx-auto px-4 py-3 flex items-center gap-4">
        <h1 className="text-xl font-bold text-green-600">SahuMart</h1>

        <LocationSelector />
        <SearchBar />

        <div className="ml-auto flex items-center gap-3">
          <Button variant="outline">Become a Seller</Button>

          {!user ? (
            <>
              <Button variant="ghost">Login</Button>
              <Button>Register</Button>
            </>
          ) : (
            <>
              <ShoppingCart className="cursor-pointer" />
              <ProfileDropdown />
            </>
          )}
        </div>
      </div>
    </header>
  );
}
