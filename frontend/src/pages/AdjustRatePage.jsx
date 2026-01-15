import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import {
  createRateAdjustment,
  fetchRateAdjustments,
  fetchRoomType,
  fetchEffectiveRate,
} from "../api";
import Loading from "../components/Loading";
import ErrorMessage from "../components/ErrorMessage";

const AdjustRatePage = () => {
  const { roomTypeId } = useParams();
  const [roomType, setRoomType] = useState(null);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [form, setForm] = useState({
    effective_date: "",
    adjustment_amount: 0,
    reason: "",
  });
  const [effectiveToday, setEffectiveToday] = useState(null);
  const [nextChange, setNextChange] = useState(null);

  const load = async () => {
    setLoading(true);
    setError("");
    try {
      const [rt, adjustments, effective] = await Promise.all([
        fetchRoomType(roomTypeId),
        fetchRateAdjustments(roomTypeId),
        fetchEffectiveRate(roomTypeId, new Date().toISOString().slice(0, 10)),
      ]);
      setRoomType(rt);
      setHistory(adjustments);
      setEffectiveToday(effective);
      const upcoming = adjustments
        .filter((a) => new Date(a.effective_date) > new Date())
        .sort(
          (a, b) => new Date(a.effective_date).getTime() - new Date(b.effective_date).getTime()
        )[0];
      if (upcoming) {
        setNextChange(upcoming);
      } else {
        setNextChange(null);
      }
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to load data");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
  }, [roomTypeId]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    try {
      await createRateAdjustment(roomTypeId, {
        ...form,
        adjustment_amount: Number(form.adjustment_amount),
      });
      setForm({ effective_date: "", adjustment_amount: 0, reason: "" });
      load();
    } catch (err) {
      setError(err.response?.data?.detail || "Save failed");
    }
  };

  if (loading) return <Loading />;
  if (!roomType) return <ErrorMessage message="Room type not found" />;

  const formatCurrency = (value) => {
    const num = Number(value);
    return isNaN(num) ? value : `$${num}`;
  };

  return (
    <div>
      <div className="breadcrumb">
        <Link to={`/hotels/${roomType.hotel_id}`}>← Back to hotel</Link>
      </div>
      <h1>Adjust Rate: {roomType.name}</h1>
      <p className="muted">
        Base rate {formatCurrency(roomType.base_rate)} • Current effective{" "}
        {formatCurrency(effectiveToday?.effective_rate)}
        {nextChange && (
          <> • Next change: {formatCurrency(nextChange.adjustment_amount)} on {nextChange.effective_date}</>
        )}
      </p>
      <ErrorMessage message={error} />
      <section className="card inline-form">
        <h3>New Adjustment</h3>
        <form onSubmit={handleSubmit} className="grid">
          <label>
            Effective Date
            <input
              type="date"
              value={form.effective_date}
              onChange={(e) => setForm({ ...form, effective_date: e.target.value })}
              required
            />
          </label>
          <label>
            Adjustment Amount
            <input
              type="number"
              step="0.01"
              value={form.adjustment_amount}
              onChange={(e) => setForm({ ...form, adjustment_amount: e.target.value })}
              required
            />
          </label>
          <label className="full-width">
            Reason
            <textarea
              value={form.reason}
              onChange={(e) => setForm({ ...form, reason: e.target.value })}
              required
            />
          </label>
          <div className="actions">
            <button type="submit">Save Adjustment</button>
          </div>
        </form>
      </section>

      <section className="card">
        <div className="card-header">
          <h3>History</h3>
        </div>
        <table>
          <thead>
            <tr>
              <th>Effective Date</th>
              <th>Adjustment</th>
              <th>Reason</th>
              <th>Created</th>
            </tr>
          </thead>
          <tbody>
            {history.map((item) => (
              <tr key={item.id}>
                <td>{item.effective_date}</td>
                <td>{item.adjustment_amount}</td>
                <td>{item.reason}</td>
                <td>{new Date(item.created_at + "Z").toLocaleString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>
    </div>
  );
};

export default AdjustRatePage;
