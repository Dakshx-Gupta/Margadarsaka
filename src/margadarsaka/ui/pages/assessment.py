"""
Assessment Page - Psychological Assessment Interface
Complete implementation using the forms and components
"""

import streamlit as st
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

# Import components with fallbacks
try:
    from margadarsaka.ui.components.forms import (
        AssessmentForm,
        AssessmentSection,
        AssessmentQuestion,
        QuestionType,
    )
    from margadarsaka.ui.utils.i18n import get_text
    from margadarsaka.ui.utils.state_manager import get_state_manager

    COMPONENTS_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Assessment page components not available: {e}")
    COMPONENTS_AVAILABLE = False


def create_personality_assessment() -> List[AssessmentSection]:
    """Create the personality assessment sections"""

    if not COMPONENTS_AVAILABLE:
        return []

    # Big Five Personality Traits Assessment
    personality_section = AssessmentSection(
        id="personality",
        title=get_text("personality_traits", "Personality Traits"),
        description=get_text(
            "personality_desc", "Discover your Big Five personality traits"
        ),
        icon="🧠",
        time_estimate=15,
    )

    # Extraversion questions
    personality_section.questions.extend(
        [
            AssessmentQuestion(
                id="extra_1",
                text=get_text(
                    "extra_q1", "I am outgoing and sociable in social situations"
                ),
                question_type=QuestionType.SCALE,
                scale_min=1,
                scale_max=5,
                scale_labels={
                    1: get_text("strongly_disagree", "Strongly Disagree"),
                    5: get_text("strongly_agree", "Strongly Agree"),
                },
                category="extraversion",
            ),
            AssessmentQuestion(
                id="extra_2",
                text=get_text(
                    "extra_q2", "I prefer working in teams rather than alone"
                ),
                question_type=QuestionType.SCALE,
                scale_min=1,
                scale_max=5,
                scale_labels={
                    1: get_text("strongly_disagree", "Strongly Disagree"),
                    5: get_text("strongly_agree", "Strongly Agree"),
                },
                category="extraversion",
            ),
            AssessmentQuestion(
                id="extra_3",
                text=get_text("extra_q3", "I feel energized by being around people"),
                question_type=QuestionType.SCALE,
                scale_min=1,
                scale_max=5,
                scale_labels={
                    1: get_text("strongly_disagree", "Strongly Disagree"),
                    5: get_text("strongly_agree", "Strongly Agree"),
                },
                category="extraversion",
            ),
        ]
    )

    # Conscientiousness questions
    personality_section.questions.extend(
        [
            AssessmentQuestion(
                id="cons_1",
                text=get_text("cons_q1", "I am organized and pay attention to details"),
                question_type=QuestionType.SCALE,
                scale_min=1,
                scale_max=5,
                scale_labels={
                    1: get_text("strongly_disagree", "Strongly Disagree"),
                    5: get_text("strongly_agree", "Strongly Agree"),
                },
                category="conscientiousness",
            ),
            AssessmentQuestion(
                id="cons_2",
                text=get_text("cons_q2", "I complete tasks on time and meet deadlines"),
                question_type=QuestionType.SCALE,
                scale_min=1,
                scale_max=5,
                scale_labels={
                    1: get_text("strongly_disagree", "Strongly Disagree"),
                    5: get_text("strongly_agree", "Strongly Agree"),
                },
                category="conscientiousness",
            ),
        ]
    )

    # Career Interests Section
    interests_section = AssessmentSection(
        id="interests",
        title=get_text("career_interests", "Career Interests"),
        description=get_text(
            "interests_desc", "Explore your professional interests and preferences"
        ),
        icon="💼",
        time_estimate=20,
    )

    interests_section.questions.extend(
        [
            AssessmentQuestion(
                id="int_1",
                text=get_text(
                    "int_q1", "Which of these activities interests you most?"
                ),
                question_type=QuestionType.MULTIPLE_CHOICE,
                options=[
                    get_text("int_opt1", "Solving technical problems"),
                    get_text("int_opt2", "Helping and advising people"),
                    get_text("int_opt3", "Creating and designing things"),
                    get_text("int_opt4", "Leading and managing teams"),
                    get_text("int_opt5", "Analyzing data and information"),
                ],
                category="interests",
            ),
            AssessmentQuestion(
                id="int_2",
                text=get_text("int_q2", "What type of work environment do you prefer?"),
                question_type=QuestionType.MULTIPLE_CHOICE,
                options=[
                    get_text("env_opt1", "Quiet office with minimal interruptions"),
                    get_text("env_opt2", "Collaborative open workspace"),
                    get_text("env_opt3", "Field work or outdoor settings"),
                    get_text("env_opt4", "Home office or remote work"),
                    get_text("env_opt5", "Fast-paced, dynamic environment"),
                ],
                category="work_environment",
            ),
            AssessmentQuestion(
                id="int_3",
                text=get_text(
                    "int_q3",
                    "Rank these career fields by your interest level (1 = most interested)",
                ),
                question_type=QuestionType.RANKING,
                options=[
                    get_text("field1", "Technology & Engineering"),
                    get_text("field2", "Healthcare & Medicine"),
                    get_text("field3", "Business & Finance"),
                    get_text("field4", "Education & Training"),
                    get_text("field5", "Arts & Creative Fields"),
                ],
                category="field_preference",
            ),
        ]
    )

    # Skills Assessment Section
    skills_section = AssessmentSection(
        id="skills",
        title=get_text("skills_assessment", "Skills Assessment"),
        description=get_text(
            "skills_desc", "Evaluate your current skills and abilities"
        ),
        icon="🛠️",
        time_estimate=10,
    )

    skills_section.questions.extend(
        [
            AssessmentQuestion(
                id="skill_1",
                text=get_text("skill_q1", "Rate your technical/computer skills"),
                question_type=QuestionType.SCALE,
                scale_min=1,
                scale_max=10,
                scale_labels={
                    1: get_text("beginner", "Beginner"),
                    10: get_text("expert", "Expert"),
                },
                category="technical_skills",
            ),
            AssessmentQuestion(
                id="skill_2",
                text=get_text("skill_q2", "Rate your communication skills"),
                question_type=QuestionType.SCALE,
                scale_min=1,
                scale_max=10,
                scale_labels={
                    1: get_text("poor", "Poor"),
                    10: get_text("excellent", "Excellent"),
                },
                category="soft_skills",
            ),
            AssessmentQuestion(
                id="skill_3",
                text=get_text(
                    "skill_q3",
                    "Which skills would you like to develop? (Select all that apply)",
                ),
                question_type=QuestionType.MULTISELECT,
                options=[
                    get_text("dev_skill1", "Programming & Software Development"),
                    get_text("dev_skill2", "Data Analysis & Statistics"),
                    get_text("dev_skill3", "Leadership & Management"),
                    get_text("dev_skill4", "Public Speaking & Presentation"),
                    get_text("dev_skill5", "Creative & Design Skills"),
                    get_text("dev_skill6", "Financial & Business Analysis"),
                ],
                category="skill_development",
            ),
        ]
    )

    return [personality_section, interests_section, skills_section]


