from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
from psycopg2 import errors
import datetime
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

# PostgreSQL Database Configuration
DB_CONFIG = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'user': os.environ.get('DB_USER', 'postgres'),
    'password': os.environ.get('DB_PASSWORD', ''),
    'database': os.environ.get('DB_NAME', 'telemedicine_db'),
    'port': int(os.environ.get('DB_PORT', 5432))
}

def get_db_connection():
    """Create and return a database connection"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"Error connecting to PostgreSQL: {e}")
        return None

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    conn = get_db_connection()
    if conn:
        conn.close()
        return jsonify({'status': 'healthy', 'message': 'Telemedicine API is running with PostgreSQL', 'database': 'PostgreSQL'})
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
            RETURNING id
        ''', (data['name'], data['email'], data['phone'], data['age'], data['gender'], data['address'], data['password']))
        patient_id = cursor.fetchone()[0]
        conn.commit()
        return jsonify({'message': 'Patient created successfully', 'id': patient_id}), 201
    except errors.UniqueViolation:
        return jsonify({'error': 'Email already exists'}), 409
    except Exception as e:
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

    cursor = conn.cursor()
    try:
        cursor.execute('SELECT * FROM patients WHERE email = %s AND password = %s', (data['email'], data['password']))
        columns = [desc[0] for desc in cursor.description]
        patient = cursor.fetchone()
        if patient:
            patient_dict = dict(zip(columns, patient))
            return jsonify({'message': 'Login successful', 'patient': patient_dict}), 200
        return jsonify({'error': 'Invalid credentials'}), 401
    finally:
        cursor.close()
        conn.close()

@app.route('/api/patients/<int:patient_id>', methods=['GET'])
def get_patient(patient_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500

    cursor = conn.cursor()
    try:
        cursor.execute('SELECT * FROM patients WHERE id = %s', (patient_id,))
        columns = [desc[0] for desc in cursor.description]
        patient = cursor.fetchone()
        if patient:
            patient_dict = dict(zip(columns, patient))
            return jsonify(patient_dict), 200
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

    cursor = conn.cursor()
    try:
        cursor.execute('SELECT * FROM doctors WHERE available = TRUE')
        columns = [desc[0] for desc in cursor.description]
        doctors = cursor.fetchall()
        doctors_list = [dict(zip(columns, doctor)) for doctor in doctors]
        return jsonify(doctors_list), 200
    finally:
        cursor.close()
        conn.close()

@app.route('/api/doctors/<int:doctor_id>', methods=['GET'])
def get_doctor(doctor_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500

    cursor = conn.cursor()
    try:
        cursor.execute('SELECT * FROM doctors WHERE id = %s', (doctor_id,))
        columns = [desc[0] for desc in cursor.description]
        doctor = cursor.fetchone()
        if doctor:
            doctor_dict = dict(zip(columns, doctor))
            return jsonify(doctor_dict), 200
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
            RETURNING id
        ''', (data['patient_id'], data['doctor_id'], data['symptoms'], 'pending', datetime.datetime.now()))
        consultation_id = cursor.fetchone()[0]
        conn.commit()
        return jsonify({'message': 'Consultation created successfully', 'id': consultation_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/consultations/<int:consultation_id>', methods=['GET'])
def get_consultation(consultation_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500

    cursor = conn.cursor()
    try:
        cursor.execute('SELECT * FROM consultations WHERE id = %s', (consultation_id,))
        columns = [desc[0] for desc in cursor.description]
        consultation = cursor.fetchone()
        if consultation:
            consultation_dict = dict(zip(columns, consultation))
            return jsonify(consultation_dict), 200
        return jsonify({'error': 'Consultation not found'}), 404
    finally:
        cursor.close()
        conn.close()

@app.route('/api/consultations/patient/<int:patient_id>', methods=['GET'])
def get_patient_consultations(patient_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500

    cursor = conn.cursor()
    try:
        cursor.execute('''
            SELECT c.*, d.name as doctor_name, d.specialization
            FROM consultations c
            JOIN doctors d ON c.doctor_id = d.id
            WHERE c.patient_id = %s
            ORDER BY c.created_at DESC
        ''', (patient_id,))
        columns = [desc[0] for desc in cursor.description]
        consultations = cursor.fetchall()
        consultations_list = [dict(zip(columns, consultation)) for consultation in consultations]
        return jsonify(consultations_list), 200
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

        cursor.execute('UPDATE consultations SET status = %s WHERE id = %s', ('completed', data['consultation_id']))

        conn.commit()
        return jsonify({'message': 'Prescription added successfully'}), 201
    except Exception as e:
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

    cursor = conn.cursor()
    try:
        cursor.execute('SELECT * FROM pharmacies')
        columns = [desc[0] for desc in cursor.description]
        pharmacies = cursor.fetchall()
        pharmacies_list = [dict(zip(columns, pharmacy)) for pharmacy in pharmacies]
        return jsonify(pharmacies_list), 200
    finally:
        cursor.close()
        conn.close()

@app.route('/api/pharmacies/<int:pharmacy_id>/medicines', methods=['GET'])
def get_pharmacy_medicines(pharmacy_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500

    cursor = conn.cursor()
    try:
        cursor.execute('SELECT * FROM medicines WHERE pharmacy_id = %s AND available = TRUE', (pharmacy_id,))
        columns = [desc[0] for desc in cursor.description]
        medicines = cursor.fetchall()
        medicines_list = [dict(zip(columns, medicine)) for medicine in medicines]
        return jsonify(medicines_list), 200
    finally:
        cursor.close()
        conn.close()

@app.route('/api/medicines/search', methods=['GET'])
def search_medicines():
    search_term = request.args.get('q', '')
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500

    cursor = conn.cursor()
    try:
        cursor.execute('''
            SELECT m.*, p.name as pharmacy_name, p.address as pharmacy_address, p.phone as pharmacy_phone
            FROM medicines m
            JOIN pharmacies p ON m.pharmacy_id = p.id
            WHERE m.name ILIKE %s AND m.available = TRUE
        ''', (f'%{search_term}%',))
        columns = [desc[0] for desc in cursor.description]
        medicines = cursor.fetchall()
        medicines_list = [dict(zip(columns, medicine)) for medicine in medicines]
        return jsonify(medicines_list), 200
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
            RETURNING id
        ''', (data['consultation_id'], data['patient_id'], data['doctor_id'], data['scheduled_date'], data.get('notes', ''), 'scheduled'))
        followup_id = cursor.fetchone()[0]
        conn.commit()
        return jsonify({'message': 'Follow-up scheduled successfully', 'id': followup_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/followups/patient/<int:patient_id>', methods=['GET'])
def get_patient_followups(patient_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500

    cursor = conn.cursor()
    try:
        cursor.execute('''
            SELECT f.*, d.name as doctor_name
            FROM followups f
            JOIN doctors d ON f.doctor_id = d.id
            WHERE f.patient_id = %s
            ORDER BY f.scheduled_date ASC
        ''', (patient_id,))
        columns = [desc[0] for desc in cursor.description]
        followups = cursor.fetchall()
        followups_list = [dict(zip(columns, followup)) for followup in followups]
        return jsonify(followups_list), 200
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
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print("\n" + "="*60)
    print("TELEMEDICINE PLATFORM - PostgreSQL Backend")
    print("="*60)
    print(f"Database: PostgreSQL - {DB_CONFIG['database']}")
    print(f"Host: {DB_CONFIG['host']}:{DB_CONFIG['port']}")
    print(f"Server running on: http://localhost:{port}")
    print("="*60 + "\n")
    print("Note: Run 'python setup_database_postgres.py' first to initialize the database")
    print("="*60 + "\n")
    app.run(debug=False, host='0.0.0.0', port=port)
