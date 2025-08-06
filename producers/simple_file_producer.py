import json
import time
from event_generator import EcommerceEventGenerator
import os

class FileProducer:
    def __init__(self):
        self.event_generator = EcommerceEventGenerator()
        self.output_file = "../data/live_events.json"
    
    def start_streaming(self, events_per_second=3, duration_seconds=300):
        """Stream events to file"""
        print(f"Starting file streaming: {events_per_second} events/sec")
        
        events_sent = 0
        start_time = time.time()
        
        try:
            while (time.time() - start_time) < duration_seconds:
                event = self.event_generator.generate_random_event()
                
                # Append to file
                with open(self.output_file, "a") as f:
                    f.write(json.dumps(event) + "\n")
                
                events_sent += 1
                if events_sent % 10 == 0:
                    print(f"Sent {events_sent} events")
                
                time.sleep(1.0 / events_per_second)
                
        except KeyboardInterrupt:
            print("Stopping...")
        
        print(f"Total events sent: {events_sent}")

if __name__ == "__main__":
    producer = FileProducer()
    producer.start_streaming()
