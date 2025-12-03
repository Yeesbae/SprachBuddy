#!/bin/bash
# -------------------------------
# Deploy SprachBuddy Bot Script
# Bash / Terminal version
# -------------------------------

set -e  # Exit on error

# Load .env file
if [ -f ".env" ]; then
  export $(grep -v '^#' .env | xargs)
else
  echo ".env file not found!"
  exit 1
fi

# Ensure required env vars exist
if [ -z "$PROJECT_ID" ] || [ -z "$BOT_TOKEN" ]; then
  echo "PROJECT_ID or BOT_TOKEN not set in .env!"
  exit 1
fi

SERVICE_NAME="sprachbuddy"
REGION="asia-southeast1"
IMAGE_NAME="$SERVICE_NAME:latest"

# Build Docker image
echo "Building Docker image..."
docker build -t $IMAGE_NAME .

# Tag Docker image for GCR
echo "Tagging Docker image for GCR..."
docker tag $IMAGE_NAME gcr.io/$PROJECT_ID/$IMAGE_NAME

# Push Docker image to GCR
echo "Pushing Docker image to GCR..."
docker push gcr.io/$PROJECT_ID/$IMAGE_NAME

# Deploy to Cloud Run
echo "Deploying to Cloud Run..."
gcloud run deploy $SERVICE_NAME \
  --image gcr.io/$PROJECT_ID/$IMAGE_NAME \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --port 8080 \
  --set-env-vars BOT_TOKEN=$BOT_TOKEN

# Get the deployed service URL
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME \
  --platform managed \
  --region $REGION \
  --format "value(status.url)")

echo "Cloud Run service URL: $SERVICE_URL"

# Set Telegram webhook
echo "Setting Telegram webhook..."
TELEGRAM_API="https://api.telegram.org/bot$BOT_TOKEN/setWebhook"
WEBHOOK_URL="$SERVICE_URL/telegram"

curl -X POST "$TELEGRAM_API" -d "url=$WEBHOOK_URL"

echo "Deployment and webhook setup complete!"
