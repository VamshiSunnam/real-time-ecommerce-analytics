import psycopg2
from psycopg2 import pool
from psycopg2.extensions import cursor as Cursor
from pyspark.sql import DataFrame
from typing import Dict, Any
import config

# Database connection pool
db_pool = psycopg2.pool.SimpleConnectionPool(
    1, 10,
    host=config.POSTGRES_HOST,
    port=config.POSTGRES_PORT,
    dbname=config.POSTGRES_DB,
    user=config.POSTGRES_USER,
    password=config.POSTGRES_PASSWORD
)

def process_batch(df: DataFrame, epoch_id: int) -> None:
    """Process a micro-batch of events from Spark."""
    if df.count() == 0:
        return
    df.foreachPartition(_process_partition)

def _process_partition(partition: iter) -> None:
    """Process a partition of data."""
    conn = db_pool.getconn()
    try:
        with conn.cursor() as cursor:
            for row in partition:
                event = row.asDict()
                event_type = event.get('event_type')
                if event_type == 'page_view':
                    _update_product_performance(cursor, event)
                elif event_type == 'add_to_cart':
                    _update_user_activity(cursor, event)
                elif event_type == 'purchase':
                    _update_purchase_metrics(cursor, event)
            conn.commit()
    finally:
        db_pool.putconn(conn)

def _update_product_performance(cursor: Cursor, event: Dict[str, Any]) -> None:
    """Update product performance metrics for page views."""
    product_id = event.get('product_id')
    product_name = event.get('product_name')
    if not product_id or not product_name:
        return

    sql = """
    INSERT INTO product_performance (product_id, product_name, total_views, updated_at)
    VALUES (%s, %s, 1, NOW())
    ON CONFLICT (product_id)
    DO UPDATE SET
        total_views = product_performance.total_views + 1,
        updated_at = NOW();
    """
    cursor.execute(sql, (product_id, product_name))

def _update_user_activity(cursor: Cursor, event: Dict[str, Any]) -> None:
    """Update user activity for cart events."""
    user_id = event.get('user_id')
    session_id = event.get('session_id')
    if not user_id or not session_id:
        return

    sql = """
    INSERT INTO user_activity (user_id, session_id, total_events, last_activity)
    VALUES (%s, %s, 1, NOW())
    ON CONFLICT (user_id, session_id)
    DO UPDATE SET
        total_events = user_activity.total_events + 1,
        last_activity = NOW();
    """
    cursor.execute(sql, (user_id, session_id))

def _update_purchase_metrics(cursor: Cursor, event: Dict[str, Any]) -> None:
    """Update various metrics for purchase events."""
    user_id = event.get('user_id')
    total_amount = event.get('total_amount')
    items = event.get('items', [])

    if not user_id or not total_amount:
        return

    hour_timestamp = event['timestamp'].replace(minute=0, second=0, microsecond=0)
    sql_hourly = """
    INSERT INTO hourly_sales (hour_timestamp, total_revenue, total_orders, unique_customers)
    VALUES (%s, %s, 1, 1)
    ON CONFLICT (hour_timestamp)
    DO UPDATE SET
        total_revenue = hourly_sales.total_revenue + EXCLUDED.total_revenue,
        total_orders = hourly_sales.total_orders + 1;
    """
    cursor.execute(sql_hourly, (hour_timestamp, total_amount))

    for item in items:
        product_id = item.get('product_id')
        item_total = item.get('item_total')
        if not product_id or not item_total:
            continue

        sql_product = """
        INSERT INTO product_performance (product_id, product_name, total_sales, updated_at)
        VALUES (%s, %s, %s, NOW())
        ON CONFLICT (product_id)
        DO UPDATE SET
            total_sales = product_performance.total_sales + EXCLUDED.total_sales,
            updated_at = NOW();
        """
        cursor.execute(sql_product, (product_id, item.get('product_name'), item_total))
