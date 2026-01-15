import { Navigate, Route, Routes } from "react-router-dom";
import { useAuth } from "../auth/AuthContext";
import LoginPage from "../pages/LoginPage";
import HotelsPage from "../pages/HotelsPage";
import HotelDetailPage from "../pages/HotelDetailPage";
import AdjustRatePage from "../pages/AdjustRatePage";
import Layout from "../components/Layout";

const ProtectedRoute = ({ children }) => {
  const { token } = useAuth();
  if (!token) {
    return <Navigate to="/login" replace />;
  }
  return children;
};

const AppRoutes = () => {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route
        path="/hotels"
        element={
          <ProtectedRoute>
            <Layout>
              <HotelsPage />
            </Layout>
          </ProtectedRoute>
        }
      />
      <Route
        path="/hotels/:hotelId"
        element={
          <ProtectedRoute>
            <Layout>
              <HotelDetailPage />
            </Layout>
          </ProtectedRoute>
        }
      />
      <Route
        path="/room-types/:roomTypeId/adjust-rate"
        element={
          <ProtectedRoute>
            <Layout>
              <AdjustRatePage />
            </Layout>
          </ProtectedRoute>
        }
      />
      <Route path="*" element={<Navigate to="/hotels" replace />} />
    </Routes>
  );
};

export default AppRoutes;
