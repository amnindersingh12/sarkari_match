#!/bin/bash

# SarkariMatch - Git Setup Script
# This script initializes the git repository and creates the initial commit

echo "🚀 Setting up Git repository for SarkariMatch..."

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Error: Git is not installed. Please install git first."
    exit 1
fi

# Initialize git repository
echo "📦 Initializing git repository..."
git init

# Add all files
echo "➕ Adding files to git..."
git add .

# Create initial commit
echo "💾 Creating initial commit..."
git commit -m "feat(core): initial commit of scraping engine and matching logic

- Add deep scraper for FreeJobAlert with vacancy and link extraction
- Implement age-based eligibility matching with category relaxations
- Create dashboard UI with job cards and action buttons
- Add parallel scraping for improved performance
- Include comprehensive documentation (README, CONTRIBUTING)"

# Create dev branch
echo "🌿 Creating dev branch..."
git checkout -b dev

# Switch back to main
git checkout main

echo ""
echo "✅ Git setup complete!"
echo ""
echo "📋 Summary:"
echo "   - Repository initialized"
echo "   - Initial commit created on 'main' branch"
echo "   - 'dev' branch created"
echo ""
echo "🎯 Next steps:"
echo "   1. Create a repository on GitHub"
echo "   2. Add remote: git remote add origin <your-repo-url>"
echo "   3. Push to GitHub: git push -u origin main"
echo "   4. Push dev branch: git push -u origin dev"
echo ""
echo "Happy coding! 🚀"
