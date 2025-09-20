"""
Secrets Management Module for Margadarsaka
Handles environment variables and secrets using Doppler or fallback to .env files
"""

import os
import logging
from typing import Optional, Dict, Any
from pathlib import Path

try:
    from dopplersdk import DopplerSDK

    DOPPLER_AVAILABLE = True
except ImportError:
    DOPPLER_AVAILABLE = False
    logging.warning("Doppler SDK not available. Falling back to environment variables.")

try:
    from dotenv import load_dotenv

    DOTENV_AVAILABLE = True
except ImportError:
    DOTENV_AVAILABLE = False
    logging.warning("python-dotenv not available. Using system environment only.")

logger = logging.getLogger(__name__)


class SecretsManager:
    """Unified secrets management using Doppler with .env fallback"""

    def __init__(self, use_doppler: bool = True):
        self.use_doppler = use_doppler and DOPPLER_AVAILABLE
        self.doppler_client = None
        self._secrets_cache: Dict[str, str] = {}

        # Initialize Doppler if available and requested
        if self.use_doppler:
            try:
                self.doppler_client = DopplerSDK()
                logger.info("✅ Doppler SDK initialized successfully")
            except Exception as e:
                logger.warning(f"⚠️ Failed to initialize Doppler: {e}")
                self.use_doppler = False

        # Load .env file as fallback
        if not self.use_doppler and DOTENV_AVAILABLE:
            env_file = Path(__file__).parent.parent.parent / ".env"
            if env_file.exists():
                load_dotenv(env_file)
                logger.info(f"✅ Loaded environment from {env_file}")
            else:
                logger.info("ℹ️ No .env file found, using system environment")

    def get_secret(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """Get a secret value by key"""
        try:
            # Check cache first
            if key in self._secrets_cache:
                return self._secrets_cache[key]

            value = None

            # Try Doppler first
            if self.use_doppler and self.doppler_client:
                try:
                    response = self.doppler_client.secrets.get(key)
                    if response and hasattr(response, "value"):
                        value = response.value
                        self._secrets_cache[key] = value
                        logger.debug(f"📥 Retrieved '{key}' from Doppler")
                except Exception as e:
                    logger.debug(f"🔍 Key '{key}' not found in Doppler: {e}")

            # Fallback to environment variables
            if value is None:
                value = os.getenv(key, default)
                if value:
                    self._secrets_cache[key] = value
                    logger.debug(f"📥 Retrieved '{key}' from environment")

            return value or default

        except Exception as e:
            logger.error(f"❌ Error retrieving secret '{key}': {e}")
            return default

    def get_all_secrets(self) -> Dict[str, str]:
        """Get all available secrets"""
        secrets = {}

        # Get from Doppler
        if self.use_doppler and self.doppler_client:
            try:
                response = self.doppler_client.secrets.list()
                if response and hasattr(response, "secrets"):
                    for secret_key, secret_data in response.secrets.items():
                        secrets[secret_key] = secret_data.get("computed", "")
                logger.debug(f"📥 Retrieved {len(secrets)} secrets from Doppler")
            except Exception as e:
                logger.warning(f"⚠️ Error retrieving secrets from Doppler: {e}")

        # Merge with environment variables (env vars take precedence)
        for key, value in os.environ.items():
            if key not in secrets:
                secrets[key] = value

        return secrets

    def set_secret(self, key: str, value: str) -> bool:
        """Set a secret value (Doppler only, not for env vars)"""
        if not self.use_doppler or not self.doppler_client:
            logger.warning(
                "⚠️ Cannot set secrets without Doppler. Use .env file instead."
            )
            return False

        try:
            # Note: Setting secrets via Doppler SDK requires appropriate permissions
            # This is typically done via Doppler CLI or dashboard
            logger.warning(
                "🔐 Secret setting should be done via Doppler CLI or dashboard"
            )
            return False
        except Exception as e:
            logger.error(f"❌ Error setting secret '{key}': {e}")
            return False

    def is_doppler_active(self) -> bool:
        """Check if Doppler is actively being used"""
        return self.use_doppler and self.doppler_client is not None


# Global secrets manager instance
secrets_manager = SecretsManager()


def get_secret(key: str, default: Optional[str] = None) -> Optional[str]:
    """Convenience function to get a secret"""
    return secrets_manager.get_secret(key, default)


def get_database_url() -> str:
    """Get database URL from secrets"""
    return (
        get_secret("DATABASE_URL", "sqlite:///margadarsaka.db")
        or "sqlite:///margadarsaka.db"
    )


def get_gemini_api_key() -> Optional[str]:
    """Get Google Gemini API key"""
    return get_secret("GEMINI_API_KEY")


def get_openai_api_key() -> Optional[str]:
    """Get OpenAI API key"""
    return get_secret("OPENAI_API_KEY")


def get_secret_key() -> str:
    """Get application secret key"""
    return (
        get_secret("SECRET_KEY", "dev-secret-key-change-in-production")
        or "dev-secret-key-change-in-production"
    )


def get_environment() -> str:
    """Get current environment"""
    return get_secret("ENVIRONMENT", "development") or "development"


def get_debug_mode() -> bool:
    """Get debug mode setting"""
    debug = get_secret("DEBUG", "false") or "false"
    return debug.lower() in ("true", "1", "yes", "on")


def get_api_base_url() -> str:
    """Get API base URL"""
    return (
        get_secret("API_BASE_URL", "http://localhost:8000") or "http://localhost:8000"
    )


def get_ui_base_url() -> str:
    """Get UI base URL"""
    return get_secret("UI_BASE_URL", "http://localhost:8501") or "http://localhost:8501"


def get_all_application_secrets() -> Dict[str, Any]:
    """Get all application-specific secrets with proper types"""
    return {
        "database_url": get_database_url(),
        "gemini_api_key": get_gemini_api_key(),
        "openai_api_key": get_openai_api_key(),
        "secret_key": get_secret_key(),
        "environment": get_environment(),
        "debug": get_debug_mode(),
        "api_base_url": get_api_base_url(),
        "ui_base_url": get_ui_base_url(),
        "doppler_active": secrets_manager.is_doppler_active(),
    }


if __name__ == "__main__":
    # Test the secrets manager
    print("🔐 Margadarsaka Secrets Manager Test")
    print("=" * 50)

    print(f"Doppler Active: {secrets_manager.is_doppler_active()}")
    print(f"Environment: {get_environment()}")
    print(f"Debug Mode: {get_debug_mode()}")
    print(f"API Base URL: {get_api_base_url()}")
    print(f"Gemini API Key: {'✅ Set' if get_gemini_api_key() else '❌ Not set'}")
    print(f"Database URL: {get_database_url()}")

    print("\n📊 All Application Secrets:")
    secrets = get_all_application_secrets()
    for key, value in secrets.items():
        if "key" in key.lower() and value:
            print(f"  {key}: {'✅ Set' if value else '❌ Not set'}")
        else:
            print(f"  {key}: {value}")
