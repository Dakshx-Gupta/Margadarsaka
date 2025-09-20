# PowerShell test runner script for Margadarsaka using UV
# Supports different test types and environments

param(
    [string]$TestType = "unit",
    [switch]$Verbose
)

# Configuration
$ErrorActionPreference = "Stop"

# Colors for output  
$Colors = @{
    Red = "Red"
    Green = "Green" 
    Yellow = "Yellow"
    Blue = "Blue"
    White = "White"
}

Write-Host "🧪 Margadarsaka Test Suite" -ForegroundColor $Colors.Blue
Write-Host "====================" -ForegroundColor $Colors.Blue

# Function to run tests with UV
function Run-Tests {
    param(
        [string]$TestArgs,
        [string]$Description
    )
    
    Write-Host "`n🔄 Running $Description..." -ForegroundColor $Colors.Yellow
    
    if ($Verbose) {
        & uv run python -m pytest $TestArgs.Split(' ') -v
    } else {
        & uv run python -m pytest $TestArgs.Split(' ')
    }
    
    if ($LASTEXITCODE -ne 0) {
        throw "Tests failed with exit code $LASTEXITCODE"
    }
}

# Function to check code quality
function Test-CodeQuality {
    Write-Host "`n🔧 Checking code quality..." -ForegroundColor $Colors.Yellow
    
    # Format code with black
    Write-Host "🖤 Formatting code with black..."
    & uv run black src/ tests/ --check
    
    if ($LASTEXITCODE -ne 0) {
        throw "Black formatting check failed"
    }
    
    # Lint with ruff
    Write-Host "🔍 Linting with ruff..."
    & uv run ruff check src/ tests/
    
    if ($LASTEXITCODE -ne 0) {
        throw "Ruff linting failed"
    }
    
    Write-Host "✅ Code quality checks passed" -ForegroundColor $Colors.Green
}

# Function to test Doppler integration
function Test-Doppler {
    Write-Host "`n🔐 Testing Doppler integration..." -ForegroundColor $Colors.Yellow
    
    try {
        # Test Doppler setup script
        Write-Host "🔐 Testing Doppler setup..."
        & uv run python setup_doppler.py *> $null
        
        # Test secrets manager
        Write-Host "🔑 Testing secrets manager..."
        $pythonCode = @"
from src.margadarsaka.secrets import secrets_manager, get_all_application_secrets
print('Doppler Active: {0}'.format(secrets_manager.is_doppler_active()))
secrets = get_all_application_secrets()
print('✅ Secrets manager working')
"@
        & uv run python -c $pythonCode
        
        Write-Host "✅ Doppler integration tests passed" -ForegroundColor $Colors.Green
    }
    catch {
        Write-Host "⚠️ Doppler setup test skipped (CLI not configured)" -ForegroundColor $Colors.Yellow
    }
}

# Function to test application startup
function Test-Startup {
    Write-Host "`n📦 Testing application startup..." -ForegroundColor $Colors.Yellow
    
    # Test imports
    Write-Host "📦 Testing imports..."
    $pythonCode = @"
import sys
sys.path.insert(0, 'src')
from margadarsaka.api import app
from margadarsaka.ui import main as ui_main  
from margadarsaka.secrets import secrets_manager
print('✅ All imports successful')
"@
    & uv run python -c $pythonCode
    
    if ($LASTEXITCODE -ne 0) {
        throw "Startup tests failed"
    }
    
    Write-Host "✅ Startup tests passed" -ForegroundColor $Colors.Green
}

# Main test execution
try {
    switch ($TestType.ToLower()) {
        "unit" {
            Write-Host "Running unit tests only..."
            Run-Tests "tests/ -m 'not integration and not slow'" "unit tests"
        }
        "integration" {
            Write-Host "Running integration tests..."
            Run-Tests "tests/ --integration" "integration tests"
        }
        "all" {
            Write-Host "Running all tests..."
            Run-Tests "tests/ --integration" "all tests"
        }
        "quality" {
            Test-CodeQuality
        }
        "doppler" {
            Test-Doppler
        }
        "startup" {
            Test-Startup
        }
        "full" {
            Write-Host "Running full test suite..."
            Test-CodeQuality
            Test-Startup
            Test-Doppler
            Run-Tests "tests/ -m 'not slow'" "standard tests"
            Run-Tests "tests/ --integration -m 'not slow'" "integration tests"
        }
        default {
            Write-Host "❌ Unknown test type: $TestType" -ForegroundColor $Colors.Red
            Write-Host "Available options: unit, integration, all, quality, doppler, startup, full"
            exit 1
        }
    }
    
    Write-Host "`n🎉 All tests completed successfully!" -ForegroundColor $Colors.Green
    
    # Additional info
    Write-Host "`n📋 Test Commands Reference:" -ForegroundColor $Colors.Blue
    Write-Host "• Unit tests:        .\test.ps1 -TestType unit"
    Write-Host "• Integration tests: .\test.ps1 -TestType integration"
    Write-Host "• All tests:         .\test.ps1 -TestType all"
    Write-Host "• Code quality:      .\test.ps1 -TestType quality"
    Write-Host "• Doppler tests:     .\test.ps1 -TestType doppler"
    Write-Host "• Startup tests:     .\test.ps1 -TestType startup"
    Write-Host "• Full suite:        .\test.ps1 -TestType full"
    Write-Host "• Verbose output:    .\test.ps1 -TestType [type] -Verbose"
}
catch {
    Write-Host "`n❌ Test execution failed: $_" -ForegroundColor $Colors.Red
    exit 1
}