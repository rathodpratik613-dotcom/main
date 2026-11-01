# Deployment Guide - GitHub & Render

This guide will help you deploy the TeleMedicine Platform to GitHub and Render.

## Part 1: Upload to GitHub

### Step 1: Create GitHub Repository

1. Go to [GitHub](https://github.com) and sign in
2. Click the "+" icon in the top right corner
3. Select "New repository"
4. Enter repository name: `telemedicine-platform`
5. Choose "Public" or "Private" (Public recommended for free Render deployment)
6. Click "Create repository"

### Step 2: Initialize Git and Push

```bash
# Navigate to your project directory
cd C:\Users\ratho\medical-main\medical-main

# Add all files to git
git add .

# Commit changes
git commit -m "Initial commit - TeleMedicine Platform with MySQL"

# Add remote repository (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/telemedicine-platform.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Step 3: Verify on GitHub

1. Go to your GitHub repository
2. You should see all the files uploaded
3. The repository is now ready for Render deployment

---

## Part 2: Deploy to Render

### Step 1: Create Render Account

1. Go to [Render](https://render.com)
2. Click "Sign Up"
3. Sign up with GitHub (recommended)
4. Authorize Render to access your GitHub repositories

### Step 2: Deploy Web Service

1. After signing in, click "New +"
2. Select "Web Service"
3. Select your `telemedicine-platform` repository from GitHub
4. Configure the service:

**Build & Deploy Settings:**
- **Name:** telemedicine-platform
- **Region:** Select region closest to you (e.g., Oregon, Frankfurt)
- **Branch:** main
- **Runtime:** Python 3
- **Build Command:** `cd backend && pip install -r requirements.txt`
- **Start Command:** `cd backend && python app.py`

**Environment Variables:**
- **PORT:** `5000`
- **DB_HOST:** (Leave empty - will be auto-filled by Render)
- **DB_USER:** (Leave empty - will be auto-filled by Render)
- **DB_PASSWORD:** (Leave empty - will be auto-filled by Render)
- **DB_NAME:** `telemedicine_db`
- **DB_PORT:** `3306`

5. Click "Advanced Settings"
6. Add environment variables from above
7. Click "Create Web Service"

### Step 3: Deploy MySQL Database

1. Go to your Render dashboard
2. Click "New +"
3. Select "Database"
4. Configure the database:

**Database Settings:**
- **Name:** telemedicine-db
- **Database:** MySQL
- **Version:** MySQL 8
- **Region:** Same as your web service
- **Plan:** Free

5. Click "Create Database"

### Step 4: Connect Database to Web Service

1. Go to your web service dashboard
2. Click "Environment"
3. Add the following environment variables (Render will auto-fill these):

```bash
DB_HOST=your-mysql-host.render.com
DB_USER=render_user
DB_PASSWORD=your_database_password
DB_NAME=telemedicine_db
DB_PORT=3306
```

4. Copy these values from your MySQL database dashboard
5. Click "Save Changes"

### Step 5: Setup Database on Render

1. Go to your MySQL database dashboard on Render
2. Click "Connect" to get connection details
3. Use the MySQL Workbench or terminal to connect:
```bash
mysql -h <host> -u <user> -p
```
4. Run the setup script to create tables and insert data:
```bash
# In Render shell or locally with Render credentials
cd backend
python setup_render.py
```

Or use the SQL schema:
```bash
# Run the SQL schema file
mysql -h <host> -u <user> -p telemedicine_db < database/mysql_schema.sql
```

### Step 6: Redeploy Web Service

1. Go to your web service dashboard
2. Click "Manual Deploy"
3. Select "Clear build cache & deploy"
4. Wait for deployment to complete

### Step 7: Access Your Application

1. Once deployed, Render will provide a URL like:
   `https://telemedicine-platform.onrender.com`
2. Open this URL in your browser
3. Test the application with sample credentials

---

## Sample Login Credentials

| Email | Password |
|-------|----------|
| john.smith@email.com | patient123 |
| jane.doe@email.com | patient123 |
| robert.johnson@email.com | patient123 |
| emily.brown@email.com | patient123 |
| michael.davis@email.com | patient123 |

---

## Troubleshooting

### Issue: Database Connection Failed

**Solution:**
1. Verify environment variables in web service
2. Check MySQL database is running
3. Ensure database tables are created
4. Check Render logs for specific error messages

### Issue: Frontend Not Connecting to Backend

**Solution:**
1. The frontend uses relative paths in production
2. Verify CORS is enabled in backend (it is)
3. Check browser console for errors
4. Ensure backend is running

### Issue: Deployment Fails

**Solution:**
1. Check build logs in Render dashboard
2. Verify all dependencies are in requirements.txt
3. Ensure Python version is compatible
4. Check for syntax errors in code

### Issue: Free Tier Limitations

**Solution:**
- Render free tier spins down after 15 minutes of inactivity
- First request may take 30-60 seconds to wake up
- Database has 90MB limit on free tier
- Consider upgrading for production use

---

## Updating the Application

### Making Changes Locally:

```bash
# Make changes to your code
# Test locally

# Commit and push to GitHub
git add .
git commit -m "Description of changes"
git push origin main
```

### Deploying to Render:

Render will automatically detect changes from GitHub and redeploy:
1. Push changes to GitHub
2. Render will automatically start a new deployment
3. Monitor deployment in Render dashboard
4. Access updated application at your Render URL

---

## Security Notes

For production deployment, consider:

1. **Environment Variables:** Never commit `.env` file to GitHub
2. **Password Hashing:** Implement bcrypt for password hashing
3. **HTTPS:** Render provides SSL certificates automatically
4. **Rate Limiting:** Add rate limiting to API endpoints
5. **Input Validation:** Sanitize all user inputs
6. **Authentication:** Implement JWT-based authentication
7. **Database Backups:** Render handles backups automatically

---

## Monitoring

### Render Dashboard Features:

- **Logs:** View real-time application logs
- **Metrics:** Monitor CPU, memory, and response times
- **Deploys:** Track deployment history
- **Database:** Monitor database performance
- **Alerts:** Set up alerts for downtime

---

## Cost Estimate

**Free Tier (Render):**
- Web Service: Free (with spin-down)
- MySQL Database: Free (90MB limit)
- Total: $0/month

**Starter Tier (if needed):**
- Web Service: $7/month
- MySQL Database: $7/month
- Total: $14/month

---

## Support

For issues:
- Render Documentation: https://render.com/docs
- GitHub Issues: Check repository issues
- Email Support: support@render.com

---

## Next Steps

After successful deployment:

1. Test all features thoroughly
2. Set up monitoring and alerts
3. Configure custom domain (optional)
4. Set up CI/CD pipeline (optional)
5. Implement additional security measures
6. Scale as needed based on traffic
