from decimal import Decimal


BASE_RATE = Decimal("40.0")
PER_KM_RATE = Decimal("12.0")

WEATHER_MULTIPLIER = Decimal("1.4")
ALARM_MULTIPLIER = Decimal("1.8")


def calculate_ride_price(distance_km: float, bad_weather: bool, alarm: bool) -> float:

    if distance_km < 0:
        raise ValueError("Distance cannot be negative")

    price = BASE_RATE + (Decimal(str(distance_km)) * PER_KM_RATE)

    if alarm:
        price *= ALARM_MULTIPLIER
    elif bad_weather:
        price *= WEATHER_MULTIPLIER

    return float(round(price, 0))
