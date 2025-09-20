#!/usr/bin/env python3
"""
Doppler Setup Script for Margadarsaka
This script helps set up Doppler secrets management for the project
"""

import os
import sys
import subprocess
from pathlib import Path


def check_doppler_cli():
    """Check if Doppler CLI is installed"""
    try:
        result = subprocess.run(
            ["doppler", "--version"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        if result.returncode == 0:
            print(f"✅ Doppler CLI found: {result.stdout.strip()}")
            return True
        else:
            print("❌ Doppler CLI not found")
            return False
    except FileNotFoundError:
        print("❌ Doppler CLI not found")
        return False


def install_doppler_cli():
    """Instructions to install Doppler CLI"""
    print("\n🔧 Installing Doppler CLI...")
    print("\nFor Windows (PowerShell):")
    print("  iwr https://cli.doppler.com/install.ps1 -useb | iex")
    print("\nFor macOS:")
    print("  brew install dopplerhq/cli/doppler")
    print("\nFor Linux:")
    print("  curl -Ls https://cli.doppler.com/install.sh | sh")
    print("\nAfter installation, run this script again.")


def setup_doppler_project():
    """Set up Doppler project and environments"""
    print("\n🚀 Setting up Doppler project...")

    # Check if already authenticated
    try:
        result = subprocess.run(
            ["doppler", "me"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        if result.returncode != 0:
            print("🔐 Please authenticate with Doppler first:")
            print("  doppler login")
            print("\nThen run this script again.")
            return False
        else:
            print("✅ Doppler authentication confirmed")
    except Exception as e:
        print(f"❌ Error checking Doppler auth: {e}")
        return False

    # Create project
    project_name = "margadarsaka"
    print(f"\n📁 Creating Doppler project: {project_name}")

    try:
        # Check if project exists
        result = subprocess.run(
            ["doppler", "projects", "get", project_name, "--json"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )

        if result.returncode == 0:
            print(f"✅ Project '{project_name}' already exists")
        else:
            # Create project
            create_result = subprocess.run(
                ["doppler", "projects", "create", project_name],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
            )
            if create_result.returncode == 0:
                print(f"✅ Project '{project_name}' created successfully")
            else:
                print(f"❌ Failed to create project: {create_result.stderr}")
                return False

    except Exception as e:
        print(f"❌ Error managing project: {e}")
        return False

    # Create configs for environments (if needed)
    additional_configs = [
        ("dev_backend", "dev", "Development backend configuration"),
        ("stg_backend", "stg", "Staging backend configuration"),
        ("prd_backend", "prd", "Production backend configuration"),
    ]

    # Note: dev_local already exists, and default configs (dev, stg, prd) are auto-created
    for config_name, env_name, env_desc in additional_configs:
        try:
            result = subprocess.run(
                [
                    "doppler",
                    "configs",
                    "create",
                    config_name,
                    "--project",
                    project_name,
                    "--environment",
                    env_name,
                ],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
            )
            if result.returncode == 0:
                print(f"✅ Config '{config_name}' created")
            elif (
                "already exists" in result.stderr.lower()
                or "already in use" in result.stderr.lower()
            ):
                print(f"ℹ️ Config '{config_name}' already exists")
            else:
                print(f"ℹ️ Config '{config_name}': {result.stderr.strip()}")
        except Exception as e:
            print(f"❌ Error creating config '{config_name}': {e}")

    # List all configs
    print(f"\n📋 Configs available for project '{project_name}':")
    try:
        result = subprocess.run(
            ["doppler", "configs", "--project", project_name, "--json"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        if result.returncode == 0:
            import json

            configs = json.loads(result.stdout)
            for config in configs:
                print(f"  • {config['name']} ({config['environment']})")
        else:
            print("  (Unable to list configs)")
    except Exception:
        print("  (Unable to list configs)")

    return True


def setup_local_config():
    """Set up local Doppler configuration"""
    print("\n⚙️ Setting up local Doppler configuration...")

    project_root = Path(__file__).parent
    os.chdir(project_root)

    try:
        # Set up local config
        result = subprocess.run(
            ["doppler", "setup", "--project", "margadarsaka", "--config", "dev"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )

        if result.returncode == 0:
            print("✅ Local Doppler configuration set up successfully")
            print("📁 Configuration saved to .doppler directory")
            return True
        else:
            print(f"❌ Failed to set up local config: {result.stderr}")
            return False

    except Exception as e:
        print(f"❌ Error setting up local config: {e}")
        return False


def add_sample_secrets():
    """Add sample secrets to development environment"""
    print("\n🔐 Adding sample secrets to development environment...")

    sample_secrets = {
        "ENVIRONMENT": "development",
        "DEBUG": "true",
        "API_BASE_URL": "http://localhost:8000",
        "UI_BASE_URL": "http://localhost:8501",
        "SECRET_KEY": "dev-secret-key-change-in-production",
        "DATABASE_URL": "sqlite:///margadarsaka.db",
        "GEMINI_API_KEY": "your_gemini_api_key_here",
        "LOG_LEVEL": "INFO",
        "ENABLE_AI_FEATURES": "true",
    }

    for key, value in sample_secrets.items():
        try:
            result = subprocess.run(
                [
                    "doppler",
                    "secrets",
                    "set",
                    f"{key}={value}",
                    "--project",
                    "margadarsaka",
                    "--config",
                    "dev",
                ],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
            )

            if result.returncode == 0:
                print(f"✅ Secret '{key}' added")
            else:
                print(f"⚠️ Could not add secret '{key}': {result.stderr}")

        except Exception as e:
            print(f"❌ Error adding secret '{key}': {e}")


def test_doppler_integration():
    """Test Doppler integration with the application"""
    print("\n🧪 Testing Doppler integration...")

    try:
        # Test secrets manager using UV run
        import subprocess

        test_result = subprocess.run(
            [
                "uv",
                "run",
                "python",
                "-c",
                "from src.margadarsaka.secrets import secrets_manager, get_all_application_secrets; "
                "print(f'Doppler Active: {secrets_manager.is_doppler_active()}'); "
                "secrets = get_all_application_secrets(); "
                "print(f'Environment: {secrets[\"environment\"]}'); "
                "print(f'Debug Mode: {secrets[\"debug\"]}'); "
                "print(f'API Base URL: {secrets[\"api_base_url\"]}')",
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )

        if test_result.returncode == 0:
            print("✅ Doppler integration test passed!")
            print(test_result.stdout.strip())
        else:
            print(f"⚠️ Integration test had issues: {test_result.stderr}")

    except Exception as e:
        print(f"❌ Error testing integration: {e}")


def main():
    """Main setup function"""
    print("🔐 Margadarsaka Doppler Setup")
    print("=" * 50)

    # Check if Doppler CLI is installed
    if not check_doppler_cli():
        install_doppler_cli()
        return 1

    # Set up Doppler project and environments
    if not setup_doppler_project():
        print("❌ Failed to set up Doppler project")
        return 1

    # Set up local configuration
    if not setup_local_config():
        print("❌ Failed to set up local configuration")
        return 1

    # Add sample secrets
    add_sample_secrets()

    # Test integration
    test_doppler_integration()

    print("\n🎉 Doppler setup complete!")
    print("\n📋 Next steps:")
    print("1. Update your API keys in Doppler:")
    print(
        "   doppler secrets set GEMINI_API_KEY=your_actual_key --project margadarsaka --config dev"
    )
    print("2. Run your application with Doppler:")
    print("   doppler run --project margadarsaka --config dev -- uv run margadarsaka")
    print("3. Test the application:")
    print("   uv run python -m pytest tests/ -v")
    print("4. Run setup verification:")
    print("   uv run python setup_doppler.py")
    print("5. View/edit secrets in Doppler dashboard:")
    print("   doppler open")
    print("\n🐳 For Docker deployment:")
    print("   docker build -t margadarsaka .")
    print("   docker run -e DOPPLER_TOKEN=your_token margadarsaka")

    return 0


if __name__ == "__main__":
    sys.exit(main())
