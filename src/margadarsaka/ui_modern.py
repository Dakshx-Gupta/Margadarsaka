"""
Modern Margadarsaka UI - Main Application Interface
Redesigned with modular components, state management, and responsive design
"""

import streamlit as st
import logging
from typing import Optional, Dict, Any
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration with performance optimizations
st.set_page_config(
    page_title="Margadarsaka - AI Career Advisor",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Add resource hints for better performance
st.markdown(
    """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="dns-prefetch" href="https://fonts.googleapis.com">
<link rel="dns-prefetch" href="https://fonts.gstatic.com">
""",
    unsafe_allow_html=True,
)

# Import application components
try:
    # UI utilities
    from margadarsaka.ui.utils.styling import apply_custom_css, inject_custom_js
    from margadarsaka.ui.utils.state_manager import init_state, get_state_manager
    from margadarsaka.ui.utils.i18n import get_text, set_language, Language

    # Navigation and components
    from margadarsaka.ui.components.navigation import render_navigation
    from margadarsaka.ui.components.navigation import PageType as NavigationPageType

    PageType = NavigationPageType  # Use the imported one
    from margadarsaka.ui.components.auth_components import show_authentication_modal

    # Services
    from margadarsaka.services.appwrite_service import AppwriteService
    from margadarsaka.secrets import SecretsManager

    COMPONENTS_AVAILABLE = True
    logger.info("✅ All UI components loaded successfully")

except ImportError as e:
    logger.error(f"❌ Failed to import UI components: {e}")
    COMPONENTS_AVAILABLE = False

    # Fallback implementations
    def apply_custom_css():
        st.markdown(
            "<style>body { font-family: Arial, sans-serif; }</style>",
            unsafe_allow_html=True,
        )

    def inject_custom_js():
        pass

    def get_text(key: str, default: Optional[str] = None, **kwargs) -> str:
        return default or key

    class MockState:
        def get(self, key: str, default=None):
            return getattr(st.session_state, key, default)

        def set(self, key: str, value):
            setattr(st.session_state, key, value)

    def init_state():
        return MockState()

    def render_navigation():
        """Fallback navigation"""
        st.sidebar.title("Navigation")
        page = st.sidebar.selectbox(
            "Go to:",
            [
                "Home",
                "Assessment",
                "Resume",
                "Chat",
                "Recommendations",
                "Resources",
                "Profile",
            ],
        )
        return page.lower()

    def show_authentication_modal(service=None):
        return None


def initialize_app():
    """Initialize the application with all necessary configurations"""

    # Apply custom styling
    apply_custom_css()
    inject_custom_js()

    # Initialize state management
    state = init_state()

    # Initialize secrets and services
    try:
        secrets_manager = SecretsManager()
        if "appwrite_service" not in st.session_state:
            st.session_state.appwrite_service = AppwriteService()
            logger.info("✅ Appwrite service initialized")
    except Exception as e:
        logger.warning(f"⚠️ Service initialization failed: {e}")
        st.session_state.appwrite_service = None

    return state


def show_welcome_banner():
    """Display a beautiful welcome banner"""
    st.markdown(
        f"""
    <div style="background: linear-gradient(135deg, #1E88E5 0%, #8E24AA 100%); 
                padding: 2.5rem 2rem; 
                border-radius: 16px; 
                margin-bottom: 2.5rem; 
                text-align: center;
                box-shadow: 0 10px 30px rgba(30, 136, 229, 0.2);"
                class="fade-in">
        <h1 style="color: white; margin: 0; font-size: 3.2rem; font-weight: 700; letter-spacing: -0.02em;">
            🚀 {get_text("app_title", "Margadarsaka")}
        </h1>
        <p style="color: rgba(255,255,255,0.95); margin: 1.2rem 0 0 0; font-size: 1.4rem; font-weight: 400; max-width: 800px; margin-left: auto; margin-right: auto;">
            {get_text("app_subtitle", "AI-Powered Career Guidance with Psychological Assessment")}
        </p>
        <p style="color: rgba(255,255,255,0.85); margin: 0.8rem 0 0 0; font-size: 1.1rem; max-width: 700px; margin-left: auto; margin-right: auto;">
            {get_text("welcome_message", "Discover your ideal career path with personalized AI guidance")}
        </p>
        <div style="margin-top: 1.5rem;">
            <span style="background-color: rgba(255,255,255,0.2); color: white; border-radius: 50px; padding: 0.4rem 1rem; font-size: 0.9rem; margin: 0 0.3rem; display: inline-block;">🧠 Psychological Assessment</span>
            <span style="background-color: rgba(255,255,255,0.2); color: white; border-radius: 50px; padding: 0.4rem 1rem; font-size: 0.9rem; margin: 0 0.3rem; display: inline-block;">🤖 AI Chat</span>
            <span style="background-color: rgba(255,255,255,0.2); color: white; border-radius: 50px; padding: 0.4rem 1rem; font-size: 0.9rem; margin: 0 0.3rem; display: inline-block;">📄 Resume Analysis</span>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )


def show_home_page():
    """Modern home page with interactive elements"""

    show_welcome_banner()

    # Feature highlights
    st.markdown(f"## 🌟 {get_text('key_features', 'Key Features')}")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            f"""
        <div class="feature-card fade-in">
            <div style="text-align: center; padding: 1.2rem;">
                <div style="font-size: 3.2em; margin-bottom: 1.2rem; background: var(--gradient-primary); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">🧠</div>
                <h3 style="color: var(--primary-color); margin: 0; font-size: 1.4rem; font-weight: 600;">
                    {get_text("psychological_assessment", "Psychological Assessment")}
                </h3>
                <p style="margin: 1.2rem 0; color: var(--text-secondary); line-height: 1.6;">
                    {get_text("assessment_desc", "Discover your personality traits, interests, and cognitive abilities through scientifically-backed assessments.")}
                </p>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        if st.button(
            "🎯 " + get_text("start_assessment", "Start Assessment"),
            use_container_width=True,
            type="primary",
        ):
            st.session_state.current_page = PageType.ASSESSMENT.value
            st.rerun()

    with col2:
        st.markdown(
            f"""
        <div class="feature-card fade-in">
            <div style="text-align: center; padding: 1.2rem;">
                <div style="font-size: 3.2em; margin-bottom: 1.2rem; background: var(--gradient-primary); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">🤖</div>
                <h3 style="color: var(--primary-color); margin: 0; font-size: 1.4rem; font-weight: 600;">
                    {get_text("ai_career_chat", "AI Career Chat")}
                </h3>
                <p style="margin: 1.2rem 0; color: var(--text-secondary); line-height: 1.6;">
                    {get_text("chat_desc", "Get instant, personalized career advice from our AI advisor trained on Indian job market data.")}
                </p>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        if st.button(
            "💬 " + get_text("chat_now", "Chat Now"),
            use_container_width=True,
            type="primary",
        ):
            st.session_state.current_page = PageType.CHAT.value
            st.rerun()

    with col3:
        st.markdown(
            f"""
        <div class="feature-card fade-in">
            <div style="text-align: center; padding: 1.2rem;">
                <div style="font-size: 3.2em; margin-bottom: 1.2rem; background: var(--gradient-primary); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">📄</div>
                <h3 style="color: var(--primary-color); margin: 0; font-size: 1.4rem; font-weight: 600;">
                    {get_text("resume_analysis", "Resume Analysis")}
                </h3>
                <p style="margin: 1.2rem 0; color: var(--text-secondary); line-height: 1.6;">
                    {get_text("resume_desc", "Get AI-powered insights on your resume with suggestions for improvement and ATS optimization.")}
                </p>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        if st.button(
            "📊 " + get_text("analyze_resume", "Analyze Resume"),
            use_container_width=True,
            type="primary",
        ):
            st.session_state.current_page = PageType.RESUME.value
            st.rerun()

    # Success stories or testimonials
    st.markdown("---")
    st.markdown(f"## 🎉 {get_text('success_stories', 'Success Stories')}")

    testimonial_col1, testimonial_col2 = st.columns(2)

    with testimonial_col1:
        st.markdown(
            f"""
        <div class="success-card fade-in">
            <div style="position: absolute; top: -10px; right: 15px; font-size: 2rem; opacity: 0.2;">❝</div>
            <blockquote style="margin: 0; font-style: italic; position: relative; z-index: 1; line-height: 1.6;">
                "{get_text("testimonial_1", "Margadarsaka helped me discover my passion for data science. The psychological assessment was spot-on!")}"
            </blockquote>
            <div style="display: flex; align-items: center; margin-top: 1rem;">
                <div style="width: 40px; height: 40px; border-radius: 50%; background: var(--primary-color); color: white; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 1.2rem; margin-right: 12px;">P</div>
                <div>
                    <p style="margin: 0; font-weight: bold;">Priya S.</p>
                    <p style="margin: 0; font-size: 0.85rem; color: var(--text-secondary);">Data Scientist</p>
                </div>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with testimonial_col2:
        st.markdown(
            f"""
        <div class="success-card fade-in" style="animation-delay: 0.2s;">
            <div style="position: absolute; top: -10px; right: 15px; font-size: 2rem; opacity: 0.2;">❝</div>
            <blockquote style="margin: 0; font-style: italic; position: relative; z-index: 1; line-height: 1.6;">
                "{get_text("testimonial_2", "The AI chat feature gave me clarity about my career transition. Highly recommended!")}"
            </blockquote>
            <div style="display: flex; align-items: center; margin-top: 1rem;">
                <div style="width: 40px; height: 40px; border-radius: 50%; background: var(--secondary-color); color: white; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 1.2rem; margin-right: 12px;">A</div>
                <div>
                    <p style="margin: 0; font-weight: bold;">Arjun K.</p>
                    <p style="margin: 0; font-size: 0.85rem; color: var(--text-secondary);">Software Engineer</p>
                </div>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    # Call to action
    st.markdown("---")
    st.markdown(
        f"""
    <div class="feature-card text-center fade-in" style="background: linear-gradient(to right bottom, rgba(30, 136, 229, 0.05), rgba(142, 36, 170, 0.05)); padding: var(--spacing-xl) var(--spacing-lg); margin-top: var(--spacing-xl); border-top: 4px solid var(--primary-color); box-shadow: var(--shadow-md); animation-delay: 0.4s;">
        <h2 style="color: var(--primary-color); font-size: 2rem; margin-bottom: var(--spacing-md); font-weight: 700;">
            {get_text("ready_to_start", "Ready to Start Your Career Journey?")}
        </h2>
        <p style="font-size: 1.2em; margin: 1.2rem auto; max-width: 700px; color: var(--text-secondary); line-height: 1.6;">
            {get_text("cta_message", "Join thousands of users who have found their ideal career path with Margadarsaka.")}
        </p>
        <div style="margin-top: var(--spacing-lg);">
            <div style="display: flex; justify-content: center; gap: 20px; flex-wrap: wrap;">
                <div style="display: flex; align-items: center;">
                    <div style="color: var(--primary-color); font-size: 1.5rem; margin-right: 8px;">✓</div>
                    <div>Free Assessment</div>
                </div>
                <div style="display: flex; align-items: center;">
                    <div style="color: var(--primary-color); font-size: 1.5rem; margin-right: 8px;">✓</div>
                    <div>Personalized Reports</div>
                </div>
                <div style="display: flex; align-items: center;">
                    <div style="color: var(--primary-color); font-size: 1.5rem; margin-right: 8px;">✓</div>
                    <div>AI-Powered Guidance</div>
                </div>
            </div>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    cta_col1, cta_col2, cta_col3 = st.columns([1, 2, 1])
    with cta_col2:
        if not st.session_state.get("user_authenticated", False):
            if st.button(
                "🚀 " + get_text("get_started", "Get Started - It's Free!"),
                use_container_width=True,
                type="primary",
            ):
                st.session_state.show_auth = True
                st.rerun()
        else:
            if st.button(
                "📊 " + get_text("view_dashboard", "View Your Dashboard"),
                use_container_width=True,
                type="primary",
            ):
                st.session_state.current_page = PageType.PROFILE.value
                st.rerun()


def show_assessment_page():
    """Psychological assessment page"""
    try:
        from margadarsaka.ui.pages.assessment import (
            show_assessment_page as assessment_show,
        )

        assessment_show()
    except ImportError:
        st.markdown(
            f"# 🧠 {get_text('psychological_assessment', 'Psychological Assessment')}"
        )
        st.info(
            get_text(
                "assessment_coming_soon",
                "Advanced psychological assessment coming soon!",
            )
        )

        # Placeholder content
        st.markdown(f"""
        ### {get_text("what_to_expect", "What to Expect")}
        
        Our comprehensive psychological assessment includes:
        
        - **Personality Analysis**: Big Five personality traits
        - **Interest Inventory**: Holland's career interest themes  
        - **Skills Assessment**: Cognitive and technical abilities
        - **Values Clarification**: Work and life priorities
        - **Career Readiness**: Preparation for career decisions
        
        {get_text("assessment_time", "Estimated completion time: 45-60 minutes")}
        """)


def show_resume_page():
    """Resume analysis page"""
    try:
        from margadarsaka.ui.pages.resume import show_resume_page as resume_show

        resume_show()
    except ImportError:
        st.markdown(f"# 📄 {get_text('resume_analysis', 'Resume Analysis')}")

        uploaded_file = st.file_uploader(
            get_text("upload_resume", "Upload your resume"),
            type=["pdf", "docx", "txt"],
            help=get_text("resume_help", "Supported formats: PDF, DOCX, TXT"),
        )

        if uploaded_file:
            st.success(get_text("resume_uploaded", "Resume uploaded successfully!"))
            st.info(
                get_text(
                    "analysis_coming_soon", "AI-powered resume analysis coming soon!"
                )
            )


def show_chat_page():
    """AI career chat page"""
    try:
        from margadarsaka.ui.pages.chat import show_chat_page as chat_show

        chat_show()
    except ImportError:
        st.markdown(f"# 🤖 {get_text('ai_career_chat', 'AI Career Chat')}")

        # Simple chat interface placeholder
        if "chat_messages" not in st.session_state:
            st.session_state.chat_messages = [
                {
                    "role": "assistant",
                    "content": get_text(
                        "chat_welcome",
                        "Hello! I'm your AI career advisor. How can I help you today?",
                    ),
                }
            ]

        # Display chat messages
        for message in st.session_state.chat_messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])

        # Chat input
        if prompt := st.chat_input(
            get_text("type_message", "Type your message here...")
        ):
            st.session_state.chat_messages.append({"role": "user", "content": prompt})

            # Add AI response (placeholder)
            response = get_text(
                "ai_response_placeholder",
                "Thank you for your question. Advanced AI responses coming soon!",
            )
            st.session_state.chat_messages.append(
                {"role": "assistant", "content": response}
            )
            st.rerun()


def show_recommendations_page():
    """Career recommendations page"""
    try:
        from margadarsaka.ui.pages.recommendations import RecommendationsPage

        recommendations_page = RecommendationsPage()
        recommendations_page.render()
    except ImportError:
        st.markdown(
            f"# 📋 {get_text('career_recommendations', 'Career Recommendations')}"
        )
        st.info(
            get_text(
                "recommendations_coming_soon",
                "Personalized career recommendations coming soon!",
            )
        )


def show_resources_page():
    """Learning resources page"""
    try:
        from margadarsaka.ui.pages.resources import ResourcesPage

        resources_page = ResourcesPage()
        resources_page.render()
    except ImportError:
        st.markdown(f"# 📚 {get_text('learning_resources', 'Learning Resources')}")
        st.info(
            get_text("resources_coming_soon", "Curated learning resources coming soon!")
        )


def show_profile_page():
    """User profile page"""
    try:
        from margadarsaka.ui.pages.profile import ProfilePage

        profile_page = ProfilePage()
        profile_page.render()
    except ImportError:
        st.markdown(f"# 👤 {get_text('profile', 'Profile')}")

        if st.session_state.get("user_authenticated", False):
            from margadarsaka.ui.components.forms import ProfileForm

            profile_form = ProfileForm()
            profile_form.render()
        else:
            st.warning(get_text("login_required", "Please login to view your profile."))


def route_page(page_type: str):
    """Route to the appropriate page based on page type"""

    page_functions = {
        "home": show_home_page,
        "assessment": show_assessment_page,
        "resume": show_resume_page,
        "chat": show_chat_page,
        "recommendations": show_recommendations_page,
        "resources": show_resources_page,
        "profile": show_profile_page,
    }

    page_function = page_functions.get(page_type, show_home_page)
    page_function()


def main():
    """Main application entry point"""

    # Initialize the application
    state = initialize_app()

    # Handle authentication modal
    if st.session_state.get("show_auth", False):
        appwrite_service = st.session_state.get("appwrite_service")
        user = show_authentication_modal(appwrite_service)

        if user:
            st.session_state.user_authenticated = True
            st.session_state.current_user = user
            st.session_state.show_auth = False
            st.rerun()

        # Show close button for auth modal
        if st.button("❌ " + get_text("close", "Close"), key="close_auth"):
            st.session_state.show_auth = False
            st.rerun()

        return

    # Render navigation and get current page
    current_page = render_navigation()

    # Main content area
    with st.container():
        # Route to appropriate page
        if isinstance(current_page, str):
            route_page(current_page)
        else:
            route_page(current_page.value if hasattr(current_page, "value") else "home")

    # Footer
    st.markdown("---")
    st.markdown(
        f"""
    <div style="text-align: center; color: var(--text-muted); padding: 2rem 0;">
        <p>© 2025 Margadarsaka - {get_text("made_with_love", "Made with ❤️ in India")}</p>
        <p>
            <a href="#" style="color: var(--primary-color); text-decoration: none;">{get_text("privacy", "Privacy")}</a> | 
            <a href="#" style="color: var(--primary-color); text-decoration: none;">{get_text("terms", "Terms")}</a> | 
            <a href="#" style="color: var(--primary-color); text-decoration: none;">{get_text("support", "Support")}</a>
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
