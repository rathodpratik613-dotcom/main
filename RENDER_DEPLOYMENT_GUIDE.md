# Render Deployment Guide

This guide will help you deploy the Telemedicine Platform to Render with MySQL database.

## Prerequisites

- A Render account (free tier available)
- GitHub account with the project repository
- The project must be pushed to GitHub (already done: https://github.com/rathodpratik613-dotcom/medical)

## Step 1: Connect GitHub to Render

1. Go to [https://dashboard.render.com](https://dashboard.render.com)
2. Sign up or log in
3. Click on "New +"
4. Select "Web Service"
5. Click "Connect GitHub" and authorize Render to access your repositories
6. Find and select the `medical` repository

## Step 2: Deploy with render.yaml

The project includes a `render.yaml` configuration file that defines all services. This is the recommended method:

1. In Render dashboard, click "New +"
2. Select "Blueprint" (this will use the render.yaml file)
3. Connect your GitHub repository
4. Render will read the `render.yaml` file and create:
   - **telemedicine-mysql**: MySQL database service
   - **telemedicine-backend**: Python Flask backend
   - **telemedicine-frontend**: Static frontend site

5. Click "Apply Changes" to start deployment

## What the render.yaml Configures

### MySQL Database Service
- **Name**: telemedicine-mysql
- **Type**: Private Service (pserv)
- **Plan**: Free tier
- **Features**: 
  - Automatic database creation
  - Secure internal networking
  - Environment variables for connection details

### Backend Service
- **Name**: telemedicine-backend
- **Type**: Web Service
- **Runtime**: Python
- **Plan**: Free tier
- **Build**: Installs dependencies from requirements.txt
- **Start**: Runs setup_database.py (to initialize DB) then app.py
- **Environment Variables**: Automatically configured from MySQL service

### Frontend Service
- **Name**: telemedicine-frontend
- **Type**: Static Site
- **Plan**: Free tier
- **Publish Directory**: frontend/
- **Environment Variable**: API_URL set to backend URL

## Step 3: Monitor Deployment

1. Go to the Render dashboard
2. You'll see three services being created:
   - telemedicine-mysql (will finish first)
   - telemedicine-backend (depends on MySQL)
   - telemedicine-frontend (will finish quickly)

3. Click on each service to view logs and status

## Step 4: Access Your Application

Once deployment is complete:

- **Frontend URL**: `https://telemedicine-frontend.onrender.com`
- **Backend API**: `https://telemedicine-backend.onrender.com/api`
- **Backend Health Check**: `https://telemedicine-backend.onrender.com/api/health`

## Step 5: Test the Application

1. Open the frontend URL in your browser
2. Use these test credentials:
   - Email: john.smith@email.com
   - Password: patient123

3. Test features:
   - Login with patient credentials
   - Browse doctors
   - Request a consultation
   - Search for medicines
   - View pharmacies

## Manual Deployment (Alternative)

If you prefer to deploy services manually instead of using render.yaml:

### Deploy MySQL Database

1. Click "New +"
2. Select "PostgreSQL" (Render's free tier only supports PostgreSQL, not MySQL)
3. **Important**: Since Render free tier doesn't support MySQL, you have two options:
   - **Option A**: Use PostgreSQL instead (requires code changes)
   - **Option B**: Use a paid MySQL service on Render
   - **Option C**: Use an external MySQL provider (Planetscale, Railway, etc.)

### Deploy Backend

1. Click "New +"
2. Select "Web Service"
3. Connect GitHub repository
4. Configure:
   - Name: telemedicine-backend
   - Runtime: Python
   - Build Command: `cd backend && pip install -r requirements.txt`
   - Start Command: `cd backend && python app.py`
5. Add Environment Variables:
   - DB_HOST (from MySQL service)
   - DB_USER (from MySQL service)
   - DB_PASSWORD (from MySQL service)
   - DB_NAME: telemedicine_db
   - DB_PORT: 3306
6. Click "Deploy"

### Deploy Frontend

1. Click "New +"
2. Select "Static Site"
3. Connect GitHub repository
4. Configure:
   - Name: telemedicine-frontend
   - Publish Directory: frontend
   - Build Command: (leave empty)
5. Add Environment Variable:
   - API_URL: https://telemedicine-backend.onrender.com/api
6. Click "Deploy"

## Important Note on Render's Free Tier

**Render's free tier only supports PostgreSQL, not MySQL.** To use MySQL:

1. **Use Render's paid MySQL plan** ($7/month minimum)
2. **Switch to PostgreSQL** (requires code changes):
   - Change mysql-connector-python to psycopg2
   - Update SQL syntax to PostgreSQL
   - Modify setup_database.py for PostgreSQL
3. **Use external MySQL** (Planetscale free tier, Railway, etc.):
   - Create MySQL database on external service
   - Update render.yaml with external connection details
   - Add connection URL as environment variable

## Troubleshooting

### Backend Deployment Fails

**Issue**: Cannot connect to database
- **Solution**: Ensure MySQL service is deployed first
- Check environment variables are correctly linked
- View backend logs for specific error messages

### Frontend Cannot Connect to Backend

**Issue**: CORS errors or 404s
- **Solution**: 
  - Verify backend is running and healthy
  - Check API_URL environment variable in frontend
  - Ensure backend has CORS enabled (it does in app.py)

### Database Not Initializing

**Issue**: setup_database.py fails
- **Solution**:
  - Check MySQL connection credentials
  - Verify database service is running
  - View logs for specific SQL errors

### Changes Not Reflecting

**Issue**: Deployed app shows old code
- **Solution**:
  - Push changes to GitHub
  - Render auto-deploys on push to main branch
  - Or manually trigger redeploy in dashboard

## Scaling and Production

For production use:

1. **Upgrade Plans**:
   - Move from free to paid tiers for better performance
   - Add more instances for backend scaling
   - Use Render's Redis for caching

2. **Security**:
   - Add SSL/TLS (Render provides automatically)
   - Implement proper authentication (JWT)
   - Add rate limiting
   - Use environment variables for secrets

3. **Monitoring**:
   - Enable Render's logging
   - Set up alerts for errors
   - Monitor database performance

4. **Custom Domain**:
   - Add custom domain in Render dashboard
   - Configure DNS records
   - Enable HTTPS (automatic with Render)

## Support

- Render Documentation: https://render.com/docs
- GitHub Repository: https://github.com/rathodpratik613-dotcom/medical
- Issue Tracker: Create issues in the GitHub repository
