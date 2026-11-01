"""
MySQL Connection Test Script
Run this to verify MySQL connection before starting the backend
"""

import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_mysql_connection():
    print("=" * 60)
    print("MYSQL CONNECTION TEST")
    print("=" * 60)

    # Configuration
    config = {
        'host': os.environ.get('DB_HOST', 'localhost'),
        'user': os.environ.get('DB_USER', 'root'),
        'password': os.environ.get('DB_PASSWORD', ''),
        'database': os.environ.get('DB_NAME', 'telemedicine_db'),
        'port': int(os.environ.get('DB_PORT', 3306))
    }

    print(f"\nConfiguration:")
    print(f"  Host: {config['host']}")
    print(f"  Port: {config['port']}")
    print(f"  User: {config['user']}")
    print(f"  Database: {config['database']}")
    print(f"  Password: {'*' * len(config['password']) if config['password'] else '(empty)'}")

    try:
        # Test connection
        print("\n[1/4] Testing connection to MySQL server...")
        conn = mysql.connector.connect(
            host=config['host'],
            user=config['user'],
            password=config['password'],
            port=config['port']
        )
        print("✅ Successfully connected to MySQL server!")
        conn.close()

        # Test database
        print("\n[2/4] Testing connection to database...")
        conn = mysql.connector.connect(**config)
        print(f"✅ Successfully connected to database '{config['database']}'!")

        # Test tables
        print("\n[3/4] Checking tables...")
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        print(f"✅ Found {len(tables)} tables:")
        for table in tables:
            print(f"   - {table[0]}")

        # Test data
        print("\n[4/4] Checking sample data...")
        cursor.execute("SELECT COUNT(*) FROM doctors")
        doctor_count = cursor.fetchone()[0]
        print(f"✅ Doctors: {doctor_count}")

        cursor.execute("SELECT COUNT(*) FROM patients")
        patient_count = cursor.fetchone()[0]
        print(f"✅ Patients: {patient_count}")

        cursor.execute("SELECT COUNT(*) FROM pharmacies")
        pharmacy_count = cursor.fetchone()[0]
        print(f"✅ Pharmacies: {pharmacy_count}")

        cursor.execute("SELECT COUNT(*) FROM medicines")
        medicine_count = cursor.fetchone()[0]
        print(f"✅ Medicines: {medicine_count}")

        cursor.close()
        conn.close()

        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED!")
        print("=" * 60)
        print("\nYou can now start the backend with:")
        print("  python app_mysql.py")
        print("\n")

        return True

    except Error as e:
        print(f"\n❌ Error: {e}")
        print("\nTroubleshooting:")
        print("1. Ensure MySQL is running")
        print("2. Check .env file for correct credentials")
        print("3. Verify database 'telemedicine_db' exists")
        print("4. Try running mysql_schema.sql in MySQL Workbench")
        print("\n")
        return False

if __name__ == '__main__':
    success = test_mysql_connection()
    exit(0 if success else 1)
