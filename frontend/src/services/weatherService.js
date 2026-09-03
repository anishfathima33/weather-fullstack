import axios from "axios";

export const getCurrentWeather = async (city) => {

  const token = localStorage.getItem("access");

  return axios.get(
    https://weather-fullstack-1.onrender.com/api/weather/current/?city=${city}    {
      headers: {
        Authorization: `Bearer ${token}`
      }
    }
  );

};