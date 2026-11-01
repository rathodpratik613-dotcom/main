# TeleMedicine Backend

This is the Flask backend API for the TeleMedicine platform.

## 📁 What's Included

- `app.py` - Flask application with all API endpoints
- `requirements.txt` - Python dependencies
- `database/` - Database folder
  - `schema.sql` - Database schema (for reference)
  - `telemedicine.db` - SQLite database (auto-created on first run)

## 🚀 How to Run

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. **Install dependencies**:
```bash
pip install -r requirements.txt
```

2. **Start the server**:
```bash
python app.py
```

The server will:
- Automatically create the SQLite database
- Load sample data (100 doctors, 30 medicines, 5 patients)
- Start on `http://localhost:5000`

3. **Verify it's running**:
Open http://localhost:5000/api/health in your browser
You should see: `{"status":"healthy","message":"Telemedicine API is running"}`

## 📡 API Endpoints

### Health Check
- `GET /api/health` - Check API status

### Patients
- `POST /api/patients` - Register new patient
- `POST /api/patients/login` - Patient login
- `GET /api/patients/<id>` - Get patient details

### Doctors
- `GET /api/doctors` - Get all available doctors
- `GET /api/doctors/<id>` - Get specific doctor

### Consultations
- `POST /api/consultations` - Create consultation
- `GET /api/consultations/<id>` - Get consultation
- `GET /api/consultations/patient/<patient_id>` - Get patient's consultations
- `POST /api/consultations/<id>/prescription` - Add prescription

### Pharmacies & Medicines
- `GET /api/pharmacies` - Get all pharmacies
- `GET /api/pharmacies/<id>/medicines` - Get pharmacy medicines
- `GET /api/medicines/search?q=<term>` - Search medicines

### Follow-ups
- `POST /api/followups` - Schedule follow-up
- `GET /api/followups/patient/<patient_id>` - Get patient's follow-ups
- `PUT /api/followups/<id>/complete` - Mark follow-up as completed

## 💾 Database

- **Type**: SQLite (built into Python)
- **Location**: `database/telemedicine.db`
- **Auto-created**: Yes, on first run
- **Sample Data**: 100 doctors, 30 medicines, 5 patients

## 🔧 Configuration

The database is configured in `app.py`:
```python
DB_PATH = os.path.join(os.path.dirname(__file__), 'database', 'telemedicine.db')
```

## 📝 Sample Data

The database is automatically populated with:
- 100 real doctors with various specializations
- 5 pharmacies
- 30 common medicines
- 5 sample patients for testing

### Test Patient Credentials
- Email: john.smith@email.com
- Password: patient123

## 🔒 Security Notes

This is a demonstration project. For production:
- Implement proper password hashing (bcrypt)
- Add JWT-based authentication
- Enable HTTPS
- Add input validation and sanitization
- Use environment variables for sensitive data
