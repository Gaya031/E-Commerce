import { BrowserRouter, Routes, Route } from "react-router-dom";
import { useAuth } from "./hooks/useAuth";

import ProtectedRoute from "./routes/ProtectedRoute";
// import RoleRoute from "./routes/RoleRoute";

import Login from "./pages/auth/Login";
import Home from "./pages/buyer/Home";
import Register from "./pages/auth/Register";
// import Home from "./pages/buyer/Home";
// import AdminSellers from "./pages/admin/Sellers";

function App() {
  useAuth();

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />

        {/* <Route
          path="/"
          element={
            <ProtectedRoute>
              <Home />
            </ProtectedRoute>
          }
        /> */}

        {/* <Route
          path="/admin/sellers"
          element={
            <ProtectedRoute>
              <RoleRoute role="admin">
                <AdminSellers />
              </RoleRoute>
            </ProtectedRoute>
          }
        /> */}
      </Routes>
    </BrowserRouter>
  );
}

export default App;
