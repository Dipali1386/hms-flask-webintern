from flask import Flask, request, jsonify
from datetime import datetime
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

# Dummy Data
doctors = [
    {"id": 1, "name": "Dr. Sharma", "department": "Cardiology", "available_slots": {"2025-06-01": ["10:00", "11:00"]}},
    {"id": 2, "name": "Dr. Verma", "department": "Neurology", "available_slots": {"2025-06-01": ["12:00", "14:00"]}},
]

patients = {
    101: {"name": "Rahul", "email": "rahul@example.com"},
    102: {"name": "Sneha", "email": "sneha@example.com"}
}

appointments = []  # Stores booked appointments

# Endpoint 1: Get doctor availability
@app.route('/doctors/availability', methods=['GET'])
def get_availability():
    department = request.args.get('department')
    date = request.args.get('date')

    if not department or not date:
        return jsonify({"error": "department and date are required"}), 400

    available = []
    for doc in doctors:
        if doc["department"].lower() == department.lower() and date in doc["available_slots"]:
            available.append({
                "doctor_id": doc["id"],
                "doctor_name": doc["name"],
                "available_slots": doc["available_slots"][date]
            })

    return jsonify({"available_doctors": available}), 200


# Endpoint 2: Book appointment
@app.route('/appointments', methods=['POST'])
def book_appointment():
    data = request.get_json()
    patient_id = data.get('patient_id')
    doctor_id = data.get('doctor_id')
    date = data.get('date')
    time_slot = data.get('time_slot')

    # Validation
    if not all([patient_id, doctor_id, date, time_slot]):
        return jsonify({"error": "All fields are required"}), 400

    doctor = next((d for d in doctors if d["id"] == doctor_id), None)
    if not doctor or date not in doctor["available_slots"] or time_slot not in doctor["available_slots"][date]:
        return jsonify({"error": "Doctor or timeslot not available"}), 400

    # Book it
    doctor["available_slots"][date].remove(time_slot)
    appointment = {
        "patient_id": patient_id,
        "doctor_id": doctor_id,
        "doctor_name": doctor["name"],
        "date": date,
        "time_slot": time_slot
    }
    appointments.append(appointment)

    return jsonify({"message": "Appointment booked", "appointment": appointment}), 201


# Endpoint 3: Get patient info
@app.route('/patients/<int:patient_id>', methods=['GET'])
def get_patient(patient_id):
    patient = patients.get(patient_id)
    if not patient:
        return jsonify({"error": "Patient not found"}), 404
    return jsonify(patient), 200


# Endpoint 4: Send confirmation email
@app.route('/notifications/email', methods=['POST'])
def send_email():
    data = request.get_json()
    to_email = data.get('to')
    subject = data.get('subject')
    message = data.get('message')

    if not all([to_email, subject, message]):
        return jsonify({"error": "Missing email fields"}), 400

    try:
        # Replace below with real email credentials if needed
        sender_email = "your_email@gmail.com"
        sender_password = "your_password"

        msg = MIMEText(message)
        msg["Subject"] = subject
        msg["From"] = sender_email
        msg["To"] = to_email

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, [to_email], msg.as_string())
        server.quit()

        return jsonify({"message": "Email sent successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
