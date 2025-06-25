import random
import requests
import time
from config import API_URL, SEND_INTERVAL

class VehicleSimulator:
    def __init__(self, vehicle_id, lat, lon):
        self.fuel = 1000
        self.vehicle_id = vehicle_id
        self.lat = lat
        self.lon = lon

    def move(self):
        self.lat += random.uniform(-0.0003, 0.0003)
        self.lon += random.uniform(-0.0003, 0.0003)

    def send_location(self):
        payload = {
            "vehicle_id": self.vehicle_id,
            "fuel": self.fuel,
            "lat": self.lat,
            "lon": self.lon,
            "speed": random.randint(10, 90),
            "battery": random.randint(40, 100)
        }

        try:
            response = requests.post(f"{API_URL}/location", json=payload)
            print(f"[{self.vehicle_id}] Sent data: {payload}, status: {response.status_code}")
        except Exception as e:
            print(f"[{self.vehicle_id}] ERROR: {e}")

    def create_vehicle(self):
        payload = {
            "vehicle_id": self.vehicle_id,
            "driver_name": self.vehicle_id + "-name"
        }

        try:
            response = requests.post(f"{API_URL}/vehicle", json=payload)
            print(f"[{self.vehicle_id}] Sent data: {payload}, status: {response.status_code}")
        except Exception as e:
            print(f"[{self.vehicle_id}] ERROR: {e}")

    def start(self):
        self.create_vehicle()
        while self.fuel > 0:
            self.move()
            self.send_location()
            time.sleep(SEND_INTERVAL)
            self.fuel -= 1