import firebase_admin, os
from firebase_admin import credentials, firestore, initialize_app
from datetime import datetime
from utils import save_log_locally, upload_to_gcs

UPLOAD_INTERVAL = 10
counter = {}

os.environ["GOOGLE_CLOUD_PROJECT"] = "fleet-manager-api"
if not firebase_admin._apps:
    cred = credentials.ApplicationDefault()
    initialize_app(cred)
db = firestore.client()


def register_vehicle(data):
    vehicle_id = data['vehicle_id']
    doc_ref = db.collection('vehicles').document(vehicle_id)
    doc_ref.set({
        'vehicle_id': vehicle_id,
        'driver_name': data.get('driver_name', ''),
        'created_at': datetime.today().strftime('%Y-%m-%d'),
    })


def add_location(data):
    vehicle_id = data['vehicle_id']
    timestamp = datetime.utcnow().isoformat()

    loc_ref = db.collection('vehicles').document(vehicle_id).collection('locations').document(timestamp)
    data = {
        'lat': data.get('lat'),
        'lon': data.get('lon'),
        'speed': data.get('speed'),
        'fuel': data.get('fuel'),
        'timestamp': timestamp
    }
    save_log_locally(vehicle_id, data)

    loc_ref.set(data)

    db.collection('vehicles').document(vehicle_id).update({
        'last_location': data
    })

    counter[vehicle_id] = counter.get(vehicle_id, 0) + 1
    if counter[vehicle_id] >= UPLOAD_INTERVAL:
        filename = f"logs/{vehicle_id}_log.json"
        upload_to_gcs(
            "fleet-manager-logs-api",
            filename,
            f"logs/{vehicle_id}/{timestamp}.json"
        )
        os.remove(filename)
        counter[vehicle_id] = 0


def get_all_vehicles():
    vehicles_ref = db.collection('vehicles').stream()
    result = []
    for doc in vehicles_ref:
        data = doc.to_dict()
        result.append(data)
    return result