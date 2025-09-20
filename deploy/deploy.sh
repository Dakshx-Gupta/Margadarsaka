#!/bin/bash
# GCP deployment script for Margadarsaka AI Career Advisor
# Usage: ./deploy.sh [PROJECT_ID] [REGION]

set -e

# Configuration
PROJECT_ID=${1:-your-gcp-project-id}
REGION=${2:-us-central1}
SERVICE_NAME="margadarsaka"
IMAGE_NAME="gcr.io/${PROJECT_ID}/${SERVICE_NAME}"

echo "🚀 Deploying Margadarsaka to Google Cloud Platform"
echo "Project: ${PROJECT_ID}"
echo "Region: ${REGION}"
echo "Service: ${SERVICE_NAME}"

# Check if required tools are installed
command -v gcloud >/dev/null 2>&1 || { echo "❌ gcloud CLI is required but not installed." >&2; exit 1; }
command -v docker >/dev/null 2>&1 || { echo "❌ Docker is required but not installed." >&2; exit 1; }

# Set up GCP project
echo "🔧 Setting up GCP project..."
gcloud config set project ${PROJECT_ID}

# Enable required APIs
echo "🔌 Enabling required GCP APIs..."
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable secretmanager.googleapis.com

# Build and push Docker image
echo "🐳 Building Docker image..."
docker build -t ${IMAGE_NAME}:latest .

echo "📤 Pushing image to Google Container Registry..."
docker push ${IMAGE_NAME}:latest

# Create Doppler token secret (if not exists)
echo "🔐 Setting up Doppler token in Secret Manager..."
if ! gcloud secrets describe doppler-token >/dev/null 2>&1; then
    echo "Please enter your Doppler token:"
    read -s DOPPLER_TOKEN
    echo -n "${DOPPLER_TOKEN}" | gcloud secrets create doppler-token --data-file=-
    echo "✅ Doppler token stored in Secret Manager"
else
    echo "ℹ️ Doppler token secret already exists"
fi

# Grant Cloud Run access to the secret
echo "🔑 Granting Cloud Run access to secrets..."
PROJECT_NUMBER=$(gcloud projects describe ${PROJECT_ID} --format="value(projectNumber)")
CLOUD_RUN_SA="${PROJECT_NUMBER}-compute@developer.gserviceaccount.com"

gcloud secrets add-iam-policy-binding doppler-token \
    --member="serviceAccount:${CLOUD_RUN_SA}" \
    --role="roles/secretmanager.secretAccessor"

# Deploy to Cloud Run
echo "🚀 Deploying to Cloud Run..."
sed "s/PROJECT_ID/${PROJECT_ID}/g" deploy/cloud-run.yaml > /tmp/cloud-run-${SERVICE_NAME}.yaml

gcloud run services replace /tmp/cloud-run-${SERVICE_NAME}.yaml \
    --region=${REGION}

# Get service URL
SERVICE_URL=$(gcloud run services describe ${SERVICE_NAME} \
    --region=${REGION} \
    --format="value(status.url)")

echo "🎉 Deployment complete!"
echo "Service URL: ${SERVICE_URL}"
echo "API Endpoint: ${SERVICE_URL}"
echo "Health Check: ${SERVICE_URL}/health"

# Clean up
rm -f /tmp/cloud-run-${SERVICE_NAME}.yaml

echo "📋 Next steps:"
echo "1. Update your Doppler secrets for production environment"
echo "2. Configure your domain (if needed): gcloud run domain-mappings create --service=${SERVICE_NAME} --domain=your-domain.com --region=${REGION}"
echo "3. Set up monitoring and logging in GCP Console"
echo "4. Update your GEMINI_API_KEY in Doppler for production use"