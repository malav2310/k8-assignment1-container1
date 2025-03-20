from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

# Persistent volume path
PERSISTENT_STORAGE_PATH = "/malav_PV_dir"
CONTAINER_2_URL = "http://container2-service:80/process"

# Ensure the storage directory exists
os.makedirs(PERSISTENT_STORAGE_PATH, exist_ok=True)

@app.route('/store-file', methods=['POST'])
def store_file():
    data = request.get_json()

    # Validate JSON input
    if not data or 'file' not in data or not data['file']:
        return jsonify({"file": None, "error": "Invalid JSON input."}), 400
    if 'data' not in data or not data['data']:
        return jsonify({"file": data['file'], "error": "No data provided."}), 400

    file_name = data['file']
    file_content = data['data']
    file_path = os.path.join(PERSISTENT_STORAGE_PATH, file_name)

    try:
        # Write data to the file
        with open(file_path, 'w') as f:
            f.write(file_content)

        return jsonify({"file": file_name, "message": "Success."}), 201
    except Exception as e:
        return jsonify({"file": file_name, "error": "Error while storing the file to the storage."}), 500

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    
    # Validate input
    if not data or 'file' not in data or not data['file']:
        return jsonify({"file": None, "error": "Invalid JSON input."}), 400

    # Check if file exists
    if not os.path.exists(file_path):
        return jsonify({"file": file_name, "error": "File not found."}), 404

    # Check if file is in valid CSV format
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
            if not lines[0].strip() == "product, amount":
                return jsonify({"file": file_name, "error": "Input file not in CSV format."}), 400
    except Exception:
        return jsonify({"file": file_name, "error": "Input file not in CSV format."}), 400

    # Send request to Container 2
    try:
        response = requests.post(CONTAINER_2_URL, json=data)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000)
