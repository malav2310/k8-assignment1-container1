from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

CONTAINER_2_URL = "http://container2:7000/process"

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    
    # Validate input
    if not data or 'file' not in data or not data['file']:
        return jsonify({"file": None, "error": "Invalid JSON input."}), 400
    
    file_name = data['file']
    file_path = f"/malav_PV_dir/{file_name}"  # Mounted volume path

    # Check if file exists
    if not os.path.exists(file_path):
        return jsonify({"file": file_name, "error": "File not found."}), 404
    
    # Send request to Container 2
    try:
        response = requests.post(CONTAINER_2_URL, json=data)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000)