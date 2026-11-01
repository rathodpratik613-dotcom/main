# How to Share This Project

## Option 1: Upload to GitHub (Recommended)

### Step 1: Create a GitHub Repository
1. Go to https://github.com and sign in (or create an account)
2. Click the "+" icon in the top-right corner
3. Select "New repository"
4. Name it: `telemedicine-platform`
5. Make it "Public" so others can see it
6. Click "Create repository"

### Step 2: Push to GitHub
Open Command Prompt in the project folder and run:

```bash
cd C:\Users\ratho\telemedicine-platform
git remote add origin https://github.com/YOUR_USERNAME/telemedicine-platform.git
git branch -M main
git push -u origin main
```

Replace `YOUR_USERNAME` with your actual GitHub username.

### Step 3: Share the Link
Once uploaded, share this URL with others:
```
https://github.com/YOUR_USERNAME/telemedicine-platform
```

## Option 2: Create a ZIP File

### Step 1: Create ZIP
1. Right-click on the `telemedicine-platform` folder
2. Select "Send to" → "Compressed (zipped) folder"
3. This creates `telemedicine-platform.zip`

### Step 2: Share the ZIP
- Send via email
- Upload to Google Drive, Dropbox, or OneDrive
- Share via WhatsApp, Telegram, etc.

## Option 3: Direct Folder Sharing

Share the project folder directly:
- Google Drive
- Dropbox
- OneDrive
- WeTransfer (for larger files)

## What Others Need to Run This Project

### Quick Setup for Others:

1. **Download/Extract** the project
2. **Install Python** (if not already installed): https://python.org
3. **Install dependencies**:
   ```bash
   cd telemedicine-platform/backend
   pip install -r requirements.txt
   ```
4. **Run the backend**:
   ```bash
   python app.py
   ```
5. **Open the frontend**:
   - Double-click `frontend/index.html`, OR
   - Run: `cd frontend && python -m http.server 8000`
   - Go to: http://localhost:8000

### Test Login Credentials:
- Email: john.smith@email.com
- Password: patient123

## Project Files Included

✅ Backend (Python + Flask)
✅ Frontend (HTML, CSS, JavaScript)
✅ Database (SQLite - auto-created)
✅ Documentation (README.md, QUICK_START.md)
✅ Sample data (100 doctors, 30 medicines, 5 patients)

## Important Notes

- The SQLite database (`telemedicine.db`) is NOT included in the git repository
- It will be automatically created when others run the backend
- All sample data (doctors, medicines, patients) is included in the code and will be loaded automatically
