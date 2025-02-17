from flask import Flask, request, jsonify
import pickle
import serial
import numpy as np

app = Flask(__name__)

# Load the saved model
with open('model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

# Set up serial communication with Arduino (adjust 'COM3' and baudrate as needed)
arduino_port = 'COM3'
baud_rate = 9600
ser = serial.Serial(arduino_port, baud_rate, timeout=1)


@app.route('/predict', methods=['POST'])
def predict():
    """
    Endpoint to make predictions using provided JSON data.
    """
    data = request.json
    if 'features' not in data:
        return jsonify({"error": "No features provided"}), 400

    features = np.array(data['features']).reshape(1, -1)
    prediction = model.predict(features)

    return jsonify({"prediction": prediction.tolist()})


@app.route('/predict/live', methods=['GET'])
def predict_live():
    """
    Endpoint to make predictions from live data coming from Arduino.
    """
    try:
        # Read a line from Arduino
        line = ser.readline().decode('utf-8').strip()
        if not line:
            return jsonify({"error": "No data received from Arduino"}), 500

        # Assume the line is comma-separated values
        features = np.array([float(value) for value in line.split(',')]).reshape(1, -1)
        prediction = model.predict(features)

        return jsonify({"prediction": prediction.tolist()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
