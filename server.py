from flask import Flask, jsonify
from flask_cors import CORS
import threading
import motion_detection_alert  # Import your motion detection script

app = Flask(__name__)
CORS(app)  # Allow frontend access

surveillance_active = False
thread = None

def run_surveillance():
    global surveillance_active
    surveillance_active = True
    motion_detection_alert.motion_detection()

@app.route('/start', methods=['POST'])  # Allow only POST requests
def start_surveillance():
    global thread, surveillance_active
    if not surveillance_active:
        thread = threading.Thread(target=run_surveillance)
        thread.start()
        return jsonify({"message": "Surveillance started!"})
    return jsonify({"message": "Surveillance is already running."})

@app.route('/stop', methods=['POST'])  # Allow only POST requests
def stop_surveillance():
    global surveillance_active
    surveillance_active = False
    return jsonify({"message": "Surveillance stopped!"})

if __name__ == '__main__':
    app.run(debug=True)
