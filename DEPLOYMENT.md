# Margadarsaka - Appwrite Deployment Guide

## Repository-Based Deployment Configuration

Since you've connected your GitHub repository directly to Appwrite, here's the optimized configuration:

### 1. Configuration Files

- **appwrite.json**: Updated for repository-based deployment with proper build and start commands
- **.appwrite**: Environment configuration for Appwrite CLI
- **build.sh**: Build script that installs dependencies and verifies installation
- **start.sh**: Start script that launches Streamlit with production settings

### 2. Deployment Settings

**Runtime**: Python 3.11
**Build Command**: `pip install -r requirements.txt && pip install -e .`
**Start Command**: `streamlit run src/margadarsaka/ui_modern.py --server.port $PORT --server.address 0.0.0.0 --server.headless true`

### 3. Environment Variables

The following environment variables are configured for production:
- `ENVIRONMENT=production`
- `STREAMLIT_SERVER_HEADLESS=true`
- `STREAMLIT_SERVER_ENABLE_CORS=false`
- `STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=false`
- `STREAMLIT_BROWSER_GATHER_USAGE_STATS=false`
- `PORT=8501`

### 4. Deployment Process

1. **Automatic Triggers**: Deployment will trigger on push to the `main` branch
2. **Build Process**: 
   - Installs Python dependencies from `requirements.txt`
   - Installs the package in development mode (`pip install -e .`)
   - Verifies installation
3. **Runtime**: Starts Streamlit application on the configured port

### 5. Key Differences from Tar.gz Upload

**Before (Tar.gz)**:
- Used Docker container with Dockerfile.sites
- Manual file upload process
- Container-based deployment

**Now (Repository)**:
- Direct Git integration
- Automatic deployment on code changes
- Native Python runtime (no Docker overhead)
- Faster build times

### 6. Monitoring and Logs

- Build logs will show dependency installation progress
- Runtime logs will display Streamlit server status
- Application logs available through Appwrite console

### 7. Optional Enhancements

If you need additional features, you can:
- Add health check endpoints
- Configure custom domains
- Set up environment-specific configurations
- Add database connections for user data persistence

The configuration is now optimized for your repository-based deployment workflow!