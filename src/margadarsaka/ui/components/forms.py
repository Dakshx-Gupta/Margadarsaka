"""
Interactive Forms for Psychological Assessment and User Profiles
Advanced form components with validation and dynamic behavior
"""

import streamlit as st
from typing import Dict, List, Optional, Any, Callable, Union
from dataclasses import dataclass, field
from enum import Enum
import logging
import json

logger = logging.getLogger(__name__)

# Import local modules with fallbacks
try:
    from margadarsaka.ui.utils.i18n import get_text
    from margadarsaka.ui.utils.state_manager import get_state_manager
    from margadarsaka.ui.components.cards import create_progress_card

    IMPORTS_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Import error in forms: {e}")
    IMPORTS_AVAILABLE = False

    def get_text(key: str, default: Optional[str] = None, **kwargs) -> str:
        return default or key

    class MockStateManager:
        def get(self, key: str, default: Any = None):
            return default

        def set(self, key: str, value: Any):
            pass

    def get_state_manager():
        return MockStateManager()

    def create_progress_card(title: str, progress: float, **kwargs):
        class MockCard:
            def render(self):
                return {}

        return MockCard()


class QuestionType(Enum):
    """Types of assessment questions"""

    MULTIPLE_CHOICE = "multiple_choice"
    SCALE = "scale"
    RANKING = "ranking"
    TEXT = "text"
    BOOLEAN = "boolean"
    SLIDER = "slider"
    MULTISELECT = "multiselect"


@dataclass
class AssessmentQuestion:
    """Configuration for an assessment question"""

    id: str
    text: str
    question_type: QuestionType
    options: Optional[List[str]] = None
    scale_min: int = 1
    scale_max: int = 5
    scale_labels: Optional[Dict[int, str]] = None
    required: bool = True
    help_text: Optional[str] = None
    category: Optional[str] = None
    weight: float = 1.0
    randomize_options: bool = False


@dataclass
class AssessmentSection:
    """Section of an assessment with multiple questions"""

    id: str
    title: str
    description: str
    questions: List[AssessmentQuestion] = field(default_factory=list)
    icon: str = "📋"
    time_estimate: Optional[int] = None  # minutes


class FormValidator:
    """Advanced form validation for assessments"""

    @staticmethod
    def validate_response(
        question: AssessmentQuestion, response: Any
    ) -> Dict[str, str]:
        """Validate a single question response"""
        errors = {}

        if question.required and (response is None or response == "" or response == []):
            errors[question.id] = get_text(
                "response_required", "This question is required"
            )
            return errors

        if question.question_type == QuestionType.SCALE:
            if isinstance(response, (int, float)):
                if not (question.scale_min <= response <= question.scale_max):
                    errors[question.id] = get_text(
                        "scale_out_of_range",
                        f"Please select a value between {question.scale_min} and {question.scale_max}",
                    )

        elif question.question_type == QuestionType.TEXT:
            if isinstance(response, str) and len(response.strip()) < 3:
                errors[question.id] = get_text(
                    "text_too_short", "Please provide at least 3 characters"
                )

        elif question.question_type == QuestionType.RANKING:
            if isinstance(response, list) and question.options:
                if len(response) != len(question.options):
                    errors[question.id] = get_text(
                        "ranking_incomplete", "Please rank all options"
                    )

        return errors

    @staticmethod
    def validate_section(
        section: AssessmentSection, responses: Dict[str, Any]
    ) -> Dict[str, str]:
        """Validate all responses in a section"""
        all_errors = {}

        for question in section.questions:
            response = responses.get(question.id)
            errors = FormValidator.validate_response(question, response)
            all_errors.update(errors)

        return all_errors


