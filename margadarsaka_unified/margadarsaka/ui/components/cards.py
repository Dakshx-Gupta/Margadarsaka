"""
Reusable Card Components for Margadarsaka
Beautiful, responsive cards for various content types
"""

import streamlit as st
from typing import Optional, Dict, Any, List, Union
from dataclasses import dataclass
from enum import Enum
import logging

logger = logging.getLogger(__name__)

# Import local modules with fallbacks
try:
    from margadarsaka.ui.utils.i18n import get_text

    IMPORTS_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Import error in cards: {e}")
    IMPORTS_AVAILABLE = False

    def get_text(key: str, default: Optional[str] = None, **kwargs) -> str:
        return default or key


class CardType(Enum):
    """Types of cards available"""

    FEATURE = "feature"
    METRIC = "metric"
    PROGRESS = "progress"
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"
    INFO = "info"
    PROFILE = "profile"
    ASSESSMENT = "assessment"
    CAREER = "career"


@dataclass
class CardAction:
    """Action button configuration for cards"""

    label: str
    key: str
    icon: Optional[str] = None
    type: str = "secondary"  # primary, secondary
    disabled: bool = False


class BaseCard:
    """Base card component with common functionality"""

    def __init__(
        self,
        title: Optional[str] = None,
        content: Optional[str] = None,
        icon: Optional[str] = None,
        card_type: CardType = CardType.FEATURE,
        actions: Optional[List[CardAction]] = None,
        expandable: bool = False,
        key: Optional[str] = None,
    ):
        self.title = title
        self.content = content
        self.icon = icon
        self.card_type = card_type
        self.actions = actions or []
        self.expandable = expandable
        self.key = key or f"card_{id(self)}"

    def _get_card_class(self) -> str:
        """Get CSS class for card type"""
        card_classes = {
            CardType.FEATURE: "feature-card",
            CardType.METRIC: "metric-card",
            CardType.PROGRESS: "feature-card",
            CardType.SUCCESS: "success-card feature-card",
            CardType.WARNING: "warning-card feature-card",
            CardType.ERROR: "error-card feature-card",
            CardType.INFO: "info-card feature-card",
            CardType.PROFILE: "feature-card",
            CardType.ASSESSMENT: "feature-card",
            CardType.CAREER: "feature-card",
        }
        return card_classes.get(self.card_type, "feature-card")

    def _render_card_header(self):
        """Render card header with title and icon"""
        if self.title or self.icon:
            header_content = ""
            if self.icon:
                header_content += f'<span style="font-size: 1.5em; margin-right: 10px; opacity: 0.9;">{self.icon}</span>'
            if self.title:
                header_content += f'<span style="font-weight: 600; font-size: 1.1em; color: var(--header-color, #333);">{self.title}</span>'

            return f'<div style="margin-bottom: 12px; display: flex; align-items: center;">{header_content}</div>'
        return ""

    def _render_card_actions(self) -> Dict[str, bool]:
        """Render action buttons and return click states"""
        if not self.actions:
            return {}

        action_results = {}

        if len(self.actions) == 1:
            action = self.actions[0]
            button_label = (
                f"{action.icon} {action.label}" if action.icon else action.label
            )
            action_results[action.key] = st.button(
                button_label,
                key=f"{self.key}_{action.key}",
                type=action.type,
                disabled=action.disabled,
                use_container_width=True,
            )
        else:
            cols = st.columns(len(self.actions))
            for i, action in enumerate(self.actions):
                with cols[i]:
                    button_label = (
                        f"{action.icon} {action.label}" if action.icon else action.label
                    )
                    action_results[action.key] = st.button(
                        button_label,
                        key=f"{self.key}_{action.key}",
                        type=action.type,
                        disabled=action.disabled,
                        use_container_width=True,
                    )

        return action_results

    def render(self) -> Dict[str, bool]:
        """Render the card and return action results"""
        card_class = self._get_card_class()

        if self.expandable and self.title:
            with st.expander(f"{self.icon} {self.title}" if self.icon else self.title):
                if self.content:
                    st.markdown(self.content)
                return self._render_card_actions()
        else:
            header = self._render_card_header()

            card_html = f"""
            <div class="{card_class}" style="transition: transform 0.2s ease, box-shadow 0.2s ease; position: relative; overflow: hidden;">
                <div style="position: absolute; top: 0; left: 0; width: 4px; height: 100%; background: var(--gradient-primary); opacity: 0.7;"></div>
                <div style="padding-left: 8px;">
                    {header}
                    <div style="color: var(--text-color); line-height: 1.5;">
                        {self.content or ""}
                    </div>
                </div>
            </div>
            """

            st.markdown(card_html, unsafe_allow_html=True)
            return self._render_card_actions()


