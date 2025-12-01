import requests

API_KEY = "0ee2ee3f6ae1b6e977c8f71fe324bd11"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather(city):
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()

        weather = {
            "city": data["name"],
            "country": data["sys"]["country"],
            "temp": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "humidity": data["main"]["humidity"],
            "condition": data["weather"][0]["description"].title(),
        }

        return weather

    except requests.exceptions.HTTPError:
        return None

def display_weather(weather):
    print("\n------------------------------")
    print(f"🌤  Weather in {weather['city']}, {weather['country']}")
    print("------------------------------")
    print(f"Temperature : {weather['temp']}°C")
    print(f"Feels Like  : {weather['feels_like']}°C")
    print(f"Humidity    : {weather['humidity']}%")
    print(f"Condition   : {weather['condition']}")
    print("------------------------------\n")

def main():
    city = input("Enter city name: ")

    weather_data = get_weather(city)

    if weather_data:
        display_weather(weather_data)
    else:
        print("\n❌ City not found or API error. Try again.\n")

if __name__ == "__main__":
    main()