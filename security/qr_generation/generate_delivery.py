import json
import qrcode
import uuid
from datetime import datetime

DATABASE_FILE = "delivery_database.json"

# Load database
def load_database():
    try:
        with open(DATABASE_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

# Save database
def save_database(data):
    with open(DATABASE_FILE, "w") as f:
        json.dump(data, f, indent=4)

# Generate unique delivery ID
delivery_id = str(uuid.uuid4())[:8]

# Get user details
name = input("Enter customer name: ")
phone = input("Enter phone number: ")

# Create delivery data
delivery_data = {
    "delivery_id": delivery_id,
    "name": name,
    "phone": phone,
    "timestamp": str(datetime.now()),
    "status": "pending"
}

# Load database
database = load_database()

# Save delivery
database[delivery_id] = delivery_data

save_database(database)

# Generate QR code
qr = qrcode.make(delivery_id)

filename = f"QR_{delivery_id}.png"
qr.save(filename)

print("\nDelivery created successfully!")
print("Delivery ID:", delivery_id)
print("QR saved as:", filename)
