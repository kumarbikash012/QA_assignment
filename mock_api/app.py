from flask import Flask, jsonify, request

app = Flask(__name__)

patients = []

@app.route('/patients', methods=['POST'])
def create_patient():
    data = request.json
    patients.append(data)
    return jsonify(data), 201

@app.route('/patients/<int:patient_id>', methods=['GET'])
def get_patient(patient_id):
    if patient_id < len(patients):
        return jsonify(patients[patient_id]), 200
    return jsonify({"error": "Patient not found"}), 404

@app.route('/patients', methods=['GET'])
def get_patients():
    return jsonify(patients), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)