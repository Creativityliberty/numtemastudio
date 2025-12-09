#!/bin/bash

# 🚀 Nümtema Agents Studio - Vercel Deployment Script (Automated)

set -e

echo "🚀 Starting Vercel Deployment..."
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Your Vercel token
VERCEL_TOKEN="KLhneBoEe2dZI55hkFv4qrHa"

# Export token
export VERCEL_TOKEN

# Step 1: Check if Vercel CLI is installed
echo -e "${BLUE}📦 Step 1: Checking Vercel CLI...${NC}"
if ! command -v vercel &> /dev/null; then
    echo -e "${YELLOW}⚠️  Vercel CLI not found. Installing...${NC}"
    npm install -g vercel
fi
echo -e "${GREEN}✅ Vercel CLI ready${NC}"
echo ""

# Step 2: Build frontend
echo -e "${BLUE}📦 Step 2: Building frontend...${NC}"
cd frontend
npm install
npm run build
cd ..
echo -e "${GREEN}✅ Frontend built successfully${NC}"
echo ""

# Step 3: Deploy to Vercel
echo -e "${BLUE}🚀 Step 3: Deploying to Vercel...${NC}"
echo "Using token: ${VERCEL_TOKEN:0:10}..."
echo ""

# Deploy with auto-confirmation
vercel --prod --confirm --token "$VERCEL_TOKEN"

echo ""
echo -e "${GREEN}✅ Deployment successful!${NC}"
echo ""

# Step 4: Show deployment info
echo -e "${BLUE}📊 Step 4: Deployment Info${NC}"
vercel status --token "$VERCEL_TOKEN"
echo ""

echo -e "${GREEN}🎉 Deployment Complete!${NC}"
echo ""
echo "Next steps:"
echo "1. Visit: https://numtemastudio.vercel.app"
echo "2. Configure environment variables in Vercel dashboard"
echo "3. Test the API: https://numtemastudio.vercel.app/api/health"
echo ""
