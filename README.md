# TeleMedicine Platform

A comprehensive telemedicine solution connecting patients with remote doctors, integrating local pharmacies for medicine availability, and managing follow-ups digitally.

## Features

- **Patient Registration & Authentication**: Easy sign-up and login for patients
- **Remote Doctor Consultations**: Request consultations with available doctors
- **Medicine Availability Search**: Find medicines at local pharmacies
- **Digital Follow-up Management**: Schedule and track follow-up appointments
- **Prescription Management**: Doctors can prescribe medicines digitally

## Tech Stack

- **Frontend**: Plain HTML, CSS, JavaScript (no frameworks required)
- **Backend**: Python + Flask
- **Database**: MySQL or PostgreSQL (production-ready)

### Database Options

1. **MySQL** (default): Production-ready, widely used
2. **PostgreSQL**: Recommended for Render free tier deployment
3. **SQLite**: Available for local development (app_sqlite.py)

## Documentation

- **ER Diagram**: See [ER_DIAGRAM.md](ER_DIAGRAM.md) for complete database schema and relationships
- **Deployment Guide**: See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions
- **Render Deployment**: See [RENDER_DEPLOYMENT_GUIDE.md](RENDER_DEPLOYMENT_GUIDE.md) for Render-specific deployment
- **Local Setup**: See [LOCAL_SETUP.md](LOCAL_SETUP.md) for local development with MySQL

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Installation & Setup

### 1. Setup Backend

1. Navigate to the backend directory:
```bash
cd telemedicine-platform/backend
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
```

3. Activate the virtual environment:

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Start the Flask server:
```bash
python app.py
```

The backend will automatically create the SQLite database with sample data on first run and will be available at `http://localhost:5000`

### 4. Setup Frontend

The frontend is static HTML/CSS/JS and doesn't require installation.

Simply open `frontend/index.html` in your web browser, or use a simple HTTP server:

**Option 1: Direct file open**
- Double-click `frontend/index.html`

**Option 2: Python HTTP server**
```bash
cd telemedicine-platform/frontend
python -m http.server 8000
```
Then open `http://localhost:8000` in your browser

**Option 3: VS Code Live Server**
- Install "Live Server" extension in VS Code
- Right-click `index.html` and select "Open with Live Server"

## Usage

### For Patients

1. **Register**: Create a new patient account
2. **Login**: Enter your credentials
3. **Find Doctors**: Browse available doctors and their specializations
4. **Request Consultation**: Select a doctor and describe your symptoms
5. **View Consultations**: Track your consultation history and status
6. **Find Medicines**: Search for medicines at local pharmacies
7. **Manage Follow-ups**: View and complete scheduled follow-ups

### Sample Data

The database includes:
- 100 real doctors with diverse specializations from around the world
- 5 pharmacies
- 100 real medicines (pain relievers, antibiotics, diabetes medications, blood pressure medications, cholesterol medications, heart medications, asthma medications, allergy medications, thyroid medications, arthritis medications, antidepressants, antipsychotics, sleep medications, ADHD medications, Alzheimer medications, and more)
- 5 sample patients for testing

### Sample Patient Login Credentials

You can use these credentials to test the application:

| Name | Email | Password |
|------|-------|----------|
| John Smith | john.smith@email.com | patient123 |
| Jane Doe | jane.doe@email.com | patient123 |
| Robert Johnson | robert.johnson@email.com | patient123 |
| Emily Brown | emily.brown@email.com | patient123 |
| Michael Davis | michael.davis@email.com | patient123 |

Or you can register a new patient account through the application.

### API Endpoints

#### Health Check
- `GET /api/health` - Check API status

#### Patients
- `POST /api/patients` - Register new patient
- `POST /api/patients/login` - Patient login
- `GET /api/patients/<id>` - Get patient details

#### Doctors
- `GET /api/doctors` - Get all available doctors
- `GET /api/doctors/<id>` - Get specific doctor details

#### Consultations
- `POST /api/consultations` - Create new consultation
- `GET /api/consultations/<id>` - Get consultation details
- `GET /api/consultations/patient/<patient_id>` - Get patient's consultations
- `POST /api/consultations/<id>/prescription` - Add prescription

#### Pharmacies & Medicines
- `GET /api/pharmacies` - Get all pharmacies
- `GET /api/pharmacies/<id>/medicines` - Get pharmacy medicines
- `GET /api/medicines/search?q=<term>` - Search medicines

#### Follow-ups
- `POST /api/followups` - Schedule follow-up
- `GET /api/followups/patient/<patient_id>` - Get patient's follow-ups
- `PUT /api/followups/<id>/complete` - Mark follow-up as completed

## Project Structure

```
telemedicine-platform/
├── backend/
│   ├── app.py              # Flask application
│   ├── requirements.txt    # Python dependencies
│   └── venv/              # Virtual environment (created during setup)
├── frontend/
│   ├── index.html         # Main HTML file
│   ├── styles.css         # Styling
│   └── script.js          # Frontend logic
├── database/
│   └── schema.sql         # MySQL database schema
└── README.md             # This file
```

## Troubleshooting

### MySQL Connection Issues
- Ensure MySQL service is running
- Check that the password in `app.py` matches your MySQL root password
- Verify the database `telemedicine_db` exists

### Backend Not Starting
- Ensure Python 3.8+ is installed
- Check that all dependencies are installed: `pip install -r requirements.txt`
- Verify port 5000 is not in use by another application

### Frontend Not Connecting to Backend
- Ensure the Flask backend is running on `http://localhost:5000`
- Check browser console for CORS errors
- Verify the API_URL in `script.js` matches your backend URL

### Permission Errors
- Run MySQL Command Line Client as administrator
- Ensure the database user has proper permissions

## Security Notes

This is a demonstration project. For production use:
- Implement proper password hashing (bcrypt)
- Add JWT-based authentication
- Enable HTTPS
- Add input validation and sanitization
- Implement rate limiting
- Add proper error handling
- Use environment variables for sensitive data

## Future Enhancements

- Real-time chat between patients and doctors
- Video consultation integration
- Prescription download/print functionality
- Payment integration for pharmacy orders
- SMS/email notifications for appointments
- Doctor dashboard for managing consultations
- Mobile app version

## License

This project is for educational purposes.
