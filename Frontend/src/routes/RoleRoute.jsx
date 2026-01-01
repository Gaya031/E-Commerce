import { Navigate } from "react-router-dom";
import { useAuthStore } from "../store/auth.store";

export default function RoleRoute({ role, children }) {
  const user = useAuthStore(s => s.user);
  if (!user || user.role !== role) {
    return <Navigate to="/login" />;
  }
  return children;
}
