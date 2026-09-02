// src/services/api.js
import axios from "axios";

// Create Axios instance
const API = axios.create({
  baseURL: "https://weather-fullstack-1.onrender.com/api/",
});

// Request interceptor to attach JWT token
API.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("access"); // get access token
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    // Handle request error
    return Promise.reject(error);
  }
);

export default API;