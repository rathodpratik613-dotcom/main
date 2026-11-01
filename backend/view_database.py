import sqlite3
import os

# Database path
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'database', 'telemedicine.db')

print("=" * 60)
print("TELEMEDICINE DATABASE VIEWER")
print("=" * 60)
print(f"\nDatabase Location: {DB_PATH}")
print(f"Database File Size: {os.path.getsize(DB_PATH) / 1024:.2f} KB")
print(f"Database Exists: {os.path.exists(DB_PATH)}\n")

# Connect to database
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Get all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

print(f"Found {len(tables)} tables in database:\n")

for table in tables:
    table_name = table[0]
    print(f"\n{'=' * 60}")
    print(f"TABLE: {table_name}")
    print(f"{'=' * 60}")

    # Get row count
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    count = cursor.fetchone()[0]
    print(f"Total Records: {count}\n")

    # Get table schema
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()
    print("Columns:")
    for col in columns:
        print(f"  - {col[1]} ({col[2]})")

    # Show sample data (first 3 records)
    if count > 0:
        print(f"\nSample Data (first 3 records):")
        cursor.execute(f"SELECT * FROM {table_name} LIMIT 3")
        rows = cursor.fetchall()
        for i, row in enumerate(rows, 1):
            print(f"\n  Record {i}:")
            for j, value in enumerate(row):
                col_name = columns[j][1]
                print(f"    {col_name}: {value}")

conn.close()

print("\n" + "=" * 60)
print("DATABASE VIEW COMPLETE")
print("=" * 60)
