import requests
from jarvis import config

def get_weather(lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=imperial&appid={config.WEATHER_API_KEY}"
    response = requests.get(url)
    weather_data = response.json()
    if weather_data["cod"] != "404":
        main_data = weather_data["main"]
        weather_description_data = weather_data["weather"][0]
        weather_description = weather_description_data["description"]
        current_temperature = main_data["temp"]
        current_pressure = main_data["pressure"]
        current_humidity = main_data["humidity"]
        wind_data = weather_data["wind"]
        wind_speed = wind_data["speed"]
        return f"""The weather is currently {weather_description} with a temperature of {current_temperature} degrees fahrenheit, atmospheric pressure of {current_pressure} a m use, humidity of {current_humidity} percent and wind speed reaching {wind_speed} miles per hour"""
    return "Sorry Sir, I couldn't find your location in my database."