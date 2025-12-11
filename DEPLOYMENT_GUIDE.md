# 🚀 Backend Deployment Guide

This guide will walk you through deploying your Gadgeto e-commerce backend to Render.

## 📋 Prerequisites

Before you begin, make sure you have:
- ✅ A GitHub account
- ✅ Your backend code in a Git repository
- ✅ A Render account (free - sign up at [render.com](https://render.com))
- ✅ Google OAuth Client ID (if using Google login)

---

## 🔧 Step 1: Prepare Your Repository

### 1.1 Initialize Git (if not already done)

```bash
cd D:\e commerce\backend
git init
```

### 1.2 Create .gitignore

Make sure you have a `.gitignore` file to exclude sensitive files:

```
.env
.venv/
__pycache__/
*.pyc
*.db
*.sqlite3
.DS_Store
```

### 1.3 Commit Your Code

```bash
git add .
git commit -m "Initial backend setup for deployment"
```

### 1.4 Push to GitHub

Create a new repository on GitHub, then:

```bash
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```

---

## 🌐 Step 2: Deploy to Render

### 2.1 Sign Up / Log In to Render

1. Go to [https://render.com](https://render.com)
2. Sign up with GitHub (recommended) or email
3. Authorize Render to access your GitHub repositories

### 2.2 Create a New Blueprint

1. Click **"New +"** in the top right
2. Select **"Blueprint"**
3. Connect your GitHub repository
4. Render will automatically detect the `render.yaml` file
5. Click **"Apply"**

### 2.3 Alternative: Manual Web Service Setup

If you prefer manual setup instead of Blueprint:

1. Click **"New +"** → **"Web Service"**
2. Connect your repository
3. Configure:
   - **Name**: `gadgeto-backend`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: Free (or choose paid plan)

---

## 🔐 Step 3: Configure Environment Variables

In your Render dashboard, go to your service → **Environment** tab and add:

| Key | Value | Notes |
|-----|-------|-------|
| `PYTHON_VERSION` | `3.11.0` | Python version |
| `SECRET_KEY` | `your-secret-key-here` | Generate a strong random key |
| `ALGORITHM` | `HS256` | JWT algorithm |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `30` | Token expiration time |
| `GOOGLE_CLIENT_ID` | `your-google-client-id` | From Google Cloud Console |

### Generate a Secret Key

Run this in Python:

```python
import secrets
print(secrets.token_urlsafe(32))
```

Or use this command:

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

---

## 💾 Step 4: Database Configuration (Optional)

### Option A: Use SQLite (Default - Free)

Your app currently uses SQLite (`ecommerce.db`). This works on Render's free tier but **data will be lost on redeploys**.

### Option B: Use PostgreSQL (Recommended for Production)

1. In Render dashboard, click **"New +"** → **"PostgreSQL"**
2. Name it `gadgeto-db`
3. Choose **Free** plan
4. Click **"Create Database"**
5. Copy the **Internal Database URL**
6. Add it as `DATABASE_URL` environment variable in your web service

**Update your code to use PostgreSQL:**

Add to `requirements.txt`:
```
psycopg2-binary==2.9.9
```

Update database connection in your code to use `DATABASE_URL` from environment.

---

## 🔍 Step 5: Verify Deployment

### 5.1 Check Build Logs

1. Go to your service in Render dashboard
2. Click **"Logs"** tab
3. Watch the build process
4. Look for: `Application startup complete`

### 5.2 Test Your API

Once deployed, your service URL will be something like:
```
https://gadgeto-backend.onrender.com
```

Test endpoints:
- **Root**: `https://gadgeto-backend.onrender.com/`
- **Docs**: `https://gadgeto-backend.onrender.com/docs`
- **Google Client ID**: `https://gadgeto-backend.onrender.com/auth/google-client-id`

### 5.3 Test API Endpoints

```bash
# Health check
curl https://gadgeto-backend.onrender.com/

# API documentation
# Open in browser: https://gadgeto-backend.onrender.com/docs
```

---

## 🔄 Step 6: Auto-Deploy on Push

Render automatically deploys when you push to your main branch:

```bash
# Make changes to your code
git add .
git commit -m "Update backend"
git push origin main
```

Render will automatically:
1. Detect the push
2. Build your application
3. Deploy the new version
4. Zero-downtime deployment

---

## 🛠️ Troubleshooting

### Issue: Build Fails

**Solution**: Check the build logs in Render dashboard. Common issues:
- Missing dependencies in `requirements.txt`
- Python version mismatch
- Syntax errors in code

### Issue: Application Crashes on Startup

**Solution**: Check runtime logs. Common issues:
- Missing environment variables
- Database connection errors
- Port binding issues (make sure you use `$PORT`)

### Issue: Database Not Persisting

**Solution**: 
- SQLite doesn't persist on Render's free tier
- Use PostgreSQL for production (see Step 4, Option B)

### Issue: CORS Errors

**Solution**: Update your frontend URL in CORS settings:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://your-frontend-domain.com",
        "http://localhost:3000"  # for local development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 📱 Step 7: Update Frontend & Mobile App

Update your frontend and mobile app to use the new backend URL:

### Frontend (JavaScript)
```javascript
const API_BASE_URL = 'https://gadgeto-backend.onrender.com';
```

### Mobile App (Android)
Update the WebView URL to point to your deployed backend.

---

## 🎯 Production Checklist

Before going live, ensure:

- [ ] All environment variables are set
- [ ] Using PostgreSQL (not SQLite)
- [ ] Secret key is strong and secure
- [ ] CORS is configured for your frontend domain
- [ ] Google OAuth is properly configured
- [ ] API endpoints are tested
- [ ] HTTPS is enabled (automatic on Render)
- [ ] Monitoring is set up
- [ ] Backup strategy is in place

---

## 📊 Monitoring & Maintenance

### View Logs
```
Render Dashboard → Your Service → Logs
```

### Monitor Performance
```
Render Dashboard → Your Service → Metrics
```

### Scale Your Service
```
Render Dashboard → Your Service → Settings → Instance Type
```

---

## 💰 Pricing

### Free Tier Limitations
- ✅ 750 hours/month free
- ⚠️ Spins down after 15 minutes of inactivity
- ⚠️ Cold starts (takes ~30 seconds to wake up)
- ⚠️ Limited resources

### Paid Plans (Starting at $7/month)
- ✅ Always on (no spin down)
- ✅ More resources
- ✅ Better performance
- ✅ Custom domains

---

## 🆘 Support

- **Render Docs**: [https://render.com/docs](https://render.com/docs)
- **Render Community**: [https://community.render.com](https://community.render.com)
- **FastAPI Docs**: [https://fastapi.tiangolo.com](https://fastapi.tiangolo.com)

---

## 🎉 Success!

Your backend is now deployed and accessible worldwide! 🌍

**Next Steps:**
1. Update your frontend to use the new backend URL
2. Test all functionality
3. Monitor logs for any issues
4. Consider upgrading to a paid plan for production use

---

*Last Updated: December 2025*
