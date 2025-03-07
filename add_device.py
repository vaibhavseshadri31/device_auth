import json
import os
import time
import uuid
import argparse

def generate_device_id():
    timestamp = int(time.time() * 1000)
    random_part = uuid.uuid4().hex[:12]
    return f"device_{timestamp}_{random_part}"

def add_trusted_device(email):
    db_file = "database.json"
    
    if not os.path.exists(db_file):
        data = {}
    else:
        with open(db_file, 'r') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                print("Error: database.json is corrupted. Creating new database.")
                data = {}
    
    device_id = generate_device_id()
    
    if device_id in data:
        print(f"Device with ID {device_id} already exists")
        return False
    
    current_time = int(time.time() * 1000)
    
    data[device_id] = {
        "email": email,
        "first_seen": current_time,
        "last_used": current_time
    }
    
    with open(db_file, 'w') as f:
        json.dump(data, f, indent=4)
    
    print(f"Successfully added device for {email}")
    print(f"Add this device ID to localStorage: {device_id}")
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Add a trusted device to database.json")
    parser.add_argument("email", help="User's email address")
    
    args = parser.parse_args()
    
    add_trusted_device(args.email)