# Render Deployment Guide for Telemedicine Platform

## Quick Deploy to Render

### Option 1: Deploy Backend Only (Recommended)

#### Step 1: Prepare Repository
The repository is already updated with necessary files:
- `Procfile` - Tells Render how to start the app
- `requirements.txt` - Python dependencies
- `app.py` - Flask application configured for production

#### Step 2: Deploy Backend on Render

1. Go to [render.com](https://render.com) and sign up/login
2. Click "New +" button
3. Select "Web Service"
4. Connect your GitHub repository: `rathodpratik613-dotcom/medical`
5. Configure the service:
   - **Name**: telemedicine-backend
   - **Runtime**: Python 3
   - **Build Command**: `cd backend && pip install -r requirements.txt`
   - **Start Command**: `cd backend && python app.py`
   - **Root Directory**: Leave empty (or set to `backend`)
6. Click "Create Web Service"

#### Step 3: Update Frontend API URL

After backend is deployed:
1. Get your backend URL from Render (e.g., `https://telemedicine-backend.onrender.com`)
2. Open `frontend/script.js`
3. Update line 2:
   ```javascript
   const API_URL = 'https://telemedicine-backend.onrender.com/api';
   ```
4. Commit and push changes

#### Step 4: Deploy Frontend (Optional)

For the frontend, you have several options:

**Option A: Netlify (Easiest)**
1. Go to [netlify.com](https://netlify.com)
2. Drag and drop the `frontend` folder
3. After deployment, update the API URL in `script.js`

**Option B: GitHub Pages**
1. Go to your repository settings on GitHub
2. Enable GitHub Pages
3. Select source: `main` branch, `/frontend` folder
4. Your site will be at: `https://rathodpratik613-dotcom.github.io/medical/`

**Option C: Vercel**
1. Go to [vercel.com](https://vercel.com)
2. Import your repository
3. Set root directory to `frontend`
4. Deploy

### Option 2: Using render.yaml (Advanced)

1. The `render.yaml` file is already in your repository
2. On Render, create a new service and select "Deploy from render.yaml"
3. This will automatically configure both backend and frontend

## Important Notes

### Backend Configuration
- The backend is now configured to use `host='0.0.0.0'` for Render compatibility
- Port is set from environment variable (Render provides PORT automatically)
- Debug mode is disabled in production

### Frontend Configuration
- Update `API_URL` in `frontend/script.js` to match your deployed backend URL
- For local development, keep it as `http://localhost:5000/api`

### Database
- The SQLite database will be created in Render's ephemeral storage
- **Important**: Render's free tier storage is ephemeral - data will be lost on redeploy
- For production, consider using Render PostgreSQL or external database

### Free Tier Limitations
- Render free tier spins down after 15 minutes of inactivity
- First request after spin-down may take up to 50 seconds
- No persistent storage on free tier

## Render Links

After deployment, your URLs will be:
- **Backend**: `https://telemedicine-backend.onrender.com`
- **Frontend**: Depends on where you deploy it (Netlify, Vercel, GitHub Pages)

## Testing Your Deployment

1. Test backend health:
   ```
   curl https://telemedicine-backend.onrender.com/api/health
   ```

2. Test doctors endpoint:
   ```
   curl https://telemedicine-backend.onrender.com/api/doctors
   ```

3. Open your frontend URL in browser
4. Test login and all features

## Troubleshooting

### Backend fails to start
- Check Render logs for errors
- Ensure `requirements.txt` is in the correct location
- Verify the start command path is correct

### Frontend can't connect to backend
- Verify CORS is enabled in `app.py` (it is)
- Check that API_URL in `script.js` matches backend URL
- Ensure backend is running (check Render dashboard)

### Database errors on Render
- Free tier has ephemeral storage - database resets on redeploy
- Consider upgrading to paid tier or using external database
- For persistent storage, use Render PostgreSQL

## Next Steps

1. Deploy backend to Render
2. Get the backend URL
3. Update frontend API_URL
4. Deploy frontend to Netlify/Vercel/GitHub Pages
5. Test the complete application

## Support

For Render-specific issues:
- [Render Documentation](https://render.com/docs)
- [Render Community](https://community.render.com)
