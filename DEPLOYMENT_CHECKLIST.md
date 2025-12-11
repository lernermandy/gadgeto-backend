# 🚀 Quick Deployment Checklist

Use this checklist to deploy your backend quickly.

## ☑️ Pre-Deployment

- [ ] Code is working locally
- [ ] All dependencies in `requirements.txt`
- [ ] `.gitignore` file created
- [ ] `.env` file is NOT committed (check .gitignore)
- [ ] `render.yaml` is configured

## ☑️ Git Setup

```bash
# Initialize git (if needed)
git init

# Add all files
git add .

# Commit
git commit -m "Ready for deployment"

# Create GitHub repo and push
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git branch -M main
git push -u origin main
```

## ☑️ Render Setup

1. [ ] Go to [render.com](https://render.com)
2. [ ] Sign up/Login with GitHub
3. [ ] Click "New +" → "Blueprint"
4. [ ] Select your repository
5. [ ] Click "Apply"

## ☑️ Environment Variables

Add these in Render Dashboard → Environment:

```
SECRET_KEY = <generate-random-key>
ALGORITHM = HS256
ACCESS_TOKEN_EXPIRE_MINUTES = 30
GOOGLE_CLIENT_ID = <your-google-client-id>
```

**Generate SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

## ☑️ Post-Deployment

- [ ] Check build logs (should see "Application startup complete")
- [ ] Visit your service URL
- [ ] Test `/docs` endpoint
- [ ] Test API endpoints
- [ ] Update frontend with new backend URL

## 📝 Your Service URLs

After deployment, note these:

- **Service URL**: `https://your-service-name.onrender.com`
- **API Docs**: `https://your-service-name.onrender.com/docs`
- **Health Check**: `https://your-service-name.onrender.com/`

## ⚠️ Important Notes

- **Free Tier**: Service spins down after 15 min of inactivity
- **Cold Start**: First request after spin down takes ~30 seconds
- **Database**: SQLite data is lost on redeploys (use PostgreSQL for production)
- **Auto-Deploy**: Enabled by default on git push

## 🔄 Update Deployment

```bash
# Make changes
git add .
git commit -m "Update description"
git push origin main
# Render auto-deploys!
```

## 🆘 Troubleshooting

**Build fails?**
→ Check Render logs for errors

**App crashes?**
→ Check environment variables are set

**CORS errors?**
→ Update CORS origins in `main.py`

**Database not persisting?**
→ Switch to PostgreSQL (see DEPLOYMENT_GUIDE.md)

---

✅ **Done?** Your backend is live! Update your frontend and mobile app URLs.
