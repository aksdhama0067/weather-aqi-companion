import requests


def get_coordinates(city_name):
    #fetches lat. and longitudes for the entered city using Open-Meteo's geocoding API.
    geocode_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1&language=en&format=json"

    try:
        response = requests.get(geocode_url)
        response.raise_for_status()
        data = response.json()

        if "results" in data and len(data["results"]) > 0:
            result = data["results"][0]
            return {
                "lat": result["latitude"],
                "lon": result["longitude"],
                "name": result["name"],
                "country": result.get("country", "")
            }
        else:
            print(f" Could not find coordinates for '{city_name}'.")
            return None
    except requests.exceptions.RequestException as e:
        print(f" Error connecting to Geocoding API: {e}")
        return None


def get_weather_and_aqi(lat, lon):
    """Fetches current weather and air quality data for given coordinates."""
    # Open-Meteo Weather API
    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code"
    # Open-Meteo Air Quality API
    aqi_url = f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={lat}&longitude={lon}&current=us_aqi"

    try:
        weather_res = requests.get(weather_url).json()
        aqi_res = requests.get(aqi_url).json()

        current_weather = weather_res.get("current", {})
        current_aqi = aqi_res.get("current", {})

        return {
            "temp": current_weather.get("temperature_2m"),
            "feels_like": current_weather.get("apparent_temperature"),
            "humidity": current_weather.get("relative_humidity_2m"),
            "precipitation": current_weather.get("precipitation"),
            "aqi": current_aqi.get("us_aqi")
        }
    except Exception as e:
        print(f" Error fetching weather or air quality data: {e}")
        return None


def analyze_conditions(data):
    """Analyzes data and decides if it's a good time for an outdoor study break."""
    temp = data["temp"]
    aqi = data["aqi"]
    precip = data["precipitation"]

    reasons_to_stay_in = []

    # 1. Check Precipitation (Rain/Snow)
    if precip > 0:
        reasons_to_stay_in.append(f"It's currently raining/snowing ({precip} mm).")

    # 2. Check Temperature (Comfort Zone: 10°C to 32°C / 50°F to 90°F)
    if temp < 10:
        reasons_to_stay_in.append(f"It's too cold ({temp}°C).")
    elif temp > 32:
        reasons_to_stay_in.append(f"It's too hot ({temp}°C).")

    # 3. Check Air Quality (US AQI standard: Healthy is under 100)
    if aqi is not None:
        if aqi > 100:
            reasons_to_stay_in.append(f"Air quality is poor (AQI: {aqi}).")
    else:
        aqi = "Unknown"

    # status
    print("\n" + "=" * 40)
    print("  CURRENT OUTDOOR CONDITIONS")
    print("=" * 40)
    print(f"Temperature:  {temp}°C (Feels like: {data['feels_like']}°C)")
    print(f" Humidity:     {data['humidity']}%")
    print(f" Precipitation:{precip} mm")
    print(f"US AQI Index: {aqi}")
    print("=" * 40)

    #decision
    print("\n STUDY COMPANION RECOMMENDATION:")
    if reasons_to_stay_in:
        print(" [STAY INDOORS]")
        print("It's not the best time to step outside right now because:")
        for reason in reasons_to_stay_in:
            print(f"  - {reason}")
        print("\n Tip: Do a quick stretch, grab some water, or meditate inside instead!")
    else:
        print(" [GO OUTSIDE FOR A BREAK!]")
        print(
            "The conditions are perfect! Step away from your screens, get some fresh air, and clear your mind for 15 minutes.")
    print("=" * 40 + "\n")


#final part
if __name__ == "__main__":
    print(" Welcome to your Smart Study Companion!")
    city = input(" Enter your city name: ").strip()

    if city:
        print(f" Looking up conditions for {city}...")
        location = get_coordinates(city)

        if location:
            print(f" Found: {location['name']}, {location['country']}")
            conditions = get_weather_and_aqi(location['lat'], location['lon'])

            if conditions:
                analyze_conditions(conditions)
    else:
        print(" City name cannot be empty.")