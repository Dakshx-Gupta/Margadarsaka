#!/usr/bin/env python3
"""
Quick test for Appwrite authentication integration
"""

import asyncio
import os
import sys
import logging

# Add the src directory to the Python path
sys.path.insert(0, "src")

from margadarsaka.services.appwrite_service import AppwriteService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def test_appwrite_auth():
    """Test basic Appwrite authentication functionality."""

    print("🧪 Testing Appwrite Authentication Integration")
    print("=" * 50)

    # Initialize service
    service = AppwriteService()

    # Check configuration
    print(f"✓ Service configured: {service.is_configured()}")
    print(f"✓ Endpoint: {service.endpoint}")
    print(f"✓ Project ID: {service.project_id}")
    print(
        f"✓ API Key: {'***' + service.api_key[-10:] if service.api_key else 'Not set'}"
    )

    if not service.is_configured():
        print("❌ Appwrite is not properly configured")
        print("Make sure all environment variables are set:")
        print("- APPWRITE_ENDPOINT")
        print("- APPWRITE_PROJECT_ID")
        print("- APPWRITE_API_KEY")
        return

    # Test getting current user (should fail if no session)
    print("\n📱 Testing authentication state...")
    current_user = await service.get_current_user()
    if current_user:
        print(f"✓ Current user: {current_user.get('email', 'Unknown')}")
    else:
        print("✓ No current user (expected for server-side)")

    print("\n✅ Appwrite integration test completed!")
    print("The service is properly configured and ready for authentication.")


if __name__ == "__main__":
    # Load environment from Doppler if available
    import subprocess
    import json

    try:
        # Get secrets from Doppler
        result = subprocess.run(
            ["doppler", "secrets", "download", "--format", "json", "--no-file"],
            capture_output=True,
            text=True,
            check=True,
        )
        secrets = json.loads(result.stdout)

        # Set environment variables
        for key, value in secrets.items():
            os.environ[key] = value

        print("🔐 Loaded secrets from Doppler")
    except (subprocess.CalledProcessError, FileNotFoundError, json.JSONDecodeError):
        print("⚠️  Using existing environment variables (Doppler not available)")

    # Run the test
    asyncio.run(test_appwrite_auth())
