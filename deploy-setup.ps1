# Deployment Setup Script for Gadgeto Backend
# GitHub Username: lernermandy

Write-Host "🚀 Starting Backend Deployment Setup..." -ForegroundColor Cyan
Write-Host ""

# Check if git is installed
Write-Host "Checking Git installation..." -ForegroundColor Yellow
try {
    git --version
    Write-Host "✅ Git is installed" -ForegroundColor Green
} catch {
    Write-Host "❌ Git is not installed. Please install Git first." -ForegroundColor Red
    Write-Host "Download from: https://git-scm.com/download/win" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "📝 Repository Information:" -ForegroundColor Cyan
Write-Host "GitHub Username: lernermandy" -ForegroundColor White
Write-Host ""

# Prompt for repository name
$repoName = Read-Host "Enter your repository name (e.g., gadgeto-backend)"

if ([string]::IsNullOrWhiteSpace($repoName)) {
    Write-Host "❌ Repository name cannot be empty" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "📦 Repository URL will be:" -ForegroundColor Yellow
Write-Host "https://github.com/lernermandy/$repoName" -ForegroundColor White
Write-Host ""

# Confirm before proceeding
$confirm = Read-Host "Continue? (y/n)"
if ($confirm -ne 'y' -and $confirm -ne 'Y') {
    Write-Host "❌ Setup cancelled" -ForegroundColor Red
    exit 0
}

Write-Host ""
Write-Host "🔧 Initializing Git repository..." -ForegroundColor Yellow

# Initialize git if not already initialized
if (-not (Test-Path ".git")) {
    git init
    Write-Host "✅ Git repository initialized" -ForegroundColor Green
} else {
    Write-Host "ℹ️  Git repository already exists" -ForegroundColor Blue
}

# Add all files
Write-Host ""
Write-Host "📁 Adding files to Git..." -ForegroundColor Yellow
git add .

# Create initial commit
Write-Host ""
Write-Host "💾 Creating initial commit..." -ForegroundColor Yellow
git commit -m "Initial commit: Gadgeto e-commerce backend ready for deployment"

# Rename branch to main if needed
Write-Host ""
Write-Host "🌿 Setting up main branch..." -ForegroundColor Yellow
git branch -M main

# Add remote
Write-Host ""
Write-Host "🔗 Adding GitHub remote..." -ForegroundColor Yellow
$remoteUrl = "https://github.com/lernermandy/$repoName.git"

# Check if remote already exists
$existingRemote = git remote get-url origin 2>$null
if ($existingRemote) {
    Write-Host "ℹ️  Remote 'origin' already exists: $existingRemote" -ForegroundColor Blue
    $updateRemote = Read-Host "Update remote URL? (y/n)"
    if ($updateRemote -eq 'y' -or $updateRemote -eq 'Y') {
        git remote set-url origin $remoteUrl
        Write-Host "✅ Remote URL updated" -ForegroundColor Green
    }
} else {
    git remote add origin $remoteUrl
    Write-Host "✅ Remote added: $remoteUrl" -ForegroundColor Green
}

Write-Host ""
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host "✅ Git Setup Complete!" -ForegroundColor Green
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host ""

Write-Host "📋 Next Steps:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Create a new repository on GitHub:" -ForegroundColor White
Write-Host "   👉 Go to: https://github.com/new" -ForegroundColor Cyan
Write-Host "   - Repository name: $repoName" -ForegroundColor White
Write-Host "   - Make it Public or Private" -ForegroundColor White
Write-Host "   - DON'T initialize with README, .gitignore, or license" -ForegroundColor Red
Write-Host ""

Write-Host "2. Push your code to GitHub:" -ForegroundColor White
Write-Host "   Run this command:" -ForegroundColor White
Write-Host "   git push -u origin main" -ForegroundColor Cyan
Write-Host ""

Write-Host "3. Deploy on Render:" -ForegroundColor White
Write-Host "   👉 Go to: https://render.com" -ForegroundColor Cyan
Write-Host "   - Sign up/Login with GitHub" -ForegroundColor White
Write-Host "   - Click 'New +' → 'Blueprint'" -ForegroundColor White
Write-Host "   - Select repository: lernermandy/$repoName" -ForegroundColor White
Write-Host "   - Click 'Apply'" -ForegroundColor White
Write-Host ""

Write-Host "4. Set Environment Variables in Render:" -ForegroundColor White
Write-Host "   - SECRET_KEY (generate with Python command below)" -ForegroundColor White
Write-Host "   - GOOGLE_CLIENT_ID (from Google Cloud Console)" -ForegroundColor White
Write-Host ""

Write-Host "🔑 Generate SECRET_KEY:" -ForegroundColor Yellow
Write-Host "python -c `"import secrets; print(secrets.token_urlsafe(32))`"" -ForegroundColor Cyan
Write-Host ""

Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host "📚 For detailed instructions, see:" -ForegroundColor Yellow
Write-Host "   - DEPLOYMENT_GUIDE.md (comprehensive guide)" -ForegroundColor White
Write-Host "   - DEPLOYMENT_CHECKLIST.md (quick reference)" -ForegroundColor White
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host ""

Write-Host "🎉 Ready to deploy! Good luck!" -ForegroundColor Green
