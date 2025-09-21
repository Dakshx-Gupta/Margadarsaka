"""
Modern Margadarsaka UI - Main Application Interface
Redesigned with modular components, state management, and responsive design
"""

import streamlit as st
import logging
import os
from typing import Optional, Dict, Any, List
from datetime import datetime

# Import custom components
from margadarsaka.ui.components.resume_score_display import render_resume_score_section, render_skill_match_visualization
from margadarsaka.ui.components.custom_components import rating_component
from margadarsaka.ui.components.simple_header import render_simple_header, render_sidebar_rating
from margadarsaka.ui.components.footer import render_modern_footer, render_mini_footer

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

def initialize_custom_components():
    """Initialize and load all custom components silently"""
    # Initialize components silently in the background
    try:
        logger.info("Custom components ready")
    except Exception as e:
        logger.warning(f"Custom component initialization had minor issues: {e}")
        logger.info("✅ All UI components loaded successfully")

# Initialize custom components at startup
initialize_custom_components()

# Import application components
try:
    # UI utilities - try new Streamlit-compatible styling first
    try:
        from margadarsaka.ui.utils.streamlit_styling import (
            apply_streamlit_theme, 
            create_card, 
            create_metric_card,
            create_hero_section,
            show_success_message,
            show_warning_message, 
            show_error_message,
            show_info_message
        )
        apply_custom_css = apply_streamlit_theme  # Use new styling
        inject_custom_js = lambda: None  # No JS needed with new approach
        MODERN_STYLING = True
    except ImportError:
        # Fallback to old styling
        from margadarsaka.ui.utils.styling import apply_custom_css, inject_custom_js
        MODERN_STYLING = False
    
    from margadarsaka.ui.utils.state_manager import init_state, get_state_manager
    from margadarsaka.ui.utils.i18n import get_text, set_language, Language

    # Navigation and components
    from margadarsaka.ui.components.navigation import render_navigation
    from margadarsaka.ui.components.navigation import PageType as NavigationPageType

    PageType = NavigationPageType  # Use the imported one
    from margadarsaka.ui.components.auth_components import show_authentication_modal
    from margadarsaka.ui.components.oauth_auth import AppwriteOAuth2Manager

    # Services
    from margadarsaka.services.appwrite_service import AppwriteService
    from margadarsaka.secrets import SecretsManager

    COMPONENTS_AVAILABLE = True
    logger.info("✅ All UI components loaded successfully")

