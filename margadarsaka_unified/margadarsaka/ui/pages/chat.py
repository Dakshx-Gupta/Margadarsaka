"""
Chat Page - AI Career Counselor Interface
"""

import streamlit as st
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

# Import components with fallbacks
try:
    from margadarsaka.ui.utils.i18n import get_text
    from margadarsaka.ui.utils.state_manager import get_state_manager

    COMPONENTS_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Chat page components not available: {e}")
    COMPONENTS_AVAILABLE = False

    def get_text(key, default):
        return default


class ChatInterface:
    """AI Career Counselor Chat Interface"""

    def __init__(self):
        self.state = get_state_manager() if COMPONENTS_AVAILABLE else None

        # Initialize chat history
        if "chat_messages" not in st.session_state:
            st.session_state.chat_messages = [
                {
                    "role": "assistant",
                    "content": get_text(
                        "welcome_message",
                        "Namaste! I am your AI career counselor. How can I help you with your career journey today?",
                    ),
                    "timestamp": "00:00",
                }
            ]

    def render_header(self):
        """Render chat page header"""
        st.markdown(
            f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 2rem; border-radius: 20px; margin-bottom: 2rem; text-align: center;
                    box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);">
            <h1 style="color: white; margin: 0; font-size: 2.5rem;">
                💬 {get_text("ai_counselor", "AI Career Counselor")}
            </h1>
            <p style="color: rgba(255,255,255,0.9); margin: 1rem 0 0 0; font-size: 1.2rem;">
                {get_text("chat_subtitle", "Get personalized career guidance and support")}
            </p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    def render_chat_features(self):
        """Render chat features and capabilities"""
        st.markdown(f"### 🌟 {get_text('what_i_can_help', 'What I Can Help You With')}")

        features = [
            {
                "icon": "🎯",
                "title": get_text("career_planning", "Career Planning"),
                "desc": get_text(
                    "career_planning_desc",
                    "Explore career paths and set professional goals",
                ),
            },
            {
                "icon": "📊",
                "title": get_text("skill_assessment", "Skill Assessment"),
                "desc": get_text(
                    "skill_assessment_desc",
                    "Identify strengths and areas for improvement",
                ),
            },
            {
                "icon": "💼",
                "title": get_text("job_search", "Job Search Strategy"),
                "desc": get_text(
                    "job_search_desc",
                    "Tips for finding and applying to jobs effectively",
                ),
            },
            {
                "icon": "📝",
                "title": get_text("resume_help", "Resume & Interview Help"),
                "desc": get_text(
                    "resume_help_desc", "Improve your resume and interview skills"
                ),
            },
            {
                "icon": "🌱",
                "title": get_text("career_growth", "Career Growth"),
                "desc": get_text(
                    "career_growth_desc",
                    "Advance in your current role or switch careers",
                ),
            },
            {
                "icon": "🎓",
                "title": get_text("education_guidance", "Education Guidance"),
                "desc": get_text(
                    "education_guidance_desc",
                    "Choose courses and certifications for your goals",
                ),
            },
        ]

        # Display features in grid
        for i in range(0, len(features), 3):
            cols = st.columns(3)
            for j, col in enumerate(cols):
                if i + j < len(features):
                    feature = features[i + j]
                    with col:
                        st.markdown(
                            f"""
                        <div class="feature-card" style="text-align: center; padding: 1rem; border-radius: 10px; 
                                                       border: 1px solid #e0e0e0; margin-bottom: 1rem;">
                            <div style="font-size: 2em; margin-bottom: 0.5rem;">{feature["icon"]}</div>
                            <h4 style="margin: 0 0 8px 0; color: var(--primary-color);">{feature["title"]}</h4>
                            <p style="margin: 0; color: var(--text-secondary); font-size: 0.9em;">{feature["desc"]}</p>
                        </div>
                        """,
                            unsafe_allow_html=True,
                        )

    def render_suggested_questions(self):
        """Render suggested questions for users"""
        st.markdown(f"### 💡 {get_text('suggested_questions', 'Suggested Questions')}")

        questions = [
            get_text("q1", "What career path is best suited for my personality?"),
            get_text("q2", "How can I transition from my current field to tech?"),
            get_text("q3", "What skills should I develop for better job prospects?"),
            get_text("q4", "How do I negotiate salary in my next job?"),
            get_text("q5", "What certifications would help advance my career?"),
            get_text("q6", "How can I improve my interview performance?"),
        ]

        # Display questions as clickable buttons
        cols = st.columns(2)
        for i, question in enumerate(questions):
            with cols[i % 2]:
                if st.button(
                    f"💭 {question}", key=f"suggested_q_{i}", use_container_width=True
                ):
                    # Add question to chat
                    self.add_message("user", question)
                    self.generate_ai_response(question)
                    st.rerun()

    def add_message(self, role: str, content: str):
        """Add a message to chat history"""
        import datetime

        timestamp = datetime.datetime.now().strftime("%H:%M")

        st.session_state.chat_messages.append(
            {"role": role, "content": content, "timestamp": timestamp}
        )

    def generate_ai_response(self, user_message: str):
        """Generate AI response (placeholder implementation)"""
        # This is a simple pattern-based response system
        # In a real implementation, this would call an AI service

        user_lower = user_message.lower()

        if any(
            word in user_lower
            for word in ["career path", "career change", "what career"]
        ):
            response = get_text(
                "career_response",
                """Great question about career paths! To provide the best guidance, I'd need to know more about:

🎯 **Your interests and passions** - What activities energize you?
📊 **Your current skills** - What are you good at naturally?
🎓 **Your educational background** - What have you studied?
💼 **Your work experience** - What roles have you held?
🌟 **Your values** - What's important to you in work?

Would you like to take our comprehensive assessment to get personalized career recommendations? Or feel free to share more about any of these areas!""",
            )

        elif any(
            word in user_lower
            for word in ["tech", "technology", "programming", "software"]
        ):
            response = get_text(
                "tech_response",
                """Excellent choice! Tech is a growing field with many opportunities. Here's a roadmap for transitioning to tech:

🚀 **Start with fundamentals:**
• Choose a programming language (Python is beginner-friendly)
• Learn basic computer science concepts
• Practice with online platforms like Codecademy or freeCodeCamp

💻 **Build projects:**
• Create a portfolio of 3-5 projects
• Contribute to open-source projects
• Document your learning journey

🔗 **Network and learn:**
• Join tech communities (Discord, Reddit, local meetups)
• Find a mentor in your target field
• Attend tech events and workshops

📚 **Consider formal education:**
• Bootcamps (3-6 months, intensive)
• Online degrees
• Professional certifications

What specific area of tech interests you most? Web development, data science, mobile apps, or something else?""",
            )

        elif any(
            word in user_lower for word in ["skills", "skill development", "learn"]
        ):
            response = get_text(
                "skills_response",
                """Skills development is key to career growth! Here are the most in-demand skills:

🔧 **Technical Skills:**
• Digital literacy (essential for all fields)
• Data analysis and Excel proficiency
• Programming/coding basics
• Digital marketing and social media

🤝 **Soft Skills:**
• Communication and presentation
• Leadership and team management
• Problem-solving and critical thinking
• Adaptability and learning agility

📈 **Industry-Specific Skills:**
• Project management (PMP, Agile, Scrum)
• Design thinking and user experience
• Financial analysis and business intelligence
• Language skills for global markets

**My recommendations:**
1. Take our skills assessment to identify gaps
2. Choose 2-3 skills to focus on this year
3. Set aside 30 minutes daily for learning
4. Practice through real projects or volunteering

Which skills area would you like to explore first?""",
            )

        elif any(
            word in user_lower
            for word in ["salary", "negotiate", "pay", "compensation"]
        ):
            response = get_text(
                "salary_response",
                """Salary negotiation is an important skill! Here's a strategic approach:

📊 **Research first:**
• Use sites like Glassdoor, PayScale, Naukri for salary data
• Consider location, experience, company size
• Know the market rate for your role

💪 **Build your case:**
• Document your achievements and impact
• Quantify your contributions (numbers, percentages)
• Gather positive feedback and testimonials
• Research the company's financial health

🗣️ **Negotiation strategies:**
• Start with a range, not a single number
• Consider the total package (benefits, growth opportunities)
• Be prepared to explain your value proposition
• Practice your pitch beforehand

⏰ **Timing matters:**
• Best time: during performance reviews or job offers
• Avoid: during company struggles or budget cuts
• Be patient: negotiations can take time

Remember: The worst they can say is no. Most employers expect some negotiation. Would you like help preparing for a specific negotiation scenario?""",
            )

        elif any(
            word in user_lower for word in ["interview", "interviews", "interview tips"]
        ):
            response = get_text(
                "interview_response",
                """Interview success comes from preparation! Here's your complete guide:

🎯 **Before the interview:**
• Research the company, role, and interviewer
• Prepare 5-7 questions to ask them
• Practice STAR method for behavioral questions
• Prepare specific examples of your achievements

🗣️ **During the interview:**
• Arrive 10 minutes early (not too early!)
• Maintain good eye contact and body language
• Listen actively and ask clarifying questions
• Be specific in your answers with concrete examples

💼 **Common question types:**
• "Tell me about yourself" (2-minute career summary)
• Behavioral: "Tell me about a time when..."
• Technical: Role-specific skills assessment
• Culture fit: "Why do you want to work here?"

✨ **Follow-up:**
• Send thank-you email within 24 hours
• Reiterate your interest and key qualifications
• Be patient but follow up if you don't hear back

Would you like me to help you prepare for a specific type of interview or practice answering common questions?""",
            )

        else:
            # Generic helpful response
            response = get_text(
                "generic_response",
                f"""Thank you for your question! I'm here to help with your career journey.

Based on what you've shared, I'd love to learn more about your specific situation to provide the most helpful guidance. 

Here are some ways I can assist you:

🎯 **Career Exploration** - Discover paths that match your interests
📊 **Skills Assessment** - Identify your strengths and growth areas  
💼 **Job Search Strategy** - Find and apply for roles effectively
📝 **Resume & Interview Prep** - Improve your application materials
🌱 **Professional Development** - Plan your career growth

Could you tell me more about:
• Your current career situation
• Your goals and aspirations
• Any specific challenges you're facing

Feel free to ask me anything about careers, job searching, skills development, or professional growth!""",
            )

        self.add_message("assistant", response)

    def render_chat_interface(self):
        """Render the main chat interface"""
        st.markdown(f"### 💬 {get_text('chat_conversation', 'Conversation')}")

        # Chat container
        chat_container = st.container()

        with chat_container:
            # Display chat messages
            for message in st.session_state.chat_messages:
                if message["role"] == "user":
                    st.markdown(
                        f"""
                    <div style="display: flex; justify-content: flex-end; margin-bottom: 1rem;">
                        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                                    color: white; padding: 1rem; border-radius: 20px 20px 5px 20px; 
                                    max-width: 70%; box-shadow: 0 2px 10px rgba(102, 126, 234, 0.3);">
                            <div style="font-size: 0.9rem; margin-bottom: 0.5rem;">{message["content"]}</div>
                            <div style="font-size: 0.7rem; opacity: 0.8; text-align: right;">{message["timestamp"]}</div>
                        </div>
                    </div>
                    """,
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        f"""
                    <div style="display: flex; justify-content: flex-start; margin-bottom: 1rem;">
                        <div style="background: #f0f2f6; color: #333; padding: 1rem; 
                                    border-radius: 20px 20px 20px 5px; max-width: 70%;
                                    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);">
                            <div style="font-size: 0.9rem; margin-bottom: 0.5rem; white-space: pre-line;">{message["content"]}</div>
                            <div style="font-size: 0.7rem; opacity: 0.6; text-align: left;">🤖 AI Counselor • {message["timestamp"]}</div>
                        </div>
                    </div>
                    """,
                        unsafe_allow_html=True,
                    )

        # Chat input
        st.markdown("---")

        # Create input form
        with st.form(key="chat_form", clear_on_submit=True):
            col1, col2 = st.columns([4, 1])

            with col1:
                user_input = st.text_area(
                    get_text("type_message", "Type your message..."),
                    placeholder=get_text(
                        "message_placeholder", "Ask me anything about your career..."
                    ),
                    height=100,
                    label_visibility="collapsed",
                )

            with col2:
                st.markdown("<br>", unsafe_allow_html=True)  # Add spacing
                submit_button = st.form_submit_button(
                    f"📤 {get_text('send', 'Send')}",
                    use_container_width=True,
                    type="primary",
                )

        # Handle message submission
        if submit_button and user_input.strip():
            self.add_message("user", user_input.strip())

            # Show typing indicator
            with st.spinner(get_text("ai_thinking", "AI is thinking...")):
                import time

                time.sleep(1)  # Simulate thinking time
                self.generate_ai_response(user_input.strip())

            st.rerun()

    def render_chat_actions(self):
        """Render chat action buttons"""
        st.markdown("---")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            if st.button(
                f"🧠 {get_text('take_assessment', 'Take Assessment')}",
                use_container_width=True,
            ):
                st.info(
                    get_text("assessment_redirect", "Redirecting to assessment page...")
                )

        with col2:
            if st.button(
                f"📄 {get_text('build_resume', 'Build Resume')}",
                use_container_width=True,
            ):
                st.info(get_text("resume_redirect", "Redirecting to resume builder..."))

        with col3:
            if st.button(
                f"💾 {get_text('save_chat', 'Save Chat')}", use_container_width=True
            ):
                st.success(get_text("chat_saved", "Chat conversation saved!"))

        with col4:
            if st.button(
                f"🗑️ {get_text('clear_chat', 'Clear Chat')}", use_container_width=True
            ):
                st.session_state.chat_messages = [
                    {
                        "role": "assistant",
                        "content": get_text(
                            "welcome_message",
                            "Namaste! I am your AI career counselor. How can I help you with your career journey today?",
                        ),
                        "timestamp": "00:00",
                    }
                ]
                st.rerun()

    def render(self):
        """Main render method"""
        self.render_header()

        # Create tabs for different sections
        tabs = st.tabs(
            [
                f"💬 {get_text('chat', 'Chat')}",
                f"🌟 {get_text('features', 'Features')}",
                f"💡 {get_text('suggestions', 'Suggestions')}",
            ]
        )

        with tabs[0]:
            self.render_chat_interface()
            self.render_chat_actions()

        with tabs[1]:
            self.render_chat_features()

        with tabs[2]:
            self.render_suggested_questions()


def show_chat_page():
    """Function to show the chat page"""
    chat_interface = ChatInterface()
    chat_interface.render()
