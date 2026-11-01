# Quick Start Guide

## Step 1: Start the Backend

1. **Open Command Prompt**
   - Navigate to the backend directory:
   ```bash
   cd C:\Users\ratho\telemedicine-platform\backend
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   ```

3. **Activate Virtual Environment**
   ```bash
   venv\Scripts\activate
   ```

4. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Start the Server**
   ```bash
   python app.py
   ```

   The database will be automatically created with sample data on first run!

6. **Verify Backend**
   - Open browser to: http://localhost:5000/api/health
   - You should see: `{"status":"healthy","message":"Telemedicine API is running"}`

## Step 4: Open the Frontend

**Option 1: Direct Open**
- Navigate to: `C:\Users\ratho\telemedicine-platform\frontend`
- Double-click `index.html`

**Option 2: Python Server** (recommended)
- In a new Command Prompt:
  ```bash
  cd C:\Users\ratho\telemedicine-platform\frontend
  python -m http.server 8000
  ```
- Open browser to: http://localhost:8000

## Step 5: Test the Application

### Option 1: Use Sample Login Credentials

You can use these pre-configured patient accounts:

| Email | Password |
|-------|----------|
| john.smith@email.com | patient123 |
| jane.doe@email.com | patient123 |
| robert.johnson@email.com | patient123 |
| emily.brown@email.com | patient123 |
| michael.davis@email.com | patient123 |

### Option 2: Register a New Patient

1. **Register a Patient**
   - Click "Register" tab
   - Fill in patient details
   - Click "Register"
   - Then login with your credentials

2. **Find a Doctor**
   - Click "Find Doctors" in navigation
   - Browse available doctors
   - Click "Request Consultation" on any doctor
   - Describe your symptoms and submit

3. **View Consultations**
   - Click "My Consultations"
   - See your consultation requests

4. **Find Medicines**
   - Click "Medicines"
   - Search for medicines (e.g., "Paracetamol")
   - See availability at local pharmacies

## Troubleshooting

**Backend won't start?**
- Check if port 5000 is already in use
- Try changing the port in `app.py`:
  ```python
  app.run(debug=True, port=5001)
  ```

**Frontend can't connect to backend?**
- Ensure backend is running (you should see "Running on http://127.0.0.1:5000")
- Check browser console (F12) for errors

**Database not created?**
- The SQLite database is created automatically on first run
- Check if the database file exists in the `database` folder
- Look for `telemedicine.db` file

## Need Help?

Check the full README.md for detailed documentation and API endpoints.
