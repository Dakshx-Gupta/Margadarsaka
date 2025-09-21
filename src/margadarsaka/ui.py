"""Enhanced Streamlit frontend for Margadarsaka AI Career Advisor"""

import streamlit as st
import requests
from typing import Optional, Dict, Any
import tempfile
import os
import logging

logger = logging.getLogger(__name__)

# Initialize secrets management early
try:
    from margadarsaka.secrets import SecretsManager

    # Initialize global secrets manager to load all configuration
    secrets_manager = SecretsManager()
    if secrets_manager.is_doppler_active():
        logger.info("✅ Doppler secrets loaded successfully")
    else:
        logger.info("ℹ️ Using environment variables for configuration")
except ImportError as e:
    logger.warning(f"Secrets management not available: {e}")

# Import Appwrite services
try:
    from margadarsaka.services.appwrite_service import AppwriteService
    from margadarsaka.ui.appwrite_components import (
        inject_appwrite_sdk,
        appwrite_auth_component,
        handle_appwrite_messages,
    )

    APPWRITE_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Appwrite integration not available: {e}")
    APPWRITE_AVAILABLE = False
    AppwriteService = None

    # Define fallback functions
    def inject_appwrite_sdk():
        pass

    def appwrite_auth_component():
        pass

    def handle_appwrite_messages():
        return {"user": None, "logged_in": False}


