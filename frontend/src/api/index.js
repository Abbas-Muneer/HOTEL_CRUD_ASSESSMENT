import api from "./client";

export const loginRequest = async (username, password) => {
  const form = new URLSearchParams();
  form.append("grant_type", "password");
  form.append("username", username);
  form.append("password", password);
  const res = await api.post("/auth/login", form, {
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
  });
  return res.data;
};

export const fetchHotels = async () => {
  const res = await api.get("/hotels");
  return res.data;
};

export const createHotel = async (payload) => {
  const res = await api.post("/hotels", payload);
  return res.data;
};

export const updateHotel = async (id, payload) => {
  const res = await api.put(`/hotels/${id}`, payload);
  return res.data;
};

export const deleteHotel = async (id) => {
  await api.delete(`/hotels/${id}`);
};

export const fetchHotelDetail = async (id) => {
  const res = await api.get(`/hotels/${id}`);
  return res.data;
};

export const fetchRoomTypes = async (hotelId) => {
  const res = await api.get(`/hotels/${hotelId}/room-types`);
  return res.data;
};

export const createRoomType = async (hotelId, payload) => {
  const res = await api.post(`/hotels/${hotelId}/room-types`, payload);
  return res.data;
};

export const fetchRoomType = async (roomTypeId) => {
  const res = await api.get(`/room-types/${roomTypeId}`);
  return res.data;
};

export const updateRoomType = async (roomTypeId, payload) => {
  const res = await api.put(`/room-types/${roomTypeId}`, payload);
  return res.data;
};

export const deleteRoomType = async (roomTypeId) => {
  await api.delete(`/room-types/${roomTypeId}`);
};

export const fetchRateAdjustments = async (roomTypeId) => {
  const res = await api.get(`/room-types/${roomTypeId}/rate-adjustments`);
  return res.data;
};

export const createRateAdjustment = async (roomTypeId, payload) => {
  const res = await api.post(`/room-types/${roomTypeId}/rate-adjustments`, payload);
  return res.data;
};

export const fetchEffectiveRate = async (roomTypeId, date) => {
  const res = await api.get(`/room-types/${roomTypeId}/effective-rate`, {
    params: { date },
  });
  return res.data;
};
