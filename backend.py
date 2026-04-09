import requests
from datetime import datetime


class WeatherBackend:
    GEO_URL = "https://geocoding-api.open-meteo.com/v1/search"
    WEATHER_URL = "https://api.open-meteo.com/v1/forecast"
    AIR_URL = "https://air-quality-api.open-meteo.com/v1/air-quality"

    WEATHER_CODES = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Cloudy",
        45: "Fog",
        48: "Depositing rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        56: "Freezing drizzle",
        57: "Heavy freezing drizzle",
        61: "Slight rain",
        63: "Rainy",
        65: "Heavy rain",
        66: "Freezing rain",
        67: "Heavy freezing rain",
        71: "Light snow",
        73: "Snowfall",
        75: "Heavy snow",
        77: "Snow grains",
        80: "Rain showers",
        81: "Heavy rain showers",
        82: "Violent rain showers",
        85: "Snow showers",
        86: "Heavy snow showers",
        95: "Thunderstorm",
        96: "Thunderstorm hail",
        99: "Severe thunderstorm hail",
    }

    def get_weather_emoji(self, code, is_day):
        if code in [61, 63, 65, 80, 81, 82]:
            return "🌧"
        if code in [71, 73, 75, 85, 86]:
            return "❄"
        if code in [95, 96, 99]:
            return "⛈"
        if code in [45, 48]:
            return "🌫"
        if code in [1, 2, 3]:
            return "⛅" if is_day else "☁"
        return "☀" if is_day else "🌙"

    def get_pollen_level(self, pollen_value):
        if pollen_value is None:
            return "N/A"
        if pollen_value < 20:
            return "Low"
        if pollen_value < 60:
            return "Moderate"
        if pollen_value < 120:
            return "High"
        return "Very High"

    def wind_direction_text(self, degrees):
        directions = [
            "N", "NNE", "NE", "ENE",
            "E", "ESE", "SE", "SSE",
            "S", "SSW", "SW", "WSW",
            "W", "WNW", "NW", "NNW"
        ]
        index = round(degrees / 22.5) % 16
        return directions[index]

    def format_time(self, iso_text):
        try:
            dt = datetime.fromisoformat(iso_text)
            return dt.strftime("%I:%M %p").lstrip("0").lower()
        except Exception:
            return iso_text

    def get_location(self, city_name):
        response = requests.get(
            self.GEO_URL,
            params={"name": city_name, "count": 1, "language": "en", "format": "json"},
            timeout=15
        )
        response.raise_for_status()
        data = response.json()

        if "results" not in data or not data["results"]:
            raise ValueError("City not found")

        place = data["results"][0]
        return {
            "name": place["name"],
            "state": place.get("admin1", ""),
            "country": place.get("country", ""),
            "latitude": place["latitude"],
            "longitude": place["longitude"],
            "timezone": place.get("timezone", "auto")
        }

    def get_weather_data(self, city_name):
        location = self.get_location(city_name)

        weather_response = requests.get(
            self.WEATHER_URL,
            params={
                "latitude": location["latitude"],
                "longitude": location["longitude"],
                "timezone": "auto",
                "current": ",".join([
                    "temperature_2m",
                    "apparent_temperature",
                    "relative_humidity_2m",
                    "surface_pressure",
                    "wind_speed_10m",
                    "wind_direction_10m",
                    "weather_code",
                    "is_day"
                ]),
                "hourly": "visibility",
                "daily": "sunrise,sunset"
            },
            timeout=15
        )
        weather_response.raise_for_status()
        weather_data = weather_response.json()

        air_response = requests.get(
            self.AIR_URL,
            params={
                "latitude": location["latitude"],
                "longitude": location["longitude"],
                "timezone": "auto",
                "current": "alder_pollen,birch_pollen,grass_pollen,mugwort_pollen,olive_pollen,ragweed_pollen,uv_index"
            },
            timeout=15
        )
        air_response.raise_for_status()
        air_data = air_response.json()

        current = weather_data["current"]
        daily = weather_data["daily"]
        hourly = weather_data["hourly"]

        current_time = current["time"]
        visibility_km = None

        if "time" in hourly and current_time in hourly["time"]:
            idx = hourly["time"].index(current_time)
            visibility_km = round(hourly["visibility"][idx] / 1000, 1)

        air_current = air_data.get("current", {})
        pollen_values = [
            air_current.get("alder_pollen"),
            air_current.get("birch_pollen"),
            air_current.get("grass_pollen"),
            air_current.get("mugwort_pollen"),
            air_current.get("olive_pollen"),
            air_current.get("ragweed_pollen"),
        ]
        valid_pollen = [p for p in pollen_values if p is not None]
        total_pollen = round(sum(valid_pollen), 1) if valid_pollen else None

        weather_code = current["weather_code"]
        is_day = bool(current["is_day"])

        display_location = location["name"]
        if location["state"]:
            display_location += f", {location['state']}"

        return {
            "location": display_location,
            "country": location["country"],
            "temperature": round(current["temperature_2m"]),
            "feels_like": round(current["apparent_temperature"]),
            "humidity": current["relative_humidity_2m"],
            "pressure": round(current["surface_pressure"]),
            "wind_speed": round(current["wind_speed_10m"], 1),
            "wind_direction": self.wind_direction_text(current["wind_direction_10m"]),
            "visibility": visibility_km if visibility_km is not None else "N/A",
            "condition": self.WEATHER_CODES.get(weather_code, "Unknown"),
            "emoji": self.get_weather_emoji(weather_code, is_day),
            "sunrise": self.format_time(daily["sunrise"][0]),
            "sunset": self.format_time(daily["sunset"][0]),
            "uv_index": air_current.get("uv_index", "N/A"),
            "pollen_value": total_pollen if total_pollen is not None else "N/A",
            "pollen_level": self.get_pollen_level(total_pollen),
        }