from flask import Flask, request, jsonify
from fire_utils import register_vehicle, add_location, get_all_vehicles

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({"status": "Fleet Manager API running"}), 200

@app.route('/vehicle', methods=['POST'])
def vehicle():
    data = request.get_json()
    if not data or 'vehicle_id' not in data:
        return jsonify({"error": "Missing vehicle_id"}), 400
    try:
        register_vehicle(data)
        return jsonify({"status": "vehicle registered"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/location', methods=['POST'])
def location():
    data = request.get_json()
    if not data or 'vehicle_id' not in data:
        return jsonify({"error": "Missing vehicle_id"}), 400
    try:
        add_location(data)
        return jsonify({"status": "location updated"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/vehicles', methods=['GET'])
def vehicles():
    try:
        vehicles_data = get_all_vehicles()
        return jsonify(vehicles_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
