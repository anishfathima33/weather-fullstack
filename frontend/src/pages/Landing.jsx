// src/pages/Landing.jsx

import { Link } from "react-router-dom";
import "../styles/landing.css";

export default function Landing() {
  return (
    <div className="landing-bg">

      {/* FLOATING WEATHER ICONS */}
      <div className="floating-icons">
        <span>☀️</span>
        <span>☁️</span>
        <span>🌧️</span>
        <span>⛅</span>
        <span>🌩️</span>
      </div>

      <div className="landing-content">

        <h1 className="landing-title">
          WeatherPro
        </h1>

        <p className="landing-subtitle">
          Get real-time weather updates anywhere
        </p>

        <Link to="/login">
          <button className="btn-primary">
            Get Started
          </button>
        </Link>

      </div>

    </div>
  );
}