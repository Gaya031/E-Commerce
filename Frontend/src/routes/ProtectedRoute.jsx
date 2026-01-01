import { useAuthStore } from "../store/auth.store";
import { Navigate } from "react-router-dom";

export default function ProtectedRoute({children}){
    const user = useAuthStore(s => s.user);
    console.log("user in Protected route: ", user);
    if(!user) return <Navigate to="/login" />;
    return children;
}

