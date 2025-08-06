# Real-time E-commerce Analytics Platform

## Project Overview

This project implements a real-time e-commerce analytics platform designed to capture, process, and visualize e-commerce events as they happen. It leverages a modern data streaming architecture to provide immediate insights into user activity, product performance, and sales metrics. The platform is built using a combination of Kafka for event streaming, Spark for real-time processing, PostgreSQL for data storage, and Streamlit for interactive dashboards.

**Key Goals:**
*   **Real-time Data Ingestion:** Capture e-commerce events (page views, purchases) as they occur.
*   **Stream Processing:** Process incoming event streams to derive meaningful metrics and aggregations.
*   **Persistent Storage:** Store aggregated data in a relational database for historical analysis and dashboarding.
*   **Interactive Visualization:** Provide a user-friendly dashboard to visualize real-time and historical e-commerce trends.
*   **Scalability:** Design a system that can handle increasing volumes of event data.

## Architecture

The platform follows a microservices-oriented architecture with distinct components handling different stages of the data pipeline:

1.  **Event Generation (Producers):**
    *   `event_generator.py`: Simulates e-commerce events (page views, purchases) using `Faker` to generate realistic data.
    *   `kafka_producer.py`: Sends these generated events to Kafka topics.

2.  **Event Streaming (Apache Kafka & Zookeeper):**
    *   Kafka acts as a high-throughput, fault-tolerant distributed streaming platform.
    *   Zookeeper is used by Kafka for coordination and managing distributed systems.
    *   Events are categorized into different topics (e.g., `ecommerce-page-views`, `ecommerce-purchases`).

3.  **Stream Processing (Apache Spark Streaming):**
    *   `spark_streaming_job.py`: A Spark Structured Streaming application consumes events from Kafka topics.
    *   `aggregation_engine.py`: Processes micro-batches of events, performs real-time aggregations, and updates metrics in PostgreSQL. This includes:
        *   Updating `product_performance` for page views and purchases.
        *   Updating `user_activity` for user interactions.
        *   Updating `hourly_sales` for revenue and order metrics.

4.  **Data Storage (PostgreSQL):**
    *   A PostgreSQL database stores the aggregated and processed data.
    *   `sql/init_tables.sql`: Defines the schema for tables like `product_performance`, `user_activity`, `hourly_sales`, and `real_time_metrics`.

5.  **Dashboard (Streamlit):**
    *   `dashboard/Home.py`: The main entry point for the Streamlit application.
    *   `dashboard/pages/*.py`: Individual pages for visualizing different aspects of the e-commerce data, such as:
        *   Hourly Sales
        *   Product Performance
        *   Real-Time Metrics
        *   User Activity

## Technologies Used

*   **Apache Kafka:** Distributed streaming platform for event ingestion.
*   **Apache Zookeeper:** Coordination service for Kafka.
*   **Apache Spark:** Unified analytics engine for large-scale data processing, used here for stream processing.
*   **PostgreSQL:** Open-source relational database for storing aggregated data.
*   **Python:** Primary programming language for producers, consumers, and dashboard.
*   **Streamlit:** Python library for quickly building interactive web applications (dashboards).
*   **Docker & Docker Compose:** For containerizing and orchestrating the various services.
*   **`psycopg2-binary`:** PostgreSQL adapter for Python.
*   **`kafka-python`:** Python client for Kafka.
*   **`pyspark`:** Python API for Spark.
*   **`Faker`:** Python library for generating fake data.
*   **`python-dotenv`:** For managing environment variables.
*   **`Plotly` & `Altair`:** For data visualization within Streamlit.

## Setup and Installation

Follow these steps to set up and run the real-time e-commerce analytics platform on your local machine.

### Prerequisites

