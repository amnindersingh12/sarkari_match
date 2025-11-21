# 🚀 Deploying SarkariMatch to Heroku

## Quick Deploy (5 minutes)

### 1. Install Heroku CLI
```bash
# macOS
brew tap heroku/brew && brew install heroku

# Or download from: https://devcenter.heroku.com/articles/heroku-cli
```

### 2. Login to Heroku
```bash
heroku login
```

### 3. Create Heroku App
```bash
# Create app (choose a unique name)
heroku create sarkari-match-demo

# Or let Heroku generate a name
heroku create
```

### 4. Add Buildpack
```bash
heroku buildpacks:set heroku/python
```

### 5. Deploy
```bash
# Push to Heroku
git push heroku main

# Run scraper to generate jobs.json
heroku run python scraper.py

# Open the app
heroku open
```

## Environment Variables (Optional)

If you want to customize scraping:
```bash
heroku config:set LIMIT_JOBS=15
heroku config:set MAX_WORKERS=10
```

## View Logs
```bash
heroku logs --tail
```

## Scale Dynos (if needed)
```bash
# Free tier (default)
heroku ps:scale web=1

# To stop (save dyno hours)
heroku ps:scale web=0
```

## Update Deployment
After making changes:
```bash
git add .
git commit -m "Update: description"
git push heroku main
```

## Troubleshooting

### Jobs not showing?
Run the scraper manually:
```bash
heroku run python scraper.py
```

### Check if app is running:
```bash
heroku ps
```

### View recent logs:
```bash
heroku logs --tail
```

## Important Notes

⚠️ **Free Tier Limitations:**
- Sleeps after 30 minutes of inactivity
- 550-1000 free dyno hours per month
- App will take ~10 seconds to wake up from sleep

💡 **For Demo Purposes:**
- Perfect for Reddit/showcase
- Users can test the live app
- No credit card required for free tier

🔄 **Auto-Scraping:**
- Currently manual (`heroku run python scraper.py`)
- For auto-refresh, consider Heroku Scheduler add-on (free)

## Cost
- **Free tier**: $0/month (perfect for demo)
- **Hobby tier**: $7/month (no sleep, custom domain)

## Demo URL
After deployment, your app will be at:
```
https://your-app-name.herokuapp.com
```

Add this to your Reddit post!
