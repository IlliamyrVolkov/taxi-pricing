import httpx
from typing import Tuple, Optional


class MapsService:
    def __init__(self):
        self.headers = {"User-Agent": "TaxiApp_Microservice_Tutorial/1.0"}

    async def _geocode(self, client: httpx.AsyncClient, address: str) -> Optional[Tuple[float, float]]:
        url = "https://nominatim.openstreetmap.org/search"
        params = {
            "q": address,
            "format": "json",
            "limit": 1
        }

        try:
            response = await client.get(url, params=params, headers=self.headers)
            data = response.json()

            if data and len(data) > 0:
                lat = float(data[0]["lat"])
                lon = float(data[0]["lon"])
                return lat, lon
            return None

        except Exception as e:
            print(f"Geocoding error for {address}: {e}")
            return None

    async def get_coords(self, address: str):
        async with httpx.AsyncClient() as client:
            return await self._geocode(client, address)

    async def get_distance(self, from_addr: str, to_addr: str) -> float:
        async with httpx.AsyncClient() as client:
            coord1 = await self._geocode(client, from_addr)
            coord2 = await self._geocode(client, to_addr)

            if not coord1 or not coord2:
                print("One of the addresses could not be found.")
                return 0.0

            """
            добавить проверку на правильность адерсов и вернуть соответственную ошибку
            """

            lat1, lon1 = coord1
            lat2, lon2 = coord2

            osrm_url = f"http://router.project-osrm.org/route/v1/driving/{lon1},{lat1};{lon2},{lat2}"

            try:
                response = await client.get(osrm_url, params={"overview": "false"})
                data = response.json()

                if data.get("code") == "Ok":
                    meters = data["routes"][0]["distance"]
                    km = meters / 1000
                    return round(km, 2)

            except Exception as e:
                print(f"Route build error: {e}")

            return 0.0


maps_client = MapsService()