# Page configuration
st.set_page_config(
    page_title="Margadarsaka - AI Career Advisor",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Constants
API_BASE_URL = "/api"


def show_authentication_modal():
    """Show authentication modal dialog."""
    try:
        # Use the already imported functions if available
        if APPWRITE_AVAILABLE:
            # Create modal using container
            with st.container():
                st.markdown("### Authentication")

                # Inject Appwrite SDK for client-side operations
                inject_appwrite_sdk()

                # Show authentication component
                appwrite_auth_component()
        else:
            raise ImportError("Appwrite not available")

    except (ImportError, NameError):
        # Fallback to simple form if appwrite_components not available
        st.markdown("### Sign In / Sign Up")

        auth_tab1, auth_tab2 = st.tabs(["Sign In", "Sign Up"])

        with auth_tab1:
            with st.form("signin_form"):
                email = st.text_input("Email")
                password = st.text_input("Password", type="password")

                if st.form_submit_button("Sign In"):
                    if st.session_state.get("appwrite_service"):
                        try:
                            user = st.session_state.appwrite_service.login_user(
                                email, password
                            )
                            if user:
                                st.session_state.user = user
                                st.success("Successfully signed in!")
                                st.rerun()
                        except Exception as e:
                            st.error(f"Sign in failed: {e}")
                    else:
                        st.error("Authentication service not available")

        with auth_tab2:
            with st.form("signup_form"):
                name = st.text_input("Full Name")
                email = st.text_input("Email")
                password = st.text_input("Password", type="password")
                confirm_password = st.text_input("Confirm Password", type="password")

                if st.form_submit_button("Sign Up"):
                    if password != confirm_password:
                        st.error("Passwords do not match")
                    elif st.session_state.get("appwrite_service"):
                        try:
                            user = st.session_state.appwrite_service.create_user(
                                email, password, name
                            )
                            if user:
                                st.session_state.user = user
                                st.success("Account created successfully!")
                                st.rerun()
                        except Exception as e:
                            st.error(f"Sign up failed: {e}")
                    else:
                        st.error("Authentication service not available")


def main():
    """Main Streamlit application"""

    # Initialize Appwrite service
    if APPWRITE_AVAILABLE and AppwriteService:
        try:
            if "appwrite_service" not in st.session_state:
                st.session_state.appwrite_service = AppwriteService()
        except Exception as e:
            logger.error(f"Failed to initialize Appwrite service: {e}")
            st.session_state.appwrite_service = None

    # Initialize Appwrite SDK if available
    if APPWRITE_AVAILABLE:
        inject_appwrite_sdk()

        # Check authentication state
        auth_state = handle_appwrite_messages()
        if "appwrite_user" not in st.session_state:
            st.session_state.appwrite_user = auth_state.get("user")
            st.session_state.appwrite_logged_in = auth_state.get("logged_in", False)

    # Custom CSS for better styling
    st.markdown(
        """
    <style>
    .main-header {
        text-align: center;
        color: #2E86AB;
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .feature-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #2E86AB;
        margin: 1rem 0;
    }
    .success-card {
        background: #d4edda;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )

    # Header
    st.markdown('<h1 class="main-header">🚀 Margadarsaka</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="subtitle">AI-Powered Career Advisor with Psychological Assessment</p>',
        unsafe_allow_html=True,
    )
    st.markdown(
        "Get personalized career guidance with psychological profiling, resume analysis, and AI-powered recommendations tailored for the Indian job market."
    )

    # Sidebar for navigation
    with st.sidebar:
        # Appwrite Authentication Section
        if APPWRITE_AVAILABLE:
            st.header("🔐 User Account")
            if st.session_state.get("appwrite_logged_in", False):
                user = st.session_state.get("appwrite_user")
                if user:
                    st.success(
                        f"✅ Welcome, {user.get('name', user.get('email', 'User'))}!"
                    )
                    if st.button("🚪 Logout"):
                        st.session_state.appwrite_user = None
                        st.session_state.appwrite_logged_in = False
                        st.rerun()
            else:
                st.info(
                    "👤 Login to save your progress and get personalized recommendations"
                )
                if st.button("🔑 Login/Register"):
                    st.session_state.show_auth = True
                    st.rerun()

            st.divider()

        st.header("🧭 Navigation")
        page = st.radio(
            "Choose a section:",
            [
                "🏠 Home",
                "🧠 Psychological Assessment",
                "📄 Resume Analysis",
                "🤖 AI Career Chat",
                "📋 Career Recommendations",
                "📚 Learning Resources",
                "📈 Progress Tracker",
            ],
        )

        # Language preference
        st.divider()
        st.subheader("🌐 Language")
        st.selectbox(
            "Choose language:",
            ["English", "हिंदी (Hindi)", "Hinglish"],
            key="language_preference",
        )

    # Handle authentication modal
    if st.session_state.get("show_auth", False):
        show_authentication_modal()
        return

    # Route to appropriate page
    if page == "🏠 Home":
        show_home_page()
    elif page == "🧠 Psychological Assessment":
        show_psychology_page()
    elif page == "📄 Resume Analysis":
        show_resume_analysis_page()
    elif page == "🤖 AI Career Chat":
        show_ai_chat_page()
    elif page == "📋 Career Recommendations":
        show_recommendations_page()
    elif page == "📚 Learning Resources":
        show_resources_page()
    elif page == "📈 Progress Tracker":
        show_progress_page()


def show_home_page():
    """Display the home page with feature overview"""

    st.header("Welcome to Margadarsaka AI Career Advisor!")

    # Feature overview
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
        <div class="feature-card">
            <h3>🧠 Psychological Assessment</h3>
            <p>Take comprehensive RIASEC personality tests and mental skills assessments to understand your natural strengths and career fit.</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
        <div class="feature-card">
            <h3>📄 Resume Analysis</h3>
            <p>Get detailed ATS scoring, identify missing keywords, and receive project recommendations to enhance your resume.</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            """
        <div class="feature-card">
            <h3>🤖 AI-Powered Guidance</h3>
            <p>Chat with our AI advisor trained on Indian job market data, supporting Hindi and English languages.</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    # Quick start section
    st.markdown("---")
    st.subheader("🚀 Quick Start")

    quick_col1, quick_col2 = st.columns(2)

    with quick_col1:
        if st.button(
            "🧠 Start Psychological Assessment",
            type="primary",
            use_container_width=True,
        ):
            st.session_state.page = "🧠 Psychological Assessment"
            st.rerun()

        if st.button("📄 Analyze My Resume", use_container_width=True):
            st.session_state.page = "📄 Resume Analysis"
            st.rerun()

    with quick_col2:
        if st.button("🤖 Chat with AI Advisor", use_container_width=True):
            st.session_state.page = "🤖 AI Career Chat"
            st.rerun()

        if st.button("📋 Get Career Recommendations", use_container_width=True):
            st.session_state.page = "📋 Career Recommendations"
            st.rerun()

    # Statistics/Info section
    st.markdown("---")
    st.subheader("📊 Platform Features")

    stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)

    with stat_col1:
        st.metric(
            "Psychological Tests", "5+", help="RIASEC, Mental Skills, Personality"
        )

    with stat_col2:
        st.metric("Supported Languages", "3", help="English, Hindi, Hinglish")

    with stat_col3:
        st.metric("Career Paths", "100+", help="Across various industries")

    with stat_col4:
        st.metric("AI Models", "2", help="Gemini AI + Local Models")


def show_psychology_page():
    """Display psychological assessment page"""

    st.header("🧠 Psychological Career Assessment")
    st.markdown(
        "Take comprehensive psychological tests to understand your career personality, mental strengths, and ideal work environment."
    )

    # Test selection
    test_type = st.selectbox(
        "Choose an assessment:",
        [
            "RIASEC Personality Assessment",
            "Mental Skills Evaluation",
            "Big Five Personality Test",
            "Complete Psychological Profile",
        ],
    )

    if test_type == "RIASEC Personality Assessment":
        show_riasec_test()
    elif test_type == "Mental Skills Evaluation":
        show_mental_skills_test()
    elif test_type == "Big Five Personality Test":
        show_personality_test()
    elif test_type == "Complete Psychological Profile":
        show_complete_assessment()


def show_riasec_test():
    """Display RIASEC personality test"""

    st.subheader("🎯 RIASEC Personality Assessment")
    st.markdown(
        "This test identifies your personality type across six dimensions: Realistic, Investigative, Artistic, Social, Enterprising, and Conventional."
    )

    # Sample RIASEC questions (in real implementation, these would come from psychology.py)
    riasec_questions = [
        {
            "question": "I enjoy working with tools and machinery",
            "category": "Realistic",
            "hindi": "मुझे उपकरण और मशीनरी के साथ काम करना पसंद है",
        },
        {
            "question": "I like to analyze data and solve complex problems",
            "category": "Investigative",
            "hindi": "मुझे डेटा का विश्लेषण करना और जटिल समस्याओं को हल करना पसंद है",
        },
        {
            "question": "I enjoy creative activities like writing, art, or music",
            "category": "Artistic",
            "hindi": "मुझे लेखन, कला या संगीत जैसी रचनात्मक गतिविधियाँ पसंद हैं",
        },
        {
            "question": "I like helping and teaching others",
            "category": "Social",
            "hindi": "मुझे दूसरों की मदद करना और पढ़ाना पसंद है",
        },
        {
            "question": "I enjoy leading teams and taking business risks",
            "category": "Enterprising",
            "hindi": "मुझे टीमों का नेतृत्व करना और व्यावसायिक जोखिम लेना पसंद है",
        },
        {
            "question": "I prefer organized, structured work environments",
            "category": "Conventional",
            "hindi": "मुझे व्यवस्थित, संरचित कार्य वातावरण पसंद है",
        },
    ]

    # Display questions
    responses = {}
    language = st.session_state.get("language_preference", "English")

    with st.form("riasec_form"):
        st.markdown(
            "Rate each statement from 1 (Strongly Disagree) to 5 (Strongly Agree):"
        )

        for i, q in enumerate(riasec_questions):
            question_text = q["hindi"] if language == "हिंदी (Hindi)" else q["question"]
            responses[q["category"]] = st.slider(
                question_text, min_value=1, max_value=5, value=3, key=f"riasec_{i}"
            )

        if st.form_submit_button("Analyze My Personality", type="primary"):
            # Calculate scores
            total_score = sum(responses.values())
            percentages = {k: (v / total_score) * 100 for k, v in responses.items()}

            # Display results
            st.success("🎉 Assessment Complete!")

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Your RIASEC Profile")
                for category, percentage in sorted(
                    percentages.items(), key=lambda x: x[1], reverse=True
                ):
                    st.metric(category, f"{percentage:.1f}%")

            with col2:
                st.subheader("Career Recommendations")
                dominant_type = max(percentages.items(), key=lambda x: x[1])[0]

                career_suggestions = {
                    "Realistic": ["Engineer", "Technician", "Mechanic", "Pilot"],
                    "Investigative": [
                        "Data Scientist",
                        "Researcher",
                        "Analyst",
                        "Doctor",
                    ],
                    "Artistic": ["Designer", "Writer", "Artist", "Musician"],
                    "Social": ["Teacher", "Counselor", "Social Worker", "HR Manager"],
                    "Enterprising": [
                        "Manager",
                        "Entrepreneur",
                        "Sales",
                        "Business Analyst",
                    ],
                    "Conventional": [
                        "Accountant",
                        "Administrator",
                        "Banker",
                        "Operations",
                    ],
                }

                st.write(f"Based on your dominant {dominant_type} personality:")
                for career in career_suggestions.get(dominant_type, []):
                    st.write(f"• {career}")


def show_mental_skills_test():
    """Display mental skills assessment"""

    st.subheader("🧩 Mental Skills Evaluation")
    st.markdown(
        "Assess your analytical, logical, creative, and problem-solving abilities."
    )

    # Sample mental skills scenarios
    scenarios = [
        {
            "title": "Problem Solving Scenario",
            "description": "A customer is unhappy with a product delay. How would you handle this?",
            "options": [
                "Apologize and offer a discount",
                "Investigate the cause and provide updates",
                "Escalate to manager immediately",
                "Blame external factors",
            ],
            "skill": "Problem Solving",
        },
        {
            "title": "Analytical Thinking",
            "description": "You have sales data showing declining trends. What's your first step?",
            "options": [
                "Panic and cut prices",
                "Analyze data patterns and root causes",
                "Increase marketing spend",
                "Wait and see if it improves",
            ],
            "skill": "Analytical Thinking",
        },
    ]

    with st.form("mental_skills_form"):
        skill_scores = {}

        for i, scenario in enumerate(scenarios):
            st.markdown(f"**Scenario {i + 1}: {scenario['title']}**")
            st.write(scenario["description"])

            choice = st.radio(
                "Choose the best approach:", scenario["options"], key=f"scenario_{i}"
            )

            # Simple scoring (in real implementation, this would be more sophisticated)
            if i == 0 and choice == scenario["options"][1]:  # Investigation approach
                skill_scores["Problem Solving"] = 85
            elif i == 1 and choice == scenario["options"][1]:  # Analysis approach
                skill_scores["Analytical Thinking"] = 90
            else:
                skill_scores[scenario["skill"]] = 60

        if st.form_submit_button("Evaluate My Skills", type="primary"):
            st.success("🎉 Skills Assessment Complete!")

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Your Mental Skills Profile")
                for skill, score in skill_scores.items():
                    st.progress(score / 100)
                    st.write(f"{skill}: {score}/100")

            with col2:
                st.subheader("Improvement Recommendations")
                for skill, score in skill_scores.items():
                    if score < 75:
                        st.info(
                            f"Consider improving {skill} through practice and training"
                        )
                    else:
                        st.success(f"Strong {skill} abilities!")


def show_resume_analysis_page():
    """Display resume analysis page"""

    st.header("📄 Resume Analysis & ATS Scoring")
    st.markdown(
        "Upload your resume to get detailed ATS scoring, keyword analysis, and improvement suggestions."
    )

    # File upload
    uploaded_file = st.file_uploader(
        "Upload your resume",
        type=["pdf", "docx", "doc"],
        help="Supported formats: PDF, DOCX, DOC",
    )

    # Target role selection
    target_role = st.selectbox(
        "Target Role (optional)",
        [
            "",
            "Software Engineer",
            "Data Scientist",
            "Product Manager",
            "Business Analyst",
            "UI/UX Designer",
            "Digital Marketing Manager",
            "Sales Manager",
        ],
    )

    if uploaded_file is not None:
        if st.button("Analyze Resume", type="primary"):
            with st.spinner("Analyzing your resume..."):
                # Save uploaded file temporarily
                with tempfile.NamedTemporaryFile(
                    delete=False, suffix=os.path.splitext(uploaded_file.name)[1]
                ) as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    tmp_file_path = tmp_file.name

                try:
                    # Call resume analysis API
                    analysis_result = analyze_resume_api(tmp_file_path, target_role)

                    if analysis_result:
                        display_resume_analysis(analysis_result)
                    else:
                        display_sample_resume_analysis()

                finally:
                    # Clean up temp file
                    if os.path.exists(tmp_file_path):
                        os.unlink(tmp_file_path)

    # Sample analysis button for demo
    if st.button("📊 See Sample Analysis"):
        display_sample_resume_analysis()


def analyze_resume_api(file_path: str, target_role: str) -> Optional[Dict[str, Any]]:
    """Call resume analysis API"""
    try:
        # In real implementation, this would call the resume_analyzer module
        files = {"resume": open(file_path, "rb")}
        data = {"target_role": target_role} if target_role else {}

        response = requests.post(
            f"{API_BASE_URL}/api/resume/analyze", files=files, data=data, timeout=30
        )

        if response.status_code == 200:
            return response.json()

        return None
    except Exception:
        st.error("Analysis error occurred")
        return None


def display_resume_analysis(analysis: Dict[str, Any]):
    """Display resume analysis results"""

    st.success("📊 Resume Analysis Complete!")

    # ATS Score
    ats_score = analysis.get("ats_score", 75)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("ATS Score", f"{ats_score:.0f}/100")

    with col2:
        score_color = (
            "green" if ats_score >= 80 else "orange" if ats_score >= 60 else "red"
        )
        st.markdown(
            f"<h3 style='color: {score_color}'>{'Excellent' if ats_score >= 80 else 'Good' if ats_score >= 60 else 'Needs Improvement'}</h3>",
            unsafe_allow_html=True,
        )

    with col3:
        if st.button("📄 Download Detailed Report"):
            st.info("PDF report feature coming soon!")

    # Detailed analysis sections
    tab1, tab2, tab3, tab4 = st.tabs(
        ["Strengths", "Weaknesses", "Keywords", "Suggestions"]
    )

    with tab1:
        st.subheader("✅ Strengths")
        strengths = analysis.get(
            "strengths", ["Well-structured format", "Clear contact information"]
        )
        for strength in strengths:
            st.write(f"• {strength}")

    with tab2:
        st.subheader("❌ Areas for Improvement")
        weaknesses = analysis.get(
            "weaknesses",
            ["Missing quantifiable achievements", "Limited technical keywords"],
        )
        for weakness in weaknesses:
            st.write(f"• {weakness}")

    with tab3:
        st.subheader("🔍 Keyword Analysis")
        missing_keywords = analysis.get(
            "missing_keywords", ["machine learning", "agile", "python"]
        )
        if missing_keywords:
            st.write("**Missing keywords for your target role:**")
            for keyword in missing_keywords:
                st.code(keyword)
        else:
            st.success("Great keyword coverage!")

    with tab4:
        st.subheader("💡 Improvement Suggestions")
        suggestions = analysis.get(
            "suggestions",
            [
                "Add more quantifiable achievements with numbers",
                "Include relevant technical keywords",
                "Add a professional summary section",
            ],
        )
        for suggestion in suggestions:
            st.write(f"• {suggestion}")

        # Project recommendations
        st.subheader("🚀 Recommended Projects")
        projects = analysis.get(
            "project_recommendations",
            [
                "Build a portfolio website with your projects",
                "Create a data analysis project using real datasets",
                "Contribute to open-source projects on GitHub",
            ],
        )
        for project in projects:
            st.write(f"• {project}")


def display_sample_resume_analysis():
    """Display sample resume analysis for demo"""
    sample_analysis = {
        "ats_score": 72,
        "strengths": [
            "Well-structured format with clear sections",
            "Professional contact information included",
            "Good use of action verbs",
            "Relevant work experience listed",
        ],
        "weaknesses": [
            "Missing quantifiable achievements",
            "Limited technical keywords for target role",
            "No professional summary section",
            "Skills section could be more detailed",
        ],
        "missing_keywords": [
            "machine learning",
            "agile methodology",
            "python",
            "data analysis",
            "project management",
        ],
        "suggestions": [
            "Add specific numbers and percentages to achievements",
            "Include more relevant technical keywords",
            "Add a compelling professional summary",
            "Quantify your impact in previous roles",
            "Include relevant certifications",
        ],
        "project_recommendations": [
            "Build a personal portfolio website showcasing your work",
            "Create a data analysis project with real datasets",
            "Develop a web application using modern frameworks",
            "Contribute to open-source projects on GitHub",
        ],
    }

    display_resume_analysis(sample_analysis)


def show_ai_chat_page():
    """Display AI chat interface"""

    st.header("🤖 AI Career Advisor Chat")
    st.markdown(
        "Chat with our AI advisor for personalized career guidance. Supports English, Hindi, and Hinglish!"
    )

    # Initialize chat history
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = [
            {
                "role": "assistant",
                "content": "Namaste! I'm your AI career advisor. I can help you with career guidance, skill development, and job search strategies. How can I assist you today? 🚀",
            }
        ]

    # Display chat messages
    for message in st.session_state.chat_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask me anything about your career..."):
        # Add user message
        st.session_state.chat_messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = get_ai_response(prompt)
                st.markdown(response)
                st.session_state.chat_messages.append(
                    {"role": "assistant", "content": response}
                )

    # Quick action buttons
    st.markdown("---")
    st.subheader("Quick Questions")

    quick_col1, quick_col2, quick_col3 = st.columns(3)

    with quick_col1:
        if st.button("💼 Career change advice"):
            prompt = "I want to change my career. What should I consider?"
            st.session_state.chat_messages.append({"role": "user", "content": prompt})
            response = get_ai_response(prompt)
            st.session_state.chat_messages.append(
                {"role": "assistant", "content": response}
            )
            st.rerun()

    with quick_col2:
        if st.button("📚 Skill development"):
            prompt = "What skills should I focus on for my career growth?"
            st.session_state.chat_messages.append({"role": "user", "content": prompt})
            response = get_ai_response(prompt)
            st.session_state.chat_messages.append(
                {"role": "assistant", "content": response}
            )
            st.rerun()

    with quick_col3:
        if st.button("🎯 Interview preparation"):
            prompt = "How should I prepare for technical interviews?"
            st.session_state.chat_messages.append({"role": "user", "content": prompt})
            response = get_ai_response(prompt)
            st.session_state.chat_messages.append(
                {"role": "assistant", "content": response}
            )
            st.rerun()


def get_ai_response(prompt: str) -> str:
    """Get AI response from the API"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/ai/chat",
            json={
                "message": prompt,
                "language": st.session_state.get("language_preference", "English"),
            },
            timeout=30,
        )

        if response.status_code == 200:
            return response.json()["response"]
        else:
            return "I'm sorry, I'm having trouble connecting right now. Please try again later."

    except Exception as e:
        # Fallback responses
        fallback_responses = {
            "career change": "Career change is a big decision! Consider your transferable skills, market demand, financial planning, and start building relevant skills gradually. What specific field interests you?",
            "skill development": "Focus on both technical and soft skills! For technical: learn programming, data analysis, or digital marketing. For soft skills: communication, leadership, and problem-solving are always valuable.",
            "interview": "For interviews: research the company, practice common questions, prepare specific examples using the STAR method, and always have thoughtful questions ready about the role and company culture.",
            "default": "I understand you're looking for career guidance. While I'm temporarily offline, I'd recommend focusing on continuous learning, networking, and building a strong portfolio. What specific area would you like to explore?",
        }

        prompt_lower = prompt.lower()
        for key in fallback_responses:
            if key in prompt_lower:
                return fallback_responses[key]

        return fallback_responses["default"]


def show_personality_test():
    """Display Big Five personality test"""
    st.subheader("🧠 Big Five Personality Test")
    st.markdown("Assess your personality across five major dimensions.")
    st.info("This feature is coming soon!")


def show_complete_assessment():
    """Display complete psychological assessment"""
    st.subheader("🎯 Complete Psychological Profile")
    st.markdown(
        "Take all assessments to get a comprehensive career personality profile."
    )
    st.info("This feature combines all tests and is coming soon!")


def show_recommendations_page():
    """Display the career recommendations page"""

    st.header("📋 Get Personalized Career Recommendations")

    # Create two columns
    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("Your Profile")

        # Profile form
        with st.form("profile_form"):
            name = st.text_input("Name (optional)", placeholder="Your name")

            interests = st.text_area(
                "Interests",
                placeholder="e.g., technology, design, data analysis, healthcare",
                help="Enter your interests separated by commas",
            )

            skills = st.text_area(
                "Current Skills",
                placeholder="e.g., python, project management, communication",
                help="List your current skills separated by commas",
            )

            goals = st.text_area(
                "Career Goals",
                placeholder="e.g., become a data scientist, lead a team, work remotely",
                help="Describe your career goals separated by commas",
            )

            experience_years = st.number_input(
                "Years of Experience",
                min_value=0.0,
                max_value=50.0,
                value=0.0,
                step=0.5,
                help="Total years of professional experience",
            )

            education_level = st.selectbox(
                "Education Level",
                [
                    "",
                    "High School",
                    "Bachelor's Degree",
                    "Master's Degree",
                    "PhD",
                    "Other",
                ],
                help="Your highest level of education",
            )

            location = st.text_input(
                "Location (optional)",
                placeholder="e.g., San Francisco, Remote, New York",
            )

            submit_button = st.form_submit_button("Get Recommendations", type="primary")

    with col2:
        if submit_button:
            if not any([interests, skills, goals]):
                st.error("Please fill in at least one of: interests, skills, or goals.")
                return

            # Prepare profile data
            profile_data = {
                "name": name if name else None,
                "interests": [
                    item.strip() for item in interests.split(",") if item.strip()
                ],
                "skills": [item.strip() for item in skills.split(",") if item.strip()],
                "goals": [item.strip() for item in goals.split(",") if item.strip()],
                "experience_years": experience_years if experience_years > 0 else None,
                "education_level": education_level if education_level else None,
                "location": location if location else None,
            }

            # Get recommendations
            with st.spinner("Generating your personalized recommendations..."):
                recommendations = get_recommendations(profile_data)

            if recommendations:
                display_recommendations(recommendations)
            else:
                # Fallback to local recommendations
                st.warning("API unavailable. Showing sample recommendations.")
                display_fallback_recommendations(profile_data)


def get_recommendations(profile_data: dict) -> Optional[dict]:
    """Get recommendations from API"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/recommend", json={"profile": profile_data}, timeout=10
        )
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API Error: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Connection error: {str(e)}")
        return None


