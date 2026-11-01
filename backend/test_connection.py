"""Test MySQL database connection"""
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DB_CONFIG = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'user': os.environ.get('DB_USER', 'root'),
    'password': os.environ.get('DB_PASSWORD', ''),
    'database': os.environ.get('DB_NAME', 'telemedicine_db'),
    'port': int(os.environ.get('DB_PORT', 3306))
}

def test_connection():
    """Test database connection"""
    try:
        print("Attempting to connect to MySQL...")
        print(f"Host: {DB_CONFIG['host']}")
        print(f"User: {DB_CONFIG['user']}")
        print(f"Database: {DB_CONFIG['database']}")
        print(f"Port: {DB_CONFIG['port']}")
        print("-" * 50)

        conn = mysql.connector.connect(**DB_CONFIG)

        if conn.is_connected():
            print("[OK] Successfully connected to MySQL database!")
            print(f"[OK] Database: {DB_CONFIG['database']}")

            # Test a query
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM doctors")
            doctor_count = cursor.fetchone()[0]
            print(f"[OK] Found {doctor_count} doctors in database")

            cursor.execute("SELECT COUNT(*) FROM patients")
            patient_count = cursor.fetchone()[0]
            print(f"[OK] Found {patient_count} patients in database")

            cursor.close()
            conn.close()
            print("\n[OK] Database connection test PASSED!")
            return True

    except Error as e:
        print(f"\n[ERROR] Error connecting to MySQL: {e}")
        print("\nTroubleshooting tips:")
        print("1. Ensure MySQL service is running")
        print("2. Check your MySQL password in .env file")
        print("3. Verify database 'telemedicine_db' exists")
        print("4. Check if MySQL is on port 3306")
        return False

if __name__ == '__main__':
    test_connection()
