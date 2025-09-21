#!/usr/bin/env python3
"""
Complete integration script for Margadarsaka
This script properly integrates the JavaScript starter with the Streamlit application
"""

import os
import subprocess
import shutil
import json
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ROOT_DIR = Path(__file__).parent
JS_DIR = ROOT_DIR / "starter-for-js"
STREAMLIT_DIR = ROOT_DIR / "src" / "margadarsaka"

def create_unified_package():
    """Create a unified package that includes both JS and Python components"""
    logger.info("Creating unified Margadarsaka package...")
    
    # 1. First, build the JavaScript components
    if not build_js_components():
        return False
    
    # 2. Create the integrated package structure
    package_dir = ROOT_DIR / "margadarsaka_unified"
    if package_dir.exists():
        shutil.rmtree(package_dir)
    
    package_dir.mkdir()
    
    # 3. Copy the Streamlit application
    streamlit_dest = package_dir / "margadarsaka"
    shutil.copytree(STREAMLIT_DIR, streamlit_dest)
    
    # 4. Copy built JavaScript assets to the Streamlit static directory
    static_dir = streamlit_dest / "static"
    static_dir.mkdir(exist_ok=True)
    
    js_assets_dir = static_dir / "js"
    css_assets_dir = static_dir / "css"
    js_assets_dir.mkdir(exist_ok=True)
    css_assets_dir.mkdir(exist_ok=True)
    
    # Copy built assets
    dist_dir = JS_DIR / "dist"
    if dist_dir.exists():
        for file in dist_dir.glob("*.js"):
            shutil.copy2(file, js_assets_dir)
        for file in dist_dir.glob("*.css"):
            shutil.copy2(file, css_assets_dir)
    
    # 5. Create package files
    create_package_files(package_dir)
    
    # 6. Create deployment configuration
    create_deployment_config(package_dir)
    
    logger.info(f"Unified package created at: {package_dir}")
    return True

