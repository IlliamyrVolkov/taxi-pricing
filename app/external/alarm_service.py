import random
import asyncio


class AlertsService:
    async def get_alarm(self, location: str) -> bool:
        await asyncio.sleep(0.2)

        value = random.random() < 0.3

        status = "Air alarm" if value else "Clear"
        print(f"{location} is {status}")

        return value

alarms_client = AlertsService()