def display_recommendations(data: dict):
    """Display the recommendations from API response"""

    recommendations = data["recommendations"]

    st.subheader("🎯 Your Personalized Recommendations")

    # Career Paths
    if recommendations["career_paths"]:
        st.markdown("### 🚀 Recommended Career Paths")

        for i, path in enumerate(recommendations["career_paths"][:3]):
            with st.expander(
                f"{path['role']} - {path['industry']} (Match: {path['score']:.0%})"
            ):
                st.markdown(f"**Why this fits:** {path['match_reason']}")
                st.markdown(f"**Growth Potential:** {path['growth_potential']}")
                st.markdown(f"**Salary Range:** {path['salary_range']}")

                st.markdown("**Required Skills:**")
                st.write(", ".join(path["required_skills"]))

                st.markdown("**Next Steps:**")
                for step in path["next_steps"]:
                    st.write(f"• {step}")

    # Learning Resources
    if recommendations["learning_resources"]:
        st.markdown("### 📚 Recommended Learning Resources")

        for resource in recommendations["learning_resources"][:4]:
            with st.container():
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"**[{resource['title']}]({resource['url']})**")
                    st.write(resource["description"])
                    st.caption(
                        f"Provider: {resource.get('provider', 'Unknown')} | Duration: {resource.get('duration', 'N/A')}"
                    )
                with col2:
                    st.markdown(f"**Level:** {resource.get('level', 'N/A')}")
                    st.markdown(f"**Cost:** {resource.get('cost', 'N/A')}")
                st.divider()

    # Skills to Develop
    if recommendations["skills_to_develop"]:
        st.markdown("### 🎯 Skills to Develop")
        cols = st.columns(3)
        for i, skill in enumerate(recommendations["skills_to_develop"][:6]):
            with cols[i % 3]:
                st.info(skill)

    # Additional Resources
    col1, col2 = st.columns(2)

    with col1:
        if recommendations["mentorship_opportunities"]:
            st.markdown("### 👥 Mentorship Opportunities")
            for mentor in recommendations["mentorship_opportunities"][:2]:
                st.markdown(
                    f"- **[{mentor['title']}]({mentor['url']})**: {mentor['description']}"
                )

    with col2:
        if recommendations["job_opportunities"]:
            st.markdown("### 💼 Job Search Resources")
            for job in recommendations["job_opportunities"][:2]:
                st.markdown(
                    f"- **[{job['title']}]({job['url']})**: {job['description']}"
                )


