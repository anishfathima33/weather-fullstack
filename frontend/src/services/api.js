import axios from "axios";

const api = axios.create({
  baseURL: (
    import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000/api/"
  ).replace(/\/+$/, "") + "/",
});

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("access");

    if (token) {
      config.headers = config.headers || {};
      config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
  },
  (error) => Promise.reject(error)
);

export default api;