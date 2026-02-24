import { useNavigate } from "react-router-dom";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { User, ShoppingBag, Wallet, LogOut, Package } from "lucide-react";
import { useAuthStore } from "../../store/auth.store";

export default function ProfileDropdown() {
  const user = useAuthStore((s) => s.user);
  const clearAuth = useAuthStore((s) => s.clearAuth);
  const navigate = useNavigate();

  const handleLogout = () => {
    clearAuth();
    navigate("/login");
  };

  const getDashboardPath = () => {
    switch (user?.role) {
      case "seller":
        return "/seller";
      case "admin":
        return "/admin";
      case "delivery":
        return "/delivery";
      default:
        return "/buyer";
    }
  };

  return (
    <DropdownMenu>
      <DropdownMenuTrigger className="flex items-center gap-2 px-2 py-1 rounded-lg hover:bg-gray-100">
        <div className="w-8 h-8 bg-green-600 rounded-full flex items-center justify-center text-white font-semibold">
          {user?.name?.charAt(0).toUpperCase() || "U"}
        </div>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end" className="w-56">
        <DropdownMenuLabel>
          <div className="flex flex-col">
            <span className="font-medium">{user?.name || "User"}</span>
            <span className="text-xs text-gray-500">{user?.email}</span>
            <span className="text-xs text-green-600 capitalize">{user?.role}</span>
          </div>
        </DropdownMenuLabel>
        <DropdownMenuSeparator />
        
        <DropdownMenuItem onClick={() => navigate(getDashboardPath())}>
          <Package className="mr-2 h-4 w-4" />
          Dashboard
        </DropdownMenuItem>
        
        <DropdownMenuItem onClick={() => navigate("/buyer/orders")}>
          <ShoppingBag className="mr-2 h-4 w-4" />
          My Orders
        </DropdownMenuItem>
        
        <DropdownMenuItem onClick={() => navigate("/buyer/wallet")}>
          <Wallet className="mr-2 h-4 w-4" />
          Wallet
          {user?.wallet_balance !== undefined && (
            <span className="ml-auto font-medium">₹{user.wallet_balance}</span>
          )}
        </DropdownMenuItem>
        
        <DropdownMenuSeparator />
        
        <DropdownMenuItem onClick={handleLogout} className="text-red-600">
          <LogOut className="mr-2 h-4 w-4" />
          Logout
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  );
}