def display_fallback_recommendations(profile_data: dict):
    """Display fallback recommendations when API is unavailable"""

    st.subheader("🎯 Sample Career Guidance")
    st.info(
        "This is a demo version. Connect to the API for personalized recommendations."
    )

    # Sample career paths based on profile
    user_skills = [skill.lower() for skill in profile_data.get("skills", [])]
    user_interests = [
        interest.lower() for interest in profile_data.get("interests", [])
    ]

    # Simple matching logic for demo
    if any(
        skill in ["python", "programming", "coding"]
        for skill in user_skills + user_interests
    ):
        st.markdown("### 🚀 Recommended: Software Engineer")
        st.write(
            "Based on your programming interests, software engineering could be a great fit!"
        )
        st.write(
            "**Next steps:** Build portfolio projects, learn frameworks, practice algorithms"
        )

    if any(
        skill in ["data", "analysis", "statistics"]
        for skill in user_skills + user_interests
    ):
        st.markdown("### 📊 Recommended: Data Scientist")
        st.write(
            "Your analytical skills suggest data science could be perfect for you!"
        )
        st.write(
            "**Next steps:** Learn Python/R, practice with datasets, understand machine learning"
        )

    # Sample resources
    st.markdown("### 📚 Learning Resources")
    st.markdown("- [Python for Beginners](https://docs.python.org/3/tutorial/)")
    st.markdown(
        "- [Data Science Handbook](https://jakevdp.github.io/PythonDataScienceHandbook/)"
    )
    st.markdown("- [Free Code Camp](https://www.freecodecamp.org/)")


