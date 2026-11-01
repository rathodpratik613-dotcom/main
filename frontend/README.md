# TeleMedicine Frontend

This is the patient-facing frontend for the TeleMedicine platform.

## 📁 What's Included

- `index.html` - Main HTML file with all pages
- `styles.css` - Modern, responsive styling
- `script.js` - Frontend logic and API integration

## 🚀 How to Use

### Option 1: Direct File Open
Simply double-click `index.html` to open in your browser.

### Option 2: Local Server (Recommended)
```bash
# Navigate to this folder
cd frontend

# Start a local server
python -m http.server 8000

# Open in browser
http://localhost:8000
```

## 🔧 Configuration

The frontend connects to the backend API at:
```
http://localhost:5000/api
```

If your backend is running on a different URL/port, edit `script.js` and change:
```javascript
const API_URL = 'http://localhost:5000/api';
```

## 📱 Features

- Patient registration and login
- Browse available doctors
- Request consultations
- Search medicines at pharmacies
- View consultation history
- Manage follow-up appointments

## 🔑 Test Credentials

Use these accounts to test:
- Email: john.smith@email.com
- Password: patient123

## 📝 Notes

- This frontend requires the backend to be running
- The backend should be started before using the frontend
- All data is stored in the backend's SQLite database
