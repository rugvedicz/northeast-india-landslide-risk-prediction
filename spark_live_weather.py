from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_timestamp, avg, max, min, count

# --------------------------------------------------
# 1. Start Spark
# --------------------------------------------------

spark = (
    SparkSession.builder
    .appName("LandslideLiveWeatherAnalytics")
    .master("local[*]")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

print("\n" + "=" * 60)
print("   LIVE WEATHER BIG DATA ANALYTICS")
print("=" * 60)

# --------------------------------------------------
# 2. Read live JSON stream file
# --------------------------------------------------

file_path = r"data\live_weather_stream.json"

df = spark.read.json(file_path)

print("\nTotal records:", df.count())

# --------------------------------------------------
# 3. Display raw data
# --------------------------------------------------

print("\nRAW LIVE WEATHER DATA")
df.show(10, truncate=False)

# --------------------------------------------------
# 4. Convert data types
# --------------------------------------------------

df = (
    df
    .withColumn("timestamp", to_timestamp(col("timestamp")))
    .withColumn("latitude", col("latitude").cast("double"))
    .withColumn("longitude", col("longitude").cast("double"))
    .withColumn("rainfall_mm", col("rainfall_mm").cast("double"))
    .withColumn("temperature_c", col("temperature_c").cast("double"))
    .withColumn("humidity_percent", col("humidity_percent").cast("double"))
    .withColumn("month", col("month").cast("int"))
)

# --------------------------------------------------
# 5. Clean data
# --------------------------------------------------

df_clean = df.dropna()

print("\nClean records:", df_clean.count())

# --------------------------------------------------
# 6. Weather analytics by location
# --------------------------------------------------

location_summary = (
    df_clean
    .groupBy("location", "state")
    .agg(
        count("*").alias("records"),
        avg("temperature_c").alias("avg_temperature"),
        avg("humidity_percent").alias("avg_humidity"),
        avg("rainfall_mm").alias("avg_rainfall"),
        max("rainfall_mm").alias("max_rainfall")
    )
    .orderBy(col("max_rainfall").desc())
)

print("\n" + "=" * 60)
print("   WEATHER ANALYTICS BY LOCATION")
print("=" * 60)

location_summary.show(truncate=False)

# --------------------------------------------------
# 7. Latest weather record for each location
# --------------------------------------------------

latest_weather = (
    df_clean
    .orderBy(col("timestamp").desc())
)

print("\n" + "=" * 60)
print("   LATEST WEATHER RECORDS")
print("=" * 60)

latest_weather.show(10, truncate=False)

# --------------------------------------------------
# 8. Overall statistics
# --------------------------------------------------

print("\n" + "=" * 60)
print("   OVERALL WEATHER STATISTICS")
print("=" * 60)

df_clean.select(
    avg("rainfall_mm").alias("average_rainfall"),
    max("rainfall_mm").alias("maximum_rainfall"),
    avg("temperature_c").alias("average_temperature"),
    avg("humidity_percent").alias("average_humidity")
).show()

print("\nSpark processing completed successfully.")

spark.stop()