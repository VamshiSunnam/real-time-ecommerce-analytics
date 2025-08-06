# Real-Time E-commerce Analytics Platform

## ✨ Project Overview

This project is a **Real-Time E-commerce Analytics Platform** that captures, processes, and visualizes e-commerce events as they occur. It is designed with a modern, scalable data streaming architecture using **Apache Kafka**, **Apache Spark**, **PostgreSQL**, and **Streamlit** to provide instantaneous insights into user behavior, product performance, and sales trends.

### 🔗 Key Features

* **⏱ Real-Time Data Ingestion**: Seamlessly capture e-commerce events like page views and purchases.
* **🌀 Stream Processing**: Leverage Spark Streaming to perform real-time aggregations and metric calculations.
* **📂 Persistent Storage**: Store processed data in PostgreSQL for historical analysis.
* **📊 Interactive Dashboards**: Visualize real-time and historical analytics using Streamlit.
* **🚀 Scalable Architecture**: Built to handle high-throughput event streams and scalable processing workloads.

---

## ⚙️ Architecture Overview

The system is composed of modular services, each responsible for a different part of the data pipeline:

### 1. 🏦 Event Generation (Producers)

* `event_generator.py`: Uses `Faker` to simulate realistic e-commerce user activity.
* `kafka_producer.py`: Publishes the generated events to Kafka topics.

### 2. 📊 Event Streaming (Kafka & Zookeeper)

* **Kafka**: Handles real-time message streaming between producers and consumers.
* **Zookeeper**: Coordinates distributed Kafka brokers.
* Events are published to topics like `ecommerce-page-views` and `ecommerce-purchases`.

### 3. 🚀 Stream Processing (Apache Spark)

* `spark_streaming_job.py`: Consumes events from Kafka and processes them using Spark Structured Streaming.
* `aggregation_engine.py`: Updates PostgreSQL with aggregated metrics:

  * `product_performance`
  * `user_activity`
  * `hourly_sales`

### 4. 📂 Data Storage (PostgreSQL)

* PostgreSQL holds aggregated, structured data.
* Tables are initialized via `sql/init_tables.sql`.

### 5. 📈 Data Visualization (Streamlit)

* `dashboard/Home.py`: Main entry point for the interactive dashboard.
* Dashboard pages include:

  * Hourly Sales
  * Product Performance
  * Real-Time Metrics
  * User Activity

---

## 🛠️ Technologies Used

| Technology    | Role                               |
| ------------- | ---------------------------------- |
| Kafka         | Real-time event streaming          |
| Zookeeper     | Kafka coordination                 |
| Spark         | Stream processing engine           |
| PostgreSQL    | Relational storage                 |
| Python        | Scripting and business logic       |
| Streamlit     | Dashboard and visualization        |
| Faker         | Synthetic data generation          |
| Docker        | Containerization and orchestration |
| Plotly/Altair | Visual analytics in Streamlit      |
| `dotenv`      | Environment variable management    |

---

## 📅 Setup & Installation

### ✅ Prerequisites

* **Docker Desktop** (Engine + Compose): [Install Docker](https://www.docker.com/products/docker-desktop)
* **Python 3.8+**: [Install Python](https://www.python.org/downloads/)

### ① Clone the Repository

```bash
git clone (https://github.com/VamshiSunnam/real-time-ecommerce-analytics.git)
cd real-time-ecommerce-analytics
```

### ② Configure Environment Variables

Create a `.env` file in the project root:

```dotenv
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=ecommerce_analytics
POSTGRES_USER=admin
POSTGRES_PASSWORD=password123
```

### ③ Start Docker Services

Run the entire stack (Kafka, Zookeeper, PostgreSQL, Spark):

```bash
docker-compose up -d
```

Verify container status:

```bash
docker-compose ps
```

### ④ Install Python Dependencies

```bash
python -m venv venv
# Windows:
.\venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

### ⑤ Start Event Producers

Simulate event generation:

```bash
python run_streaming.py
```

### ⑥ Start Spark Stream Processor

```bash
python consumers/spark_streaming_job.py
```

### ⑦ Launch Streamlit Dashboard

```bash
streamlit run dashboard/Home.py
```

Navigate to: [http://localhost:8501](http://localhost:8501)

---

## 📄 Project Structure

```
real-time-ecommerce-analytics/
├── .env                     # Environment variables
├── config.py                # Global config
├── docker-compose.yml       # Docker services setup
├── requirements.txt         # Python dependencies
├── run_streaming.py         # Event orchestration
├── producers/               # Event generators
│   ├── event_generator.py
│   └── kafka_producer.py
├── consumers/               # Spark jobs
│   ├── spark_streaming_job.py
│   └── aggregation_engine.py
├── dashboard/               # Streamlit app
│   ├── Home.py
│   └── pages/
│       ├── Hourly_Sales.py
│       ├── Product_Performance.py
│       ├── Real_Time_Metrics.py
│       └── User_Activity.py
├── sql/
│   └── init_tables.sql      # PostgreSQL schema
└── data/
    └── sample_products.json
```

---

## 🔍 Dashboard Insights

* **Hourly Sales:** Revenue, order count, unique customers over time.
* **Product Performance:** Views, purchases, conversion rates.
* **Real-Time Metrics:** Key indicators such as revenue, AOV, session count.
* **User Activity:** Engagement trends and user interactions.

---

## 🧑‍💻 Future Enhancements

* [ ] Add support for more event types (e.g. cart updates, search)
* [ ] Implement user sessionization & funnel analysis
* [ ] Integrate machine learning models for prediction & recommendation
* [ ] Deploy with user authentication for dashboards
* [ ] Enable cloud deployment on AWS/GCP
* [ ] Setup monitoring with Prometheus + Grafana
* [ ] Implement alerting system for critical metrics

---

## 🚀 Contributing

We welcome contributions! Feel free to submit issues or pull requests.

---

## ✉️ Contact

For questions, feel free to reach out or open an issue.

---

## © License

MIT License. See `LICENSE` file for details.
