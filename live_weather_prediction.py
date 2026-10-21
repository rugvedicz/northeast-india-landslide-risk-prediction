import requests
import joblib
import pandas as pd
from datetime import datetime

# --------------------------------------------------
# 1. Load trained model
# --------------------------------------------------

MODEL_PATH = r"models\random_forest_landslide.pkl"

model = joblib.load(MODEL_PATH)

# --------------------------------------------------
# 2. Northeast location
# Shillong, Meghalaya
# --------------------------------------------------

latitude = 25.5788
longitude = 91.8933

# --------------------------------------------------
# 3. Get live weather
# --------------------------------------------------

url = "https://api.open-meteo.com/v1/forecast"

params = {
    "latitude": latitude,
    "longitude": longitude,
    "current": "temperature_2m,relative_humidity_2m,precipitation",
    "timezone": "Asia/Kolkata"
}

response = requests.get(url, params=params, timeout=15)
response.raise_for_status()

weather = response.json()

current = weather["current"]

temperature = current["temperature_2m"]
humidity = current["relative_humidity_2m"]
rainfall = current["precipitation"]

now = datetime.now()
month = now.month

# --------------------------------------------------
# 4. Create model input
# --------------------------------------------------

input_data = pd.DataFrame([{
    "latitude": latitude,
    "longitude": longitude,
    "rainfall_mm": rainfall,
    "temperature_c": temperature,
    "humidity_percent": humidity,
    "month": month
}])

# Make absolutely sure feature order matches training
input_data = input_data[
    [
        "latitude",
        "longitude",
        "rainfall_mm",
        "temperature_c",
        "humidity_percent",
        "month"
    ]
]

# --------------------------------------------------
# 5. Prediction
# --------------------------------------------------

prediction = model.predict(input_data)[0]

probability = model.predict_proba(input_data)[0][1]

risk = "LANDSLIDE RISK" if prediction == 1 else "LOW RISK"

# --------------------------------------------------
# 6. Display result
# --------------------------------------------------

print("\n" + "=" * 50)
print("     LIVE LANDSLIDE RISK PREDICTION")
print("=" * 50)

print(f"Location      : Shillong, Meghalaya")
print(f"Latitude      : {latitude}")
print(f"Longitude     : {longitude}")
print(f"Temperature   : {temperature:.2f} °C")
print(f"Humidity      : {humidity:.2f} %")
print(f"Rainfall      : {rainfall:.2f} mm")
print(f"Month         : {month}")

print("-" * 50)

print(f"Prediction    : {risk}")
print(f"Probability   : {probability * 100:.2f}%")

print("=" * 50)