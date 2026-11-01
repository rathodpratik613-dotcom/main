from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import sqlite3
import datetime
import os

app = Flask(__name__, static_folder='frontend', static_url_path='')
CORS(app)

# SQLite Database
DB_PATH = os.environ.get('DB_PATH', 'telemedicine.db')

def get_db_connection():
    """Create and return a database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database with tables and sample data"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT NOT NULL,
            age INTEGER NOT NULL,
            gender TEXT NOT NULL,
            address TEXT,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS doctors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT NOT NULL,
            specialization TEXT NOT NULL,
            experience_years INTEGER,
            available BOOLEAN DEFAULT 1,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pharmacies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            address TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT,
            operating_hours TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS medicines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pharmacy_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL,
            stock_quantity INTEGER DEFAULT 0,
            available BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (pharmacy_id) REFERENCES pharmacies(id) ON DELETE CASCADE
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS consultations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            doctor_id INTEGER NOT NULL,
            symptoms TEXT NOT NULL,
            diagnosis TEXT,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (patient_id) REFERENCES patients(id) ON DELETE CASCADE,
            FOREIGN KEY (doctor_id) REFERENCES doctors(id) ON DELETE CASCADE
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS prescriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            consultation_id INTEGER NOT NULL,
            medicines TEXT NOT NULL,
            instructions TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (consultation_id) REFERENCES consultations(id) ON DELETE CASCADE
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS followups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            consultation_id INTEGER NOT NULL,
            patient_id INTEGER NOT NULL,
            doctor_id INTEGER NOT NULL,
            scheduled_date DATE NOT NULL,
            notes TEXT,
            status TEXT DEFAULT 'scheduled',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (consultation_id) REFERENCES consultations(id) ON DELETE CASCADE,
            FOREIGN KEY (patient_id) REFERENCES patients(id) ON DELETE CASCADE,
            FOREIGN KEY (doctor_id) REFERENCES doctors(id) ON DELETE CASCADE
        )
    ''')
    
    # Check if data exists
    cursor.execute('SELECT COUNT(*) FROM doctors')
    if cursor.fetchone()[0] == 0:
        # Insert sample data
        doctors = [
            ('Dr. Rajesh Kumar', 'rajesh.kumar@email.com', '+919876543210', 'General Physician', 25, 'doctor123'),
            ('Dr. Maria Garcia', 'maria.garcia@email.com', '+1234567890', 'Cardiologist', 18, 'doctor123'),
            ('Dr. James Wilson', 'james.wilson@email.com', '+1234567891', 'Neurologist', 22, 'doctor123'),
            ('Dr. Sarah Ahmed', 'sarah.ahmed@email.com', '+1234567892', 'Pediatrician', 15, 'doctor123'),
            ('Dr. David Lee', 'david.lee@email.com', '+1234567893', 'Dermatologist', 20, 'doctor123'),
        ]
        cursor.executemany('INSERT INTO doctors (name, email, phone, specialization, experience_years, password) VALUES (?, ?, ?, ?, ?, ?)', doctors)
        
        pharmacies = [
            ('HealthPlus Pharmacy', '123 Main Street, City Center', '+1234567894', 'healthplus@email.com', '9:00 AM - 9:00 PM'),
            ('MediCare Store', '456 Oak Avenue, West Side', '+1234567895', 'medicare@email.com', '8:00 AM - 10:00 PM'),
            ('QuickMeds', '789 Pine Road, East District', '+1234567896', 'quickmeds@email.com', '24/7'),
        ]
        cursor.executemany('INSERT INTO pharmacies (name, address, phone, email, operating_hours) VALUES (?, ?, ?, ?, ?)', pharmacies)
        
        medicines = [
            (1, 'Paracetamol 500mg', 'Pain reliever and fever reducer', 5.99, 150),
            (1, 'Ibuprofen 400mg', 'Anti-inflammatory pain reliever', 7.99, 120),
            (1, 'Amoxicillin 500mg', 'Antibiotic for bacterial infections', 12.99, 80),
            (2, 'Omeprazole 20mg', 'Proton pump inhibitor for acid reflux', 8.99, 130),
            (2, 'Metformin 500mg', 'Type 2 diabetes medication', 15.99, 140),
            (3, 'Cetirizine 10mg', 'Antihistamine for allergies', 6.99, 150),
        ]
        cursor.executemany('INSERT INTO medicines (pharmacy_id, name, description, price, stock_quantity) VALUES (?, ?, ?, ?, ?)', medicines)
        
        patients = [
            ('John Smith', 'john.smith@email.com', '+1234567890', 35, 'male', '123 Oak Street, City Center', 'patient123'),
            ('Jane Doe', 'jane.doe@email.com', '+1234567891', 28, 'female', '456 Maple Avenue, West Side', 'patient123'),
            ('Robert Johnson', 'robert.johnson@email.com', '+1234567892', 42, 'male', '789 Pine Road, East District', 'patient123'),
        ]
        cursor.executemany('INSERT INTO patients (name, email, phone, age, gender, address, password) VALUES (?, ?, ?, ?, ?, ?, ?)', patients)
    
    conn.commit()
    conn.close()

# Initialize database on startup
init_db()

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    try:
        conn = get_db_connection()
        conn.close()
        return jsonify({'status': 'healthy', 'message': 'Telemedicine API is running with SQLite', 'database': 'SQLite'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Patient endpoints
@app.route('/api/patients', methods=['POST'])
def create_patient():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO patients (name, email, phone, age, gender, address, password)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (data['name'], data['email'], data['phone'], data['age'], data['gender'], data['address'], data['password']))
        conn.commit()
        return jsonify({'message': 'Patient created successfully', 'id': cursor.lastrowid}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/patients/login', methods=['POST'])
def patient_login():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT * FROM patients WHERE email = ? AND password = ?', (data['email'], data['password']))
        patient = cursor.fetchone()
        if patient:
            patient_dict = dict(patient)
            patient_dict.pop('password', None)
            return jsonify({'message': 'Login successful', 'patient': patient_dict}), 200
        return jsonify({'error': 'Invalid credentials'}), 401
    finally:
        conn.close()

@app.route('/api/patients/<int:patient_id>', methods=['GET'])
def get_patient(patient_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT * FROM patients WHERE id = ?', (patient_id,))
        patient = cursor.fetchone()
        if patient:
            patient_dict = dict(patient)
            patient_dict.pop('password', None)
            return jsonify(patient_dict), 200
        return jsonify({'error': 'Patient not found'}), 404
    finally:
        conn.close()

# Doctor endpoints
@app.route('/api/doctors', methods=['GET'])
def get_doctors():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT * FROM doctors WHERE available = 1')
        doctors = cursor.fetchall()
        doctors_list = []
        for doc in doctors:
            doc_dict = dict(doc)
            doc_dict.pop('password', None)
            doctors_list.append(doc_dict)
        return jsonify(doctors_list), 200
    finally:
        conn.close()

@app.route('/api/doctors/<int:doctor_id>', methods=['GET'])
def get_doctor(doctor_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT * FROM doctors WHERE id = ?', (doctor_id,))
        doctor = cursor.fetchone()
        if doctor:
            doctor_dict = dict(doctor)
            doctor_dict.pop('password', None)
            return jsonify(doctor_dict), 200
        return jsonify({'error': 'Doctor not found'}), 404
    finally:
        conn.close()

# Consultation endpoints
@app.route('/api/consultations', methods=['POST'])
def create_consultation():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO consultations (patient_id, doctor_id, symptoms, status, created_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (data['patient_id'], data['doctor_id'], data['symptoms'], 'pending', datetime.datetime.now()))
        conn.commit()
        return jsonify({'message': 'Consultation created successfully', 'id': cursor.lastrowid}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/consultations/<int:consultation_id>', methods=['GET'])
def get_consultation(consultation_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT * FROM consultations WHERE id = ?', (consultation_id,))
        consultation = cursor.fetchone()
        if consultation:
            return jsonify(dict(consultation)), 200
        return jsonify({'error': 'Consultation not found'}), 404
    finally:
        conn.close()

@app.route('/api/consultations/patient/<int:patient_id>', methods=['GET'])
def get_patient_consultations(patient_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            SELECT c.*, d.name as doctor_name, d.specialization
            FROM consultations c
            JOIN doctors d ON c.doctor_id = d.id
            WHERE c.patient_id = ?
            ORDER BY c.created_at DESC
        ''', (patient_id,))
        consultations = cursor.fetchall()
        return jsonify([dict(c) for c in consultations]), 200
    finally:
        conn.close()

@app.route('/api/consultations/<int:consultation_id>/prescription', methods=['POST'])
def add_prescription():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO prescriptions (consultation_id, medicines, instructions, created_at)
            VALUES (?, ?, ?, ?)
        ''', (data['consultation_id'], data['medicines'], data['instructions'], datetime.datetime.now()))
        conn.commit()

        cursor.execute('UPDATE consultations SET status = ? WHERE id = ?', ('completed', data['consultation_id']))
        conn.commit()

        return jsonify({'message': 'Prescription added successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

# Pharmacy endpoints
@app.route('/api/pharmacies', methods=['GET'])
def get_pharmacies():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT * FROM pharmacies')
        pharmacies = cursor.fetchall()
        return jsonify([dict(p) for p in pharmacies]), 200
    finally:
        conn.close()

@app.route('/api/pharmacies/<int:pharmacy_id>/medicines', methods=['GET'])
def get_pharmacy_medicines(pharmacy_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT * FROM medicines WHERE pharmacy_id = ? AND available = 1', (pharmacy_id,))
        medicines = cursor.fetchall()
        return jsonify([dict(m) for m in medicines]), 200
    finally:
        conn.close()

@app.route('/api/medicines/search', methods=['GET'])
def search_medicines():
    search_term = request.args.get('q', '')
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            SELECT m.*, p.name as pharmacy_name, p.address as pharmacy_address, p.phone as pharmacy_phone
            FROM medicines m
            JOIN pharmacies p ON m.pharmacy_id = p.id
            WHERE m.name LIKE ? AND m.available = 1
        ''', (f'%{search_term}%',))
        medicines = cursor.fetchall()
        return jsonify([dict(m) for m in medicines]), 200
    finally:
        conn.close()

# Follow-up endpoints
@app.route('/api/followups', methods=['POST'])
def create_followup():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO followups (consultation_id, patient_id, doctor_id, scheduled_date, notes, status)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (data['consultation_id'], data['patient_id'], data['doctor_id'], data['scheduled_date'], data.get('notes', ''), 'scheduled'))
        conn.commit()
        return jsonify({'message': 'Follow-up scheduled successfully', 'id': cursor.lastrowid}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/followups/patient/<int:patient_id>', methods=['GET'])
def get_patient_followups(patient_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            SELECT f.*, d.name as doctor_name
            FROM followups f
            JOIN doctors d ON f.doctor_id = d.id
            WHERE f.patient_id = ?
            ORDER BY f.scheduled_date ASC
        ''', (patient_id,))
        followups = cursor.fetchall()
        return jsonify([dict(f) for f in followups]), 200
    finally:
        conn.close()

@app.route('/api/followups/<int:followup_id>/complete', methods=['PUT'])
def complete_followup(followup_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('UPDATE followups SET status = ? WHERE id = ?', ('completed', followup_id))
        conn.commit()
        return jsonify({'message': 'Follow-up marked as completed'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
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
    print("TELEMEDICINE PLATFORM - SQLite Backend")
    print("="*60)
    print(f"Database: SQLite - {DB_PATH}")
    print(f"Server running on: http://localhost:{port}")
    print("="*60 + "\n")
    app.run(debug=False, host='0.0.0.0', port=port)
