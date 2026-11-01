# MySQL Setup Guide for Telemedicine Platform

## Quick Setup (For Presentation Tomorrow)

### Step 1: Install MySQL (if not already installed)

**Windows:**
1. Download MySQL Installer from: https://dev.mysql.com/downloads/installer/
2. Run the installer and select "Developer Default"
3. Set root password (remember it!)
4. Complete the installation

**Alternative - XAMPP (Easier Option):**
1. Download XAMPP from: https://www.apachefriends.org/
2. Install XAMPP
3. Start MySQL from XAMPP Control Panel
4. Default password: (empty/blank)

### Step 2: Create Database in MySQL Workbench

1. Open MySQL Workbench
2. Click the "+" to create a new connection
3. Connection Name: `telemedicine`
4. Hostname: `localhost`
5. Port: `3306`
6. Username: `root`
7. Password: (your MySQL password or leave blank for XAMPP)
8. Click "Test Connection" then "OK"

### Step 3: Run the Schema Script

1. In MySQL Workbench, open the connection
2. Click "File" → "Open SQL Script"
3. Navigate to: `telemedicine-platform/database/mysql_schema.sql`
4. Click the lightning bolt ⚡ to execute the script
5. You should see "Database setup complete!" in the output

**Alternative - Command Line:**
```bash
mysql -u root -p < database/mysql_schema.sql
```

### Step 4: Configure Backend

1. Open `telemedicine-platform/backend/.env`
2. Update your MySQL password:
   ```
   DB_PASSWORD=your_mysql_password_here
   ```
3. If using XAMPP with no password, leave it blank:
   ```
   DB_PASSWORD=
   ```

### Step 5: Install MySQL Dependencies

```bash
cd telemedicine-platform/backend
pip install -r requirements.txt
```

This will install:
- Flask
- flask-cors
- mysql-connector-python
- python-dotenv

### Step 6: Run the MySQL Backend

```bash
cd telemedicine-platform/backend
python app_mysql.py
```

You should see:
```
============================================================
TELEMEDICINE PLATFORM - MySQL Backend
============================================================
Database: MySQL - telemedicine_db
Host: localhost:3306
Server running on: http://localhost:5000
============================================================

✅ Successfully connected to MySQL database!
```

### Step 7: Test the Connection

Open your browser and go to:
```
http://localhost:5000/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "message": "Telemedicine API is running with MySQL",
  "database": "MySQL"
}
```

### Step 8: Start Frontend

```bash
cd telemedicine-platform/frontend
python -m http.server 8000
```

Open in browser:
```
http://localhost:8000
```

## Verify Everything is Working

1. ✅ MySQL database `telemedicine_db` exists
2. ✅ All tables are created (7 tables)
3. ✅ Sample data is inserted (100 doctors, 5 patients, etc.)
4. ✅ Backend connects to MySQL successfully
5. ✅ Frontend connects to backend
6. ✅ You can login with: `john.smith@email.com` / `patient123`

## Sample Login Credentials

**Patient:**
- Email: `john.smith@email.com`
- Password: `patient123`

**Doctor:**
- Email: `rajesh.kumar@email.com`
- Password: `doctor123`

## Troubleshooting

### Error: "Access denied for user 'root'@'localhost'"
- Check your MySQL password in `.env` file
- Try resetting MySQL password if needed

### Error: "Unknown database 'telemedicine_db'"
- Make sure you ran the `mysql_schema.sql` script
- Check in MySQL Workbench if database exists

### Error: "Can't connect to MySQL server"
- Ensure MySQL service is running
- In XAMPP: Start MySQL from Control Panel
- In standalone MySQL: Start MySQL service

### Backend won't start
- Check if port 5000 is available
- Verify MySQL credentials in `.env`
- Check error messages in terminal

## Presentation Tips

1. **Show ER Diagram:** Open `ER_DIAGRAM_PRESENTATION.html` in browser
2. **Show Database:** Open MySQL Workbench and show tables
3. **Show Data:** Run `SELECT * FROM doctors LIMIT 5;` in Workbench
4. **Show Backend:** Show terminal with "Successfully connected to MySQL"
5. **Show Frontend:** Demo the application features
6. **Show API:** Show `/api/health` response

## Files Reference

- **Schema:** `database/mysql_schema.sql` - Database structure and sample data
- **Backend:** `backend/app_mysql.py` - Flask app with MySQL
- **Config:** `backend/.env` - Database credentials
- **ER Diagram:** `ER_DIAGRAM_PRESENTATION.html` - Visual ER diagram
- **Dependencies:** `backend/requirements.txt` - Python packages

## Quick Reference Commands

```bash
# Start MySQL (XAMPP)
# Open XAMPP Control Panel → Start MySQL

# Start MySQL (Standalone)
# Windows Services → MySQL80 → Start

# Create database (if schema not run)
mysql -u root -p -e "CREATE DATABASE telemedicine_db;"

# Run schema
mysql -u root -p telemedicine_db < database/mysql_schema.sql

# Check tables
mysql -u root -p telemedicine_db -e "SHOW TABLES;"

# Check data
mysql -u root -p telemedicine_db -e "SELECT COUNT(*) FROM doctors;"

# Start backend
cd backend
python app_mysql.py

# Start frontend
cd frontend
python -m http.server 8000
```

## Success Checklist

Before your presentation, verify:

- [ ] MySQL is installed and running
- [ ] Database `telemedicine_db` exists
- [ ] All 7 tables are created
- [ ] Sample data is inserted (100 doctors, 5 patients, etc.)
- [ ] Backend connects to MySQL
- [ ] Backend API is accessible at http://localhost:5000
- [ ] Frontend is accessible at http://localhost:8000
- [ ] Login works with sample credentials
- [ ] Can view doctors
- [ ] Can search medicines
- [ ] ER diagram opens in browser

Good luck with your presentation! 🎉
