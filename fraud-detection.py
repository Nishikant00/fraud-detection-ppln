from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, count, window
from pyspark.sql.types import StructType, StructField, StringType, DoubleType

# Set Spark logging level
import logging
logging.getLogger("org").setLevel(logging.ERROR)

spark = SparkSession.builder \
    .appName("EnhancedFraudDetection") \
    .getOrCreate()

schema = StructType([
    StructField("transaction_id", StringType(), True),
    StructField("account_id", StringType(), True),
    StructField("transaction_amount", DoubleType(), True),
    StructField("transaction_type", StringType(), True),
    StructField("timestamp", StringType(), True)
])

df = spark \
  .readStream \
  .format("kafka") \
  .option("kafka.bootstrap.servers", "localhost:9092") \
  .option("subscribe", "transactions") \
  .load()

transaction_data = df.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*")

# Define potential fraud indicators
high_amount_threshold = 10000
time_window_duration = "10 minutes"  # Time window for counting transactions

# Identify potential fraudulent transactions
suspicious_transactions = transaction_data \
    .filter((transaction_data.transaction_amount > high_amount_threshold) | 
            (transaction_data.transaction_type.isin(["suspicious_type_1", "suspicious_type_2"]))) \
    .withWatermark("timestamp", time_window_duration) \
    .groupBy(window(col("timestamp"), time_window_duration), "account_id") \
    .agg(count("*").alias("transaction_count")) \
    .filter(col("transaction_count") > 5)  # More than 5 transactions in the window

# Join back to get original transaction details
potential_fraud = transaction_data.join(suspicious_transactions, 
                                         (transaction_data.account_id == suspicious_transactions.account_id) & 
                                         (transaction_data.timestamp >= suspicious_transactions.window.start) & 
                                         (transaction_data.timestamp <= suspicious_transactions.window.end), 
                                         "inner") \
                                    .select(transaction_data["*"])

def write_to_console(batch_df, batch_id):
    if not batch_df.isEmpty():
        batch_df.show(truncate=False)

query = potential_fraud \
    .writeStream \
    .outputMode("append") \
    .foreachBatch(write_to_console) \
    .option("numRows", 20) \
    .start()

query.awaitTermination()
