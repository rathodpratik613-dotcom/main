"""
Database Setup Script for Telemedicine Platform - PostgreSQL
This script initializes the PostgreSQL database with schema and sample data
"""
import psycopg2
from psycopg2 import sql, errors
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

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

def create_database():
    """Create the database if it doesn't exist"""
    try:
        # Connect to default postgres database
        config = DB_CONFIG.copy()
        config['database'] = 'postgres'
        conn = psycopg2.connect(**config)
        conn.autocommit = True
        cursor = conn.cursor()
        
        cursor.execute(f"CREATE DATABASE {DB_CONFIG['database']}")
        print(f"Database '{DB_CONFIG['database']}' created successfully")
        
        cursor.close()
        conn.close()
        return True
    except errors.DuplicateDatabase:
        print(f"Database '{DB_CONFIG['database']}' already exists")
        return True
    except Exception as e:
        print(f"Error creating database: {e}")
        return False

def init_db():
    """Initialize the database with schema and sample data"""
    conn = get_db_connection()
    if not conn:
        print("Failed to connect to PostgreSQL database!")
        return False

    cursor = conn.cursor()
    
    try:
        # Create tables
        print("Creating tables...")
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS patients (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                phone VARCHAR(20) NOT NULL,
                age INTEGER NOT NULL,
                gender VARCHAR(10) NOT NULL,
                address TEXT,
                password VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS doctors (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                phone VARCHAR(20) NOT NULL,
                specialization VARCHAR(100) NOT NULL,
                experience_years INTEGER,
                available BOOLEAN DEFAULT TRUE,
                password VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pharmacies (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                address TEXT NOT NULL,
                phone VARCHAR(20) NOT NULL,
                email VARCHAR(100),
                operating_hours VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS medicines (
                id SERIAL PRIMARY KEY,
                pharmacy_id INTEGER NOT NULL,
                name VARCHAR(200) NOT NULL,
                description TEXT,
                price DECIMAL(10, 2) NOT NULL,
                stock_quantity INTEGER DEFAULT 0,
                available BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (pharmacy_id) REFERENCES pharmacies(id) ON DELETE CASCADE
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS consultations (
                id SERIAL PRIMARY KEY,
                patient_id INTEGER NOT NULL,
                doctor_id INTEGER NOT NULL,
                symptoms TEXT NOT NULL,
                diagnosis TEXT,
                status VARCHAR(20) DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (patient_id) REFERENCES patients(id) ON DELETE CASCADE,
                FOREIGN KEY (doctor_id) REFERENCES doctors(id) ON DELETE CASCADE
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS prescriptions (
                id SERIAL PRIMARY KEY,
                consultation_id INTEGER NOT NULL,
                medicines TEXT NOT NULL,
                instructions TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (consultation_id) REFERENCES consultations(id) ON DELETE CASCADE
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS followups (
                id SERIAL PRIMARY KEY,
                consultation_id INTEGER NOT NULL,
                patient_id INTEGER NOT NULL,
                doctor_id INTEGER NOT NULL,
                scheduled_date DATE NOT NULL,
                notes TEXT,
                status VARCHAR(20) DEFAULT 'scheduled',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (consultation_id) REFERENCES consultations(id) ON DELETE CASCADE,
                FOREIGN KEY (patient_id) REFERENCES patients(id) ON DELETE CASCADE,
                FOREIGN KEY (doctor_id) REFERENCES doctors(id) ON DELETE CASCADE
            )
        ''')
        
        print("Tables created successfully")
        
        # Check if data already exists
        cursor.execute('SELECT COUNT(*) FROM doctors')
        doctor_count = cursor.fetchone()[0]
        
        if doctor_count == 0:
            print("Inserting sample data...")
            
            # Insert sample doctors
            doctors_data = [
                ('Dr. Rajesh Kumar', 'rajesh.kumar@email.com', '+919876543210', 'General Physician', 25, True, 'doctor123'),
                ('Dr. Maria Garcia', 'maria.garcia@email.com', '+1234567890', 'Cardiologist', 18, True, 'doctor123'),
                ('Dr. James Wilson', 'james.wilson@email.com', '+1234567891', 'Neurologist', 22, True, 'doctor123'),
                ('Dr. Sarah Ahmed', 'sarah.ahmed@email.com', '+1234567892', 'Pediatrician', 15, True, 'doctor123'),
                ('Dr. David Lee', 'david.lee@email.com', '+1234567893', 'Dermatologist', 20, True, 'doctor123'),
                ('Dr. Emily Chen', 'emily.chen@email.com', '+1234567894', 'Orthopedic Surgeon', 17, True, 'doctor123'),
                ('Dr. Michael Brown', 'michael.brown@email.com', '+1234567895', 'Gynecologist', 19, True, 'doctor123'),
                ('Dr. Lisa Patel', 'lisa.patel@email.com', '+1234567896', 'Ophthalmologist', 14, True, 'doctor123'),
                ('Dr. Robert Taylor', 'robert.taylor@email.com', '+1234567897', 'ENT Specialist', 21, True, 'doctor123'),
                ('Dr. Jennifer White', 'jennifer.white@email.com', '+1234567898', 'Psychiatrist', 16, True, 'doctor123'),
                ('Dr. William Johnson', 'william.johnson@email.com', '+1234567899', 'Gastroenterologist', 23, True, 'doctor123'),
                ('Dr. Amanda Martinez', 'amanda.martinez@email.com', '+1234567900', 'Nephrologist', 12, True, 'doctor123'),
                ('Dr. Christopher Davis', 'christopher.davis@email.com', '+1234567901', 'Pulmonologist', 20, True, 'doctor123'),
                ('Dr. Jessica Rodriguez', 'jessica.rodriguez@email.com', '+1234567902', 'Endocrinologist', 18, True, 'doctor123'),
                ('Dr. Daniel Anderson', 'daniel.anderson@email.com', '+1234567903', 'Rheumatologist', 15, True, 'doctor123'),
                ('Dr. Michelle Thomas', 'michelle.thomas@email.com', '+1234567904', 'Oncologist', 24, True, 'doctor123'),
                ('Dr. Matthew Jackson', 'matthew.jackson@email.com', '+1234567905', 'Hematologist', 19, True, 'doctor123'),
                ('Dr. Laura Harris', 'laura.harris@email.com', '+1234567906', 'Infectious Disease Specialist', 17, True, 'doctor123'),
                ('Dr. Kevin Clark', 'kevin.clark@email.com', '+1234567907', 'Urologist', 21, True, 'doctor123'),
                ('Dr. Nicole Lewis', 'nicole.lewis@email.com', '+1234567908', 'Plastic Surgeon', 16, True, 'doctor123'),
            ]
            cursor.executemany('INSERT INTO doctors (name, email, phone, specialization, experience_years, available, password) VALUES (%s, %s, %s, %s, %s, %s, %s)', doctors_data)
            
            # Insert pharmacies
            pharmacies_data = [
                ('HealthPlus Pharmacy', '123 Main Street, City Center', '+1234567894', 'healthplus@email.com', '9:00 AM - 9:00 PM'),
                ('MediCare Store', '456 Oak Avenue, West Side', '+1234567895', 'medicare@email.com', '8:00 AM - 10:00 PM'),
                ('QuickMeds', '789 Pine Road, East District', '+1234567896', 'quickmeds@email.com', '24/7'),
                ('PharmaWell', '321 Elm Street, North Side', '+1234567897', 'pharmawell@email.com', '10:00 AM - 8:00 PM'),
                ('City Drugs', '654 Maple Drive, South Side', '+1234567898', 'citydrugs@email.com', '8:00 AM - 9:00 PM'),
            ]
            cursor.executemany('INSERT INTO pharmacies (name, address, phone, email, operating_hours) VALUES (%s, %s, %s, %s, %s)', pharmacies_data)
            
            # Insert medicines
            medicines_data = [
                (1, 'Paracetamol 500mg', 'Pain reliever and fever reducer', 5.99, 150, True),
                (1, 'Ibuprofen 400mg', 'Anti-inflammatory pain reliever', 7.99, 120, True),
                (1, 'Aspirin 100mg', 'Blood thinner and pain reliever', 4.99, 200, True),
                (1, 'Amoxicillin 500mg', 'Antibiotic for bacterial infections', 12.99, 80, True),
                (1, 'Azithromycin 500mg', 'Antibiotic for respiratory infections', 15.99, 60, True),
                (1, 'Omeprazole 20mg', 'Proton pump inhibitor for acid reflux', 8.99, 130, True),
                (1, 'Metformin 500mg', 'Type 2 diabetes medication', 15.99, 140, True),
                (1, 'Lisinopril 10mg', 'ACE inhibitor for blood pressure', 7.99, 160, True),
                (1, 'Amlodipine 5mg', 'Calcium channel blocker for blood pressure', 9.99, 145, True),
                (1, 'Losartan 50mg', 'ARB for blood pressure', 11.99, 125, True),
                (2, 'Simvastatin 20mg', 'Statin for cholesterol', 13.99, 110, True),
                (2, 'Atorvastatin 10mg', 'Statin for cholesterol', 16.99, 95, True),
                (2, 'Clopidogrel 75mg', 'Antiplatelet for heart protection', 18.99, 120, True),
                (2, 'Albuterol Inhaler', 'Bronchodilator for asthma', 25.99, 80, True),
                (2, 'Fluticasone Inhaler', 'Inhaled corticosteroid for asthma', 32.99, 65, True),
                (3, 'Cetirizine 10mg', 'Antihistamine for allergies', 6.99, 150, True),
                (3, 'Loratadine 10mg', 'Antihistamine for allergies', 7.99, 140, True),
                (3, 'Fexofenadine 180mg', 'Antihistamine for allergies', 11.99, 120, True),
                (3, 'Prednisone 5mg', 'Oral corticosteroid', 8.99, 110, True),
                (3, 'Levothyroxine 50mcg', 'Thyroid hormone replacement', 12.99, 140, True),
                (4, 'Gabapentin 300mg', 'Anticonvulsant for nerve pain', 19.99, 95, True),
                (4, 'Sertraline 50mg', 'SSRI for depression and anxiety', 16.99, 120, True),
                (4, 'Fluoxetine 20mg', 'SSRI for depression and anxiety', 14.99, 135, True),
                (4, 'Zolpidem 10mg', 'Sedative for insomnia', 19.99, 95, True),
                (4, 'Methylphenidate 10mg', 'Stimulant for ADHD', 22.99, 80, True),
                (5, 'Donepezil 5mg', 'Cholinesterase inhibitor for Alzheimer', 24.99, 60, True),
                (5, 'Tadalafil 5mg', 'PDE5 inhibitor for erectile dysfunction', 35.99, 75, True),
                (5, 'Orlistat 120mg', 'Lipase inhibitor for weight loss', 45.99, 80, True),
                (5, 'Isotretinoin 20mg', 'Retinoid for severe acne', 45.99, 55, True),
                (5, 'Tretinoin 0.025% Cream', 'Retinoid for acne and anti-aging', 28.99, 85, True),
            ]
            cursor.executemany('INSERT INTO medicines (pharmacy_id, name, description, price, stock_quantity, available) VALUES (%s, %s, %s, %s, %s, %s)', medicines_data)
            
            # Insert sample patients
            patients_data = [
                ('John Smith', 'john.smith@email.com', '+1234567890', 35, 'male', '123 Oak Street, City Center', 'patient123'),
                ('Jane Doe', 'jane.doe@email.com', '+1234567891', 28, 'female', '456 Maple Avenue, West Side', 'patient123'),
                ('Robert Johnson', 'robert.johnson@email.com', '+1234567892', 42, 'male', '789 Pine Road, East District', 'patient123'),
                ('Emily Brown', 'emily.brown@email.com', '+1234567893', 31, 'female', '321 Elm Street, North Side', 'patient123'),
                ('Michael Davis', 'michael.davis@email.com', '+1234567894', 55, 'male', '654 Birch Drive, South Side', 'patient123'),
            ]
            cursor.executemany('INSERT INTO patients (name, email, phone, age, gender, address, password) VALUES (%s, %s, %s, %s, %s, %s, %s)', patients_data)
            
            conn.commit()
            print("Sample data inserted successfully")
        else:
            print(f"Database already contains {doctor_count} doctors. Skipping data insertion.")
        
        conn.commit()
        print("\n" + "="*60)
        print("Database setup completed successfully!")
        print("="*60)
        return True
        
    except Exception as e:
        print(f"Error initializing database: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    print("\n" + "="*60)
    print("TELEMEDICINE PLATFORM - PostgreSQL Database Setup")
    print("="*60)
    print(f"Database: {DB_CONFIG['database']}")
    print(f"Host: {DB_CONFIG['host']}:{DB_CONFIG['port']}")
    print("="*60 + "\n")
    
    # First create the database
    if create_database():
        # Then initialize it with schema and data
        init_db()
