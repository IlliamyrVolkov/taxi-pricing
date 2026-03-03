import pytest
from app.domain.calculator import calculate_ride_price

def test_calculate_short_ride():
    price = calculate_ride_price(5.0)
    assert price == 100.0

def test_calculate_zero_distance():
    price = calculate_ride_price(0.0)
    assert price == 40.0

def test_negative_distance():
    with pytest.raises(ValueError):
        calculate_ride_price(-1.0)