class FeatureCard(BaseCard):
    """Feature highlight card"""

    def __init__(
        self,
        title: str,
        description: str,
        icon: str = "⭐",
        benefits: Optional[List[str]] = None,
        action_label: Optional[str] = None,
        action_key: Optional[str] = None,
    ):
        content = f"<p>{description}</p>"

        if benefits:
            content += "<ul>"
            for benefit in benefits:
                content += f"<li>{benefit}</li>"
            content += "</ul>"

        actions = []
        if action_label and action_key:
            actions.append(
                CardAction(label=action_label, key=action_key, type="primary")
            )

        super().__init__(
            title=title,
            content=content,
            icon=icon,
            card_type=CardType.FEATURE,
            actions=actions,
        )


class MetricCard(BaseCard):
    """Metric display card with value and optional delta"""

    def __init__(
        self,
        title: str,
        value: Union[str, int, float],
        delta: Optional[Union[str, int, float]] = None,
        delta_color: str = "normal",  # normal, inverse, off
        help_text: Optional[str] = None,
        icon: Optional[str] = None,
    ):
        # Format the metric display
        content = f"""
        <div style="text-align: center;">
            <div style="font-size: 2.5em; font-weight: bold; color: var(--primary-color);">
                {value}
            </div>
        """

        if delta:
            delta_color_map = {
                "normal": "var(--success-color)",
                "inverse": "var(--error-color)",
                "off": "var(--text-secondary)",
            }
            color = delta_color_map.get(delta_color, "var(--text-secondary)")

            content += f"""
            <div style="font-size: 1em; color: {color}; margin-top: 4px;">
                {delta}
            </div>
            """

        if help_text:
            content += f"""
            <div style="font-size: 0.8em; color: var(--text-secondary); margin-top: 8px;">
                {help_text}
            </div>
            """

        content += "</div>"

        super().__init__(
            title=title, content=content, icon=icon, card_type=CardType.METRIC
        )


class ProgressCard(BaseCard):
    """Progress tracking card"""

    def __init__(
        self,
        title: str,
        progress: float,  # 0.0 to 1.0
        total_steps: Optional[int] = None,
        current_step: Optional[int] = None,
        description: Optional[str] = None,
        show_percentage: bool = True,
        color: str = "primary",
    ):
        # Progress bar HTML
        percentage = int(progress * 100)

        color_map = {
            "primary": "var(--primary-color)",
            "success": "var(--success-color)",
            "warning": "var(--warning-color)",
            "error": "var(--error-color)",
        }
        bar_color = color_map.get(color, "var(--primary-color)")

        content = f"""
        <div class="progress-container">
            <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                <span style="font-weight: 500;">{description or ""}</span>
                {f'<span style="font-weight: bold;">{percentage}%</span>' if show_percentage else ""}
            </div>
            <div style="background: var(--light-color); border-radius: 20px; height: 12px; overflow: hidden;">
                <div style="background: {bar_color}; height: 100%; width: {percentage}%; 
                           border-radius: 20px; transition: width 0.3s ease;"></div>
            </div>
        """

        if total_steps and current_step:
            content += f"""
            <div style="text-align: center; margin-top: 8px; font-size: 0.9em; color: var(--text-secondary);">
                {get_text("step", "Step")} {current_step} {get_text("of", "of")} {total_steps}
            </div>
            """

        content += "</div>"

        super().__init__(
            title=title, content=content, icon="📊", card_type=CardType.PROGRESS
        )


class ProfileCard(BaseCard):
    """User profile display card"""

    def __init__(
        self,
        user_name: str,
        user_email: Optional[str] = None,
        avatar_emoji: str = "👤",
        join_date: Optional[str] = None,
        stats: Optional[Dict[str, Union[str, int]]] = None,
        badges: Optional[List[str]] = None,
    ):
        content = f"""
        <div style="display: flex; align-items: center; gap: 16px; margin-bottom: 16px;">
            <div style="font-size: 3em;">{avatar_emoji}</div>
            <div>
                <h3 style="margin: 0; color: var(--primary-color);">{user_name}</h3>
                {f'<p style="margin: 4px 0; color: var(--text-secondary);">{user_email}</p>' if user_email else ""}
                {f'<small style="color: var(--text-muted);">{get_text("joined", "Joined")} {join_date}</small>' if join_date else ""}
            </div>
        </div>
        """

        if stats:
            content += '<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(100px, 1fr)); gap: 12px; margin: 16px 0;">'
            for label, value in stats.items():
                content += f"""
                <div style="text-align: center; padding: 8px; background: var(--surface-color); border-radius: 8px;">
                    <div style="font-weight: bold; color: var(--primary-color);">{value}</div>
                    <small style="color: var(--text-secondary);">{label}</small>
                </div>
                """
            content += "</div>"

        if badges:
            content += '<div style="margin-top: 16px;">'
            content += f'<small style="color: var(--text-secondary); margin-bottom: 8px; display: block;">{get_text("achievements", "Achievements")}:</small>'
            content += '<div style="display: flex; flex-wrap: wrap; gap: 4px;">'
            for badge in badges:
                content += f'<span style="background: var(--gradient-primary); color: white; padding: 4px 8px; border-radius: 12px; font-size: 0.8em;">{badge}</span>'
            content += "</div></div>"

        super().__init__(title=None, content=content, card_type=CardType.PROFILE)


