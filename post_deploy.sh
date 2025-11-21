#!/bin/bash
# This script runs on Heroku after deployment to generate jobs.json

echo "🚀 Running post-deployment scraper..."
python scraper.py
echo "✅ Jobs data generated!"
