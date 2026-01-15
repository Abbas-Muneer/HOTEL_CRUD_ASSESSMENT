import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import {
  fetchHotels,
  createHotel,
  updateHotel,
  deleteHotel,
} from "../api";
import Loading from "../components/Loading";
import ErrorMessage from "../components/ErrorMessage";

const HotelsPage = () => {
  const [hotels, setHotels] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [form, setForm] = useState({ name: "", address: "", city: "" });
  const [editingId, setEditingId] = useState(null);

  const load = async () => {
    setLoading(true);
    setError("");
    try {
      const data = await fetchHotels();
      setHotels(data);
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to load hotels");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editingId) {
        await updateHotel(editingId, form);
      } else {
        await createHotel(form);
      }
      setForm({ name: "", address: "", city: "" });
      setEditingId(null);
      load();
    } catch (err) {
      setError(err.response?.data?.detail || "Save failed");
    }
  };

  const startEdit = (hotel) => {
    setEditingId(hotel.id);
    setForm({ name: hotel.name, address: hotel.address || "", city: hotel.city || "" });
  };

  const handleDelete = async (id) => {
    if (!confirm("Delete this hotel?")) return;
    try {
      await deleteHotel(id);
      load();
    } catch (err) {
      setError(err.response?.data?.detail || "Delete failed");
    }
  };

  if (loading) return <Loading />;

  return (
    <div>
      <h1>Hotels</h1>
      <ErrorMessage message={error} />

      <form className="card inline-form" onSubmit={handleSubmit}>
        <h3>{editingId ? "Edit Hotel" : "Create Hotel"}</h3>
        <div className="grid">
          <label>
            Name
            <input
              value={form.name}
              onChange={(e) => setForm({ ...form, name: e.target.value })}
              required
            />
          </label>
          <label>
            City
            <input
              value={form.city}
              onChange={(e) => setForm({ ...form, city: e.target.value })}
            />
          </label>
          <label>
            Address
            <input
              value={form.address}
              onChange={(e) => setForm({ ...form, address: e.target.value })}
            />
          </label>
        </div>
        <button type="submit">{editingId ? "Update" : "Create"}</button>
        {editingId && (
          <button
            type="button"
            className="secondary"
            onClick={() => {
              setEditingId(null);
              setForm({ name: "", address: "", city: "" });
            }}
          >
            Cancel
          </button>
        )}
      </form>

      <div className="card">
        <table>
          <thead>
            <tr>
              <th>Name</th>
              <th>City</th>
              <th>Status</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {hotels.map((hotel) => (
              <tr key={hotel.id}>
                <td>
                  <Link to={`/hotels/${hotel.id}`}>{hotel.name}</Link>
                </td>
                <td>{hotel.city || "-"}</td>
                <td>{hotel.status}</td>
                <td>
                  <button className="secondary" onClick={() => startEdit(hotel)}>
                    Edit
                  </button>
                  <button className="danger" onClick={() => handleDelete(hotel.id)}>
                    Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default HotelsPage;