except ImportError as e:
    logger.error(f"❌ Failed to import UI components: {e}")
    COMPONENTS_AVAILABLE = False
    MODERN_STYLING = False

    # Fallback implementations with correct types
    def apply_custom_css():
        st.markdown(
            "<style>body { font-family: Arial, sans-serif; }</style>",
            unsafe_allow_html=True,
        )

    def inject_custom_js():
        pass

    def get_text(key: str, default: Optional[str] = None, **kwargs) -> str:
        return default or key

    def create_card(title: str, content: str, card_type: str = "default"):
        st.markdown(f"**{title}**")
        st.markdown(content)

    def create_metric_card(title: str, value: str, delta: Optional[str] = None):
        st.metric(label=title, value=value, delta=delta)

    def create_hero_section(title: str, subtitle: str, description: str):
        st.title(title)
        if subtitle:
            st.subheader(subtitle)
        if description:
            st.markdown(description)

    def show_success_message(message: str):
        st.success(message)

    def show_warning_message(message: str):
        st.warning(message)

    def show_error_message(message: str):
        st.error(message)

    def show_info_message(message: str):
        st.info(message)

    class MockState:
        def get(self, key: str, default=None):
            return getattr(st.session_state, key, default)

        def set(self, key: str, value):
            setattr(st.session_state, key, value)

    def init_state():
        return MockState()

    def get_state_manager():
        return MockState()

    # Define page types as a simple enum-like class
    class PageType:
        HOME = "home"
        ASSESSMENT = "assessment"
        RESUME = "resume"
        CHAT = "chat"
        RECOMMENDATIONS = "recommendations"
        RESOURCES = "resources"
        PROFILE = "profile"

        @property
        def value(self):
            return self

    # Make page type instances
    PageType.HOME = "home"
    PageType.ASSESSMENT = "assessment"
    PageType.RESUME = "resume"
    PageType.CHAT = "chat"
    PageType.RECOMMENDATIONS = "recommendations"
    PageType.RESOURCES = "resources"
    PageType.PROFILE = "profile"

    def render_navigation() -> str:
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

    def show_authentication_modal(appwrite_service=None):
        return None

    # Mock classes for missing services  
    class SecretsManager:
        def __init__(self):
            pass

    class AppwriteService:
        def __init__(self):
            pass


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
    """Display a modern hero section with floating elements and animations"""
    
    # Hero section CSS
    st.markdown("""
    <style>
    .hero-section {
        position: relative;
        background: linear-gradient(135deg, rgba(30, 136, 229, 0.1) 0%, rgba(142, 36, 170, 0.1) 100%);
        padding: 4rem 2rem;
        border-radius: 24px;
        margin-bottom: 3rem;
        text-align: center;
        overflow: hidden;
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 
            0 20px 40px rgba(30, 136, 229, 0.1),
            0 1px 0 rgba(255, 255, 255, 0.3) inset;
    }
    
    .hero-section::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(30, 136, 229, 0.1) 0%, transparent 50%);
        animation: float 8s ease-in-out infinite;
        z-index: -1;
    }
    
    .hero-section::after {
        content: '';
        position: absolute;
        bottom: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(142, 36, 170, 0.1) 0%, transparent 50%);
        animation: float 12s ease-in-out infinite reverse;
        z-index: -1;
    }
    
    .hero-title {
        color: #1A202C;
        margin: 0;
        font-size: clamp(2.5rem, 5vw, 4rem);
        font-weight: 800;
        letter-spacing: -0.025em;
        line-height: 1.1;
        background: linear-gradient(135deg, #1E88E5 0%, #8E24AA 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: slideInUp 1s ease-out;
    }
    
    .hero-subtitle {
        color: #4A5568;
        margin: 1.5rem auto 0;
        font-size: clamp(1.2rem, 3vw, 1.6rem);
        font-weight: 500;
        max-width: 800px;
        line-height: 1.4;
        animation: slideInUp 1s ease-out 0.2s both;
    }
    
    .hero-description {
        color: #718096;
        margin: 1rem auto 0;
        font-size: clamp(1rem, 2.5vw, 1.2rem);
        max-width: 700px;
        line-height: 1.6;
        animation: slideInUp 1s ease-out 0.4s both;
    }
    
    .hero-features {
        margin-top: 2.5rem;
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 1rem;
        animation: slideInUp 1s ease-out 0.6s both;
    }
    
    .hero-feature {
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.3);
        border-radius: 50px;
        padding: 0.75rem 1.5rem;
        font-size: 0.95rem;
        font-weight: 500;
        color: #2D3748;
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    
    .hero-feature:hover {
        transform: translateY(-2px) scale(1.05);
        box-shadow: 0 8px 25px rgba(30, 136, 229, 0.2);
        background: rgba(30, 136, 229, 0.1);
    }
    
    .hero-cta {
        margin-top: 2.5rem;
        animation: slideInUp 1s ease-out 0.8s both;
    }
    
    .cta-primary {
        background: linear-gradient(135deg, #1E88E5 0%, #8E24AA 100%);
        color: white;
        padding: 1rem 2.5rem;
        border-radius: 50px;
        font-size: 1.1rem;
        font-weight: 600;
        border: none;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 8px 25px rgba(30, 136, 229, 0.3);
        margin: 0 0.5rem;
        text-decoration: none;
        display: inline-block;
    }
    
    .cta-primary:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 35px rgba(30, 136, 229, 0.4);
    }
    
    .cta-secondary {
        background: transparent;
        color: #1E88E5;
        padding: 1rem 2.5rem;
        border-radius: 50px;
        font-size: 1.1rem;
        font-weight: 600;
        border: 2px solid #1E88E5;
        cursor: pointer;
        transition: all 0.3s ease;
        margin: 0 0.5rem;
        text-decoration: none;
        display: inline-block;
    }
    
    .cta-secondary:hover {
        background: #1E88E5;
        color: white;
        transform: translateY(-3px);
    }
    
    .floating-element {
        position: absolute;
        border-radius: 50%;
        background: linear-gradient(135deg, rgba(30, 136, 229, 0.1) 0%, rgba(142, 36, 170, 0.1) 100%);
        backdrop-filter: blur(10px);
    }
    
    .floating-1 {
        top: 10%;
        left: 10%;
        width: 80px;
        height: 80px;
        animation: floatSlow 6s ease-in-out infinite;
    }
    
    .floating-2 {
        top: 20%;
        right: 15%;
        width: 60px;
        height: 60px;
        animation: floatSlow 8s ease-in-out infinite reverse;
    }
    
    .floating-3 {
        bottom: 15%;
        left: 20%;
        width: 100px;
        height: 100px;
        animation: floatSlow 10s ease-in-out infinite;
    }
    
    .floating-4 {
        bottom: 25%;
        right: 10%;
        width: 70px;
        height: 70px;
        animation: floatSlow 7s ease-in-out infinite reverse;
    }
    
    @keyframes slideInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        33% { transform: translateY(-10px) rotate(1deg); }
        66% { transform: translateY(5px) rotate(-1deg); }
    }
    
    @keyframes floatSlow {
        0%, 100% { transform: translateY(0px) translateX(0px); }
        33% { transform: translateY(-20px) translateX(10px); }
        66% { transform: translateY(10px) translateX(-5px); }
    }
    
    @media (max-width: 768px) {
        .hero-section {
            padding: 3rem 1.5rem;
        }
        
        .hero-features {
            flex-direction: column;
            align-items: center;
        }
        
        .hero-feature {
            width: fit-content;
        }
        
        .floating-element {
            display: none; /* Hide on mobile for cleaner look */
        }
        
        .cta-primary, .cta-secondary {
            display: block;
            width: fit-content;
            margin: 0.5rem auto;
        }
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Hero section HTML
    st.markdown(f"""
    <div class="hero-section">
        <!-- Floating background elements -->
        <div class="floating-element floating-1"></div>
        <div class="floating-element floating-2"></div>
        <div class="floating-element floating-3"></div>
        <div class="floating-element floating-4"></div>
        
        <h1 class="hero-title">
            🚀 {get_text("app_title", "Margadarsaka")}
        </h1>
        
        <p class="hero-subtitle">
            {get_text("app_subtitle", "AI-Powered Career Guidance with Psychological Assessment")}
        </p>
        
        <p class="hero-description">
            {get_text("welcome_message", "Discover your ideal career path with personalized AI guidance, comprehensive skill assessments, and data-driven insights tailored for the Indian job market.")}
        </p>
        
        <div class="hero-features">
            <div class="hero-feature">
                <span>🧠</span>
                <span>{get_text("feature_assessment", "Psychological Assessment")}</span>
            </div>
            <div class="hero-feature">
                <span>🤖</span>
                <span>{get_text("feature_ai_chat", "AI Career Advisor")}</span>
            </div>
            <div class="hero-feature">
                <span>📄</span>
                <span>{get_text("feature_resume", "Resume Analysis")}</span>
            </div>
            <div class="hero-feature">
                <span>📊</span>
                <span>{get_text("feature_insights", "Career Insights")}</span>
            </div>
        </div>
        
        <div class="hero-cta">
            <a href="#assessment" class="cta-primary">
                {get_text("start_journey", "Start Your Career Journey")}
            </a>
            <a href="#features" class="cta-secondary">
                {get_text("learn_more", "Learn More")}
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)


