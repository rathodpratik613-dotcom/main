# Local Setup Guide for MySQL

## Prerequisites
- MySQL installed and running locally
- Python 3.8+ installed
- pip installed

## Step 1: Setup Backend

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

## Step 2: Configure MySQL Credentials

Create a `.env` file in the backend directory with your MySQL credentials:

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password_here
DB_NAME=telemedicine_db
DB_PORT=3306
```

Note: If you don't have a password for MySQL root, leave DB_PASSWORD empty.

## Step 3: Initialize Database

Run the database setup script to create the database and insert sample data:

```bash
python setup_database.py
```

This will:
- Create the `telemedicine_db` database
- Create all required tables
- Insert sample data (doctors, pharmacies, medicines, patients)

## Step 4: Start the Backend Server

```bash
python app.py
```

The backend will be available at `http://localhost:5000`

## Step 5: Setup Frontend

The frontend is static HTML/CSS/JS and doesn't require installation.

Simply open `frontend/index.html` in your web browser, or use a simple HTTP server:

**Option 1: Direct file open**
- Double-click `frontend/index.html`

**Option 2: Python HTTP server**
```bash
cd frontend
python -m http.server 8000
```
Then open `http://localhost:8000` in your browser

**Option 3: VS Code Live Server**
- Install "Live Server" extension in VS Code
- Right-click `index.html` and select "Open with Live Server"

## Testing

Use these sample credentials to test:

| Name | Email | Password |
|------|-------|----------|
| John Smith | john.smith@email.com | patient123 |
| Jane Doe | jane.doe@email.com | patient123 |
| Robert Johnson | robert.johnson@email.com | patient123 |
| Emily Brown | emily.brown@email.com | patient123 |
| Michael Davis | michael.davis@email.com | patient123 |

## Troubleshooting

### MySQL Connection Issues
- Ensure MySQL service is running
- Check that the password in `.env` matches your MySQL root password
- Verify the database `telemedicine_db` exists (setup script will create it)

### Backend Not Starting
- Ensure Python 3.8+ is installed
- Check that all dependencies are installed: `pip install -r requirements.txt`
- Verify port 5000 is not in use by another application

### Frontend Not Connecting to Backend
- Ensure the Flask backend is running on `http://localhost:5000`
- Check browser console for CORS errors
- Verify the API_URL in `script.js` matches your backend URL
