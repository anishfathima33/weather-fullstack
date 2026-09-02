import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import API from "../services/api";
import "../styles/dashboard.css";

import sunnyVideo from "../assets/weather/sunny.mp4";
import cloudyVideo from "../assets/weather/cloudy.mp4";
import rainVideo from "../assets/weather/rain.mp4";
import snowVideo from "../assets/weather/snow.mp4";
import stormVideo from "../assets/weather/storm.mp4";
import defaultVideo from "../assets/weather/default.mp4";

export default function Dashboard() {

const navigate = useNavigate();

const [city,setCity] = useState("");
const [weather,setWeather] = useState(null);
const [forecast,setForecast] = useState([]);
const [bgVideo,setBgVideo] = useState(defaultVideo);
const [favorites,setFavorites] = useState([]);
const [username,setUsername] = useState("");
const [greeting,setGreeting] = useState("");
const [loading,setLoading] = useState(false);

/* LOAD USER + FAVORITES */

useEffect(()=>{

try{
const fav = JSON.parse(localStorage.getItem("favCities")) || [];
setFavorites(fav);
}catch{
setFavorites([]);
}

const name = localStorage.getItem("username") || "User";
setUsername(name);

const hour = new Date().getHours();

if(hour < 12) setGreeting("Good Morning");
else if(hour < 18) setGreeting("Good Afternoon");
else setGreeting("Good Evening");

},[]);

/* SAVE FAVORITE */

const saveFavorite = ()=>{

const trimmedCity = city.trim();

if(!trimmedCity) return;

if(favorites.includes(trimmedCity)) return;

const updated = [...favorites,trimmedCity];

setFavorites(updated);

localStorage.setItem("favCities",JSON.stringify(updated));

};

/* DELETE FAVORITE */

const deleteFavorite = (cityName)=>{

const updated = favorites.filter(
(c)=>c !== cityName
);

setFavorites(updated);

localStorage.setItem("favCities",JSON.stringify(updated));

};

/* BACKGROUND VIDEO */

const updateBackground = (description)=>{

const desc = description?.toLowerCase() || "";

if(desc.includes("thunder"))
setBgVideo(stormVideo);

else if(desc.includes("rain") || desc.includes("drizzle"))
setBgVideo(rainVideo);

else if(desc.includes("snow"))
setBgVideo(snowVideo);

else if(desc.includes("cloud"))
setBgVideo(cloudyVideo);

else if(desc.includes("clear"))
setBgVideo(sunnyVideo);

else
setBgVideo(defaultVideo);

};

/* SEARCH WEATHER */

const searchWeather = async(searchCity = city.trim())=>{

if(!searchCity){
alert("Enter city");
return;
}

try{

setLoading(true);

const resWeather = await API.get(`weather/current/?city=${searchCity}`);
const resForecast = await API.get(`weather/forecast/?city=${searchCity}`);

setWeather(resWeather.data);
setForecast(resForecast.data.forecast);

updateBackground(resWeather.data.description);

}

catch(error){

console.error(error);
alert("City not found");

}

finally{
setLoading(false);
}

};

/* LOCATION WEATHER */

const getLocationWeather = ()=>{

if(!navigator.geolocation){
alert("Geolocation not supported");
return;
}

navigator.geolocation.getCurrentPosition(

async(position)=>{

const lat = position.coords.latitude;
const lon = position.coords.longitude;

try{

setLoading(true);

const resWeather = await API.get(`weather/current/?lat=${lat}&lon=${lon}`);
const resForecast = await API.get(`weather/forecast/?lat=${lat}&lon=${lon}`);

setWeather(resWeather.data);
setForecast(resForecast.data.forecast);

updateBackground(resWeather.data.description);

}

catch{
alert("Location weather failed");
}

finally{
setLoading(false);
}

},

()=>{
alert("Location permission denied");
}

);

};

/* LOGOUT */

const handleLogout = ()=>{

localStorage.removeItem("access");
localStorage.removeItem("refresh");
localStorage.removeItem("username");

navigate("/login");

};

return(

<div className="dashboard-container">

{/* LOADING */}

{loading && (
<div className="loading">
Fetching Weather...
</div>
)}

{/* BACKGROUND VIDEO */}

<video
key={bgVideo}
autoPlay
muted
loop
playsInline
className="background-video"
>
<source src={bgVideo} type="video/mp4"/>
</video>

{/* HEADER */}

<header className="dashboard-header">

<h1>🌤 Live Weather</h1>

<div className="header-right">

<div className="profile">

<div className="avatar">
{username.charAt(0).toUpperCase()}
</div>

<h3 className="welcome-text">
{greeting} {username}
</h3>

</div>

<button
className="logout-btn"
onClick={handleLogout}
>
Logout
</button>

</div>

</header>

{/* SEARCH */}

<div className="search-center">

<input
placeholder="Enter city"
value={city}
onChange={(e)=>setCity(e.target.value)}
onKeyDown={(e)=>{
if(e.key==="Enter"){
searchWeather();
}
}}
/>

<button onClick={()=>searchWeather()}>
Search
</button>

<button onClick={getLocationWeather}>
📍 My Location
</button>

<button onClick={saveFavorite}>
⭐ Save
</button>

</div>

{/* FAVORITE CITIES */}

{favorites.length>0 &&(

<div className="favorites">

<h3>⭐ Favorite Cities</h3>

{favorites.map((c,i)=>(

<div key={i} className="fav-item">

<button
onClick={()=>searchWeather(c)}
>
{c}
</button>

<button
className="delete-btn"
onClick={()=>deleteFavorite(c)}
>
❌
</button>

</div>

))}

</div>

)}

{/* CURRENT WEATHER */}

{weather &&(

<div className="current-weather-card">

<div className="weather-main">

<img
src={`https://openweathermap.org/img/wn/${weather.icon}@2x.png`}
alt="icon"
/>

<div>

<h2>{Math.round(weather.temperature)}°C</h2>

<p>{weather.description}</p>

<h4>
{weather.city}, {weather.country}
</h4>

<p>
🌅 Sunrise:
{weather.sunrise
? new Date(weather.sunrise*1000).toLocaleTimeString()
:"N/A"}
</p>

<p>
🌇 Sunset:
{weather.sunset
? new Date(weather.sunset*1000).toLocaleTimeString()
:"N/A"}
</p>

</div>

</div>

<div className="weather-stats">

<p>💨 Wind: {weather.wind_speed} m/s</p>
<p>💧 Humidity: {weather.humidity}%</p>
<p>🌡 Feels like: {weather.feels_like}°C</p>
<p>🧭 Pressure: {weather.pressure} hPa</p>

</div>

{/* WEATHER TIP */}

<div className="weather-tip">

<h3>Weather Tip</h3>

<p>{weather.advice}</p>

</div>

</div>

)}

{/* HOURLY FORECAST */}

{forecast.length > 0 && (

<div className="hourly-section">

<h3>Hourly Forecast</h3>

<div className="hourly-slider">

{forecast.slice(0,8).map((hour,i)=>(

<div className="hour-card" key={i}>

<p>{hour.time || hour.date}</p>

<img src={hour.icon} alt="icon"/>

<p>{Math.round(hour.max_temp)}°C</p>

</div>

))}

</div>

</div>

)}

{/* 5 DAY FORECAST */}

{forecast.length>0 &&(

<div className="forecast-section">

<h3>5 Day Forecast</h3>

<div className="forecast-slider">

{forecast.map((day,i)=>(

<div
className="forecast-card"
key={i}
>

<h4>{day.date}</h4>

<img
src={day.icon}
alt="icon"
/>

<p>Min: {Math.round(day.min_temp)}°C</p>
<p>Max: {Math.round(day.max_temp)}°C</p>
<p>💨 {day.wind_speed} m/s</p>
<p>💧 {day.humidity}%</p>

</div>

))}

</div>

</div>

)}

</div>

);

}