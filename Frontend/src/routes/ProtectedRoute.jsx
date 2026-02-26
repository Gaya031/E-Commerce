import { useAuthStore } from "../store/auth.store";
import { Navigate } from "react-router-dom";

export default function ProtectedRoute({children}){
    const user = useAuthStore(s => s.user);
    const token = useAuthStore(s => s.accessToken);

    if(!user && !token) return <Navigate to="/login" replace />;
    if(!user && token){
        return (
          <div className="min-h-screen bg-gray-50 flex items-center justify-center text-sm text-gray-500">
            Restoring session...
          </div>
        );
    }
    return children;
}