class AssessmentForm:
    """Interactive psychological assessment form"""

    def __init__(self, sections: List[AssessmentSection]):
        self.sections = sections
        self.state = get_state_manager()
        self.validator = FormValidator()

        # Initialize assessment state
        self._init_assessment_state()

    def _init_assessment_state(self):
        """Initialize assessment state in session"""
        if not self.state.get("assessment_initialized", False):
            self.state.set("assessment_responses", {})
            self.state.set("current_section_index", 0)
            self.state.set("assessment_start_time", None)
            self.state.set("section_completion", {})
            self.state.set("assessment_initialized", True)

    def _get_current_section(self) -> AssessmentSection:
        """Get the currently active section"""
        index = self.state.get("current_section_index", 0)
        return (
            self.sections[index]
            if 0 <= index < len(self.sections)
            else self.sections[0]
        )

    def _calculate_progress(self) -> float:
        """Calculate overall assessment progress"""
        total_questions = sum(len(section.questions) for section in self.sections)
        if total_questions == 0:
            return 0.0

        responses = self.state.get("assessment_responses", {})
        answered_questions = len(
            [q for q in responses.values() if q is not None and q != ""]
        )

        return answered_questions / total_questions

    def _calculate_section_progress(self, section: AssessmentSection) -> float:
        """Calculate progress for a specific section"""
        if not section.questions:
            return 0.0

        responses = self.state.get("assessment_responses", {})
        answered = len(
            [
                q
                for q in section.questions
                if responses.get(q.id) is not None and responses.get(q.id) != ""
            ]
        )

        return answered / len(section.questions)

    def render_progress_overview(self):
        """Render overall progress and section overview"""
        # Enhanced progress header
        st.markdown(
            f"""
            <div style="background: var(--gradient-primary); padding: 20px; border-radius: var(--border-radius-lg); 
                     color: white; margin-bottom: 20px; box-shadow: var(--shadow-md);">
                <div style="display: flex; align-items: center; margin-bottom: 15px;">
                    <div style="font-size: 2rem; margin-right: 15px;">📊</div>
                    <h2 style="margin: 0; font-weight: 600;">{get_text("assessment_progress", "Assessment Progress")}</h2>
                </div>
                
                <div style="background: rgba(255,255,255,0.2); height: 12px; border-radius: 20px; overflow: hidden;">
                    <div style="background: white; height: 100%; width: {int(self._calculate_progress() * 100)}%; 
                             border-radius: 20px; transition: width 0.5s ease;"></div>
                </div>
                
                <div style="display: flex; justify-content: space-between; margin-top: 10px;">
                    <span>{get_text("questions_completed", "Questions Completed")}</span>
                    <span style="font-weight: bold;">{int(self._calculate_progress() * 100)}%</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Section overview with modern styling
        st.markdown(
            f"""
            <h4 style="margin-bottom: 15px; color: var(--primary-color);">
                {get_text("sections_overview", "Sections Overview")}
            </h4>
            """,
            unsafe_allow_html=True,
        )

        for i, section in enumerate(self.sections):
            section_progress = self._calculate_section_progress(section)
            current_section_index = self.state.get("current_section_index", 0)

            # Section status with better visual indicators
            if i < current_section_index:
                status = "✅"
                status_text = get_text("completed", "Completed")
                status_color = "var(--success-color)"
                bg_color = "rgba(46, 125, 50, 0.1)"  # Light green background
            elif i == current_section_index:
                status = "🔄"
                status_text = get_text("in_progress", "In Progress")
                status_color = "var(--primary-color)"
                bg_color = "rgba(30, 136, 229, 0.1)"  # Light blue background
            else:
                status = "⏳"
                status_text = get_text("pending", "Pending")
                status_color = "var(--text-secondary)"
                bg_color = "rgba(120, 144, 156, 0.1)"  # Light gray background

            # Enhanced section progress card
            st.markdown(
                f"""
                <div style="background: {bg_color}; border-radius: var(--border-radius-md); 
                         padding: 15px; margin-bottom: 10px; border-left: 4px solid {status_color};">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                        <div style="display: flex; align-items: center;">
                            <span style="font-size: 1.2rem; margin-right: 10px;">{status}</span>
                            <strong>{section.title}</strong>
                        </div>
                        <div style="color: {status_color}; font-weight: 600;">{status_text}</div>
                    </div>
                    
                    <div style="margin-bottom: 10px; font-size: 0.9rem; color: var(--text-secondary);">
                        {section.description}
                    </div>
                    
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div style="flex-grow: 1; margin-right: 15px;">
                            <div style="background: rgba(255,255,255,0.6); height: 8px; border-radius: 10px; overflow: hidden;">
                                <div style="background: {status_color}; height: 100%; width: {int(section_progress * 100)}%; 
                                        border-radius: 10px; transition: width 0.3s ease;"></div>
                            </div>
                        </div>
                        <div style="font-weight: 600; min-width: 40px; text-align: right;">
                            {int(section_progress * 100)}%
                        </div>
                        {f'<div style="margin-left: 15px; font-size: 0.9rem;">⏱️ {section.time_estimate} min</div>' if section.time_estimate else ""}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    def render_question(self, question: AssessmentQuestion) -> Any:
        """Render a single question based on its type"""
        responses = self.state.get("assessment_responses", {})
        current_value = responses.get(question.id)

        # Create modern question container
        st.markdown(
            f"""
        <div class="form-question-container">
            <div class="question-text">
                {question.text}
                {f'<span class="required-indicator">*</span>' if question.required else ""}
            </div>
            {f'<div class="question-help">{question.help_text}</div>' if question.help_text else ""}
        </div>
        """,
            unsafe_allow_html=True,
        )

        # Use columns for better layout
        # (Apply styling through CSS instead of columns to avoid indentation issues)

        response = None

        if question.question_type == QuestionType.MULTIPLE_CHOICE:
            if question.options:
                response = st.radio(
                    label="",
                    options=question.options,
                    index=question.options.index(current_value)
                    if current_value in question.options
                    else None,
                    key=f"q_{question.id}",
                    label_visibility="collapsed",
                )

        elif question.question_type == QuestionType.SCALE:
            # Create scale with labels
            if question.scale_labels:
                # Custom labeled scale
                col1, col2, col3 = st.columns([1, 3, 1])
                with col1:
                    st.caption(
                        question.scale_labels.get(
                            question.scale_min, str(question.scale_min)
                        )
                    )
                with col2:
                    response = st.slider(
                        label="",
                        min_value=question.scale_min,
                        max_value=question.scale_max,
                        value=current_value or question.scale_min,
                        key=f"q_{question.id}",
                        label_visibility="collapsed",
                    )
                with col3:
                    st.caption(
                        question.scale_labels.get(
                            question.scale_max, str(question.scale_max)
                        )
                    )
            else:
                response = st.slider(
                    label="",
                    min_value=question.scale_min,
                    max_value=question.scale_max,
                    value=current_value or question.scale_min,
                    key=f"q_{question.id}",
                    label_visibility="collapsed",
                )

        elif question.question_type == QuestionType.RANKING:
            if question.options:
                st.markdown(
                    get_text("drag_to_rank", "Drag to rank in order of preference:")
                )
                # For now, use selectbox for each rank
                response = []
                available_options = [opt for opt in question.options]

                for i in range(len(question.options)):
                    if current_value and i < len(current_value):
                        default_index = (
                            available_options.index(current_value[i])
                            if current_value[i] in available_options
                            else 0
                        )
                    else:
                        default_index = 0

                    choice = st.selectbox(
                        f"{get_text('rank', 'Rank')} {i + 1}:",
                        available_options,
                        index=default_index,
                        key=f"q_{question.id}_rank_{i}",
                    )
                    response.append(choice)

                    # Remove selected option from available options for next rank
                    if choice in available_options:
                        available_options.remove(choice)

        elif question.question_type == QuestionType.TEXT:
            response = st.text_area(
                label="",
                value=current_value or "",
                placeholder=get_text("enter_your_response", "Enter your response..."),
                key=f"q_{question.id}",
                label_visibility="collapsed",
            )

        elif question.question_type == QuestionType.BOOLEAN:
            response = st.checkbox(
                get_text("yes", "Yes"),
                value=current_value or False,
                key=f"q_{question.id}",
            )

        elif question.question_type == QuestionType.SLIDER:
            response = st.slider(
                label="",
                min_value=question.scale_min,
                max_value=question.scale_max,
                value=current_value or question.scale_min,
                key=f"q_{question.id}",
                label_visibility="collapsed",
            )

        elif question.question_type == QuestionType.MULTISELECT:
            if question.options:
                response = st.multiselect(
                    label="",
                    options=question.options,
                    default=current_value or [],
                    key=f"q_{question.id}",
                    label_visibility="collapsed",
                )

        return response

    def render_section(self, section: AssessmentSection):
        """Render a complete assessment section"""
        # Enhanced Section header with visual elements
        st.markdown(
            f"""
        <div class="feature-card" style="background: linear-gradient(135deg, var(--surface-color) 0%, #ffffff 100%);">
            <div style="display: flex; align-items: center; margin-bottom: 12px;">
                <div style="font-size: 2.2rem; margin-right: 15px; opacity: 0.9;">{
                section.icon
            }</div>
                <div>
                    <h2 style="color: var(--primary-color); margin: 0; font-weight: 600;">
                        {section.title}
                    </h2>
                    <p style="margin: 8px 0 0 0; color: var(--text-secondary); line-height: 1.5;">
                        {section.description}
                    </p>
                </div>
            </div>
            {
                f'''
            <div style="display: flex; align-items: center; padding: 8px 12px; background: rgba(30, 136, 229, 0.1); 
                        border-radius: var(--border-radius-md); margin-top: 8px;">
                <div style="font-size: 1.2rem; margin-right: 8px;">⏱️</div>
                <div style="font-size: 0.9rem; color: var(--primary-color);">
                    {get_text("estimated_time", "Estimated time")}: <strong>{section.time_estimate} {get_text("minutes", "minutes")}</strong>
                </div>
            </div>
            '''
                if section.time_estimate
                else ""
            }
        </div>
        """,
            unsafe_allow_html=True,
        )

        # Render questions
        responses = self.state.get("assessment_responses", {})

        for i, question in enumerate(section.questions, 1):
            with st.container():
                st.markdown(f"---")
                st.markdown(
                    f"##### {get_text('question', 'Question')} {i}/{len(section.questions)}"
                )

                response = self.render_question(question)

                # Update response in state
                if response is not None:
                    responses[question.id] = response
                    self.state.set("assessment_responses", responses)

        return responses

    def render_section_navigation(self):
        """Render navigation between sections"""
        current_index = self.state.get("current_section_index", 0)

        col1, col2, col3 = st.columns([1, 2, 1])

        with col1:
            if current_index > 0:
                if st.button(
                    "⬅️ " + get_text("previous_section", "Previous Section"),
                    use_container_width=True,
                ):
                    self.state.set("current_section_index", current_index - 1)
                    st.rerun()

        with col2:
            # Section selector
            section_names = [
                f"{section.icon} {section.title}" for section in self.sections
            ]
            selected_index = st.selectbox(
                get_text("jump_to_section", "Jump to section:"),
                range(len(section_names)),
                index=current_index,
                format_func=lambda i: section_names[i],
                key="section_selector",
            )

            if selected_index != current_index:
                self.state.set("current_section_index", selected_index)
                st.rerun()

        with col3:
            if current_index < len(self.sections) - 1:
                if st.button(
                    get_text("next_section", "Next Section") + " ➡️",
                    use_container_width=True,
                ):
                    # Validate current section before proceeding
                    current_section = self._get_current_section()
                    responses = self.state.get("assessment_responses", {})
                    errors = self.validator.validate_section(current_section, responses)

                    if errors:
                        st.error(
                            get_text(
                                "complete_required_questions",
                                "Please complete all required questions before proceeding.",
                            )
                        )
                        for error in errors.values():
                            st.error(f"• {error}")
                    else:
                        self.state.set("current_section_index", current_index + 1)
                        st.rerun()
            else:
                if st.button(
                    "✅ " + get_text("complete_assessment", "Complete Assessment"),
                    use_container_width=True,
                    type="primary",
                ):
                    self._complete_assessment()

    def _complete_assessment(self):
        """Handle assessment completion"""
        # Validate all sections
        responses = self.state.get("assessment_responses", {})
        all_errors = {}

        for section in self.sections:
            errors = self.validator.validate_section(section, responses)
            all_errors.update(errors)

        if all_errors:
            st.error(
                get_text(
                    "assessment_has_errors", "Please complete all required questions:"
                )
            )
            for error in all_errors.values():
                st.error(f"• {error}")
            return

        # Mark as completed
        self.state.set("assessment_completed", True)
        self.state.set(
            "assessment_completion_time", st.session_state.get("assessment_start_time")
        )

        st.success(
            "🎉 "
            + get_text("assessment_completed", "Assessment completed successfully!")
        )
        st.balloons()

        # Show results preview
        self._show_results_preview()

    def _show_results_preview(self):
        """Show a preview of assessment results"""
        st.markdown(f"### 📊 {get_text('results_preview', 'Results Preview')}")

        responses = self.state.get("assessment_responses", {})

        # Calculate some basic statistics
        total_questions = len(responses)
        scale_responses = []

        for section in self.sections:
            for question in section.questions:
                response = responses.get(question.id)
                if (
                    question.question_type == QuestionType.SCALE
                    and response is not None
                ):
                    scale_responses.append(response)

        if scale_responses:
            avg_score = sum(scale_responses) / len(scale_responses)

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(
                    get_text("questions_answered", "Questions Answered"),
                    total_questions,
                )
            with col2:
                st.metric(
                    get_text("average_score", "Average Score"), f"{avg_score:.1f}"
                )
            with col3:
                st.metric(get_text("completion_rate", "Completion Rate"), "100%")

        st.info(
            get_text(
                "detailed_results_available",
                "Detailed results and recommendations will be available in your dashboard.",
            )
        )

        if st.button(
            get_text("view_detailed_results", "View Detailed Results"), type="primary"
        ):
            self.state.set("current_page", "recommendations")
            st.rerun()

    def render(self):
        """Main render method for the assessment form"""
        # Start time tracking
        if not self.state.get("assessment_start_time"):
            import datetime

            self.state.set("assessment_start_time", datetime.datetime.now())

        # Check if assessment is completed
        if self.state.get("assessment_completed", False):
            self._show_results_preview()
            return

        # Show progress overview
        with st.expander(
            "📊 " + get_text("view_progress", "View Progress"), expanded=False
        ):
            self.render_progress_overview()

        st.markdown("---")

        # Render current section
        current_section = self._get_current_section()
        section_responses = self.render_section(current_section)

        st.markdown("---")

        # Section navigation
        self.render_section_navigation()


class ProfileForm:
    """User profile management form"""

    def __init__(self):
        self.state = get_state_manager()

    def render_basic_info(self):
        """Render basic profile information form"""
        st.markdown(f"### 👤 {get_text('basic_information', 'Basic Information')}")

        with st.form("basic_info_form"):
            col1, col2 = st.columns(2)

            with col1:
                first_name = st.text_input(get_text("first_name", "First Name"))
                email = st.text_input(get_text("email", "Email"))
                phone = st.text_input(get_text("phone", "Phone Number"))

            with col2:
                last_name = st.text_input(get_text("last_name", "Last Name"))
                date_of_birth = st.date_input(
                    get_text("date_of_birth", "Date of Birth")
                )
                location = st.text_input(get_text("location", "Location"))

            bio = st.text_area(
                get_text("bio", "Bio"),
                placeholder=get_text("bio_placeholder", "Tell us about yourself..."),
            )

            if st.form_submit_button(
                get_text("save_changes", "Save Changes"), type="primary"
            ):
                # Save profile data
                profile_data = {
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": email,
                    "phone": phone,
                    "date_of_birth": str(date_of_birth),
                    "location": location,
                    "bio": bio,
                }

                self.state.set("user_profile", profile_data)
                st.success(get_text("profile_saved", "Profile saved successfully!"))

    def render_education_form(self):
        """Render education information form"""
        st.markdown(f"### 🎓 {get_text('education', 'Education')}")

        education_levels = [
            get_text("high_school", "High School"),
            get_text("undergraduate", "Undergraduate"),
            get_text("graduate", "Graduate"),
            get_text("postgraduate", "Postgraduate"),
            get_text("doctorate", "Doctorate"),
        ]

        with st.form("education_form"):
            current_education = st.selectbox(
                get_text("current_education_level", "Current Education Level"),
                education_levels,
            )

            institution = st.text_input(
                get_text("institution", "Institution/University")
            )
            field_of_study = st.text_input(get_text("field_of_study", "Field of Study"))

            col1, col2 = st.columns(2)
            with col1:
                start_year = st.number_input(
                    get_text("start_year", "Start Year"),
                    min_value=1950,
                    max_value=2030,
                    value=2020,
                )
            with col2:
                end_year = st.number_input(
                    get_text("end_year", "End Year"),
                    min_value=1950,
                    max_value=2030,
                    value=2024,
                )

            if st.form_submit_button(
                get_text("save_education", "Save Education Info"), type="primary"
            ):
                education_data = {
                    "current_education": current_education,
                    "institution": institution,
                    "field_of_study": field_of_study,
                    "start_year": start_year,
                    "end_year": end_year,
                }

                self.state.set("user_education", education_data)
                st.success(get_text("education_saved", "Education information saved!"))

    def render(self):
        """Main render method for profile form"""
        tabs = st.tabs(
            [
                "👤 " + get_text("basic_info", "Basic Info"),
                "🎓 " + get_text("education", "Education"),
                "💼 " + get_text("experience", "Experience"),
                "🎯 " + get_text("preferences", "Preferences"),
            ]
        )

        with tabs[0]:
            self.render_basic_info()

        with tabs[1]:
            self.render_education_form()

        with tabs[2]:
            st.info(
                get_text("experience_coming_soon", "Work experience form coming soon!")
            )

        with tabs[3]:
            st.info(
                get_text("preferences_coming_soon", "Preferences form coming soon!")
            )
