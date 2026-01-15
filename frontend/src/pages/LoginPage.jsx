import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { loginRequest } from "../api";
import { useAuth } from "../auth/AuthContext";
import Loading from "../components/Loading";
import ErrorMessage from "../components/ErrorMessage";

const LoginPage = () => {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const data = await loginRequest(username, password);
      login(data.access_token);
      navigate("/hotels");
    } catch (err) {
      setError(err.response?.data?.detail || "Login failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-container">
      <h1>Hotel Admin Login</h1>
      <form className="card" onSubmit={handleSubmit}>
        <label>
          Username or Email
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </label>
        <label>
          Password
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </label>
        <ErrorMessage message={error} />
        <button type="submit" disabled={loading}>
          {loading ? "Signing in..." : "Login"}
        </button>
      </form>
    </div>
  );
};

export default LoginPage;