def show_resources_page():
    """Display the resources browser page"""

    st.header("📚 Browse Learning Resources")

    # Show disclaimer at the top
    st.info(
        "📣 **Legal Disclaimer**: All guidance resources provided are external third-party materials. These resources are curated for educational purposes and are suitable for various skill levels (beginner to advanced). Margadarsaka does not own, control, or guarantee the accuracy, completeness, or availability of external content. Users should verify information independently and use resources at their own discretion."
    )

    # Resource type filter
    resource_type = st.selectbox(
        "Filter by type:",
        [
            "All Resources",
            "Learning Courses",
            "Job Search",
            "Mentorship",
            "Career Roadmaps",
        ],
    )

    # Special handling for roadmaps
    if resource_type == "Career Roadmaps":
        show_roadmaps_section()
    else:
        # Try to get resources from API
        resources = get_resources_from_api(resource_type)

        if resources:
            display_resources_grid(resources)
        else:
            st.warning("API unavailable. Showing sample resources.")
            display_sample_resources()


def show_roadmaps_section():
    """Display roadmap.sh roadmaps section"""
    st.markdown("### 🗺️ Career & Skill Roadmaps")
    st.markdown("*Powered by roadmap.sh - Interactive learning paths for developers*")

    # Roadmap category filter
    roadmap_category = st.selectbox(
        "Choose roadmap category:",
        ["All Roadmaps", "Role-Based Roadmaps", "Skill-Based Roadmaps"],
    )

    # Get roadmaps from API
    try:
        category_map = {
            "All Roadmaps": "all",
            "Role-Based Roadmaps": "role_based",
            "Skill-Based Roadmaps": "skill_based",
        }

        response = requests.get(
            f"{API_BASE_URL}/api/resources/roadmaps?category={category_map[roadmap_category]}"
        )
        if response.status_code == 200:
            data = response.json()
            roadmaps = data.get("roadmaps", [])

            st.write(f"**Found {len(roadmaps)} roadmaps**")

            # Display roadmaps in grid
            cols = st.columns(3)
            for i, roadmap in enumerate(roadmaps):
                with cols[i % 3]:
                    with st.container():
                        st.markdown(f"**{roadmap['title']}**")
                        st.markdown(roadmap["description"])
                        st.markdown(
                            f"🏷️ *{roadmap.get('category', 'roadmap').replace('_', ' ').title()}*"
                        )
                        if st.button("View Roadmap", key=f"roadmap_{i}"):
                            st.write(f"🔗 [Open {roadmap['title']}]({roadmap['url']})")
                        st.markdown("---")

        else:
            st.error("Failed to load roadmaps from API")

    except Exception as e:
        st.error(f"Error loading roadmaps: {str(e)}")
        show_sample_roadmaps()


