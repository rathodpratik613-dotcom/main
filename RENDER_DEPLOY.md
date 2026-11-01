# Render Deployment Guide - Single Service

## 🚀 Quick Deploy to Render

### Step 1: Push to GitHub

If you haven't already:

```bash
cd C:\Users\ratho\telemedicine-dist
git init
git add .
git commit -m "Ready for Render deployment"
git remote add origin https://github.com/rathodpratik613-dotcom/medical.git
git branch -M main
git push -u origin main
```

### Step 2: Deploy to Render

1. **Go to Render**: https://render.com
2. **Sign up/login** with your GitHub account
3. **Click "New +"** → "Web Service"
4. **Connect your GitHub** and select the `medical` repository
5. **Configure the service**:

   **Basic Settings:**
   - **Name**: `telemedicine-platform`
   - **Region**: Choose nearest (e.g., Oregon)
   - **Branch**: `main`

   **Build & Deploy:**
   - **Root Directory**: `backend`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`

   **Advanced:**
   - **Instance Type**: `Free`
   - **Instances**: 1

6. **Click "Create Web Service"**

### Step 3: Wait for Deployment

- Render will automatically build and deploy
- Takes about 2-5 minutes
- You'll see logs in the Render dashboard
- Watch for "Your service is live" message

### Step 4: Access Your App

Once deployed:
- Open the URL provided by Render
- It will look like: `https://telemedicine-platform.onrender.com`
- Login with: john.smith@email.com / patient123

## ✅ What Changed

I restructured the project for easier deployment:

**New Structure:**
```
backend/
├── app.py              # Updated to serve frontend
├── requirements.txt
├── database/
│   └── schema.sql
└── static/             # Frontend files moved here
    ├── index.html
    ├── styles.css
    └── script.js
```

**Changes Made:**
1. ✅ Frontend files moved to `backend/static/`
2. ✅ Updated `app.py` to serve static files
3. ✅ Changed API URL to relative path (`/api`)
4. ✅ Now deploys as a single service

## 🔧 Configuration Details

### Render Build Settings

- **Root Directory**: `backend`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python app.py`
- **Port**: 5000 (automatic)

### Environment Variables (Optional)

If needed, add these in Render dashboard:
- `PORT`: 5000 (Render sets this automatically)
- `FLASK_ENV`: production

## 🌐 Testing After Deployment

1. **Check the backend**:
   - Go to: `https://your-app.onrender.com/api/health`
   - Should see: `{"status":"healthy","message":"Telemedicine API is running"}`

2. **Check the frontend**:
   - Go to: `https://your-app.onrender.com`
   - Should see the login page

3. **Test login**:
   - Email: john.smith@email.com
   - Password: patient123

## ⚠️ Important Notes

### Database Persistence

Render's free tier uses ephemeral storage:
- Database resets on every deploy
- Sample data reloads automatically
- For production, use Render PostgreSQL or external database

### Cold Starts

Free tier has cold starts:
- First load may take 30-60 seconds
- Subsequent loads are faster
- Upgrade to paid tier for always-on

### API URL

The frontend now uses relative URLs:
- Old: `http://localhost:5000/api`
- New: `/api`
- Works on both local and Render

## 🔄 Updating the App

To make changes:

1. **Edit files locally**
2. **Commit and push**:
   ```bash
   git add .
   git commit -m "Your message"
   git push
   ```
3. **Render auto-deploys** on push

## 📊 Monitoring

- Check Render dashboard for logs
- Monitor deployment status
- View metrics (response time, etc.)

## 🆘 Troubleshooting

**Build fails?**
- Check Render logs for errors
- Verify `requirements.txt` is correct
- Ensure Python version is compatible

**Can't access the app?**
- Wait for deployment to complete
- Check service status in dashboard
- Verify the URL is correct

**Database errors?**
- Database auto-creates on first run
- Check logs for schema errors
- Ensure `database/` folder exists

**Frontend not loading?**
- Check `static/` folder exists
- Verify files are in correct location
- Check browser console (F12) for errors

## 🎯 Next Steps

After successful deployment:

1. **Share the URL** with others
2. **Test all features** thoroughly
3. **Monitor usage** in Render dashboard
4. **Consider upgrading** for production use

---

**Your app will be live at**: `https://telemedicine-platform.onrender.com` (or similar URL based on your service name)
