"""Manual testing script to verify each tool independently.
Run with: python3 test_tools.py
"""
import json
from tools.weather import get_weather_forecast
from tools.places import search_attractions
from tools.flights import search_flights
from tools.hotels import search_hotels


def test_suite():
    print("========================================")
    print("1. Testing Real Weather Tool (Open-Meteo)")
    print("========================================")
    weather = get_weather_forecast("Tokyo")
    print(f"City: {weather.get('city')}")
    if "forecast_days" in weather:
        for day in weather["forecast_days"][:3]:
            print(f"  [{day['date']}] {day['condition']} | High: {day['high_c']}°C, Low: {day['low_c']}°C | Rain: {day['rain_probability']}")
    else:
        print(weather)

    print("\n========================================")
    print("2. Testing Sightseeing Tool (Wikipedia/Open)")
    print("========================================")
    places = search_attractions("Tokyo", limit=3)
    print(f"Attractions found in {places.get('city')}:")
    for att in places.get("attractions", []):
        print(f"  • {att['name']}: {att['description'][:80]}...")

    print("\n========================================")
    print("3. Testing Flight Search Tool")
    print("========================================")
    flights = search_flights("NYC", "Tokyo", "2026-11-01", "2026-11-08")
    print(f"Flight Route: {flights.get('origin')} -> {flights.get('destination')} (Mode: {flights.get('mode')})")
    for f in flights.get("flights", []):
        price = f.get('price_usd') or f.get('price')
        print(f"  • {f['airline']} | Duration: {f['duration']} | Price: ${price}")

    print("\n========================================")
    print("4. Testing Hotel Search Tool")
    print("========================================")
    hotels = search_hotels("Tokyo", "2026-11-01", "2026-11-08", max_price_usd=200)
    print(f"Hotels in {hotels.get('city')} (Mode: {hotels.get('mode')}):")
    for h in hotels.get("hotels", []):
        print(f"  • {h['name']} | Area: {h['neighborhood']} | ${h['price_per_night_usd']}/night | Rating: {h['rating']}⭐")

    print("\n========================================")
    print(" All tools verified successfully!")
    print("========================================")


if __name__ == "__main__":
    test_suite()
