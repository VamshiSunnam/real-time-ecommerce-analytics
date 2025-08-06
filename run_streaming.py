#!/usr/bin/env python3

import subprocess
import time
import signal
import sys
import threading
from concurrent.futures import ThreadPoolExecutor

class StreamingOrchestrator:
    def __init__(self):
        self.processes = []
        self.running = True
    
    def signal_handler(self, signum, frame):
        """Handle Ctrl+C gracefully"""
        print("\n🛑 Shutting down streaming pipeline...")
        self.running = False
        for process in self.processes:
            process.terminate()
        sys.exit(0)
    
    def run_producer(self):
        """Run Kafka producer"""
        print("🚀 Starting Kafka Producer...")
        cmd = [sys.executable, "-c", "from producers.simple_kafka_producer import SimpleKafkaProducer; p = SimpleKafkaProducer(); p.start_streaming(events_per_second=3, duration_seconds=3600)"]
        process = subprocess.Popen(cmd, cwd=".")
        self.processes.append(process)
        return process
    
    def run_spark_consumer(self):
        """Run Spark consumer"""
        print("⚡ Starting Spark Consumer...")
        cmd = [sys.executable, "consumers/spark_streaming_consumer.py"]
        process = subprocess.Popen(cmd)
        self.processes.append(process)
        return process
    
    def run_dashboard(self):
        """Run Streamlit dashboard"""
        print("📊 Starting Dashboard...")
        cmd = [sys.executable, "-m", "streamlit", "run", "dashboard/realtime_dashboard.py", "--server.port", "8501"]
        process = subprocess.Popen(cmd)
        self.processes.append(process)
        return process
    
    def start_pipeline(self):
        """Start the complete pipeline"""
        # Set up signal handler
        signal.signal(signal.SIGINT, self.signal_handler)
        
        print("🔥 Starting Real-time E-commerce Analytics Pipeline!")
        print("=" * 60)
        
        try:
            # Start components with delays
            producer_process = self.run_producer()
            time.sleep(10)  # Let producer start first
            
            consumer_process = self.run_spark_consumer() 
            time.sleep(15)  # Let Spark initialize
            
            dashboard_process = self.run_dashboard()
            time.sleep(5)
            
            print("✅ All components started successfully!")
            print("📊 Dashboard: http://localhost:8501")
            print("⚡ Spark UI: http://localhost:4040")
            print("📈 Events are streaming...")
            print("Press Ctrl+C to stop all services")
            
            # Keep main thread alive
            while self.running:
                time.sleep(1)
                
        except Exception as e:
            print(f"❌ Error starting pipeline: {e}")
            self.signal_handler(None, None)

if __name__ == "__main__":
    orchestrator = StreamingOrchestrator()
    orchestrator.start_pipeline()