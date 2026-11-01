from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
import datetime
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__, static_folder='frontend', static_url_path='')
CORS(app)

# MySQL Database Configuration
DB_CONFIG = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'user': os.environ.get('DB_USER', 'root'),
    'password': os.environ.get('DB_PASSWORD', ''),
    'database': os.environ.get('DB_NAME', 'telemedicine_db'),
    'port': int(os.environ.get('DB_PORT', 3306))
}

def get_db_connection():
    """Create and return a database connection"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    conn = get_db_connection()
    if conn:
        conn.close()
        return jsonify({'status': 'healthy', 'message': 'Telemedicine API is running with MySQL', 'database': 'MySQL'})
    else:
        return jsonify({'status': 'error', 'message': 'Database connection failed'}), 500

# Patient endpoints
@app.route('/api/patients', methods=['POST'])
def create_patient():
    data = request.json
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500

    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO patients (name, email, phone, age, gender, address, password)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        ''', (data['name'], data['email'], data['phone'], data['age'], data['gender'], data['address'], data['password']))
        conn.commit()
        return jsonify({'message': 'Patient created successfully', 'id': cursor.lastrowid}), 201
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/patients/login', methods=['POST'])
def patient_login():
    data = request.json
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500

    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute('SELECT * FROM patients WHERE email = %s AND password = %s', (data['email'], data['password']))
        patient = cursor.fetchone()
        if patient:
            patient.pop('password', None)
            return jsonify({'message': 'Login successful', 'patient': patient}), 200
        return jsonify({'error': 'Invalid credentials'}), 401
    finally:
        cursor.close()
        conn.close()

@app.route('/api/patients/<int:patient_id>', methods=['GET'])
def get_patient(patient_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500

    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute('SELECT * FROM patients WHERE id = %s', (patient_id,))
        patient = cursor.fetchone()
        if patient:
            patient.pop('password', None)
            return jsonify(patient), 200
        return jsonify({'error': 'Patient not found'}), 404
    finally:
        cursor.close()
        conn.close()

# Doctor endpoints
@app.route('/api/doctors', methods=['GET'])
def get_doctors():
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500

    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute('SELECT * FROM doctors WHERE available = TRUE')
        doctors = cursor.fetchall()
        for doc in doctors:
            doc.pop('password', None)
        return jsonify(doctors), 200
    finally:
        cursor.close()
        conn.close()

@app.route('/api/doctors/<int:doctor_id>', methods=['GET'])
def get_doctor(doctor_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500

    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute('SELECT * FROM doctors WHERE id = %s', (doctor_id,))
        doctor = cursor.fetchone()
        if doctor:
            doctor.pop('password', None)
            return jsonify(doctor), 200
        return jsonify({'error': 'Doctor not found'}), 404
    finally:
        cursor.close()
        conn.close()

# Consultation endpoints
@app.route('/api/consultations', methods=['POST'])
def create_consultation():
    data = request.json
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500

    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO consultations (patient_id, doctor_id, symptoms, status, created_at)
            VALUES (%s, %s, %s, %s, %s)
        ''', (data['patient_id'], data['doctor_id'], data['symptoms'], 'pending', datetime.datetime.now()))
        conn.commit()
        return jsonify({'message': 'Consultation created successfully', 'id': cursor.lastrowid}), 201
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/consultations/<int:consultation_id>', methods=['GET'])
def get_consultation(consultation_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500

    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute('SELECT * FROM consultations WHERE id = %s', (consultation_id,))
        consultation = cursor.fetchone()
        if consultation:
            return jsonify(consultation), 200
        return jsonify({'error': 'Consultation not found'}), 404
    finally:
        cursor.close()
        conn.close()

@app.route('/api/consultations/patient/<int:patient_id>', methods=['GET'])
def get_patient_consultations(patient_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500

    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute('''
            SELECT c.*, d.name as doctor_name, d.specialization
            FROM consultations c
            JOIN doctors d ON c.doctor_id = d.id
            WHERE c.patient_id = %s
            ORDER BY c.created_at DESC
        ''', (patient_id,))
        consultations = cursor.fetchall()
        return jsonify(consultations), 200
    finally:
        cursor.close()
        conn.close()

@app.route('/api/consultations/<int:consultation_id>/prescription', methods=['POST'])
def add_prescription():
    data = request.json
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500

    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO prescriptions (consultation_id, medicines, instructions, created_at)
            VALUES (%s, %s, %s, %s)
        ''', (data['consultation_id'], data['medicines'], data['instructions'], datetime.datetime.now()))
        conn.commit()

        cursor.execute('UPDATE consultations SET status = %s WHERE id = %s', ('completed', data['consultation_id']))
        conn.commit()

        return jsonify({'message': 'Prescription added successfully'}), 201
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Pharmacy endpoints
@app.route('/api/pharmacies', methods=['GET'])
def get_pharmacies():
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500

    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute('SELECT * FROM pharmacies')
        pharmacies = cursor.fetchall()
        return jsonify(pharmacies), 200
    finally:
        cursor.close()
        conn.close()

@app.route('/api/pharmacies/<int:pharmacy_id>/medicines', methods=['GET'])
def get_pharmacy_medicines(pharmacy_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500

    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute('SELECT * FROM medicines WHERE pharmacy_id = %s AND available = TRUE', (pharmacy_id,))
        medicines = cursor.fetchall()
        return jsonify(medicines), 200
    finally:
        cursor.close()
        conn.close()

@app.route('/api/medicines/search', methods=['GET'])
def search_medicines():
    search_term = request.args.get('q', '')
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500

    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute('''
            SELECT m.*, p.name as pharmacy_name, p.address as pharmacy_address, p.phone as pharmacy_phone
            FROM medicines m
            JOIN pharmacies p ON m.pharmacy_id = p.id
            WHERE m.name LIKE %s AND m.available = TRUE
        ''', (f'%{search_term}%',))
        medicines = cursor.fetchall()
        return jsonify(medicines), 200
    finally:
        cursor.close()
        conn.close()

# Follow-up endpoints
@app.route('/api/followups', methods=['POST'])
def create_followup():
    data = request.json
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500

    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO followups (consultation_id, patient_id, doctor_id, scheduled_date, notes, status)
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', (data['consultation_id'], data['patient_id'], data['doctor_id'], data['scheduled_date'], data.get('notes', ''), 'scheduled'))
        conn.commit()
        return jsonify({'message': 'Follow-up scheduled successfully', 'id': cursor.lastrowid}), 201
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/followups/patient/<int:patient_id>', methods=['GET'])
def get_patient_followups(patient_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500

    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute('''
            SELECT f.*, d.name as doctor_name
            FROM followups f
            JOIN doctors d ON f.doctor_id = d.id
            WHERE f.patient_id = %s
            ORDER BY f.scheduled_date ASC
        ''', (patient_id,))
        followups = cursor.fetchall()
        return jsonify(followups), 200
    finally:
        cursor.close()
        conn.close()

@app.route('/api/followups/<int:followup_id>/complete', methods=['PUT'])
def complete_followup(followup_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500

    cursor = conn.cursor()
    try:
        cursor.execute('UPDATE followups SET status = %s WHERE id = %s', ('completed', followup_id))
        conn.commit()
        return jsonify({'message': 'Follow-up marked as completed'}), 200
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Serve frontend
@app.route('/')
def index():
    return send_from_directory('frontend', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('frontend', path)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print("\n" + "="*60)
    print("TELEMEDICINE PLATFORM - MySQL Backend")
    print("="*60)
    print(f"Database: MySQL - {DB_CONFIG['database']}")
    print(f"Host: {DB_CONFIG['host']}:{DB_CONFIG['port']}")
    print(f"Server running on: http://localhost:{port}")
    print("="*60 + "\n")
    app.run(debug=False, host='0.0.0.0', port=port)