def show_sample_roadmaps():
    """Show sample roadmaps when API is unavailable"""
    st.markdown("### 🗺️ Sample Career Roadmaps")

    sample_roadmaps = [
        {
            "title": "Frontend Developer",
            "url": "https://roadmap.sh/frontend",
            "description": "Complete frontend development learning path",
        },
        {
            "title": "Backend Developer",
            "url": "https://roadmap.sh/backend",
            "description": "Full backend development roadmap",
        },
        {
            "title": "Python",
            "url": "https://roadmap.sh/python",
            "description": "Python programming language mastery",
        },
        {
            "title": "DevOps",
            "url": "https://roadmap.sh/devops",
            "description": "DevOps practices and tools",
        },
        {
            "title": "Data Science",
            "url": "https://roadmap.sh/ai-data-scientist",
            "description": "Data science and AI career path",
        },
        {
            "title": "Cybersecurity",
            "url": "https://roadmap.sh/cyber-security",
            "description": "Cybersecurity fundamentals and advanced topics",
        },
    ]

    cols = st.columns(3)
    for i, roadmap in enumerate(sample_roadmaps):
        with cols[i % 3]:
            st.markdown(f"**{roadmap['title']}**")
            st.markdown(roadmap["description"])
            st.markdown(f"🔗 [View Roadmap]({roadmap['url']})")
            st.markdown("---")