def build_js_components():
    """Build the JavaScript components using Deno"""
    logger.info("Building JavaScript components using Deno...")
    
    if not JS_DIR.exists():
        logger.error(f"JavaScript directory not found: {JS_DIR}")
        return False
    
    original_cwd = os.getcwd()
    
    try:
        # Change to JS directory
        os.chdir(JS_DIR)
        
        # Check if we have Deno available
        try:
            subprocess.run(["deno", "--version"], check=True, capture_output=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            logger.error("Deno not found. Please install Deno first.")
            return False
        
        # Create a simple Deno build script for our components
        build_script = '''
// Deno build script for Margadarsaka components
import { ensureDir } from "https://deno.land/std@0.208.0/fs/ensure_dir.ts";

async function buildComponents() {
  console.log("Building components with Deno...");
  
  // Ensure dist directory exists
  await ensureDir("./dist");
  
  // Read and process the rating component
  try {
    const ratingComponentPath = "./src/rating_component.js";
    const componentExists = await Deno.stat(ratingComponentPath).catch(() => false);
    
    if (componentExists) {
      console.log("Processing rating_component.js...");
      const content = await Deno.readTextFile(ratingComponentPath);
      
      // Simple processing - in a real scenario, you might want to minify or transform
      const processedContent = `// Built with Deno\\n${content}`;
      
      await Deno.writeTextFile("./dist/rating_component.js", processedContent);
      console.log("rating_component.js built");
    } else {
      console.log("No rating_component.js found, creating placeholder...");
      const placeholderContent = `
// Placeholder rating component
console.log("Rating component placeholder loaded");
export default function ratingComponent() {
  return { initialized: true };
}
`;
      await Deno.writeTextFile("./dist/rating_component.js", placeholderContent);
    }
    
    // Copy any CSS files
    try {
      const cssContent = await Deno.readTextFile("./style/main.css").catch(() => "/* No CSS found */");
      await Deno.writeTextFile("./dist/main.css", cssContent);
      console.log("CSS files processed");
    } catch (e) {
      console.log("No CSS files found, creating empty CSS");
      await Deno.writeTextFile("./dist/main.css", "/* Generated CSS */");
    }
    
    // Create a simple index.html for components
    const indexHtml = `<!DOCTYPE html>
<html>
<head>
    <title>Margadarsaka Components</title>
    <link rel="stylesheet" href="main.css">
</head>
<body>
    <div id="components-root"></div>
    <script type="module" src="rating_component.js"></script>
</body>
</html>`;
    
    await Deno.writeTextFile("./dist/index.html", indexHtml);
    console.log("index.html created");
    
    console.log("Build completed successfully!");
    
  } catch (error) {
    console.error("Build failed:", error);
    Deno.exit(1);
  }
}

if (import.meta.main) {
  await buildComponents();
}
'''
        
        # Write the build script
        with open("build_with_deno.ts", "w") as f:
            f.write(build_script)
        
        # Run the Deno build script
        logger.info("Running Deno build script...")
        result = subprocess.run([
            "deno", "run", 
            "--allow-read", "--allow-write", 
            "build_with_deno.ts"
        ], check=True, capture_output=True, text=True)
        
        logger.info("Deno build output:")
        logger.info(result.stdout)
        
        if result.stderr:
            logger.warning(f"Deno build warnings: {result.stderr}")
        
        # Verify that dist directory was created
        if not (JS_DIR / "dist").exists():
            logger.error("Build failed: dist directory not created")
            return False
            
        logger.info("JavaScript components built successfully with Deno!")
        return True
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Deno build failed: {e}")
        logger.error(f"Stderr: {e.stderr.decode() if hasattr(e, 'stderr') and e.stderr else 'No stderr'}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error during Deno build: {e}")
        return False
    finally:
        os.chdir(original_cwd)

def create_package_files(package_dir):
    """Create necessary package files"""
    
    # Create pyproject.toml instead of requirements.txt for uv
    pyproject_content = '''[project]
name = "margadarsaka"
version = "1.0.0"
description = "AI-Powered Career Guidance Platform"
readme = "README.md"
requires-python = ">=3.10"
license = {text = "MIT"}
authors = [
    {name = "Dakshx-Gupta", email = "your-email@example.com"}
]
keywords = ["career", "ai", "guidance", "streamlit", "appwrite"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: End Users/Desktop",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
]

dependencies = [
    "streamlit>=1.49.0",
    "streamlit-component-lib>=2.0.0",
    "appwrite>=17.0.0",
    "pandas>=1.5.0",
    "numpy>=1.24.0",
    "plotly>=5.0.0",
    "python-dotenv>=1.0.0",
    "pydantic>=2.0.0",
    "requests>=2.31.0",
    "PyPDF2>=3.0.0",
    "python-docx>=0.8.11",
    "spacy>=3.7.0",
    "scikit-learn>=1.3.0"
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "black>=23.0.0",
    "ruff>=0.1.0",
    "mypy>=1.0.0"
]

[project.scripts]
margadarsaka = "margadarsaka.ui_modern:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["margadarsaka"]

[tool.hatch.build.targets.wheel.force-include]
"margadarsaka/static" = "margadarsaka/static"

[tool.ruff]
line-length = 88
target-version = "py310"

[tool.ruff.lint]
select = ["E", "F", "W", "I", "N", "UP", "B", "A", "C4", "T20"]
ignore = ["E501", "B008"]

[tool.mypy]
python_version = "3.10"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
'''
    
    with open(package_dir / "pyproject.toml", "w") as f:
        f.write(pyproject_content)
    
    # Create uv.lock file (will be generated by uv, but we can create a placeholder)
    uv_lock_content = '''# This file is automatically generated by uv.
# To update, run `uv lock`.
version = 1
requires-python = ">=3.10"
'''
    
    with open(package_dir / "uv.lock", "w") as f:
        f.write(uv_lock_content)
    
    # Create __init__.py files
    (package_dir / "margadarsaka" / "__init__.py").touch()
    
    # Create a run script that uses uv
    run_script = '''#!/usr/bin/env python3
"""
Run Margadarsaka application using uv
"""
import streamlit.web.cli as stcli
import sys
import subprocess
from pathlib import Path

def main():
    """Main entry point for the application"""
    # Get the directory where this script is located
    app_dir = Path(__file__).parent
    app_file = app_dir / "margadarsaka" / "ui_modern.py"
    
    # Check if we're in a uv environment, if not, use uv run
    if "UV_PROJECT_ENVIRONMENT" in os.environ or "VIRTUAL_ENV" in os.environ:
        # We're already in a virtual environment, run directly
        sys.argv = [
            "streamlit",
            "run",
            str(app_file),
            "--server.port=8501",
            "--server.address=0.0.0.0"
        ]
        sys.exit(stcli.main())
    else:
        # Use uv run to execute in the project environment
        cmd = [
            "uv", "run", "streamlit", "run", str(app_file),
            "--server.port=8501", "--server.address=0.0.0.0"
        ]
        sys.exit(subprocess.call(cmd))

if __name__ == "__main__":
    import os
    main()
'''
    
    with open(package_dir / "run.py", "w") as f:
        f.write(run_script)

def create_deployment_config(package_dir):
    """Create deployment configuration files"""
    
    # Create Dockerfile that uses uv
    dockerfile_content = '''# Use the official Python image with uv pre-installed
FROM ghcr.io/astral-sh/uv:python3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \\
    curl \\
    && apt-get clean \\
    && rm -rf /var/lib/apt/lists/*

# Copy the project files
COPY pyproject.toml uv.lock ./

# Install dependencies using uv
RUN uv sync --frozen

# Copy the application
COPY . .

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run the application using uv
CMD ["uv", "run", "python", "run.py"]
'''
    
    with open(package_dir / "Dockerfile", "w") as f:
        f.write(dockerfile_content)
    
    # Create .dockerignore
    dockerignore_content = '''
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
.venv/
.uv-cache/
pip-log.txt
pip-delete-this-directory.txt
.tox
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.log
.git
.mypy_cache
.pytest_cache
.hypothesis
.DS_Store
node_modules/
starter-for-js/node_modules/
starter-for-js/dist/
'''
    
    with open(package_dir / ".dockerignore", "w") as f:
        f.write(dockerignore_content)
    
    # Create appwrite.json for Sites deployment
    appwrite_config = {
        "projectId": "margadarsaka",
        "projectName": "Margadarsaka - AI Career Advisor",
        "platforms": [
            {
                "type": "web",
                "name": "Margadarsaka Web App",
                "hostname": "margadarsaka.appwrite.io"
            }
        ]
    }
    
    with open(package_dir / "appwrite.json", "w") as f:
        json.dump(appwrite_config, f, indent=2)

def create_zip_for_upload():
    """Create a zip file ready for Appwrite Sites upload"""
    logger.info("Creating zip file for Appwrite Sites upload...")
    
    package_dir = ROOT_DIR / "margadarsaka_unified"
    if not package_dir.exists():
        logger.error("Unified package not found. Run create_unified_package() first.")
        return False
    
    # Create zip file
    zip_path = ROOT_DIR / "margadarsaka_for_appwrite.zip"
    
    # Remove existing zip if it exists
    if zip_path.exists():
        zip_path.unlink()
    
    # Create the zip
    shutil.make_archive(
        str(zip_path.with_suffix('')),
        'zip',
        package_dir
    )
    
    logger.info(f"Zip file created: {zip_path}")
    logger.info(f"File size: {zip_path.stat().st_size / (1024*1024):.2f} MB")
    
    return True

def main():
    """Main function to create the integrated package"""
    logger.info("Starting Margadarsaka integration process...")
    
    # Step 1: Create unified package
    if not create_unified_package():
        logger.error("Failed to create unified package")
        return False
    
    # Step 2: Create zip for upload
    if not create_zip_for_upload():
        logger.error("Failed to create zip file")
        return False
    
    logger.info("Integration complete!")
    logger.info("\nNext steps for Appwrite Sites deployment:")
    logger.info("1. Upload margadarsaka_for_appwrite.zip to Appwrite Sites")
    logger.info("2. Configure build settings:")
    logger.info("   - Install command: curl -LsSf https://astral.sh/uv/install.sh | sh && uv sync")
    logger.info("   - Build command: (leave empty - JavaScript components built with Deno)")
    logger.info("   - Output directory: ./")
    logger.info("3. Set environment variables as needed:")
    logger.info("   - APPWRITE_ENDPOINT: Your Appwrite endpoint")
    logger.info("   - APPWRITE_PROJECT_ID: Your project ID")
    logger.info("   - Any other environment variables needed")
    logger.info("4. Deploy!")
    logger.info("\nAlternatively, you can run locally with:")
    logger.info("   cd margadarsaka_unified")
    logger.info("   uv run python run.py")
    logger.info("\nNote: JavaScript components were built using Deno (no Node.js required)")
    
    return True

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Integrate Margadarsaka for deployment")
    parser.add_argument("--package-only", action="store_true", help="Create package only, don't zip")
    parser.add_argument("--zip-only", action="store_true", help="Create zip only (assumes package exists)")
    
    args = parser.parse_args()
    
    if args.package_only:
        create_unified_package()
    elif args.zip_only:
        create_zip_for_upload()
    else:
        main()