from vehicle import VehicleSimulator
import threading
import random
from config import VEHICLE_COUNT


def create_vehicle_sim(vehicle_id):
    start_lat = 52.2297 + random.uniform(-0.01, 0.01)
    start_lon = 21.0122 + random.uniform(-0.01, 0.01)
    sim = VehicleSimulator(vehicle_id, start_lat, start_lon)
    sim.start()

def main():
    for i in range(1, VEHICLE_COUNT):
        vehicle_id = f"car-{i:03d}"
        thread = threading.Thread(target=create_vehicle_sim, args=(vehicle_id,))
        thread.start()

if __name__ == "__main__":
    main()