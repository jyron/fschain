# Deployment Guide for Financial Index API

Your FastAPI application is now ready to deploy! Here are several hosting options, from easiest to more advanced:

## Option 1: Railway (Recommended - Easiest)

Railway offers simple deployment from GitHub with automatic builds.

### Steps:

1. **Push to GitHub** (if not already):

   ```bash
   git add .
   git commit -m "Add deployment files"
   git push origin main
   ```

2. **Deploy on Railway**:
   - Go to [railway.app](https://railway.app)
   - Sign up/login with GitHub
   - Click "Deploy from GitHub repo"
   - Select your repository
   - Railway will automatically detect the Dockerfile and deploy
   - Your app will be live at: `https://your-app-name.railway.app`

**Cost**: Free tier available, ~$5/month for basic usage

## Option 2: Render (Also Easy)

Similar to Railway, with generous free tier.

### Steps:

1. Go to [render.com](https://render.com)
2. Connect GitHub account
3. Click "New +" → "Web Service"
4. Select your repository
5. Use these settings:
   - **Environment**: Docker
   - **Build Command**: `docker build -t app .`
   - **Start Command**: `docker run -p 10000:8000 app`

**Cost**: Free tier available (with some limitations)

## Option 3: DigitalOcean App Platform

### Steps:

1. Go to [cloud.digitalocean.com](https://cloud.digitalocean.com)
2. Create account, go to "Apps"
3. Create app from GitHub repository
4. Select your repo and branch
5. DigitalOcean will auto-detect the Dockerfile

**Cost**: ~$5/month minimum

## Option 4: Google Cloud Run (Pay-per-use)

Most cost-effective for low traffic.

### Steps:

1. Install [Google Cloud CLI](https://cloud.google.com/sdk/docs/install)
2. Build and deploy:
   ```bash
   gcloud auth login
   gcloud config set project YOUR_PROJECT_ID
   gcloud run deploy financial-index-api --source . --platform managed --region us-central1 --allow-unauthenticated
   ```

**Cost**: Pay only when used, typically $0-2/month for small apps

## Option 5: Local Testing

Test locally before deploying:

```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
cd index_api
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Visit: http://localhost:8000

## What Your API Provides

Once deployed, your API will have these endpoints:

- `/` - Landing page with navigation
- `/plot/{ticker}` - Interactive radar chart for any stock ticker
- `/scatter` - Multi-company dashboard
- `/available-tickers` - List of all available stock tickers
- `/index/f/{ticker}` - JSON data for specific ticker
- `/index/f/` - JSON data for all companies

## Next Steps After Deployment

1. **Custom Domain**: Most platforms allow you to add a custom domain
2. **HTTPS**: All these platforms provide HTTPS automatically
3. **Environment Variables**: If you need API keys later, all platforms support them
4. **Monitoring**: Most platforms provide basic monitoring and logs

## Recommended: Start with Railway

Railway is the easiest option - just connect your GitHub repo and it deploys automatically. The free tier is generous for getting started.
