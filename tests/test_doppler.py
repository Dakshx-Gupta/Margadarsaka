"""
Test suite for Doppler integration
Tests secrets management and configuration
"""

import pytest
import os
from unittest.mock import patch, MagicMock


def test_doppler_sdk_import():
    """Test that doppler SDK can be imported"""
    try:
        import dopplersdk

        assert True
    except ImportError:
        pytest.fail("Doppler SDK not available")


def test_secrets_manager_initialization():
    """Test secrets manager can be initialized"""
    from src.margadarsaka.secrets import SecretsManager

    manager = SecretsManager()
    assert manager is not None


def test_get_secret_with_fallback():
    """Test secret retrieval with environment fallback"""
    from src.margadarsaka.secrets import get_secret

    # Test with environment variable
    with patch.dict(os.environ, {"TEST_SECRET": "test_value"}):
        result = get_secret("TEST_SECRET", "default")
        assert result == "test_value"

    # Test with default
    result = get_secret("NON_EXISTENT_SECRET", "default_value")
    assert result == "default_value"


def test_application_secrets():
    """Test application-specific secret getters"""
    from src.margadarsaka.secrets import (
        get_environment,
        get_debug_mode,
        get_api_base_url,
        get_gemini_api_key,
        get_secret_key,
    )

    # Test that functions return values (either from Doppler or defaults)
    env = get_environment()
    assert env in ["development", "staging", "production"]

    debug = get_debug_mode()
    assert isinstance(debug, bool)

    api_url = get_api_base_url()
    assert api_url.startswith("http")

    # API key can be None if not configured - this is expected
    api_key = get_gemini_api_key()
    assert isinstance(api_key, (str, type(None)))

    secret_key = get_secret_key()
    assert isinstance(secret_key, str)
    assert len(secret_key) > 0  # Should have some value


@pytest.mark.integration
def test_doppler_cli_available():
    """Test that Doppler CLI is available in environment"""
    import subprocess

    try:
        result = subprocess.run(
            ["doppler", "--version"], capture_output=True, text=True, timeout=10
        )
        assert result.returncode == 0
        # Doppler version output is just the version number (e.g., "v3.75.1")
        assert (
            result.stdout.strip().startswith("v") or "doppler" in result.stdout.lower()
        )
    except FileNotFoundError:
        pytest.skip("Doppler CLI not installed")
    except subprocess.TimeoutExpired:
        pytest.fail("Doppler CLI command timed out")


@pytest.mark.integration
def test_doppler_project_exists():
    """Test that margadarsaka project exists in Doppler"""
    import subprocess
    import json

    try:
        result = subprocess.run(
            ["doppler", "projects", "get", "margadarsaka", "--json"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        # Project should exist (return code 0) or we should get a specific error
        if result.returncode != 0:
            pytest.skip("Doppler project not set up")

        project_data = json.loads(result.stdout)
        assert project_data["name"] == "margadarsaka"

    except (FileNotFoundError, subprocess.TimeoutExpired, json.JSONDecodeError):
        pytest.skip("Doppler CLI not available or project not configured")
