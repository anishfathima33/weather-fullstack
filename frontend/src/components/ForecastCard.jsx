import "../styles/forecastcard.css"

export default function ForecastCard({day}){

  return(

    <div className="forecast-card">

      <h3>{day.date}</h3>

      <img
        src={`https://openweathermap.org/img/wn/${day.icon}@2x.png`}
        alt="weather"
      />

      <p>{day.temp}°C</p>

      <span>{day.description}</span>

    </div>

  )

}