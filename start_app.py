import os
import sys
import time
import subprocess
import webbrowser
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(BASE_DIR, 'backend')
FRONTEND_DIR = os.path.join(BASE_DIR, 'frontend')

def test_mysql():
    """Test if MySQL can be reached with current .env credentials"""
    try:
        from dotenv import load_dotenv
        import mysql.connector
        
        env_path = os.path.join(BACKEND_DIR, '.env')
        if os.path.exists(env_path):
            load_dotenv(env_path)
            
        password = os.environ.get('DB_PASSWORD', '')
        if not password:
            return False, "No password provided in .env"
            
        conn = mysql.connector.connect(
            host=os.environ.get('DB_HOST', 'localhost'),
            user=os.environ.get('DB_USER', 'root'),
            password=password,
            database=os.environ.get('DB_NAME', 'telemedicine_db'),
            port=int(os.environ.get('DB_PORT', 3306)),
            connection_timeout=3
        )
        conn.close()
        return True, "Connected successfully"
    except Exception as e:
        return False, str(e)

def start_frontend_server(port=8000):
    class FrontendHandler(SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=FRONTEND_DIR, **kwargs)
        def log_message(self, format, *args):
            pass # Suppress noisy request logs
            
    server = HTTPServer(('127.0.0.1', port), FrontendHandler)
    server.serve_forever()

def main():
    print("=" * 65)
    print("      🏥 TELEMEDICINE PLATFORM - STARTING SERVICES 🏥")
    print("=" * 65)
    
    can_mysql, mysql_msg = test_mysql()
    if can_mysql:
        backend_script = 'app_mysql.py'
        print("✅ Database: MySQL 8.0 (telemedicine_db)")
    else:
        backend_script = 'app.py'
        print(f"ℹ️  Database: SQLite SQL database (telemedicine.db - 100+ doctors seeded)")
        print(f"    (To use MySQL, set DB_PASSWORD in backend/.env: {mysql_msg})")
        
    print("🚀 Starting Flask Backend on http://localhost:5000 ...")
    backend_proc = subprocess.Popen(
        [sys.executable, backend_script],
        cwd=BACKEND_DIR
    )
    
    time.sleep(1.5)
    
    print("🌐 Starting Frontend Server on http://localhost:8000 ...")
    frontend_thread = threading.Thread(target=start_frontend_server, args=(8000,), daemon=True)
    frontend_thread.start()
    
    print("=" * 65)
    print("✅ APPLICATION IS LIVE!")
    print("   👉 Frontend URL: http://localhost:8000")
    print("   👉 Backend API:  http://localhost:5000/api")
    print("   👉 Health Check: http://localhost:5000/api/health")
    print("=" * 65)
    print("Opening application in your default browser...")
    webbrowser.open('http://localhost:8000')
    
    try:
        backend_proc.wait()
    except KeyboardInterrupt:
        print("\nStopping services...")
        backend_proc.terminate()

if __name__ == '__main__':
    main()
