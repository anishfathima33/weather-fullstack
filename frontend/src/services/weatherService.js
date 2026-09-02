import axios from "axios";

export const getCurrentWeather = async (city) => {

  const token = localStorage.getItem("access");

  return axios.get(
    `http://127.0.0.1:8000/api/weather/current/?city=${city}`,
    {
      headers: {
        Authorization: `Bearer ${token}`
      }
    }
  );

};