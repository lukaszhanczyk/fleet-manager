import json, os
from google.cloud import storage

def get_storage_client():
    return storage.Client()

def upload_to_gcs(bucket_name, source_file, destination_blob):
    client = get_storage_client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob)
    blob.upload_from_filename(source_file)
    print(f"✅ Uploaded {source_file} to gs://{bucket_name}/{destination_blob}")

def save_log_locally(vehicle_id, data):
    folder = 'logs'
    os.makedirs(folder, exist_ok=True)
    filename = f"{folder}/{vehicle_id}_log.json"

    entry = {
        "vehicle_id": vehicle_id,
        "timestamp": data["timestamp"],
        "lat": data["lat"],
        "lon": data["lon"],
        "speed": data["speed"],
        "fuel": data["fuel"]
    }

    with open(filename, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")