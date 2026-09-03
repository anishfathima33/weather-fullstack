// src/services/accountsServices.js

const API_BASE_URL = "https://weather-fullstack-1.onrender.com/api";

/* ---------------- REGISTER USER ---------------- */

export const registerUser = async (formData) => {
  try {
    const response = await fetch(`${API_BASE_URL}/accounts/register/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        username: formData.username,
        email: formData.email,
        password: formData.password,
      }),
    });

    let data;
    try {
      data = await response.json();
    } catch {
      throw new Error("Server returned invalid response");
    }

    if (!response.ok) {
      throw new Error(data?.error || data?.detail || "Registration failed");
    }

    return data;

  } catch (error) {
    console.error("Register Error:", error.message);
    throw error;
  }
};


/* ---------------- LOGIN USER ---------------- */

export const loginUser = async (formData) => {
  try {
    const response = await fetch(`${API_BASE_URL}/token/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        username: formData.username,
        password: formData.password,
      }),
    });

    let data;
    try {
      data = await response.json();
    } catch {
      throw new Error("Server returned invalid response");
    }

    if (!response.ok) {
      throw new Error(data?.detail || "Invalid username or password");
    }

    // Save tokens safely
    if (data.access && data.refresh) {
      localStorage.setItem("access", data.access);
      localStorage.setItem("refresh", data.refresh);
    }

    return data;

  } catch (error) {
    console.error("Login Error:", error.message);
    throw error;
  }
};


/* ---------------- GET TOKEN ---------------- */

export const getToken = () => {
  return localStorage.getItem("access");
};


/* ---------------- LOGOUT USER ---------------- */

export const logoutUser = () => {
  localStorage.removeItem("access");
  localStorage.removeItem("refresh");
};