import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Kafka Configuration
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
KAFKA_TOPICS = {
    "page_view": "ecommerce-page-views",
    "add_to_cart": "ecommerce-cart-events",
    "purchase": "ecommerce-purchases",
}

# PostgreSQL Configuration
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB = os.getenv("POSTGRES_DB", "ecommerce_analytics")
POSTGRES_USER = os.getenv("POSTGRES_USER", "admin")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "password123")

# Spark Configuration
SPARK_APP_NAME = "EcommerceAnalytics"
SPARK_MASTER = "local[*]"
SPARK_KAFKA_PACKAGE = "org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.2"

# Streamlit Dashboard Configuration
DASHBOARD_TITLE = "Real-time Ecommerce Analytics"