class AssessmentPage:
    """Assessment page component"""

    def __init__(self):
        self.state = get_state_manager() if COMPONENTS_AVAILABLE else None

    def render_intro(self):
        """Render assessment introduction"""
        st.markdown(
            f"""
        <div style="background: linear-gradient(135deg, #2E86AB 0%, #A23B72 100%); 
                    padding: 2rem; border-radius: 20px; margin-bottom: 2rem; text-align: center;
                    box-shadow: 0 10px 30px rgba(46, 134, 171, 0.3);">
            <h1 style="color: white; margin: 0; font-size: 2.5rem;">
                🧠 {get_text("psychological_assessment", "Psychological Assessment")}
            </h1>
            <p style="color: rgba(255,255,255,0.9); margin: 1rem 0 0 0; font-size: 1.2rem;">
                {get_text("assessment_subtitle", "Discover your personality, interests, and ideal career path")}
            </p>
        </div>
        """,
            unsafe_allow_html=True,
        )

        if not COMPONENTS_AVAILABLE:
            st.error(
                "⚠️ Assessment components are not available. Please check your installation."
            )
            return False

        # Assessment information
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(
                f"""
            <div class="info-card text-center">
                <div style="font-size: 2em; margin-bottom: 0.5rem;">⏱️</div>
                <h4>{get_text("duration", "Duration")}</h4>
                <p>45-60 {get_text("minutes", "minutes")}</p>
            </div>
            """,
                unsafe_allow_html=True,
            )

        with col2:
            st.markdown(
                f"""
            <div class="info-card text-center">
                <div style="font-size: 2em; margin-bottom: 0.5rem;">📊</div>
                <h4>{get_text("sections", "Sections")}</h4>
                <p>3 {get_text("main_areas", "main areas")}</p>
            </div>
            """,
                unsafe_allow_html=True,
            )

        with col3:
            st.markdown(
                f"""
            <div class="info-card text-center">
                <div style="font-size: 2em; margin-bottom: 0.5rem;">🎯</div>
                <h4>{get_text("outcome", "Outcome")}</h4>
                <p>{get_text("personalized_report", "Personalized report")}</p>
            </div>
            """,
                unsafe_allow_html=True,
            )

        return True

    def render_assessment_benefits(self):
        """Render assessment benefits"""
        st.markdown(f"### 🌟 {get_text('what_youll_discover', "What You'll Discover")}")

        benefits = [
            {
                "icon": "🧠",
                "title": get_text("personality_insights", "Personality Insights"),
                "desc": get_text(
                    "personality_benefit",
                    "Understand your unique personality traits and how they influence your work style",
                ),
            },
            {
                "icon": "💼",
                "title": get_text("career_matches", "Career Matches"),
                "desc": get_text(
                    "career_benefit",
                    "Discover careers that align with your interests, skills, and personality",
                ),
            },
            {
                "icon": "📈",
                "title": get_text("growth_opportunities", "Growth Opportunities"),
                "desc": get_text(
                    "growth_benefit",
                    "Identify areas for skill development and career advancement",
                ),
            },
            {
                "icon": "🎯",
                "title": get_text("action_plan", "Personalized Action Plan"),
                "desc": get_text(
                    "action_benefit", "Get specific steps to achieve your career goals"
                ),
            },
        ]

        for i in range(0, len(benefits), 2):
            cols = st.columns(2)
            for j, col in enumerate(cols):
                if i + j < len(benefits):
                    benefit = benefits[i + j]
                    with col:
                        st.markdown(
                            f"""
                        <div class="feature-card">
                            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 8px;">
                                <span style="font-size: 2em;">{benefit["icon"]}</span>
                                <h4 style="margin: 0; color: var(--primary-color);">{benefit["title"]}</h4>
                            </div>
                            <p style="margin: 0; color: var(--text-secondary);">{benefit["desc"]}</p>
                        </div>
                        """,
                            unsafe_allow_html=True,
                        )

    def render_start_section(self):
        """Render the start assessment section"""
        if not COMPONENTS_AVAILABLE:
            return False

        # Check if assessment is already in progress
        assessment_started = (
            self.state.get("assessment_initialized", False) if self.state else False
        )

        if not assessment_started:
            st.markdown(f"### 🚀 {get_text('ready_to_begin', 'Ready to Begin?')}")

            # Terms and conditions
            terms_accepted = st.checkbox(
                get_text(
                    "accept_assessment_terms",
                    "I understand that this assessment will take 45-60 minutes and I agree to answer honestly",
                ),
                key="assessment_terms",
            )

            privacy_accepted = st.checkbox(
                get_text(
                    "privacy_agreement",
                    "I agree to the data privacy policy and understand my responses will be used to generate personalized recommendations",
                ),
                key="privacy_terms",
            )

            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button(
                    "🎯 " + get_text("start_assessment", "Start Assessment"),
                    use_container_width=True,
                    type="primary",
                    disabled=not (terms_accepted and privacy_accepted),
                ):
                    if self.state:
                        self.state.set("assessment_initialized", True)
                        import datetime

                        self.state.set("assessment_start_time", datetime.datetime.now())
                    st.rerun()

            if not (terms_accepted and privacy_accepted):
                st.caption(
                    get_text(
                        "accept_terms_to_start",
                        "Please accept the terms to start the assessment",
                    )
                )

        return assessment_started

    def render(self):
        """Main render method for assessment page"""
        # Render introduction
        if not self.render_intro():
            return

        # Check if assessment should start
        assessment_started = self.render_start_section()

        if not assessment_started:
            # Show benefits while waiting to start
            st.markdown("---")
            self.render_assessment_benefits()

            # Sample questions preview
            st.markdown("---")
            st.markdown(f"### 👀 {get_text('sample_questions', 'Sample Questions')}")

            with st.expander(get_text("view_sample", "View Sample Questions")):
                st.markdown(f"""
                **{get_text("sample_personality", "Personality Question")}:**
                {get_text("sample_p_q", "I am outgoing and sociable in social situations")}
                
                Scale: 1 (Strongly Disagree) → 5 (Strongly Agree)
                
                **{get_text("sample_interest", "Interest Question")}:**
                {get_text("sample_i_q", "Which type of work environment do you prefer?")}
                
                Options: Office, Remote, Outdoor, Collaborative, etc.
                
                **{get_text("sample_skills", "Skills Question")}:**
                {get_text("sample_s_q", "Rate your communication skills on a scale of 1-10")}
                """)

            return

        # Render the actual assessment
        st.markdown("---")

        try:
            sections = create_personality_assessment()
            if sections:
                assessment_form = AssessmentForm(sections)
                assessment_form.render()
            else:
                st.error("❌ Failed to create assessment sections")
        except Exception as e:
            logger.error(f"Assessment rendering error: {e}")
            st.error(f"❌ Assessment error: {str(e)}")

            # Fallback simple assessment
            st.markdown(f"### 📝 {get_text('simple_assessment', 'Simple Assessment')}")
            st.info(
                get_text("fallback_message", "Using simplified assessment interface")
            )

            # Simple questions
            q1 = st.slider(get_text("simple_q1", "How outgoing are you?"), 1, 5, 3)
            q2 = st.selectbox(
                get_text("simple_q2", "Preferred work environment"),
                [
                    get_text("office", "Office"),
                    get_text("remote", "Remote"),
                    get_text("hybrid", "Hybrid"),
                ],
            )
            q3 = st.multiselect(
                get_text("simple_q3", "Your interests"),
                [
                    get_text("tech", "Technology"),
                    get_text("business", "Business"),
                    get_text("creative", "Creative"),
                ],
            )

            if st.button(
                get_text("submit_simple", "Submit Simple Assessment"), type="primary"
            ):
                st.success(
                    get_text(
                        "simple_completed",
                        "Assessment completed! Basic recommendations available.",
                    )
                )


# Create the page instance
def show_assessment_page():
    """Function to show the assessment page"""
    assessment_page = AssessmentPage()
    assessment_page.render()
