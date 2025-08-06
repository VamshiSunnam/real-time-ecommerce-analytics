import json
import random
from datetime import datetime
from faker import Faker
import uuid

fake = Faker()

class EcommerceEventGenerator:
    def __init__(self):
        self.products = self._load_products()
        self.users = self._generate_users(100)  # Reduced for faster startup
        self.sessions = {}
        
    def _load_products(self) -> list[dict]:
        """Load sample products"""
        try:
            with open('data/sample_products.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            # Fallback products
            return [
                {"id": "P001", "name": "Sample Product", "price": 29.99, "category": "General"}
            ]
    
    def _generate_users(self, count):
        """Generate fake users"""
        users = []
        for _ in range(count):
            users.append({
                "id": str(uuid.uuid4()),
                "name": fake.name(),
                "email": fake.email(),
                "location": fake.city(),
                "age_group": random.choice(["18-25", "26-35", "36-45", "46-55", "55+"])
            })
        return users
    
    def generate_page_view_event(self):
        """Generate a page view event"""
        user = random.choice(self.users)
        product = random.choice(self.products)
        
        session_id = self.sessions.get(user["id"], str(uuid.uuid4()))
        self.sessions[user["id"]] = session_id
        
        return {
            "event_type": "page_view",
            "timestamp": datetime.now().isoformat(),
            "user_id": user["id"],
            "session_id": session_id,
            "product_id": product["id"],
            "product_name": product["name"],
            "product_category": product["category"],
            "product_price": product["price"]
        }
    
    def generate_purchase_event(self):
        """Generate purchase event"""
        user = random.choice(self.users)
        product = random.choice(self.products)
        quantity = random.randint(1, 3)
        total_amount = product["price"] * quantity
        
        session_id = self.sessions.get(user["id"], str(uuid.uuid4()))
        
        return {
            "event_type": "purchase",
            "timestamp": datetime.now().isoformat(),
            "user_id": user["id"],
            "session_id": session_id,
            "order_id": str(uuid.uuid4()),
            "product_id": product["id"],
            "product_name": product["name"],
            "quantity": quantity,
            "total_amount": round(total_amount, 2),
            "payment_method": random.choice(["credit_card", "paypal", "apple_pay"])
        }
    
    def generate_random_event(self):
        """Generate a random event"""
        event_type = random.choices(
            ["page_view", "purchase"],
            weights=[80, 20]  # 80% page views, 20% purchases
        )[0]
        
        if event_type == "page_view":
            return self.generate_page_view_event()
        else:
            return self.generate_purchase_event()

# Test the generator
if __name__ == "__main__":
    print("Testing Event Generator...")
    generator = EcommerceEventGenerator()
    
    # Generate 3 sample events
    for i in range(3):
        event = generator.generate_random_event()
        print(f"\nEvent {i+1}:")
        print(f"Type: {event['event_type']}")
        print(f"Product: {event['product_name']}")
        if event['event_type'] == 'purchase':
            print(f"Total: ${event['total_amount']}")
    
    print("\nEvent generator working successfully!")