def weather_advice(temp, condition):
    if condition.lower() == "rain":
        return "Carry an umbrella ☔"
    if temp > 35:
        return "Drink more water 🥵"
    if temp < 15:
        return "Wear warm clothes 🧥"
    return "Good day to go outside ☀️"