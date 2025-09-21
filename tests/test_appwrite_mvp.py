"""
Appwrite MVP Test for Margadarsaka
This is a proof-of-concept implementation showing Appwrite integration
for authentication, database operations, and file storage.
"""

import streamlit as st
import sys
import os
import asyncio
from pathlib import Path

# Add src to path for imports
current_dir = Path(__file__).parent
src_path = current_dir / "src"
sys.path.insert(0, str(src_path))

# Import our services
try:
    from margadarsaka.services.appwrite_service import (
        appwrite_service,
        get_appwrite_health,
    )
    from margadarsaka.ui.appwrite_components import (
        inject_appwrite_sdk,
        appwrite_auth_component,
        appwrite_file_upload_component,
        handle_appwrite_messages,
        get_appwrite_config,
    )

    IMPORTS_OK = True
except ImportError as e:
    st.error(f"Import error: {e}")
    st.error("Some features may not work. Check if all dependencies are installed.")
    IMPORTS_OK = False

    # Create mock functions for testing
    def inject_appwrite_sdk():
        st.info("📝 Mock: Appwrite SDK would be injected here")

    def appwrite_auth_component():
        st.info("📝 Mock: Authentication component would be rendered here")
        return None

    def appwrite_file_upload_component():
        st.info("📝 Mock: File upload component would be rendered here")

    def handle_appwrite_messages():
        return {"user": None, "logged_in": False}

    def get_appwrite_config():
        return {
            "endpoint": "https://cloud.appwrite.io/v1",
            "project_id": "not_configured",
            "database_id": "main",
            "storage_bucket_id": "files",
        }

    def get_appwrite_health():
        return {
            "configured": False,
            "endpoint": None,
            "project_id": None,
            "database_id": "main",
            "connection": "not_configured",
            "timestamp": "2025-09-20T12:00:00Z",
        }

    class MockAppwriteService:
        def is_configured(self):
            return False

    appwrite_service = MockAppwriteService()