def get_resources_from_api(resource_type: str) -> Optional[list]:
    """Get resources from API"""
    try:
        if resource_type == "All Resources":
            endpoint = f"{API_BASE_URL}/api/resources"
        elif resource_type == "Learning Courses":
            endpoint = f"{API_BASE_URL}/api/resources/learning"
        elif resource_type == "Job Search":
            endpoint = f"{API_BASE_URL}/api/resources/jobs"
        elif resource_type == "Mentorship":
            endpoint = f"{API_BASE_URL}/api/resources/mentorship"
        else:
            return None

        response = requests.get(endpoint, timeout=5)
        if response.status_code == 200:
            return response.json()["resources"]
        return None
    except Exception:
        return None


def display_resources_grid(resources: list):
    """Display resources in a grid layout"""

    for i in range(0, len(resources), 2):
        col1, col2 = st.columns(2)

        with col1:
            if i < len(resources):
                display_resource_card(resources[i])

        with col2:
            if i + 1 < len(resources):
                display_resource_card(resources[i + 1])


def display_resource_card(resource: dict):
    """Display a single resource card"""

    with st.container():
        st.markdown(f"### [{resource['title']}]({resource['url']})")
        st.write(resource["description"])

        col1, col2 = st.columns(2)
        with col1:
            st.caption(f"**Type:** {resource.get('type', 'N/A')}")
            st.caption(f"**Level:** {resource.get('level', 'N/A')}")
        with col2:
            st.caption(f"**Provider:** {resource.get('provider', 'N/A')}")
            st.caption(f"**Cost:** {resource.get('cost', 'N/A')}")

        if resource.get("tags"):
            st.markdown("**Tags:** " + ", ".join(resource["tags"]))

        st.divider()


