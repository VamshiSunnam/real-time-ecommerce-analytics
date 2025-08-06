-- Real-time aggregations table
CREATE TABLE IF NOT EXISTS real_time_metrics (
    id SERIAL PRIMARY KEY,
    metric_name VARCHAR(100) NOT NULL,
    metric_value DECIMAL(15,2) NOT NULL,
    time_window VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Product performance table
CREATE TABLE IF NOT EXISTS product_performance (
    id SERIAL PRIMARY KEY,
    product_id VARCHAR(50) NOT NULL,
    product_name VARCHAR(200) NOT NULL,
    total_sales DECIMAL(15,2) DEFAULT 0,
    total_views INTEGER DEFAULT 0,
    conversion_rate DECIMAL(5,4) DEFAULT 0,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User activity summary
CREATE TABLE IF NOT EXISTS user_activity (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL,
    session_id VARCHAR(100) NOT NULL,
    total_events INTEGER DEFAULT 0,
    total_spent DECIMAL(15,2) DEFAULT 0,
    last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Hourly sales summary
CREATE TABLE IF NOT EXISTS hourly_sales (
    id SERIAL PRIMARY KEY,
    hour_timestamp TIMESTAMP NOT NULL,
    total_revenue DECIMAL(15,2) DEFAULT 0,
    total_orders INTEGER DEFAULT 0,
    unique_customers INTEGER DEFAULT 0,
    avg_order_value DECIMAL(10,2) DEFAULT 0
);

-- Create indexes for better performance
CREATE INDEX idx_real_time_metrics_name ON real_time_metrics(metric_name);
CREATE INDEX idx_product_performance_id ON product_performance(product_id);
CREATE INDEX idx_user_activity_user ON user_activity(user_id);
CREATE INDEX idx_hourly_sales_timestamp ON hourly_sales(hour_timestamp);