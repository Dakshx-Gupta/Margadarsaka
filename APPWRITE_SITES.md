# Appwrite Sites Integration for Margadarsaka

This guide explains how to deploy Margadarsaka to Appwrite Sites, taking advantage of both static hosting and server-side rendering options.

## Overview

Appwrite Sites provides a fast, scalable, and secure way to deploy web apps directly from source control. Margadarsaka can benefit from this by:

1. Hosting a static marketing site with documentation
2. Deploying the Streamlit application as a container service

## Prerequisites

- Appwrite account with access to the Cloud console or a self-hosted instance
- Appwrite CLI installed (`npm install -g appwrite-cli`)
- Node.js and npm
- Docker (for containerizing the Streamlit app)

## Configuration

We've provided several files to help you deploy to Appwrite Sites:

- `docs/appwrite/sites.md` - Detailed documentation about Appwrite Sites features
- `src/margadarsaka/services/sites/` - Python module for managing Appwrite Sites deployments
- `configure_sites.js` - Script to configure the JavaScript starter for Appwrite Sites
- `deploy_sites.py` - Deployment script for Appwrite Sites
- `Dockerfile.sites` - Docker configuration for containerizing the Streamlit app
- `appwrite.json` - Appwrite Sites configuration file

## Getting Started

### 1. Configure the JavaScript Starter for Appwrite Sites

Run the configuration script to prepare the JavaScript starter for deployment:

```bash
node configure_sites.js
```

This will:
- Update the `package.json` with Appwrite Sites specific scripts
- Create a Sites-specific Vite configuration
- Generate a landing page template
- Add CSS and JavaScript for the landing page

### 2. Build the Static Site

```bash
cd starter-for-js
npm install
npm run build:sites
cd ..
```

### 3. Deploy to Appwrite Sites

First, ensure you're logged in to the Appwrite CLI:

```bash
appwrite login
```

Then deploy using our Python script:

```bash
python deploy_sites.py --site-id margadarsaka
```

Or deploy only the marketing site:

```bash
python deploy_sites.py --site-id margadarsaka --static-only
```

### 4. Deploy the Streamlit App (Advanced)

The Streamlit app requires containerization:

```bash
# Build the Docker image
docker build -f Dockerfile.sites -t margadarsaka-app .

# Test locally
docker run -p 8501:8501 margadarsaka-app

# Deploy to Appwrite (requires container registry)
python deploy_sites.py --site-id margadarsaka --app-only
```

## Rendering Options

Appwrite Sites supports two rendering strategies:

### Static Site Generation (SSG)

Best for:
- Marketing site
- Documentation
- Landing pages

### Server-Side Rendering (SSR)

Best for:
- Dynamic content
- User-specific experiences
- Applications requiring server access

## Architecture

The Margadarsaka deployment uses a hybrid approach:

1. **Marketing Site**: Static site hosted directly on Appwrite Sites
   - Built from the `starter-for-js` directory
   - Fast loading times and global CDN benefits

2. **Streamlit Application**: Containerized application
   - Runs as a custom runtime on Appwrite Sites
   - Provides the full interactive experience

## Custom Domain Setup

To configure a custom domain:

1. Add your domain in the Appwrite Console
2. Configure DNS records as instructed
3. Wait for SSL certificate provisioning

## Environment Variables

You can configure environment variables through the Appwrite Console or using the CLI:

```bash
appwrite variables create \
  --key "VARIABLE_NAME" \
  --value "variable_value" \
  --site-id "margadarsaka"
```

## Monitoring and Logs

Access logs and monitor your deployment through the Appwrite Console under the Sites section.

## Learn More

- [Appwrite Sites Documentation](https://appwrite.io/docs/products/sites)
- [Streamlit Deployment Guide](https://docs.streamlit.io/knowledge-base/deploy)
- Review `docs/appwrite/sites.md` for more detailed information