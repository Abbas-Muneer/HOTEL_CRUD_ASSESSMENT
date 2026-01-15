import { useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import {
  fetchHotelDetail,
  createRoomType,
  updateRoomType,
  deleteRoomType,
} from "../api";
import Loading from "../components/Loading";
import ErrorMessage from "../components/ErrorMessage";

const HotelDetailPage = () => {
  const { hotelId } = useParams();
  const navigate = useNavigate();
  const [hotel, setHotel] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [form, setForm] = useState({ name: "", description: "", base_rate: 0 });
  const [editingId, setEditingId] = useState(null);

  const load = async () => {
    setLoading(true);
    setError("");
    try {
      const data = await fetchHotelDetail(hotelId);
      setHotel(data);
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to load hotel");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
  }, [hotelId]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editingId) {
        await updateRoomType(editingId, {
          name: form.name,
          description: form.description,
          base_rate: Number(form.base_rate),
        });
      } else {
        await createRoomType(hotelId, {
          name: form.name,
          description: form.description,
          base_rate: Number(form.base_rate),
        });
      }
      setForm({ name: "", description: "", base_rate: 0 });
      setEditingId(null);
      load();
    } catch (err) {
      setError(err.response?.data?.detail || "Save failed");
    }
  };

  const startEdit = (rt) => {
    setEditingId(rt.id);
    setForm({
      name: rt.name,
      description: rt.description || "",
      base_rate: rt.base_rate,
    });
  };

  const handleDelete = async (id) => {
    if (!confirm("Delete this room type?")) return;
    try {
      await deleteRoomType(id);
      load();
    } catch (err) {
      setError(err.response?.data?.detail || "Delete failed");
    }
  };

  if (loading) return <Loading />;
  if (!hotel) return <ErrorMessage message="Hotel not found" />;

  return (
    <div>
      <div className="breadcrumb">
        <Link to="/hotels">← Back to hotels</Link>
      </div>
      <h1>{hotel.name}</h1>
      <p className="muted">
        {hotel.city} {hotel.address && `• ${hotel.address}`} • Status: {hotel.status}
      </p>

      <section className="card inline-form">
        <h3>{editingId ? "Edit Room Type" : "Create Room Type"}</h3>
        <form onSubmit={handleSubmit} className="grid">
          <label>
            Name
            <input
              value={form.name}
              onChange={(e) => setForm({ ...form, name: e.target.value })}
              required
            />
          </label>
          <label>
            Base Rate
            <input
              type="number"
              step="0.01"
              min="0"
              value={form.base_rate}
              onChange={(e) => setForm({ ...form, base_rate: e.target.value })}
              required
            />
          </label>
          <label className="full-width">
            Description
            <textarea
              value={form.description}
              onChange={(e) => setForm({ ...form, description: e.target.value })}
            />
          </label>
          <div className="actions">
            <button type="submit">{editingId ? "Update" : "Create"}</button>
            {editingId && (
              <button
                type="button"
                className="secondary"
                onClick={() => {
                  setEditingId(null);
                  setForm({ name: "", description: "", base_rate: 0 });
                }}
              >
                Cancel
              </button>
            )}
          </div>
        </form>
      </section>

      <ErrorMessage message={error} />

      <section className="card">
        <div className="card-header">
          <h3>Room Types</h3>
          <button className="secondary" onClick={load}>
            Refresh
          </button>
        </div>
        <table>
          <thead>
            <tr>
              <th>Name</th>
              <th>Base Rate</th>
              <th>Current Adj</th>
              <th>Upcoming</th>
              <th>Effective Rate</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {hotel.room_types?.map((rt) => (
              <tr key={rt.id}>
                <td>{rt.name}</td>
                <td>${rt.base_rate}</td>
                <td>
                  {rt.current_adjustment_effective_date
                    ? `${rt.current_adjustment} since ${rt.current_adjustment_effective_date}`
                    : "No adjustment"}
                </td>
                <td>
                  {rt.next_adjustment_effective_date
                    ? `${rt.next_adjustment} on ${rt.next_adjustment_effective_date}`
                    : "None scheduled"}
                </td>
                <td>${rt.current_effective_rate}</td>
                <td>
                  <button className="secondary" onClick={() => startEdit(rt)}>
                    Edit
                  </button>
                  <button className="danger" onClick={() => handleDelete(rt.id)}>
                    Delete
                  </button>
                  <button onClick={() => navigate(`/room-types/${rt.id}/adjust-rate`)}>
                    Adjust Rate
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>
    </div>
  );
};

export default HotelDetailPage;