def display_sample_resources():
    """Display sample resources when API is unavailable"""

    sample_resources = [
        {
            "title": "Python for Beginners",
            "url": "https://docs.python.org/3/tutorial/",
            "description": "Official Python tutorial covering fundamentals",
            "type": "course",
            "level": "beginner",
            "provider": "Python.org",
            "cost": "Free",
            "tags": ["python", "programming"],
        },
        {
            "title": "LinkedIn Learning",
            "url": "https://www.linkedin.com/learning/",
            "description": "Professional development courses",
            "type": "course",
            "level": "all",
            "provider": "LinkedIn",
            "cost": "$29.99/month",
            "tags": ["business", "technology"],
        },
    ]

    display_resources_grid(sample_resources)


def show_progress_page():
    """Display the progress tracking page"""

    st.header("📈 Progress Tracker")
    st.info(
        "This feature will help you track your skill development and career progress."
    )

    # Simple progress tracker
    st.subheader("Skill Development Goals")

    # Sample skills with progress
    skills_progress = {
        "Python Programming": 75,
        "Data Analysis": 60,
        "Communication": 80,
        "Project Management": 45,
    }

    for skill, progress in skills_progress.items():
        st.markdown(f"**{skill}**")
        st.progress(progress / 100)
        st.caption(f"{progress}% complete")

    st.subheader("Set New Goals")

    with st.form("goal_form"):
        new_skill = st.text_input("Skill to develop")
        st.date_input("Target completion date")
        st.selectbox("Priority", ["High", "Medium", "Low"])

        if st.form_submit_button("Add Goal"):
            st.success(f"Added goal: {new_skill}")


if __name__ == "__main__":
    main()
