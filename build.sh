# Deployment Build Script for Appwrite
echo "Starting Margadarsaka deployment build..."

# Install Python dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
pip install -e .

# Verify installation
echo "Verifying installation..."
python -c "import streamlit; print(f'Streamlit version: {streamlit.__version__}')"
python -c "import src.margadarsaka; print('Margadarsaka package imported successfully')"

# Create necessary directories
mkdir -p logs
mkdir -p temp

echo "Build completed successfully!"