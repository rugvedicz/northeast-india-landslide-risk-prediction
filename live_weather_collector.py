import requests
import json
import time
from datetime import datetime
import os


OUTPUT_FILE = "data/live_weather_stream.json"


locations = {
    "Itanagar": {
        "state": "Arunachal Pradesh",
        "latitude": 27.0844,
        "longitude": 93.6053
    },
    "Dispur": {
        "state": "Assam",
        "latitude": 26.1433,
        "longitude": 91.7898
    },
    "Imphal": {
        "state": "Manipur",
        "latitude": 24.8170,
        "longitude": 93.9368
    },
    "Shillong": {
        "state": "Meghalaya",
        "latitude": 25.5788,
        "longitude": 91.8933
    },
    "Aizawl": {
        "state": "Mizoram",
        "latitude": 23.7271,
        "longitude": 92.7176
    },
    "Kohima": {
        "state": "Nagaland",
        "latitude": 25.6751,
        "longitude": 94.1086
    },
    "Gangtok": {
        "state": "Sikkim",
        "latitude": 27.3389,
        "longitude": 88.6065
    },
    "Agartala": {
        "state": "Tripura",
        "latitude": 23.8315,
        "longitude": 91.2868
    }
}


# Make sure data folder exists
os.makedirs("data", exist_ok=True)


while True:

    for location_name, location_data in locations.items():

        params = {
            "latitude": location_data["latitude"],
            "longitude": location_data["longitude"],
            "current": "temperature_2m,relative_humidity_2m,precipitation",
            "timezone": "Asia/Kolkata"
        }

        try:

            response = requests.get(
                "https://api.open-meteo.com/v1/forecast",
                params=params,
                timeout=15
            )

            response.raise_for_status()

            weather = response.json()["current"]

            record = {
                "timestamp": datetime.now().isoformat(),
                "location": location_name,
                "state": location_data["state"],
                "latitude": location_data["latitude"],
                "longitude": location_data["longitude"],
                "rainfall_mm": weather["precipitation"],
                "temperature_c": weather["temperature_2m"],
                "humidity_percent": weather["relative_humidity_2m"],
                "month": datetime.now().month
            }

            with open(
                OUTPUT_FILE,
                "a",
                encoding="utf-8"
            ) as f:

                f.write(
                    json.dumps(record) + "\n"
                )

            print(
                f"✅ {location_name}, "
                f"{location_data['state']} | "
                f"Temp: {weather['temperature_2m']}°C | "
                f"Humidity: {weather['relative_humidity_2m']}% | "
                f"Rainfall: {weather['precipitation']} mm"
            )

        except Exception as e:

            print(
                f"❌ Error for {location_name}: {e}"
            )

    print("\n⏳ Waiting 10 minutes...\n")

    time.sleep(600)