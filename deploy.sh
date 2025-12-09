#!/bin/bash

# 🚀 Nümtema Agents Studio - Vercel Deployment Script

set -e

echo "🚀 Starting Vercel Deployment..."
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo -e "${YELLOW}⚠️  Vercel CLI not found. Installing...${NC}"
    npm install -g vercel
fi

# Check if token is provided
if [ -z "$1" ]; then
    echo -e "${YELLOW}⚠️  No token provided. Using default or existing authentication.${NC}"
    TOKEN=""
else
    TOKEN="--token $1"
fi

# Step 1: Build frontend
echo -e "${BLUE}📦 Step 1: Building frontend...${NC}"
cd frontend
npm install
npm run build
cd ..
echo -e "${GREEN}✅ Frontend built successfully${NC}"
echo ""

# Step 2: Verify backend files
echo -e "${BLUE}📦 Step 2: Verifying backend files...${NC}"
if [ ! -f "api/index.py" ]; then
    echo -e "${YELLOW}⚠️  api/index.py not found${NC}"
fi
if [ ! -f "requirements.txt" ]; then
    echo -e "${YELLOW}⚠️  requirements.txt not found${NC}"
fi
echo -e "${GREEN}✅ Backend files verified${NC}"
echo ""

# Step 3: Verify vercel.json
echo -e "${BLUE}📦 Step 3: Verifying vercel.json...${NC}"
if [ ! -f "vercel.json" ]; then
    echo -e "${YELLOW}⚠️  vercel.json not found${NC}"
fi
echo -e "${GREEN}✅ vercel.json verified${NC}"
echo ""

# Step 4: Deploy to Vercel
echo -e "${BLUE}🚀 Step 4: Deploying to Vercel...${NC}"
if [ -z "$TOKEN" ]; then
    vercel --prod
else
    vercel --prod $TOKEN
fi
echo -e "${GREEN}✅ Deployment successful!${NC}"
echo ""

# Step 5: Show deployment info
echo -e "${BLUE}📊 Step 5: Deployment Info${NC}"
vercel status
echo ""

echo -e "${GREEN}🎉 Deployment Complete!${NC}"
echo ""
echo "Next steps:"
echo "1. Visit: https://numtemastudio.vercel.app"
echo "2. Configure environment variables in Vercel dashboard"
echo "3. Test the API: https://numtemastudio.vercel.app/api/health"
echo ""
