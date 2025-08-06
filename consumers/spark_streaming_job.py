from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import (
    StructType, StructField, StringType, TimestampType, 
    DoubleType, IntegerType, ArrayType, MapType
)
from consumers.aggregation_engine import process_batch
import config

def create_spark_session() -> SparkSession:
    """Create and configure a Spark session."""
    return (
        SparkSession.builder
        .appName(config.SPARK_APP_NAME)
        .config("spark.jars.packages", config.SPARK_KAFKA_PACKAGE)
        .config("spark.sql.shuffle.partitions", "4")
        .getOrCreate()
    )

def main() -> None:
    """Main Spark streaming job."""
    spark = create_spark_session()
    spark.sparkContext.setLogLevel("ERROR")

    schema = StructType([
        StructField("event_type", StringType(), True),
        StructField("timestamp", TimestampType(), True),
        StructField("user_id", StringType(), True),
        StructField("session_id", StringType(), True),
        StructField("product_id", StringType(), True),
        StructField("product_name", StringType(), True),
        StructField("product_category", StringType(), True),
        StructField("product_price", DoubleType(), True),
        StructField("quantity", IntegerType(), True),
        StructField("total_value", DoubleType(), True),
        StructField("order_id", StringType(), True),
        StructField("items", ArrayType(MapType(StringType(), StringType())), True),
        StructField("total_amount", DoubleType(), True),
        StructField("payment_method", StringType(), True),
        StructField("shipping_address", MapType(StringType(), StringType()), True),
        StructField("user_agent", StringType(), True),
        StructField("ip_address", StringType(), True),
        StructField("referrer", StringType(), True),
    ])

    kafka_df = (
        spark.readStream.format("kafka")
        .option("kafka.bootstrap.servers", config.KAFKA_BOOTSTRAP_SERVERS)
        .option("subscribe", ",".join(config.KAFKA_TOPICS.values()))
        .option("startingOffsets", "latest")
        .load()
    )

    parsed_df = kafka_df.select(
        from_json(col("value").cast("string"), schema).alias("data")
    ).select("data.*")

    query = (
        parsed_df.writeStream.foreachBatch(process_batch)
        .outputMode("update")
        .trigger(processingTime="15 seconds")
        .start()
    )

    query.awaitTermination()

if __name__ == "__main__":
    main()
