# Hospital Management System - Flask Backend

This project is a backend service for a Hospital Management System (HMS), developed as part of a software engineering internship assignment.

## 📌 Project Objective

To develop a RESTful backend in Python (Flask) that allows:
- Viewing doctor availability by department and date
- Booking appointments based on doctor and time slot
- Retrieving patient details
- Sending email confirmations for appointments

## 🛠 Tech Stack

- **Backend**: Python, Flask
- **Database**: In-memory (using dictionaries for demo)
- **Email**: SMTP (Gmail)
- **Tools**: Git, VS Code

## 🚀 API Endpoints

### 1. Get Available Doctors
`GET /doctors/availability?department={department}&date={date}`  
→ Returns available doctors and time slots.

### 2. Book Appointment
`POST /appointments`  
→ JSON input: `patient_id`, `doctor_id`, `date`, `time_slot`

### 3. Get Patient Info
`GET /patients/{id}`  
→ Returns patient details.

### 4. Send Email Notification
`POST /notifications/email`  
→ Sends confirmation email with appointment details.

## 📦 Setup Instructions

```bash
pip install flask
python app.py
