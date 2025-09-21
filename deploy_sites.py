#!/usr/bin/env python3
"""
Appwrite Sites deployment script for Margadarsaka
"""

import os
import sys
import argparse
import logging
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

from src.margadarsaka.services.sites import AppwriteSitesManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger("appwrite-sites-deploy")

def main():
    """Main deployment function"""
    parser = argparse.ArgumentParser(description="Deploy Margadarsaka to Appwrite Sites")
    
    parser.add_argument("--endpoint", help="Appwrite endpoint URL")
    parser.add_argument("--project", help="Appwrite project ID")
    parser.add_argument("--key", help="Appwrite API key")
    parser.add_argument("--site-id", default="margadarsaka", help="Site ID for deployment")
    parser.add_argument("--domain", help="Custom domain for the site")
    parser.add_argument("--ssr", action="store_true", help="Use server-side rendering")
    parser.add_argument("--static-only", action="store_true", help="Deploy only the static marketing site")
    parser.add_argument("--app-only", action="store_true", help="Deploy only the Streamlit app")
    parser.add_argument("--source-dir", default="starter-for-js", help="Source directory for static site")
    parser.add_argument("--build-cmd", default="npm run build", help="Build command for static site")
    parser.add_argument("--output-dir", default="dist", help="Output directory for build artifacts")
    
    args = parser.parse_args()
    
    # Initialize the Sites Manager
    sites_manager = AppwriteSitesManager(
        appwrite_endpoint=args.endpoint,
        project_id=args.project,
        api_key=args.key
    )
    
    if args.static_only:
        # Deploy just the marketing site
        logger.info("Deploying static marketing site...")
        deploy_marketing_site(sites_manager, args)
    elif args.app_only:
        # Deploy just the Streamlit app
        logger.info("Deploying Streamlit app...")
        deploy_streamlit_app(sites_manager, args)
    else:
        # Deploy both
        logger.info("Deploying hybrid setup (marketing site + Streamlit app)...")
        deploy_hybrid(sites_manager, args)
    
    logger.info("Deployment process completed!")

def deploy_marketing_site(sites_manager, args):
    """Deploy the static marketing site"""
    # Prepare the static site
    if not sites_manager.prepare_static_deployment(
        source_dir=args.source_dir,
        build_command=args.build_cmd,
        output_dir=args.output_dir
    ):
        logger.error("Failed to prepare static site for deployment")
        return False
    
    # Deploy to Appwrite Sites
    success = sites_manager.deploy_site(
        site_id=f"{args.site_id}-marketing",
        source_dir=args.source_dir,
        output_dir=args.output_dir,
        domain=args.domain,
        use_ssr=False,  # Marketing site is always static
        env_vars={
            "SITE_TYPE": "marketing",
            "APPWRITE_ENDPOINT": os.getenv("APPWRITE_ENDPOINT", "")
        }
    )
    
    if success:
        site_url = sites_manager.get_site_url(f"{args.site_id}-marketing")
        logger.info(f"Marketing site deployed successfully at: {site_url}")
        return True
    else:
        logger.error("Marketing site deployment failed")
        return False

def deploy_streamlit_app(sites_manager, args):
    """Deploy the Streamlit app to Appwrite Sites"""
    logger.info("Streamlit app deployment requires additional configuration.")
    logger.info("See the docs/appwrite/sites.md file for detailed instructions.")
    
    # This would typically involve:
    # 1. Building a Docker container for the Streamlit app
    # 2. Publishing it to a container registry
    # 3. Configuring Appwrite Sites to use that container
    
    logger.info("For now, you can run the following to deploy manually:")
    logger.info("1. Build the Docker image: docker build -t margadarsaka-app .")
    logger.info("2. Publish to container registry: docker push <registry>/margadarsaka-app")
    logger.info("3. Configure in Appwrite Console: Sites > New Site > Custom Runtime")
    
    return False  # Not implemented yet

def deploy_hybrid(sites_manager, args):
    """Deploy both marketing site and Streamlit app"""
    # Deploy the marketing site
    marketing_success = deploy_marketing_site(sites_manager, args)
    
    # Attempt to deploy the app (will provide instructions)
    app_success = deploy_streamlit_app(sites_manager, args)
    
    return marketing_success

if __name__ == "__main__":
    main()