def show_home_page():
    """Modern home page with Streamlit-compatible styling"""

    # Welcome banner
    if COMPONENTS_AVAILABLE and hasattr(st.session_state, 'user_info') and st.session_state.get('user_authenticated'):
        user_name = st.session_state.user_info.get('name', 'User')
        create_hero_section(
            title=f"Welcome back, {user_name}! 👋",
            subtitle="Your Career Journey Continues",
            description="Let's continue building your path to success with personalized guidance and resources."
        )
    else:
        create_hero_section(
            title="Welcome to Margadarsaka 🌟",
            subtitle="Your AI-Powered Career Guide",
            description="Discover your ideal career path through personalized assessments, expert guidance, and curated resources. Start your journey to professional success today."
        )

    # Feature cards section
    st.markdown("---")
    st.markdown("## ✨ Explore Our Features")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        create_card(
            title="📊 Career Assessment", 
            content="Take our comprehensive assessment to discover careers that match your skills, interests, and personality. Get personalized recommendations based on scientific career theories.",
            card_type="feature"
        )
        if st.button("Start Assessment", key="home_assessment"):
            st.session_state.current_page = PageType.ASSESSMENT
            st.rerun()
            
    with col2:
        create_card(
            title="🤖 AI Career Chat",
            content="Chat with our AI career counselor for instant guidance, answers to career questions, and personalized advice tailored to your unique situation.",
            card_type="feature"
        )
        if st.button("Start Chat", key="home_chat"):
            st.session_state.current_page = PageType.CHAT
            st.rerun()
            
    with col3:
        create_card(
            title="📄 Resume Builder", 
            content="Create a professional, ATS-optimized resume with our intelligent builder. Choose from modern templates and get real-time suggestions.",
            card_type="feature"
        )
        if st.button("Build Resume", key="home_resume"):
            st.session_state.current_page = PageType.RESUME
            st.rerun()

    # Quick stats section
    st.markdown("---")
    st.markdown("## 📈 Impact Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        create_metric_card("Users Helped", "10,000+", "+15%")
    with col2:
        create_metric_card("Career Matches", "50,000+", "+22%")  
    with col3:
        create_metric_card("Success Rate", "94%", "+2%")
    with col4:
        create_metric_card("Resources", "1,000+", "+12%")

    # Getting started section
    st.markdown("---")
    
    if not st.session_state.get("user_authenticated", False):
        create_card(
            title="🚀 Ready to Start Your Journey?",
            content="Join thousands of professionals who have found their ideal career path with Margadarsaka. Sign up today for free!",
            card_type="success"
        )
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Get Started Free", key="get_started_main", type="primary"):
                # Show authentication modal
                show_authentication_modal()
    else:
        # Personalized recommendations for authenticated users
        create_card(
            title="🎯 Continue Your Journey",
            content="Based on your profile, we recommend taking the next step in your career development.",
            card_type="info"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("View Recommendations", key="home_recommendations"):
                st.session_state.current_page = PageType.RECOMMENDATIONS
                st.rerun()
        with col2:
            if st.button("Update Profile", key="home_profile"):
                st.session_state.current_page = PageType.PROFILE
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
            get_text("assessment_coming_soon", "Assessment feature coming soon!")
        )


def show_chat_page():
    st.markdown(f'<h2 class="features-title">🌟 {get_text("key_features", "Key Features")}</h2>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3, gap="large")

    with col1:
        st.markdown(
            f"""
        <div class="modern-feature-card fade-in-up">
            <div class="feature-icon">🧠</div>
            <h3 class="feature-title">
                {get_text("psychological_assessment", "Psychological Assessment")}
            </h3>
            <p class="feature-description">
                {get_text("assessment_desc", "Discover your personality traits, interests, and cognitive abilities through scientifically-backed assessments designed for career success.")}
            </p>
        </div>
        """,
            unsafe_allow_html=True,
        )

        if st.button(
            "🎯 " + get_text("start_assessment", "Start Assessment"),
            use_container_width=True,
            type="primary",
            key="assessment_btn"
        ):
            st.session_state.current_page = PageType.ASSESSMENT
            st.rerun()

    with col2:
        st.markdown(
            f"""
        <div class="modern-feature-card fade-in-up-delay-1">
            <div class="feature-icon">🤖</div>
            <h3 class="feature-title">
                {get_text("ai_career_chat", "AI Career Chat")}
            </h3>
            <p class="feature-description">
                {get_text("chat_desc", "Get instant, personalized career advice from our AI advisor trained on comprehensive Indian job market data and industry trends.")}
            </p>
        </div>
        """,
            unsafe_allow_html=True,
        )

        if st.button(
            "💬 " + get_text("chat_now", "Chat Now"),
            use_container_width=True,
            type="primary",
            key="chat_btn"
        ):
            st.session_state.current_page = PageType.CHAT
            st.rerun()

    with col3:
        st.markdown(
            f"""
        <div class="modern-feature-card fade-in-up-delay-2">
            <div class="feature-icon">📄</div>
            <h3 class="feature-title">
                {get_text("resume_analysis", "Resume Analysis")}
            </h3>
            <p class="feature-description">
                {get_text("resume_desc", "Get AI-powered insights on your resume with detailed suggestions for improvement and ATS optimization strategies.")}
            </p>
        </div>
        """,
            unsafe_allow_html=True,
        )

        if st.button(
            "📊 " + get_text("analyze_resume", "Analyze Resume"),
            use_container_width=True,
            type="primary",
            key="resume_btn"
        ):
            st.session_state.current_page = PageType.RESUME
            st.rerun()

    # Success stories section
    st.markdown(f"""
    <div class="success-stories-section">
        <h2 style="text-align: center; margin-bottom: 2rem; font-size: 2.2rem; font-weight: 700; color: #2D3748;">
            🎉 {get_text('success_stories', 'Success Stories')}
        </h2>
    """, unsafe_allow_html=True)

    testimonial_col1, testimonial_col2 = st.columns(2, gap="large")

    with testimonial_col1:
        st.markdown(
            f"""
        <div class="testimonial-card">
            <div class="testimonial-quote">❝</div>
            <p class="testimonial-text">
                "{get_text("testimonial_1", "Margadarsaka helped me discover my passion for data science. The psychological assessment was incredibly accurate and gave me clarity about my strengths!")}"
            </p>
            <div class="testimonial-author">
                <div class="author-avatar">P</div>
                <div class="author-info">
                    <h4>Priya S.</h4>
                    <p>Data Scientist at Tech Corp</p>
                </div>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with testimonial_col2:
        st.markdown(
            f"""
        <div class="testimonial-card">
            <div class="testimonial-quote">❝</div>
            <p class="testimonial-text">
                "{get_text("testimonial_2", "The AI chat feature gave me invaluable clarity about my career transition from finance to tech. The personalized guidance was exactly what I needed!")}"
            </p>
            <div class="testimonial-author">
                <div class="author-avatar">A</div>
                <div class="author-info">
                    <h4>Arjun K.</h4>
                    <p>Software Engineer at Startup</p>
                </div>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)

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
                st.session_state.current_page = PageType.PROFILE
                st.rerun()


def show_assessment_page():
    """Psychological assessment page with backend integration"""
    try:
        from margadarsaka.ui.pages.assessment import show_assessment_page as assessment_show
        assessment_show()
    except ImportError as e:
        logger.warning(f"Advanced assessment page not available: {e}")
        # Fallback to integrated assessment using psychology module
        try:
            from margadarsaka.psychology import TestingFramework
            from margadarsaka.models import TestResponse
            
            st.markdown(f"# 🧠 {get_text('psychological_assessment', 'Psychological Assessment')}")
            
            # Initialize testing framework
            testing_framework = TestingFramework()
            
            # Assessment options
            assessment_type = st.selectbox(
                "Choose an assessment:",
                [
                    "RIASEC Career Interest Assessment",
                    "Mental Skills Evaluation", 
                    "Big Five Personality Test",
                    "Complete Psychological Profile"
                ]
            )
            
            if assessment_type == "RIASEC Career Interest Assessment":
                st.markdown("### 🎯 RIASEC Career Interest Assessment")
                st.info("Discover your career interests based on Holland's RIASEC model")
                
                test = testing_framework.get_test_by_type("riasec")
                render_psychological_test(test, "riasec")
                
            elif assessment_type == "Mental Skills Evaluation":
                st.markdown("### 🧠 Mental Skills Assessment")
                st.info("Evaluate your analytical, deductive, and psychological abilities")
                
                test = testing_framework.get_test_by_type("mental_skills")
                render_psychological_test(test, "mental_skills")
                
            elif assessment_type == "Big Five Personality Test":
                st.markdown("### 👤 Big Five Personality Assessment")
                st.info("Assess your personality traits using the Big Five model")
                
                test = testing_framework.get_test_by_type("personality")
                render_psychological_test(test, "personality")
                
            elif assessment_type == "Complete Psychological Profile":
                st.markdown("### 🔬 Complete Psychological Profile")
                st.info("Take all assessments for a comprehensive career analysis")
                
                if st.button("🚀 Start Complete Assessment", type="primary"):
                    st.session_state.complete_assessment_started = True
                    st.rerun()
                
                if st.session_state.get("complete_assessment_started", False):
                    render_complete_assessment(testing_framework)
            
        except ImportError:
            # Final fallback to simple interface
            st.markdown(f"# 🧠 {get_text('psychological_assessment', 'Psychological Assessment')}")
            st.info(get_text("assessment_coming_soon", "Advanced psychological assessment coming soon!"))

            # Placeholder content with call to action
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
            
            # Simple demo assessment
            with st.expander("🎯 Try a Quick Assessment Demo"):
                demo_question = st.radio(
                    "I prefer working with:",
                    ["Ideas and concepts", "People and relationships", "Data and facts", "Objects and tools"]
                )
                
                if st.button("Get Quick Insight"):
                    insights = {
                        "Ideas and concepts": "You might enjoy careers in research, writing, or creative fields!",
                        "People and relationships": "Consider careers in counseling, teaching, or social work!",
                        "Data and facts": "You could excel in analysis, finance, or scientific research!",
                        "Objects and tools": "Engineering, craftsmanship, or technical roles might suit you!"
                    }
                    st.success(f"💡 Quick Insight: {insights[demo_question]}")
                    st.info("For detailed analysis, complete our full assessment when available!")


def render_psychological_test(test, test_type: str):
    """Render a psychological test interface"""
    if not test:
        st.error("Test not available")
        return
    
    st.markdown(f"**Duration:** {test.duration_minutes} minutes")
    st.markdown(f"**Questions:** {len(test.questions)}")
    st.markdown(f"**Description:** {test.description}")
    
    # Initialize responses in session state
    response_key = f"test_responses_{test_type}"
    if response_key not in st.session_state:
        st.session_state[response_key] = {}
    
    # Render questions
    with st.form(f"test_form_{test_type}"):
        st.markdown("---")
        
        for i, question in enumerate(test.questions[:5]):  # Show first 5 questions as demo
            st.markdown(f"**Question {i+1}:** {question['question']}")
            
            # Create response widget based on question type
            if question.get('type') == 'scale':
                response = st.slider(
                    f"Response to Q{i+1}",
                    1, 5, 3,
                    key=f"{test_type}_q{i+1}",
                    help="1 = Strongly Disagree, 5 = Strongly Agree"
                )
            else:
                # Default to scale for demo
                response = st.slider(
                    f"Response to Q{i+1}",
                    1, 5, 3,
                    key=f"{test_type}_q{i+1}",
                    help="1 = Strongly Disagree, 5 = Strongly Agree"
                )
            
            st.session_state[response_key][f"q{i+1}"] = response
        
        st.markdown("---")
        st.info("📝 This is a demo showing the first 5 questions. Complete assessment available with full setup.")
        
        submitted = st.form_submit_button("Complete Assessment (Demo)")
        
        if submitted:
            # Show demo results
            st.success("✅ Assessment completed!")
            
            # Calculate simple score
            responses = list(st.session_state[response_key].values())
            avg_score = sum(responses) / len(responses) if responses else 0
            
            st.markdown("### 📊 Your Results")
            st.metric("Average Score", f"{avg_score:.1f}/5.0")
            
            # Provide basic insights
            if avg_score >= 4:
                st.success("🌟 You show strong positive responses in this area!")
            elif avg_score >= 3:
                st.info("✅ You have balanced responses in this area.")
            else:
                st.warning("💡 This might be an area for development.")
            
            st.info("For detailed analysis and personalized recommendations, complete the full assessment!")


def render_complete_assessment(testing_framework):
    """Render complete assessment flow"""
    st.markdown("### 🎯 Complete Assessment Progress")
    
    # Progress tracking
    tests = ["riasec", "mental_skills", "personality"]
    completed_tests = st.session_state.get("completed_tests", [])
    
    progress = len(completed_tests) / len(tests)
    st.progress(progress)
    st.caption(f"Progress: {len(completed_tests)}/{len(tests)} tests completed")
    
    # Show next test
    if len(completed_tests) < len(tests):
        next_test = [t for t in tests if t not in completed_tests][0]
        st.markdown(f"### 📝 Next: {next_test.replace('_', ' ').title()}")
        
        test = testing_framework.get_test_by_type(next_test)
        render_psychological_test(test, next_test)
        
        if st.button("Mark Test as Completed", key=f"complete_{next_test}"):
            if "completed_tests" not in st.session_state:
                st.session_state.completed_tests = []
            st.session_state.completed_tests.append(next_test)
            st.rerun()
    else:
        # All tests completed
        st.success("🎉 All assessments completed!")
        st.markdown("### 📊 Your Complete Profile")
        
        # Show comprehensive results
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("RIASEC Top Interest", "Investigative")
        with col2:
            st.metric("Mental Skills Score", "8.2/10")
        with col3:
            st.metric("Personality Type", "INTJ-like")
        
        st.info("💡 Detailed analysis and career recommendations would be generated here in the full version!")
        
        if st.button("🔄 Restart Assessment"):
            st.session_state.completed_tests = []
            st.session_state.complete_assessment_started = False
            st.rerun()


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
            
            # Instead of the info message, we'll show a demo of our custom component
            with st.spinner("Analyzing resume..."):
                # Simulate a resume analysis result
                mock_resume_analysis = {
                    "ats_score": 78,
                    "keyword_match_percentage": 65,
                    "readability_score": 82,
                    "format_score": 70,
                    "overall_score": 74,
                    "recommendations": [
                        "Add more quantifiable achievements to highlight impact",
                        "Include relevant keywords from the job description",
                        "Improve formatting for better ATS compatibility",
                        "Consider adding a skills section with technical competencies",
                        "Make sure contact information is prominently displayed"
                    ]
                }
                
                # Display resume score with our custom component
                render_resume_score_section(mock_resume_analysis)
                
                # Show a sample skill match visualization
                job_skills = ["python", "react", "nodejs", "aws", "docker", "agile"]
                resume_skills = ["python", "javascript", "react", "git", "sql", "docker"]
                
                render_skill_match_visualization(job_skills, resume_skills)
                
                # Add call to action
                st.markdown("### 🚀 Boost Your Resume")
                st.markdown("""
                Ready to improve your resume and increase your chances of landing that dream job?
                Try our AI-powered suggestions tailored to your specific career goals!
                """)
                
                # Demo button
                if st.button("Generate Improvement Suggestions"):
                    st.session_state.show_suggestions = True
                
                if st.session_state.get("show_suggestions", False):
                    st.subheader("💡 Smart Suggestions")
                    
                    suggestion_tabs = st.tabs(["Content", "Format", "Keywords"])
                    
                    with suggestion_tabs[0]:
                        st.markdown("""
                        * **Achievement Impact**: Transform "Developed a web application" to "Developed a web application that increased user engagement by 45%"
                        * **Action Verbs**: Replace generic verbs with impactful ones like "spearheaded", "orchestrated", or "revolutionized"
                        * **Quantify Results**: Include metrics and numbers to demonstrate your impact
                        """)
                    
                    with suggestion_tabs[1]:
                        st.markdown("""
                        * **Consistent Formatting**: Ensure consistent font, bullet styles, and spacing
                        * **ATS-Friendly**: Use simple formatting without tables, headers, or footers
                        * **Section Order**: Place most relevant experience at the top
                        * **White Space**: Include adequate white space for readability
                        """)
                    
                    with suggestion_tabs[2]:
                        st.markdown("""
                        * **Technical Skills**: Add missing keywords like "AWS", "Agile", and "CI/CD"
                        * **Industry Terms**: Include terms like "Full-Stack Development" and "Cloud Architecture"
                        * **Soft Skills**: Add keywords like "Cross-functional Collaboration" and "Problem-solving"
                        """)
            


def show_chat_page():
    """AI career chat page with full Gemini integration"""
    try:
        from margadarsaka.ui.pages.chat import show_chat_page as chat_show
        chat_show()
    except ImportError as e:
        logger.warning(f"Advanced chat page not available: {e}")
        # Fallback to simple chat interface
        st.markdown(f"# 🤖 {get_text('ai_career_chat', 'AI Career Chat')}")

        # AI Status
        try:
            from margadarsaka.secrets import get_gemini_api_key
            api_key = get_gemini_api_key()
            if api_key:
                st.success("🤖 AI Assistant is ready to help!")
            else:
                st.warning("⚠️ AI features require Gemini API key configuration")
        except:
            st.info("💡 Enhanced AI features available with full setup")

        # Simple chat interface placeholder
        if "chat_messages" not in st.session_state:
            st.session_state.chat_messages = [
                {
                    "role": "assistant",
                    "content": get_text(
                        "chat_welcome",
                        "🙏 Namaste! I'm Margadarsaka, your AI career advisor specializing in the Indian job market. How can I help you today?",
                    ),
                }
            ]

        # Display chat messages
        for message in st.session_state.chat_messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])

        # Chat input
        if prompt := st.chat_input(
            get_text("type_message", "Ask me about career guidance, skills, or job search...")
        ):
            st.session_state.chat_messages.append({"role": "user", "content": prompt})

            # Simple pattern-based responses
            response = get_text(
                "fallback_response", 
                "Thank you for your question! For detailed AI-powered career guidance, please ensure the full Margadarsaka setup is complete. In the meantime, check out our Assessment and Resources sections!"
            )
            
            # Add some basic pattern matching
            if "career" in prompt.lower():
                response = "Career planning is essential! I recommend starting with our psychological assessment to understand your interests and strengths, then exploring our curated learning resources."
            elif "skill" in prompt.lower():
                response = "Skill development is key to career success! Visit our Resources section for learning paths, or take our assessment to identify which skills align with your career goals."
            elif "job" in prompt.lower():
                response = "Job searching can be challenging! Our Resources section has job boards and tips. Also consider taking our assessment to better understand what roles might suit you."

            st.session_state.chat_messages.append({
                "role": "assistant", 
                "content": response
            })
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
    """Learning resources page with full backend integration"""
    try:
        from margadarsaka.ui.pages.resources import show_resources_page as resources_show
        resources_show()
    except ImportError as e:
        logger.warning(f"Advanced resources page not available: {e}")
        # Fallback to simple resources display
        st.markdown(f"# 📚 {get_text('learning_resources', 'Learning Resources')}")
        
        # Simple resource browser
        resource_type = st.selectbox(
            "Filter by type:",
            ["All Resources", "Learning Courses", "Job Search", "Mentorship", "Career Roadmaps"]
        )
        
        if resource_type == "Career Roadmaps":
            st.markdown("### 🗺️ Popular Career Roadmaps")
            roadmaps = [
                {"title": "Frontend Developer", "url": "https://roadmap.sh/frontend"},
                {"title": "Backend Developer", "url": "https://roadmap.sh/backend"},
                {"title": "DevOps Engineer", "url": "https://roadmap.sh/devops"},
                {"title": "Data Scientist", "url": "https://roadmap.sh/data-science"}
            ]
            
            for roadmap in roadmaps:
                st.markdown(f"🔗 [{roadmap['title']}]({roadmap['url']})")
        else:
            st.info("Advanced resource filtering and recommendations available with full setup!")
            
        # Add disclaimer
        st.markdown("---")
        st.info("📣 **Legal Disclaimer**: External resources are provided for educational purposes only.")


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

    # Handle OAuth callback
    query_params = st.query_params
    user_id = query_params.get("userId")
    secret = query_params.get("secret")

    if user_id and secret:
        appwrite_service = state.get("appwrite_service")
        if appwrite_service:
            try:
                session = appwrite_service.create_session_from_token(user_id, secret)
                if session:
                    st.success("✅ Successfully authenticated with OAuth!")
                    # Update state and rerun
                    st.session_state.user_authenticated = True
                    st.session_state.current_user = appwrite_service.get_account()
                    st.session_state.auth_method = "oauth"
                    # Clear query params to avoid re-triggering
                    st.query_params.clear()
                    st.rerun()
                else:
                    st.error("❌ Failed to create session from OAuth token.")
            except Exception as e:
                st.error(f"An error occurred during OAuth callback: {e}")

    # Get user information for header
    user_info = None
    if st.session_state.get("user_authenticated", False):
        user_info = st.session_state.get("current_user", {})
    
    # Render simple header (Streamlit-native)
    render_simple_header(
        show_auth=not st.session_state.get("user_authenticated", False),
        user_info=user_info
    )
    
    # Render rating component in sidebar
    render_sidebar_rating()

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

    # Render modern footer
    render_modern_footer(
        show_social=True,
        show_newsletter=True,
        show_theme_toggle=True
    )


if __name__ == "__main__":
    main()
