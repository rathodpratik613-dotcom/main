# Render Deployment Guide

## 🔴 Current Issue

The deployment failed because Render couldn't find the publish directory. This happens when the configuration doesn't match your folder structure.

## ✅ Solution: Deploy as Two Separate Services

### Step 1: Restructure for Easier Deployment

For Render, it's easier to have the frontend files in the backend folder. Let me restructure:

**Option A: Move frontend into backend (Recommended for Render)**

This allows deploying as a single service.

**Option B: Deploy two separate services**
- Backend as Web Service
- Frontend as Static Site

## 🚀 Option A: Single Service Deployment (Easier)

### 1. Reorganize Files

Move frontend files into the backend folder:

```
backend/
├── app.py
├── requirements.txt
├── database/
│   └── schema.sql
└── static/          <-- New folder
    ├── index.html
    ├── styles.css
    └── script.js
```

### 2. Update Backend to Serve Frontend

I'll update app.py to serve the frontend files.

### 3. Deploy to Render

- Create one Web Service
- Root directory: `backend`
- Build command: `pip install -r requirements.txt`
- Start command: `python app.py`

## 🚀 Option B: Two Separate Services (Current Structure)

### Deploy Backend

1. Go to Render Dashboard
2. New → Web Service
3. Connect GitHub repo
4. Configure:
   - **Name**: `telemedicine-backend`
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`
   - **Runtime**: Python 3
5. Click "Create Web Service"

### Deploy Frontend

1. Go to Render Dashboard
2. New → Static Site
3. Connect GitHub repo
4. Configure:
   - **Name**: `telemedicine-frontend`
   - **Root Directory**: `frontend`  <-- IMPORTANT!
   - **Build Command**: (leave empty)
   - **Publish Directory**: `.` (dot - current directory)
5. Click "Create Static Site"

### Update Frontend API URL

After backend is deployed:
1. Get the backend URL from Render (e.g., `https://telemedicine-backend.onrender.com`)
2. Edit `frontend/script.js`
3. Change:
   ```javascript
   const API_URL = 'http://localhost:5000/api';
   ```
   To:
   ```javascript
   const API_URL = 'https://telemedicine-backend.onrender.com/api';
   ```
4. Commit and push changes

## 🔧 Fix Current Deployment

If you want to fix the current failed deployment:

1. **Delete the failed service** from Render dashboard
2. **Create a new Static Site** with correct settings:
   - Root Directory: `frontend` (not empty!)
   - Publish Directory: `.` (dot)
3. **Create a separate Web Service** for the backend

## 💡 My Recommendation

**Use Option A (Single Service)** - it's simpler:
- Only one service to manage
- Frontend and backend always together
- Easier to maintain
- Works better with Render's free tier

Would you like me to restructure the project for Option A (single service deployment)?