# Page configuration
st.set_page_config(
    page_title="Margadarsaka - Appwrite MVP",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
st.markdown(
    """
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        border-bottom: 2px solid #e0e0e0;
        margin-bottom: 2rem;
    }
    .status-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #007bff;
        margin: 1rem 0;
    }
    .success-card {
        background: #d4edda;
        border-left-color: #28a745;
    }
    .error-card {
        background: #f8d7da;
        border-left-color: #dc3545;
    }
</style>
""",
    unsafe_allow_html=True,
)


def main():
    """Main application function."""

    if not IMPORTS_OK:
        st.warning("⚠️ Some imports failed. Running in limited mode.")
        st.markdown("**Missing components:**")
        st.markdown("- Appwrite service integration")
        st.markdown("- Authentication components")
        st.markdown("- File upload components")
        return

    # Header
    st.markdown(
        """
    <div class="main-header">
        <h1>🎯 Margadarsaka Appwrite MVP</h1>
        <p>Testing Backend-as-a-Service Integration</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Initialize Appwrite SDK in browser
    inject_appwrite_sdk()

    # Sidebar for navigation
    st.sidebar.title("🚀 MVP Features")
    page = st.sidebar.selectbox(
        "Choose a feature to test:",
        [
            "🏠 Overview",
            "🔍 Health Check",
            "🔐 Authentication",
            "💾 Database Operations",
            "📁 File Storage",
            "⚙️ Configuration",
        ],
    )

    if page == "🏠 Overview":
        show_overview()
    elif page == "🔍 Health Check":
        show_health_check()
    elif page == "🔐 Authentication":
        show_authentication()
    elif page == "💾 Database Operations":
        show_database_operations()
    elif page == "📁 File Storage":
        show_file_storage()
    elif page == "⚙️ Configuration":
        show_configuration()


def show_overview():
    """Show overview of Appwrite integration."""

    st.header("📋 Appwrite Integration Overview")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("✅ What's Working")
        st.markdown("""
        - **Python SDK**: Installed and configured
        - **JavaScript SDK**: Injected via CDN
        - **Service Wrapper**: Complete abstraction layer
        - **Environment Config**: Doppler + .env support
        - **Streamlit Components**: Auth, upload, database
        """)

    with col2:
        st.subheader("🎯 MVP Features")
        st.markdown("""
        - **User Authentication**: Login, register, OAuth
        - **User Profiles**: Create and manage user data
        - **Assessment Storage**: Save RIASEC results
        - **Career Recommendations**: Store AI suggestions
        - **File Upload**: Resume and document storage
        """)

    st.subheader("🏗️ Architecture")

    st.markdown("""
    ```
    Frontend (Streamlit)
    ├── JavaScript SDK (Client-side auth, real-time)
    └── Python Integration
        ├── Appwrite Service Wrapper
        ├── Doppler/Environment Config
        └── Backend Operations
    
    Appwrite Cloud/Self-hosted
    ├── Authentication Service
    ├── Database (Documents)
    ├── Storage (Files)
    └── Functions (Future: AI processing)
    ```
    """)

    # Quick status check
    health = get_appwrite_health()
    if health["configured"]:
        st.success("🎉 Appwrite is configured and ready!")
    else:
        st.warning("⚠️ Appwrite configuration incomplete. Check environment variables.")


def show_health_check():
    """Show Appwrite service health status."""

    st.header("🔍 Appwrite Health Check")

    with st.spinner("Checking Appwrite service health..."):
        health = get_appwrite_health()

    # Overall status
    if health["configured"]:
        if health.get("connection") == "healthy":
            st.markdown(
                '<div class="status-card success-card"><h3>✅ Appwrite Service: Healthy</h3></div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                '<div class="status-card error-card"><h3>❌ Appwrite Service: Connection Error</h3></div>',
                unsafe_allow_html=True,
            )
    else:
        st.markdown(
            '<div class="status-card error-card"><h3>⚠️ Appwrite Service: Not Configured</h3></div>',
            unsafe_allow_html=True,
        )

    # Detailed status
    st.subheader("📊 Detailed Status")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Configuration:**")
        st.json(
            {
                "Configured": health["configured"],
                "Endpoint": health["endpoint"] or "Not set",
                "Project ID": health["project_id"] or "Not set",
                "Database ID": health["database_id"] or "Not set",
            }
        )

    with col2:
        st.markdown("**Connection:**")
        connection_status = {
            "Status": health.get("connection", "unknown"),
            "Timestamp": health["timestamp"],
        }
        if "error" in health:
            connection_status["Error"] = health["error"]
        st.json(connection_status)

    # Refresh button
    if st.button("🔄 Refresh Health Check"):
        st.rerun()


def show_authentication():
    """Show authentication features."""

    st.header("🔐 Authentication Demo")

    st.markdown("""
    This demonstrates Appwrite's authentication system with:
    - Email/password login and registration
    - OAuth integration (Google, GitHub)
    - Session management
    - Real-time state updates
    """)

    # Authentication component
    st.subheader("🚪 Login / Register")
    auth_result = appwrite_auth_component()

    # Handle authentication messages
    auth_state = handle_appwrite_messages()

    # Show current authentication state
    st.subheader("📊 Current Auth State")
    if auth_state["logged_in"]:
        st.success(f"✅ Logged in as: {auth_state['user']['email']}")
        st.json(auth_state["user"])
    else:
        st.info("ℹ️ Not logged in")

    # Additional auth features
    st.subheader("🔧 Additional Features")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Available OAuth Providers:**")
        st.markdown("- Google")
        st.markdown("- GitHub")
        st.markdown("- Facebook (configurable)")
        st.markdown("- Apple (configurable)")

    with col2:
        st.markdown("**Security Features:**")
        st.markdown("- Argon2 password hashing")
        st.markdown("- Session management")
        st.markdown("- MFA support")
        st.markdown("- JWT tokens")


def show_database_operations():
    """Show database operations."""

    st.header("💾 Database Operations Demo")

    if not appwrite_service.is_configured():
        st.error("Appwrite not configured. Please check your environment variables.")
        return

    # User Profile Operations
    st.subheader("👤 User Profile Operations")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Create User Profile:**")
        with st.form("create_user"):
            name = st.text_input("Name", "John Doe")
            email = st.text_input("Email", "john.doe@example.com")
            age = st.number_input("Age", 25, 100, 30)
            skills = st.text_area(
                "Skills (comma-separated)", "Python, AI, Career Counseling"
            )

            if st.form_submit_button("Create Profile"):
                with st.spinner("Creating user profile..."):
                    user_data = {
                        "name": name,
                        "email": email,
                        "age": age,
                        "skills": [s.strip() for s in skills.split(",")],
                    }

                    # This would normally be async, but for demo we'll simulate
                    try:
                        st.success("✅ User profile created! (Simulated)")
                        st.json(user_data)
                    except Exception as e:
                        st.error(f"❌ Error: {e}")

    with col2:
        st.markdown("**Assessment Results:**")
        with st.form("save_assessment"):
            assessment_type = st.selectbox(
                "Assessment Type", ["RIASEC", "Big Five", "Skills"]
            )
            scores = st.text_area(
                "Scores (JSON format)",
                '{"realistic": 80, "investigative": 90, "artistic": 60}',
            )

            if st.form_submit_button("Save Assessment"):
                with st.spinner("Saving assessment..."):
                    try:
                        import json

                        assessment_data = {
                            "type": assessment_type,
                            "scores": json.loads(scores),
                            "completed_at": "2025-09-20T12:00:00Z",
                        }
                        st.success("✅ Assessment saved! (Simulated)")
                        st.json(assessment_data)
                    except Exception as e:
                        st.error(f"❌ Error: {e}")

    # Career Recommendations
    st.subheader("🎯 Career Recommendations")

    with st.form("save_recommendation"):
        st.markdown("**Save Career Recommendation:**")
        career = st.text_input("Career Title", "Data Scientist")
        match_score = st.slider("Match Score", 0, 100, 85)
        reasoning = st.text_area(
            "AI Reasoning",
            "Strong analytical skills and interest in investigation align well with data science.",
        )

        if st.form_submit_button("Save Recommendation"):
            recommendation_data = {
                "career": career,
                "match_score": match_score,
                "reasoning": reasoning,
                "generated_by": "AI_Assistant",
            }
            st.success("✅ Career recommendation saved! (Simulated)")
            st.json(recommendation_data)


def show_file_storage():
    """Show file storage capabilities."""

    st.header("📁 File Storage Demo")

    if not appwrite_service.is_configured():
        st.error("Appwrite not configured. Please check your environment variables.")
        return

    st.markdown("""
    This demonstrates Appwrite's file storage capabilities:
    - Direct browser uploads
    - Secure file storage
    - Image processing
    - Access control
    """)

    # File upload component
    st.subheader("📤 Upload Files")
    appwrite_file_upload_component()

    # File management
    st.subheader("🗂️ File Management")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Supported File Types:**")
        st.markdown("- **Documents**: PDF, DOC, DOCX")
        st.markdown("- **Images**: JPG, PNG, GIF, WebP")
        st.markdown("- **Text**: TXT, CSV, JSON")
        st.markdown("- **Archives**: ZIP, RAR")

    with col2:
        st.markdown("**Storage Features:**")
        st.markdown("- **Security**: Encryption at rest")
        st.markdown("- **Scanning**: Antivirus protection")
        st.markdown("- **Processing**: Image manipulation")
        st.markdown("- **CDN**: Global distribution")

    # Example file operations
    st.subheader("🔧 File Operations")

    example_files = [
        {
            "id": "file_123",
            "name": "resume.pdf",
            "size": "2.3 MB",
            "type": "application/pdf",
        },
        {
            "id": "file_456",
            "name": "profile.jpg",
            "size": "1.1 MB",
            "type": "image/jpeg",
        },
        {
            "id": "file_789",
            "name": "assessment.json",
            "size": "15 KB",
            "type": "application/json",
        },
    ]

    for file in example_files:
        col1, col2, col3, col4 = st.columns([3, 1, 1, 1])

        with col1:
            st.write(f"📄 {file['name']}")
        with col2:
            st.write(file["size"])
        with col3:
            if st.button("View", key=f"view_{file['id']}"):
                st.info(f"Opening {file['name']} (Simulated)")
        with col4:
            if st.button("Delete", key=f"delete_{file['id']}"):
                st.warning(f"Deleted {file['name']} (Simulated)")


def show_configuration():
    """Show Appwrite configuration."""

    st.header("⚙️ Appwrite Configuration")

    config = get_appwrite_config()

    st.subheader("🔧 Current Configuration")

    # Configuration display
    config_display = {
        "Endpoint": config.get("endpoint", "Not configured"),
        "Project ID": config.get("project_id", "Not configured"),
        "Database ID": config.get("database_id", "Not configured"),
        "Storage Bucket ID": config.get("storage_bucket_id", "Not configured"),
    }

    st.json(config_display)

    # Configuration instructions
    st.subheader("📋 Setup Instructions")

    with st.expander("🌟 Appwrite Cloud Setup"):
        st.markdown("""
        1. **Create Account**: Go to [cloud.appwrite.io](https://cloud.appwrite.io)
        2. **Create Project**: Click "Create Project"
        3. **Get Project ID**: Copy from project settings
        4. **Create API Key**: Go to API Keys → Create Key
        5. **Create Database**: Go to Databases → Create Database
        6. **Create Collections**: Set up users, assessments, recommendations
        7. **Create Storage Bucket**: Go to Storage → Create Bucket
        """)

    with st.expander("🏠 Self-hosted Setup"):
        st.markdown("""
        1. **Install Docker**: Ensure Docker is running
        2. **Run Appwrite**: 
           ```bash
           docker run -it --rm --volume /var/run/docker.sock:/var/run/docker.sock --volume "$(pwd)"/appwrite:/usr/src/code/appwrite:rw --entrypoint="install" appwrite/appwrite:1.7.4
           ```
        3. **Access Console**: Open http://localhost
        4. **Configure Project**: Follow same steps as cloud
        5. **Update Endpoint**: Set to http://localhost/v1
        """)

    with st.expander("🔐 Environment Variables"):
        st.markdown("""
        Add these to your `.env` file or Doppler:
        
        ```bash
        APPWRITE_ENDPOINT=https://cloud.appwrite.io/v1
        APPWRITE_PROJECT_ID=your_project_id
        APPWRITE_API_KEY=your_api_key
        APPWRITE_DATABASE_ID=main
        APPWRITE_USERS_COLLECTION_ID=users
        APPWRITE_ASSESSMENTS_COLLECTION_ID=assessments
        APPWRITE_RECOMMENDATIONS_COLLECTION_ID=recommendations
        APPWRITE_STORAGE_BUCKET_ID=files
        ```
        """)

    # Test configuration
    st.subheader("🧪 Test Configuration")

    if st.button("🔍 Test Connection"):
        with st.spinner("Testing Appwrite connection..."):
            health = get_appwrite_health()

            if health["configured"]:
                if health.get("connection") == "healthy":
                    st.success("✅ Connection successful!")
                else:
                    st.error(
                        f"❌ Connection failed: {health.get('error', 'Unknown error')}"
                    )
            else:
                st.warning("⚠️ Configuration incomplete")


if __name__ == "__main__":
    main()
