# weather_app/views.py
import requests
import json
from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

# -----------------------------
# Weather Advice Helper
# -----------------------------
def weather_advice(temp, condition):
    condition = condition.lower()
    if "rain" in condition:
        return "Carry an umbrella ☔"
    if temp > 35:
        return "Stay hydrated 🥵"
    if temp < 15:
        return "Wear warm clothes 🧥"
    return "Great day to go outside ☀️"

# -----------------------------
# User Registration Endpoint
# -----------------------------
@csrf_exempt
def register(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required"}, status=400)

    try:
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")
        email = data.get("email", "")

        if not username or not password:
            return JsonResponse({"error": "Username and password required"}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({"error": "Username already exists"}, status=400)

        User.objects.create_user(username=username, password=password, email=email)
        return JsonResponse({"message": "User registered successfully"}, status=201)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

# -----------------------------
# Current Weather Endpoint
# -----------------------------
def current_weather(request):
    city = request.GET.get("city")
    if not city:
        return JsonResponse({"error": "City is required"}, status=400)

    api_key = getattr(settings, "OPENWEATHER_API_KEY", None)
    if not api_key:
        return JsonResponse({"error": "API key not set"}, status=500)

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    try:
        response = requests.get(url, timeout=10)
        data = response.json()
    except requests.RequestException as e:
        return JsonResponse({"error": "Failed to fetch weather", "details": str(e)}, status=500)

    if response.status_code != 200:
        return JsonResponse(data, status=response.status_code)

    temp = data.get("main", {}).get("temp", 0)
    condition = data.get("weather", [{}])[0].get("main", "")

    weather_data = {
    "city": data.get("name", ""),
    "country": data.get("sys", {}).get("country", ""),
    "temperature": temp,
    "feels_like": data.get("main", {}).get("feels_like", 0),
    "pressure": data.get("main", {}).get("pressure", 0),
    "humidity": data.get("main", {}).get("humidity", 0),
    "description": data.get("weather", [{}])[0].get("description", ""),
    "icon": data["weather"][0]["icon"],
    "wind_speed": data.get("wind", {}).get("speed", 0),

    # ⭐ ADD THIS
    "sunrise": data.get("sys", {}).get("sunrise"),
    "sunset": data.get("sys", {}).get("sunset"),

    "advice": weather_advice(temp, condition),
}

    return JsonResponse(weather_data)

# -----------------------------
# 5-Day Forecast Endpoint
# -----------------------------
def forecast_weather(request):
    city = request.GET.get("city")
    if not city:
        return JsonResponse({"error": "City is required"}, status=400)

    api_key = getattr(settings, "OPENWEATHER_API_KEY", None)
    if not api_key:
        return JsonResponse({"error": "API key not set"}, status=500)

    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"

    try:
        response = requests.get(url, timeout=10)
        data = response.json()
    except requests.RequestException as e:
        return JsonResponse({"error": "Failed to fetch forecast", "details": str(e)}, status=500)

    if response.status_code != 200:
        return JsonResponse(data, status=response.status_code)

    # Aggregate one forecast per day (OpenWeather gives 3-hour intervals)
    daily_forecast = {}
    for item in data.get("list", []):
        date = item.get("dt_txt", "").split(" ")[0]
        if date and date not in daily_forecast:
            daily_forecast[date] = {
    "date": date,
    "min_temp": item.get("main", {}).get("temp_min", 0),
    "max_temp": item.get("main", {}).get("temp_max", 0),
    "description": item.get("weather", [{}])[0].get("description", ""),
    "icon": f"https://openweathermap.org/img/wn/{item.get('weather', [{}])[0].get('icon', '01d')}@2x.png",
    "wind_speed": item.get("wind", {}).get("speed", 0),
    "humidity": item.get("main", {}).get("humidity", 0),
}
    return JsonResponse({"forecast": list(daily_forecast.values())[:5]})