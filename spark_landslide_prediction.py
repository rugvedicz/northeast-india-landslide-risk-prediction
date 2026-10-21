from pyspark.sql import SparkSession
from pyspark.sql.functions import col, row_number
from pyspark.sql.window import Window
import joblib
import pandas as pd

# ============================================================
# 1. START SPARK
# ============================================================

spark = (
    SparkSession.builder
    .appName("LiveLandslideRiskPrediction")
    .master("local[*]")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

print("\n" + "=" * 65)
print("        LIVE LANDSLIDE RISK PREDICTION")
print("=" * 65)

# ============================================================
# 2. READ LIVE WEATHER DATA
# ============================================================

file_path = r"data\live_weather_stream.json"

df = spark.read.json(file_path)

# ============================================================
# 3. CLEAN / CAST DATA
# ============================================================

df = (
    df
    .withColumn("timestamp", col("timestamp").cast("timestamp"))
    .withColumn("latitude", col("latitude").cast("double"))
    .withColumn("longitude", col("longitude").cast("double"))
    .withColumn("rainfall_mm", col("rainfall_mm").cast("double"))
    .withColumn("temperature_c", col("temperature_c").cast("double"))
    .withColumn("humidity_percent", col("humidity_percent").cast("double"))
    .withColumn("month", col("month").cast("int"))
    .dropna()
)

# ============================================================
# 4. GET LATEST RECORD FOR EACH LOCATION
# ============================================================

window = Window.partitionBy("location").orderBy(
    col("timestamp").desc()
)

latest_df = (
    df
    .withColumn("row_num", row_number().over(window))
    .filter(col("row_num") == 1)
    .drop("row_num")
)

print("\nLATEST WEATHER DATA")
latest_df.select(
    "location",
    "state",
    "rainfall_mm",
    "temperature_c",
    "humidity_percent",
    "month",
    "timestamp"
).show(truncate=False)

# ============================================================
# 5. CONVERT SPARK DATA → PANDAS
# ============================================================

prediction_data = latest_df.select(
    "latitude",
    "longitude",
    "rainfall_mm",
    "temperature_c",
    "humidity_percent",
    "month"
).toPandas()

# ============================================================
# 6. LOAD TRAINED RANDOM FOREST MODEL
# ============================================================

MODEL_PATH = r"models\random_forest_landslide.pkl"

model = joblib.load(MODEL_PATH)

print("\nModel loaded successfully.")

# ============================================================
# 7. PREDICT
# ============================================================

predictions = model.predict(prediction_data)

probabilities = model.predict_proba(prediction_data)[:, 1]

# ============================================================
# 8. ADD RESULTS
# ============================================================

result = latest_df.select(
    "location",
    "state",
    "rainfall_mm",
    "temperature_c",
    "humidity_percent"
).toPandas()

result["prediction"] = predictions
result["risk_probability"] = probabilities * 100

result["risk"] = result["prediction"].apply(
    lambda x: "LANDSLIDE RISK" if x == 1 else "LOW RISK"
)

# ============================================================
# 9. DISPLAY RESULTS
# ============================================================

print("\n" + "=" * 65)
print("              PREDICTION RESULTS")
print("=" * 65)

for _, row in result.iterrows():

    print(f"\nLocation       : {row['location']}, {row['state']}")
    print(f"Temperature    : {row['temperature_c']:.2f} °C")
    print(f"Humidity       : {row['humidity_percent']:.2f} %")
    print(f"Rainfall       : {row['rainfall_mm']:.2f} mm")
    print(f"Prediction     : {row['risk']}")
    print(f"Probability    : {row['risk_probability']:.2f}%")

print("\n" + "=" * 65)

spark.stop()