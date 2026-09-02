export default function WeatherCard({ data }) {

  return (

    <div className="weather-card">

      <h3>{data.city}</h3>

      <h1>{data.temperature}°C</h1>

      <p>{data.description}</p>

      <p>Humidity : {data.humidity}%</p>

      <p>Wind : {data.wind_speed} km/h</p>

    </div>
  );
}