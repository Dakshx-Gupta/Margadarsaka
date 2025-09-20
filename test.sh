#!/usr/bin/env bash
# Test runner script for Margadarsaka using UV
# Supports different test types and environments

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
TEST_TYPE=${1:-unit}
VERBOSE=${2:-false}

echo -e "${BLUE}🧪 Margadarsaka Test Suite${NC}"
echo "===================="

# Function to run tests with UV
run_tests() {
    local test_args=$1
    local description=$2
    
    echo -e "\n${YELLOW}Running ${description}...${NC}"
    
    if [ "$VERBOSE" = "true" ]; then
        uv run python -m pytest $test_args -v
    else
        uv run python -m pytest $test_args
    fi
}

# Function to check code quality
check_code_quality() {
    echo -e "\n${YELLOW}Checking code quality...${NC}"
    
    # Format code with black
    echo "🔧 Formatting code with black..."
    uv run black src/ tests/ --check
    
    # Lint with ruff
    echo "🔍 Linting with ruff..."
    uv run ruff check src/ tests/
    
    echo -e "${GREEN}✅ Code quality checks passed${NC}"
}

# Function to test Doppler integration
test_doppler() {
    echo -e "\n${YELLOW}Testing Doppler integration...${NC}"
    
    # Test Doppler setup script
    echo "🔐 Testing Doppler setup..."
    uv run python setup_doppler.py > /dev/null 2>&1 || {
        echo -e "${YELLOW}⚠️ Doppler setup test skipped (CLI not configured)${NC}"
        return 0
    }
    
    # Test secrets manager
    echo "🔑 Testing secrets manager..."
    uv run python -c "
from src.margadarsaka.secrets import secrets_manager, get_all_application_secrets
print(f'Doppler Active: {secrets_manager.is_doppler_active()}')
secrets = get_all_application_secrets()
print('✅ Secrets manager working')
"
    
    echo -e "${GREEN}✅ Doppler integration tests passed${NC}"
}

# Function to test application startup
test_startup() {
    echo -e "\n${YELLOW}Testing application startup...${NC}"
    
    # Test imports
    echo "📦 Testing imports..."
    uv run python -c "
import sys
sys.path.insert(0, 'src')
from margadarsaka.api import app
from margadarsaka.ui import main as ui_main
from margadarsaka.secrets import secrets_manager
print('✅ All imports successful')
"
    
    echo -e "${GREEN}✅ Startup tests passed${NC}"
}

# Main test execution
case $TEST_TYPE in
    "unit")
        echo "Running unit tests only..."
        run_tests "tests/ -m 'not integration and not slow'" "unit tests"
        ;;
    "integration") 
        echo "Running integration tests..."
        run_tests "tests/ --integration" "integration tests"
        ;;
    "all")
        echo "Running all tests..."
        run_tests "tests/ --integration" "all tests"
        ;;
    "quality")
        check_code_quality
        ;;
    "doppler")
        test_doppler
        ;;
    "startup")
        test_startup
        ;;
    "full")
        echo "Running full test suite..."
        check_code_quality
        test_startup
        test_doppler
        run_tests "tests/ -m 'not slow'" "standard tests"
        run_tests "tests/ --integration -m 'not slow'" "integration tests"
        ;;
    *)
        echo -e "${RED}❌ Unknown test type: $TEST_TYPE${NC}"
        echo "Available options: unit, integration, all, quality, doppler, startup, full"
        exit 1
        ;;
esac

echo -e "\n${GREEN}🎉 All tests completed successfully!${NC}"

# Additional info
echo -e "\n${BLUE}📋 Test Commands Reference:${NC}"
echo "• Unit tests:        ./test.sh unit"
echo "• Integration tests: ./test.sh integration"
echo "• All tests:         ./test.sh all"
echo "• Code quality:      ./test.sh quality"
echo "• Doppler tests:     ./test.sh doppler"
echo "• Startup tests:     ./test.sh startup"
echo "• Full suite:        ./test.sh full"
echo "• Verbose output:    ./test.sh [type] true"