class AssessmentCard(BaseCard):
    """Assessment or quiz question card"""

    def __init__(
        self,
        question: str,
        question_number: Optional[int] = None,
        total_questions: Optional[int] = None,
        options: Optional[List[str]] = None,
        question_type: str = "multiple_choice",  # multiple_choice, scale, text
        required: bool = True,
    ):
        title = ""
        if question_number and total_questions:
            title = f"{get_text('question', 'Question')} {question_number}/{total_questions}"

        content = f'<p style="font-size: 1.1em; margin-bottom: 16px;">{question}</p>'

        if required:
            content += f'<small style="color: var(--error-color);">* {get_text("required", "Required")}</small>'

        super().__init__(
            title=title, content=content, icon="❓", card_type=CardType.ASSESSMENT
        )


class CareerCard(BaseCard):
    """Career option display card"""

    def __init__(
        self,
        career_title: str,
        description: str,
        match_percentage: Optional[int] = None,
        salary_range: Optional[str] = None,
        growth_rate: Optional[str] = None,
        skills_required: Optional[List[str]] = None,
        education_required: Optional[str] = None,
    ):
        content = f"<p>{description}</p>"

        # Match percentage
        if match_percentage:
            color = (
                "var(--success-color)"
                if match_percentage >= 80
                else "var(--warning-color)"
                if match_percentage >= 60
                else "var(--error-color)"
            )
            content += f"""
            <div style="margin: 12px 0;">
                <span style="background: {color}; color: white; padding: 4px 12px; border-radius: 16px; font-weight: bold;">
                    {match_percentage}% {get_text("match", "Match")}
                </span>
            </div>
            """

        # Career details
        details = []
        if salary_range:
            details.append(f"💰 {get_text('salary', 'Salary')}: {salary_range}")
        if growth_rate:
            details.append(f"📈 {get_text('growth', 'Growth')}: {growth_rate}")
        if education_required:
            details.append(
                f"🎓 {get_text('education', 'Education')}: {education_required}"
            )

        if details:
            content += '<div style="margin: 12px 0;">'
            for detail in details:
                content += (
                    f'<div style="margin: 4px 0; font-size: 0.9em;">{detail}</div>'
                )
            content += "</div>"

        # Skills required
        if skills_required:
            content += f'<div style="margin-top: 12px;"><strong>{get_text("skills_required", "Skills Required")}:</strong></div>'
            content += '<div style="margin-top: 8px; display: flex; flex-wrap: wrap; gap: 4px;">'
            for skill in skills_required[:6]:  # Limit to 6 skills
                content += f'<span style="background: var(--surface-color); color: var(--text-primary); padding: 2px 8px; border-radius: 12px; font-size: 0.8em; border: 1px solid var(--border-color);">{skill}</span>'
            if len(skills_required) > 6:
                content += f'<span style="color: var(--text-secondary); font-size: 0.8em;">+{len(skills_required) - 6} {get_text("more", "more")}</span>'
            content += "</div>"

        actions = [
            CardAction(
                label=get_text("learn_more", "Learn More"),
                key="learn_more",
                icon="📖",
                type="primary",
            ),
            CardAction(
                label=get_text("save", "Save"), key="save", icon="💾", type="secondary"
            ),
        ]

        super().__init__(
            title=career_title,
            content=content,
            icon="💼",
            card_type=CardType.CAREER,
            actions=actions,
        )


# Convenience functions for creating cards


def create_feature_card(title: str, description: str, **kwargs) -> FeatureCard:
    """Create a feature card"""
    return FeatureCard(title, description, **kwargs)


def create_metric_card(
    title: str, value: Union[str, int, float], **kwargs
) -> MetricCard:
    """Create a metric card"""
    return MetricCard(title, value, **kwargs)


def create_progress_card(title: str, progress: float, **kwargs) -> ProgressCard:
    """Create a progress card"""
    return ProgressCard(title, progress, **kwargs)


def create_profile_card(user_name: str, **kwargs) -> ProfileCard:
    """Create a profile card"""
    return ProfileCard(user_name, **kwargs)


def create_assessment_card(question: str, **kwargs) -> AssessmentCard:
    """Create an assessment card"""
    return AssessmentCard(question, **kwargs)


def create_career_card(career_title: str, description: str, **kwargs) -> CareerCard:
    """Create a career card"""
    return CareerCard(career_title, description, **kwargs)


# Grid layout helper
def render_card_grid(
    cards: List[BaseCard], columns: int = 3
) -> Dict[str, Dict[str, bool]]:
    """Render cards in a grid layout"""
    results = {}

    # Split cards into rows
    rows = [cards[i : i + columns] for i in range(0, len(cards), columns)]

    for row in rows:
        cols = st.columns(len(row))
        for i, card in enumerate(row):
            with cols[i]:
                card_key = card.key or f"card_{id(card)}"
                results[card_key] = card.render()

    return results
