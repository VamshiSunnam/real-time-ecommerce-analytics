import json
import time
import logging
from kafka import KafkaProducer
from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import KafkaError
from producers.event_generator import EcommerceEventGenerator
import config

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class EcommerceKafkaProducer:
    def __init__(self):
        self.bootstrap_servers = config.KAFKA_BOOTSTRAP_SERVERS
        self.topics = config.KAFKA_TOPICS
        self.producer = self._create_producer()
        self.event_generator = EcommerceEventGenerator()
        
    def _create_producer(self):
        """Create Kafka producer with retry logic"""
        max_retries = 5
        retry_count = 0
        while retry_count < max_retries:
            try:
                producer = KafkaProducer(
                    bootstrap_servers=[self.bootstrap_servers],
                    value_serializer=lambda x: json.dumps(x).encode('utf-8'),
                    key_serializer=lambda x: x.encode('utf-8') if x else None,
                    acks='all',
                    retries=3,
                    batch_size=16384,
                    linger_ms=10,
                    compression_type='gzip'
                )
                logger.info(f"Successfully connected to Kafka at {self.bootstrap_servers}")
                return producer
            except Exception as e:
                retry_count += 1
                logger.error(f"Failed to connect to Kafka (attempt {retry_count}): {e}")
                if retry_count < max_retries:
                    time.sleep(5)
                else:
                    logger.error("Max retries reached. Could not connect to Kafka.")
                    return None
    
    def create_topics(self):
        """Create Kafka topics if they don't exist"""
        try:
            admin_client = KafkaAdminClient(
                bootstrap_servers=[self.bootstrap_servers],
                client_id='ecommerce_admin'
            )
            topic_list = [NewTopic(name=topic, num_partitions=3, replication_factor=1) for topic in self.topics.values()]
            admin_client.create_topics(new_topics=topic_list, validate_only=False)
            logger.info("Topics created successfully")
        except Exception as e:
            logger.warning(f"Topic creation failed (topics might already exist): {e}")
    
    def send_event(self, event):
        """Send event to appropriate Kafka topic"""
        try:
            event_type = event['event_type']
            topic = self.topics.get(event_type, list(self.topics.values())[0])
            key = event.get('user_id')
            future = self.producer.send(topic, key=key, value=event)
            future.get(timeout=10)
            return True
        except KafkaError as e:
            logger.error(f"Failed to send event: {e}")
            return False
    
    def start_streaming(self, events_per_second=10, duration_seconds=None):
        """Start streaming events to Kafka"""
        if not self.producer:
            return
        
        self.create_topics()
        logger.info(f"Starting event streaming at {events_per_second} events/second")
        events_sent = 0
        start_time = time.time()
        
        try:
            while not duration_seconds or (time.time() - start_time) < duration_seconds:
                event = self.event_generator.generate_random_event()
                if self.send_event(event):
                    events_sent += 1
                    if events_sent % 100 == 0:
                        logger.info(f"Sent {events_sent} events")
                time.sleep(1.0 / events_per_second)
        except KeyboardInterrupt:
            logger.info("Stopping event streaming...")
        finally:
            if self.producer:
                self.producer.flush()
                self.producer.close()
            logger.info(f"Total events sent: {events_sent}")

def main():
    producer = EcommerceKafkaProducer()
    producer.start_streaming(events_per_second=5, duration_seconds=600)

if __name__ == "__main__":
    main()
