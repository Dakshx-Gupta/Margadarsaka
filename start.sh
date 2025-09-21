# Start Script for Appwrite Deployment
echo "Starting Margadarsaka application..."

# Set environment variables for production
export STREAMLIT_SERVER_HEADLESS=true
export STREAMLIT_SERVER_ENABLE_CORS=false
export STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=false
export STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Use PORT from environment or default to 8501
PORT=${PORT:-8501}

echo "Starting Streamlit on port $PORT..."
streamlit run src/margadarsaka/ui_modern.py \
  --server.port $PORT \
  --server.address 0.0.0.0 \
  --server.headless true \
  --server.enableCORS false \
  --server.enableXsrfProtection false \
  --browser.gatherUsageStats false