*   **Docker Desktop:** Ensure Docker Desktop is installed and running on your system. This includes Docker Engine and Docker Compose.
    *   [Download Docker Desktop](https://www.docker.com/products/docker-desktop/)
*   **Python 3.8+:** Make sure you have Python installed.
    *   [Download Python](https://www.python.org/downloads/)

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/real-time-ecommerce-analytics.git
cd real-time-ecommerce-analytics
```

### 2. Environment Variables

Create a `.env` file in the root directory of the project. This file will store sensitive information and configuration parameters. A sample `.env` file is provided below. You can adjust values as needed, but the defaults in `config.py` are set to work with the `docker-compose.yml` setup.

```dotenv
# Kafka Configuration
KAFKA_BOOTSTRAP_SERVERS=localhost:9092

# PostgreSQL Configuration
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=ecommerce_analytics
POSTGRES_USER=admin
POSTGRES_PASSWORD=password123
```

### 3. Docker Compose Setup

Start all the necessary services (Zookeeper, Kafka, PostgreSQL, Spark Master, Spark Worker) using Docker Compose. This will also initialize the PostgreSQL database with the required tables.

```bash
docker-compose up -d
```

This command will:
*   Pull the necessary Docker images.
*   Start Zookeeper and Kafka.
*   Start PostgreSQL and run the `init_tables.sql` script to create the database schema.
*   Start Spark Master and Spark Worker nodes.

Verify that all containers are running:
```bash
docker-compose ps
```

### 4. Install Python Dependencies

It's recommended to use a virtual environment.

```bash
python -m venv venv
# On Windows
.\venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
```

### 5. Run the Producers (Generate Events)

Open a new terminal and navigate to the project root. Activate your virtual environment.

This script will start generating simulated e-commerce events and sending them to Kafka topics.

```bash
python run_streaming.py
```
*(Note: `run_streaming.py` likely orchestrates the `kafka_producer.py` to start event generation.)*

### 6. Run the Spark Streaming Job (Process Events)

Open another new terminal and navigate to the project root. Activate your virtual environment.

This script will consume events from Kafka, process them using Spark, and store the aggregated results in PostgreSQL.

```bash
python consumers/spark_streaming_job.py
```

### 7. Run the Streamlit Dashboard (Visualize Data)

Open a third new terminal and navigate to the project root. Activate your virtual environment.

This will start the Streamlit web server and open the dashboard in your default web browser.

```bash
streamlit run dashboard/Home.py
```

You should now be able to see the real-time analytics dashboard updating with the incoming data.

## Project Structure

```
.
├── .env                      # Environment variables for configuration
├── .gitignore                # Git ignore file
├── config.py                 # Centralized configuration for the application
├── docker-compose.yml        # Docker Compose configuration for services
├── downloads_jars.py         # (Optional) Script to download necessary Spark JARs
├── README.md                 # This README file
├── requirements.txt          # Python dependencies
├── run_streaming.py          # Main script to start event generation
├── consumers/                # Spark streaming and data aggregation logic
│   ├── aggregation_engine.py # Processes Spark dataframes and writes to PostgreSQL
│   └── spark_streaming_job.py# Main Spark Structured Streaming application
├── dashboard/                # Streamlit dashboard application
│   ├── Home.py               # Main dashboard entry point
│   ├── auth.py               # (Optional) Authentication logic for dashboard
│   ├── dashboard/            # Sub-directory for dashboard specific files
│   │   ├── docker_dashboard.py
│   │   ├── file_dashboard.py
│   │   └── setup_spark.bat
│   └── pages/                # Individual dashboard pages
│       ├── Hourly_Sales.py
│       ├── Product_Performance.py
│       ├── Real_Time_Metrics.py
│       └── User_Activity.py
├── data/                     # Sample data files
│   └── sample_products.json  # Sample product data for event generation
├── docs/                     # Documentation files
│   └── architecture.md       # Detailed architecture documentation
├── producers/                # Event generation and Kafka publishing
│   ├── event_generator.py    # Generates simulated e-commerce events
│   ├── kafka_producer.py     # Publishes events to Kafka
│   └── simple_file_producer.py # (Optional) Producer for file-based events
└── sql/                      # SQL scripts for database initialization
    └── init_tables.sql       # SQL script to create PostgreSQL tables
```

## Dashboard Features

The Streamlit dashboard provides the following real-time and aggregated insights:

*   **Hourly Sales:** Visualizes total revenue, number of orders, and unique customers per hour.
*   **Product Performance:** Displays product views, sales, and conversion rates.
*   **Real-Time Metrics:** Shows immediate key performance indicators (KPIs).
*   **User Activity:** Tracks user sessions, total events, and spending.

## Future Enhancements

*   **More Event Types:** Introduce additional e-commerce event types (e.g., cart abandonment, search queries).
*   **Advanced Analytics:** Implement more sophisticated Spark analytics, such as sessionization, funnel analysis, or anomaly detection.
*   **Machine Learning Integration:** Integrate machine learning models for recommendations or fraud detection.
*   **User Authentication:** Enhance the Streamlit dashboard with robust user authentication and authorization.
*   **Alerting:** Set up alerts for critical business metrics (e.g., sudden drop in sales).
*   **Cloud Deployment:** Provide instructions and configurations for deploying the platform on cloud providers (AWS, GCP, Azure).
*   **Monitoring:** Integrate with monitoring tools like Prometheus and Grafana.#   r e a l - t i m e - e c o m m e r c e - a n a l y t i c s  
 