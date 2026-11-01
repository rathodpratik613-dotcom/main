# Telemedicine Platform - Deployment Guide

## Overview
This guide will help you deploy the Telemedicine Platform locally and prepare it for production deployment.

## Prerequisites
- Python 3.8 or higher
- Modern web browser (Chrome, Firefox, Edge, Safari)
- Basic knowledge of command line

## Local Development Setup

### 1. Backend Setup

#### Navigate to backend directory
```bash
cd telemedicine-platform/backend
```

#### Create virtual environment (recommended)
```bash
python -m venv venv
```

#### Activate virtual environment
- **Windows:**
  ```bash
  venv\Scripts\activate
  ```
- **Mac/Linux:**
  ```bash
  source venv/bin/activate
  ```

#### Install dependencies
```bash
pip install -r requirements.txt
```

#### Run the backend server
```bash
python app.py
```

The backend will start on `http://localhost:5000`

### 2. Frontend Setup

#### Option 1: Simple HTTP Server (Recommended for testing)

Navigate to frontend directory:
```bash
cd telemedicine-platform/frontend
```

Start a simple HTTP server:
- **Python 3:**
  ```bash
  python -m http.server 8000
  ```
- **Python 2:**
  ```bash
  python -m SimpleHTTPServer 8000
  ```

Access the frontend at: `http://localhost:8000`

#### Option 2: Using Live Server (VS Code)
1. Install the "Live Server" extension in VS Code
2. Right-click on `index.html`
3. Select "Open with Live Server"

#### Option 3: Using Node.js (if you have Node.js installed)
```bash
cd telemedicine-platform/frontend
npx serve
```

## Testing the Application

### 1. Test Backend API
Open your browser or use curl to test:
```bash
curl http://localhost:5000/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "message": "Telemedicine API is running"
}
```

### 2. Test Frontend-Backend Connection
1. Open your frontend URL (e.g., `http://localhost:8000`)
2. You should see the TeleMedicine login page
3. Register a new account or login with existing credentials
4. Navigate through the application to test all features

### Sample Login Credentials
The backend is pre-populated with sample data:

**Patient Accounts:**
- Email: `john.smith@email.com`
- Password: `patient123`

- Email: `jane.doe@email.com`
- Password: `patient123`

**Doctor Accounts:**
- Email: `rajesh.kumar@email.com`
- Password: `doctor123`

- Email: `maria.garcia@email.com`
- Password: `doctor123`

## API Endpoints Reference

### Health Check
- `GET /api/health` - Check API status

### Patients
- `POST /api/patients` - Register new patient
- `POST /api/patients/login` - Patient login
- `GET /api/patients/<id>` - Get patient details

### Doctors
- `GET /api/doctors` - Get all available doctors
- `GET /api/doctors/<id>` - Get specific doctor details

### Consultations
- `POST /api/consultations` - Create consultation request
- `GET /api/consultations/<id>` - Get consultation details
- `GET /api/consultations/patient/<patient_id>` - Get patient's consultations
- `POST /api/consultations/<id>/prescription` - Add prescription

### Pharmacies & Medicines
- `GET /api/pharmacies` - Get all pharmacies
- `GET /api/pharmacies/<id>/medicines` - Get medicines from a pharmacy
- `GET /api/medicines/search?q=<query>` - Search medicines

### Follow-ups
- `POST /api/followups` - Schedule follow-up
- `GET /api/followups/patient/<patient_id>` - Get patient's follow-ups
- `PUT /api/followups/<id>/complete` - Mark follow-up as completed

## Production Deployment

### Backend Deployment Options

#### Option 1: Gunicorn (Linux/Mac)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

#### Option 2: Waitress (Windows)
```bash
pip install waitress
waitress-serve --port=5000 app:app
```

#### Option 3: Docker
Create a `Dockerfile` in the backend directory:
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

Build and run:
```bash
docker build -t telemedicine-backend .
docker run -p 5000:5000 telemedicine-backend
```

### Frontend Deployment Options

#### Option 1: Netlify/Vercel (Recommended)
1. Push your frontend code to GitHub
2. Connect your repository to Netlify or Vercel
3. Deploy with default settings
4. Update `API_URL` in `script.js` to point to your production backend URL

#### Option 2: Apache/Nginx
Place the frontend files in your web server's document root:
```bash
# Apache
/var/www/html/telemedicine/

# Nginx
/usr/share/nginx/html/telemedicine/
```

#### Option 3: GitHub Pages
1. Create a `gh-pages` branch
2. Push frontend code to that branch
3. Enable GitHub Pages in repository settings
4. Update `API_URL` in `script.js` to point to your production backend

### Environment Variables
For production, consider using environment variables for sensitive data:

Create a `.env` file in the backend directory:
```env
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
DB_PATH=/path/to/production/database.db
```

Update `app.py` to load environment variables:
```python
from dotenv import load_dotenv
load_dotenv()
```

Add to `requirements.txt`:
```
python-dotenv==1.0.0
```

### Security Considerations

1. **Password Hashing**: Currently, passwords are stored in plain text. Implement password hashing using bcrypt or similar:
   ```python
   from werkzeug.security import generate_password_hash, check_password_hash
   ```

2. **HTTPS**: Always use HTTPS in production
3. **CORS**: Restrict CORS to specific domains in production
4. **Input Validation**: Add proper input validation and sanitization
5. **Rate Limiting**: Implement rate limiting to prevent abuse
6. **Database Security**: Use proper database credentials and encryption

### Database Backup
Regular backups are essential. Set up automated backups:
```bash
# Backup
cp database/telemedicine.db backup/telemedicine_$(date +%Y%m%d).db

# Restore
cp backup/telemedicine_20240101.db database/telemedicine.db
```

## Troubleshooting

### Backend won't start
- Check if port 5000 is already in use
- Verify Python version (3.8+)
- Ensure all dependencies are installed

### Frontend can't connect to backend
- Verify backend is running on `http://localhost:5000`
- Check CORS settings in `app.py`
- Ensure `API_URL` in `script.js` matches backend URL

### Database errors
- Check database file permissions
- Verify database file exists in the correct location
- Try deleting `telemedicine.db` and restarting (will recreate with sample data)

### Doctors not showing
- Ensure doctors have `available = 1` in the database
- Check the `/api/doctors` endpoint returns data

## Next Steps
1. Implement proper authentication with JWT tokens
2. Add email verification for registrations
3. Implement file upload for medical documents
4. Add real-time chat functionality
5. Integrate payment gateway for consultations
6. Add doctor availability calendar
7. Implement video consultation integration
8. Add multi-language support
9. Create admin dashboard
10. Implement analytics and reporting

## Support
For issues or questions, please refer to the project documentation or contact the development team.
