import httpx


class WeatherService:

    async def get_weather_coef(self, lat: float, lon: float) -> bool:
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": lat,
            "longitude": lon,
            "current_weather": "true",
            "timezone": "auto",
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=params)

                data = response.json()

                if "current_weather" in data:
                    code = data["current_weather"]["weathercode"]
                else:
                    return False

                return code >= 51

        except Exception as e:
            print(f"Weather error: {e}")
            return False


weather_client = WeatherService()
