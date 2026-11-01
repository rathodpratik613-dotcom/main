# Quick Deploy Guide - Render (Free Tier)

## Step 1: Create Render Account
1. Go to https://dashboard.render.com
2. Sign up with your GitHub account (recommended)
3. Verify your email

## Step 2: Connect GitHub Repository
1. Click "New +" button
2. Select "Blueprint" (recommended for easy deployment)
3. Click "Connect GitHub"
4. Authorize Render to access your repositories
5. Find and select `medical` repository
6. Click "Connect"

## Step 3: Deploy with Blueprint
1. After connecting, Render will detect the `render_postgres.yaml` file
2. Review the configuration:
   - PostgreSQL database (free tier)
   - Python backend
   - Static frontend
3. Click "Apply Changes" or "Deploy Blueprint"
4. Wait for deployment to complete (5-10 minutes)

## Step 4: Access Your Website
Once deployment is complete, you'll get URLs like:
- **Frontend**: https://telemedicine-frontend.onrender.com
- **Backend**: https://telemedicine-backend.onrender.com

## Step 5: Test Your Website
1. Open the frontend URL in your browser
2. Login with: john.smith@email.com / patient123
3. Test all features:
   - Home page with Indian context
   - Emergency services
   - Lab tests
   - Video consultation
   - Health blog
   - Medicine search (prices in ₹)

## What Gets Deployed

### Services Created:
1. **telemedicine-postgres** - PostgreSQL database (free)
2. **telemedicine-backend** - Python Flask API (free)
3. **telemedicine-frontend** - Static website (free)

### Features Included:
- ✅ Indian context & branding
- ✅ Emergency services (112, 108, 181, 1098)
- ✅ Lab tests with Indian pricing
- ✅ Video consultation interface
- ✅ Health blog
- ✅ Medicine search in ₹
- ✅ Doctor consultations
- ✅ Medicine pharmacy search
- ✅ Follow-up management

## Troubleshooting

### Deployment Fails
- Check the Render dashboard logs
- Ensure GitHub repository is public or connected properly
- Wait a few minutes and try again

### Website Not Loading
- Check if all services are running in Render dashboard
- Wait 5-10 minutes for services to fully start
- Check logs for errors

### Database Issues
- The setup script automatically initializes the database
- Check backend logs for database connection errors
- Ensure PostgreSQL service is running

## Cost
- **FREE** - All services use Render's free tier
- No credit card required
- 750 hours of free service per month

## Next Steps
After deployment:
1. Share your website URL with others
2. Customize the content as needed
3. Add more doctors, medicines, or features
4. Consider upgrading to paid tiers for better performance

## Support
- Render Docs: https://render.com/docs
- GitHub Repo: https://github.com/rathodpratik613-dotcom/medical
