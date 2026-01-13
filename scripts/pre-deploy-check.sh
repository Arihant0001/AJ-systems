#!/bin/bash
# Quick deployment test script
# Run this locally before pushing to production

set -e

echo "🔍 Pre-deployment verification..."
echo "=================================="

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

check_file() {
    if [ -f "$1" ]; then
        echo -e "${GREEN}✓${NC} $1 exists"
        return 0
    else
        echo -e "${RED}✗${NC} $1 missing"
        return 1
    fi
}

check_env_var() {
    if grep -q "^$1=" backend/.env 2>/dev/null; then
        echo -e "${GREEN}✓${NC} $1 configured in .env"
        return 0
    else
        echo -e "${RED}✗${NC} $1 missing from .env"
        return 1
    fi
}

echo ""
echo "📁 Backend Files..."
check_file "backend/app/main.py"
check_file "backend/app/core/config.py"
check_file "backend/app/api/routes/auth.py"
check_file "backend/requirements.txt"
check_file "backend/alembic.ini"

echo ""
echo "📁 Frontend Files..."
check_file "frontend/package.json"
check_file "frontend/vite.config.ts"
check_file "frontend/src/main.tsx"
check_file "frontend/index.html"
check_file "frontend/public/manifest.json"
check_file "frontend/public/sw.js"

echo ""
echo "🔐 Environment Variables (backend/.env)..."
check_env_var "ENV"
check_env_var "DATABASE_URL"
check_env_var "JWT_SECRET"
check_env_var "CORS_ORIGINS"

echo ""
echo "✅ Pre-deployment checks complete!"
echo ""
echo "Next steps:"
echo "1. Commit changes: git add . && git commit -m 'chore: prepare for deployment'"
echo "2. Push to GitHub: git push origin main"
echo "3. Follow DEPLOYMENT_GUIDE.md for Supabase → Render → Vercel setup"
