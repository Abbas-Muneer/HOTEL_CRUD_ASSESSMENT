import { Link } from "react-router-dom";
import { useAuth } from "../auth/AuthContext";

const Layout = ({ children }) => {
  const { logout } = useAuth();
  return (
    <div className="app-shell">
      <header className="app-header">
        <div className="brand">
          <Link to="/hotels">Hotel Admin</Link>
        </div>
        <button className="secondary" onClick={logout}>
          Logout
        </button>
      </header>
      <main className="app-main">{children}</main>
    </div>
  );
};

export default Layout;
