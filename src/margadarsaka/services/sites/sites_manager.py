"""
Appwrite Sites integration for Margadarsaka
Provides utilities for deploying and managing Margadarsaka on Appwrite Sites
"""

import os
import json
import subprocess
from pathlib import Path
import logging
from typing import Dict, List, Optional, Any, Union
import shutil

logger = logging.getLogger(__name__)

class AppwriteSitesManager:
    """
    Manages deployment and configuration for Appwrite Sites
    """
    
    def __init__(
        self, 
        appwrite_endpoint: str = None,
        project_id: str = None,
        api_key: str = None
    ):
        """
        Initialize the AppwriteSitesManager
        
        Args:
            appwrite_endpoint: The Appwrite API endpoint URL
            project_id: The Appwrite project ID
            api_key: The Appwrite API key with Sites privileges
        """
        self.appwrite_endpoint = appwrite_endpoint or os.getenv("APPWRITE_ENDPOINT")
        self.project_id = project_id or os.getenv("APPWRITE_PROJECT_ID")
        self.api_key = api_key or os.getenv("APPWRITE_API_KEY")
        
        # Project root directory
        self.project_root = Path(__file__).parent.parent.parent.parent.parent
        
        # Check if we have the Appwrite CLI installed
        self._check_cli()
    
    def _check_cli(self) -> None:
        """Check if Appwrite CLI is installed and configured"""
        try:
            result = subprocess.run(
                ["appwrite", "--version"], 
                capture_output=True, 
                text=True,
                check=False
            )
            
            if result.returncode != 0:
                logger.warning("Appwrite CLI not found. Please install it using 'npm install -g appwrite-cli'")
            else:
                logger.info(f"Found Appwrite CLI: {result.stdout.strip()}")
                
        except FileNotFoundError:
            logger.warning("Appwrite CLI not installed. Install with: npm install -g appwrite-cli")
    
    def login(self) -> bool:
        """Log in to Appwrite CLI"""
        if not all([self.appwrite_endpoint, self.project_id, self.api_key]):
            logger.error("Missing Appwrite credentials. Set environment variables or provide in constructor.")
            return False
            
        try:
            # Configure the CLI
            subprocess.run(
                ["appwrite", "client", "--endpoint", self.appwrite_endpoint],
                check=True,
                capture_output=True
            )
            
            # Login with the API key
            result = subprocess.run(
                ["appwrite", "login", "--key", self.api_key],
                check=True,
                capture_output=True
            )
            
            logger.info("Successfully logged in to Appwrite CLI")
            return True
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to login to Appwrite: {e.stderr.decode() if hasattr(e, 'stderr') else str(e)}")
            return False
    
    def prepare_static_deployment(
        self, 
        source_dir: str = "starter-for-js",
        build_command: str = "npm run build",
        output_dir: str = "dist"
    ) -> bool:
        """
        Prepare static site for deployment
        
        Args:
            source_dir: Directory containing the static site source
            build_command: Command to build the static site
            output_dir: Directory where build outputs are generated
            
        Returns:
            bool: True if preparation was successful
        """
        source_path = self.project_root / source_dir
        
        if not source_path.exists():
            logger.error(f"Source directory {source_path} does not exist")
            return False
        
        try:
            # Navigate to the source directory
            os.chdir(source_path)
            
            # Install dependencies
            logger.info("Installing dependencies...")
            subprocess.run(["npm", "install"], check=True)
            
            # Build the site
            logger.info(f"Building site with command: {build_command}")
            subprocess.run(build_command.split(), check=True)
            
            # Check if the output directory exists
            if not (source_path / output_dir).exists():
                logger.error(f"Build failed: {output_dir} directory not found")
                return False
                
            logger.info(f"Static site prepared successfully in {source_path / output_dir}")
            return True
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to prepare static site: {str(e)}")
            return False
        finally:
            # Return to project root
            os.chdir(self.project_root)
    
    def deploy_site(
        self,
        site_id: str,
        source_dir: str = "starter-for-js",
        output_dir: str = "dist",
        domain: Optional[str] = None,
        use_ssr: bool = False,
        env_vars: Optional[Dict[str, str]] = None
    ) -> bool:
        """
        Deploy a site to Appwrite Sites
        
        Args:
            site_id: Unique ID for the site
            source_dir: Directory containing the site source
            output_dir: Directory containing built assets
            domain: Custom domain for the site
            use_ssr: Whether to use server-side rendering
            env_vars: Environment variables for the site
            
        Returns:
            bool: True if deployment was successful
        """
        if not self.login():
            return False
            
        source_path = self.project_root / source_dir
        build_path = source_path / output_dir
        
        if not build_path.exists():
            logger.error(f"Build directory {build_path} does not exist")
            return False
        
        try:
            # Base deployment command
            deploy_cmd = [
                "appwrite", "deploy", "site",
                "--site-id", site_id,
                "--path", str(build_path)
            ]
            
            # Add optional parameters
            if domain:
                deploy_cmd.extend(["--domain", domain])
            
            if use_ssr:
                deploy_cmd.append("--ssr")
                
            # Execute deployment
            logger.info(f"Deploying to Appwrite Sites with ID: {site_id}")
            result = subprocess.run(deploy_cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                logger.error(f"Deployment failed: {result.stderr}")
                return False
                
            logger.info(f"Site deployed successfully: {result.stdout}")
            
            # Set environment variables if provided
            if env_vars:
                for key, value in env_vars.items():
                    self.set_environment_variable(site_id, key, value)
            
            return True
            
        except Exception as e:
            logger.error(f"Error deploying site: {str(e)}")
            return False
    
    def set_environment_variable(self, site_id: str, key: str, value: str) -> bool:
        """
        Set an environment variable for a site
        
        Args:
            site_id: ID of the site
            key: Environment variable name
            value: Environment variable value
            
        Returns:
            bool: True if setting the variable was successful
        """
        if not self.login():
            return False
            
        try:
            cmd = [
                "appwrite", "variables", "create",
                "--site-id", site_id,
                "--key", key,
                "--value", value
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                logger.error(f"Failed to set environment variable {key}: {result.stderr}")
                return False
                
            logger.info(f"Set environment variable {key} for site {site_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error setting environment variable: {str(e)}")
            return False
    
    def get_site_url(self, site_id: str) -> Optional[str]:
        """
        Get the URL for a deployed site
        
        Args:
            site_id: ID of the site
            
        Returns:
            str: URL of the site or None if not found
        """
        if not self.login():
            return None
            
        try:
            cmd = ["appwrite", "sites", "get", "--site-id", site_id]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                logger.error(f"Failed to get site info: {result.stderr}")
                return None
                
            # Parse the JSON response to extract the URL
            site_info = json.loads(result.stdout)
            return site_info.get("url")
            
        except Exception as e:
            logger.error(f"Error getting site URL: {str(e)}")
            return None
    
    def create_hybrid_deployment(
        self,
        marketing_site_id: str = "margadarsaka-marketing",
        app_site_id: str = "margadarsaka-app",
        streamlit_port: int = 8501
    ) -> Dict[str, Any]:
        """
        Create a hybrid deployment with static marketing site and Streamlit app
        
        Args:
            marketing_site_id: Site ID for the marketing/docs site
            app_site_id: Site ID for the Streamlit app
            streamlit_port: Port for the Streamlit app
            
        Returns:
            Dict with deployment status and URLs
        """
        results = {
            "marketing_deployed": False,
            "app_deployed": False,
            "marketing_url": None,
            "app_url": None
        }
        
        # 1. Deploy the static marketing site
        if self.prepare_static_deployment():
            results["marketing_deployed"] = self.deploy_site(
                site_id=marketing_site_id,
                domain=f"{marketing_site_id}.appwrite.io"
            )
            results["marketing_url"] = self.get_site_url(marketing_site_id)
            
        # 2. Deploy the Streamlit app via a Docker container
        # This would typically require a more complex setup with Dockerfile
        # For now, we'll just add placeholder logic
        
        logger.info("Streamlit app deployment requires additional configuration.")
        logger.info("See the docs/appwrite/sites.md file for detailed instructions.")
        
        return results