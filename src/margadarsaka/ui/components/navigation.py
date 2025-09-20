"""
Navigation Components for Margadarsaka
Modern sidebar navigation and page routing system
"""

import streamlit as st
from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass
from enum import Enum
import logging

logger = logging.getLogger(__name__)

# Import local modules with fallbacks
try:
    from margadarsaka.ui.utils.i18n import get_text
    from margadarsaka.ui.utils.state_manager import get_state_manager

    IMPORTS_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Import error in navigation: {e}")
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


class PageType(Enum):
    """Types of pages in the application"""

    HOME = "home"
    ASSESSMENT = "assessment"
    RESUME = "resume"
    CHAT = "chat"
    RECOMMENDATIONS = "recommendations"
    RESOURCES = "resources"
    PROFILE = "profile"
    SETTINGS = "settings"


@dataclass
class NavigationItem:
    """Configuration for a navigation item"""

    key: str
    title: str
    icon: str
    page_type: PageType
    description: Optional[str] = None
    requires_auth: bool = False
    badge: Optional[str] = None
    disabled: bool = False
    children: Optional[List["NavigationItem"]] = None


class NavigationConfig:
    """Configuration for the navigation system"""

    @staticmethod
    def get_default_navigation() -> List[NavigationItem]:
        """Get the default navigation structure"""
        return [
            NavigationItem(
                key="home",
                title=get_text("home"),
                icon="🏠",
                page_type=PageType.HOME,
                description=get_text("home_desc"),
            ),
            NavigationItem(
                key="assessment",
                title=get_text("psychological_assessment"),
                icon="🧠",
                page_type=PageType.ASSESSMENT,
                description=get_text("assessment_description"),
                requires_auth=True,
            ),
            NavigationItem(
                key="resume",
                title=get_text("resume_analysis"),
                icon="📄",
                page_type=PageType.RESUME,
                description=get_text("resume_desc"),
            ),
            NavigationItem(
                key="chat",
                title=get_text("ai_career_chat"),
                icon="🤖",
                page_type=PageType.CHAT,
                description=get_text("chat_desc"),
            ),
            NavigationItem(
                key="recommendations",
                title=get_text("career_recommendations"),
                icon="📋",
                page_type=PageType.RECOMMENDATIONS,
                description=get_text("recommendations_desc"),
                requires_auth=True,
            ),
            NavigationItem(
                key="resources",
                title=get_text("learning_resources"),
                icon="📚",
                page_type=PageType.RESOURCES,
                description=get_text("resources_desc"),
            ),
            NavigationItem(
                key="profile",
                title=get_text("profile"),
                icon="👤",
                page_type=PageType.PROFILE,
                description=get_text("profile_desc"),
                requires_auth=True,
            ),
        ]


class Sidebar:
    """Enhanced sidebar navigation component"""

    def __init__(self):
        self.state = get_state_manager()
        self.navigation_items = NavigationConfig.get_default_navigation()

    def _is_user_authenticated(self) -> bool:
        """Check if user is authenticated using Streamlit's native auth"""
        try:
            # Try Streamlit's native authentication first
            if hasattr(st, "user") and hasattr(st.user, "is_logged_in"):
                return st.user.is_logged_in

            # Fallback to session state for custom auth
            return self.state.get("user_authenticated", False)
        except Exception:
            return self.state.get("user_authenticated", False)

    def _get_current_user(self) -> Optional[Dict[str, Any]]:
        """Get current user information"""
        return self.state.get("current_user")

    def render_user_section(self):
        """Render the user authentication section with support for both OIDC and custom auth"""
        # Import OIDC auth at runtime to avoid circular imports
        from .oidc_auth import OIDCAuthManager

        st.markdown(
            f"""
            <h3 style="font-size: 1.1rem; margin-bottom: 10px; color: var(--primary-color); 
                      display: flex; align-items: center; gap: 8px;">
                <span style="font-size: 1.2rem;">🔐</span> 
                {get_text("user_account", "User Account")}
            </h3>
            """,
            unsafe_allow_html=True,
        )

        # Initialize OIDC auth manager
        oidc_auth = OIDCAuthManager()

        # Check if OIDC is available and user is logged in with OIDC
        if oidc_auth.is_user_logged_in():
            # Show OIDC user profile
            oidc_auth.render_user_profile()

            # Quick actions with enhanced styling
            col1, col2 = st.columns(2)
            with col1:
                if st.button(
                    "⚙️ " + get_text("settings", "Settings"),
                    use_container_width=True,
                    key="oidc_user_settings_button",
                ):
                    self.state.set("current_page", PageType.SETTINGS.value)
                    st.rerun()

            with col2:
                oidc_auth.render_logout_button("🚪 " + get_text("logout", "Logout"))

        elif self._is_user_authenticated():
            # Fall back to custom authentication system
            user = self._get_current_user()
            if user:
                # User profile card with enhanced design
                st.markdown(
                    f"""
                <div class="feature-card fade-in" style="padding: var(--spacing-md); margin-bottom: var(--spacing-md); box-shadow: var(--shadow-sm);">
                    <div style="display: flex; align-items: center; gap: 12px;">
                        <div style="width: 45px; height: 45px; border-radius: 50%; background: var(--gradient-primary); 
                                   color: white; display: flex; align-items: center; justify-content: center; 
                                   font-size: 1.4rem; box-shadow: var(--shadow-sm);">
                            👤
                        </div>
                        <div style="flex-grow: 1;">
                            <div style="font-weight: 600; font-size: 1rem; color: var(--text-primary);">
                                {user.get("name", user.get("email", "User"))}
                            </div>
                            <div style="font-size: 0.85rem; color: var(--text-secondary); margin-top: 2px;">
                                {user.get("email", "")}
                            </div>
                        </div>
                    </div>
                    <div style="margin-top: 12px; padding-top: 8px; border-top: 1px solid var(--border-color);">
                        <div style="display: flex; align-items: center; color: var(--text-secondary); font-size: 0.85rem;">
                            <div style="flex-grow: 1;">✅ {get_text("premium_status", "Premium User")}</div>
                            <div style="font-weight: 600; color: var(--success-color);">Active</div>
                        </div>
                    </div>
                </div>
                """,
                    unsafe_allow_html=True,
                )

                # Quick actions with enhanced styling
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(
                        "⚙️ " + get_text("settings", "Settings"),
                        use_container_width=True,
                        key="custom_user_settings_button",
                    ):
                        self.state.set("current_page", PageType.SETTINGS.value)
                        st.rerun()

                with col2:
                    if st.button(
                        "🚪 " + get_text("logout", "Logout"),
                        use_container_width=True,
                        key="custom_user_logout_button",
                    ):
                        self._handle_logout()
            else:
                # Simple authenticated state with enhanced design
                st.markdown(
                    f"""
                    <div class="success-card fade-in" style="padding: var(--spacing-sm) var(--spacing-md); margin-bottom: var(--spacing-md);">
                        <div style="display: flex; align-items: center; gap: 8px;">
                            <span style="font-size: 1.1rem;">✅</span>
                            <span style="font-weight: 500;">{get_text("authenticated", "Authenticated")}</span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                if st.button(
                    "🚪 " + get_text("logout", "Logout"),
                    use_container_width=True,
                    key="custom_simple_logout_button",
                ):
                    self._handle_logout()
        else:
            # Not logged in state - show both OIDC and custom auth options
            st.markdown(
                f"""
                <div style="background: linear-gradient(135deg, #E1F5FE 0%, #B3E5FC 100%); 
                          border: 1px solid var(--info-color); 
                          color: #01579B; 
                          border-radius: var(--border-radius-md); 
                          padding: var(--spacing-sm) var(--spacing-md); 
                          margin-bottom: var(--spacing-md); 
                          box-shadow: var(--shadow-sm);">
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <span style="font-size: 1.1rem;">👤</span>
                        <span style="color: #01579B; font-weight: 500;">{get_text("login_prompt", "Login to save your progress")}</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Show OIDC login option
            col1, col2 = st.columns(2)
            with col1:
                oidc_auth.render_login_button(
                    "🔐 " + get_text("sso_login", "SSO Login")
                )

            with col2:
                # Custom auth login button
                if st.button(
                    "🔑 " + get_text("login_register", "Login/Register"),
                    use_container_width=True,
                    type="primary",
                    key="custom_login_register_button",
                ):
                    self.state.set("show_auth", True)
                    st.rerun()

    def _handle_logout(self):
        """Handle user logout"""
        self.state.set("user_authenticated", False)
        self.state.set("current_user", None)
        self.state.set("show_auth", False)
        self.state.set("current_page", PageType.HOME.value)
        st.success("👋 " + get_text("logged_out", "Successfully logged out"))
        st.rerun()

    def render_navigation_item(self, item: NavigationItem, current_page: str) -> bool:
        """Render a single navigation item"""
        # Check authentication requirement
        if item.requires_auth and not self._is_user_authenticated():
            # Show locked item with enhanced styling
            st.markdown(
                f"""
            <div style="padding: 12px 15px; margin: 8px 0; border-radius: var(--border-radius-md); 
                        background-color: var(--surface-color); 
                        border: 1px solid var(--border-color);
                        color: var(--text-secondary); opacity: 0.75;
                        transition: all var(--transition-fast);
                        box-shadow: var(--shadow-xs);">
                <div style="display: flex; align-items: center; gap: 12px;">
                    <div style="font-size: 1.3rem; width: 28px; text-align: center; opacity: 0.7;">{item.icon}</div>
                    <div style="flex-grow: 1; font-size: 0.95rem; font-weight: 500;">{item.title}</div>
                    <div style="background: rgba(210, 210, 210, 0.3); border-radius: 50%; height: 24px; width: 24px; 
                             display: flex; align-items: center; justify-content: center;">
                        <span style="color: var(--muted-color); font-size: 0.8rem;">🔒</span>
                    </div>
                </div>
                <div style="font-size: 0.8rem; margin-left: 40px; margin-top: 6px; color: var(--muted-color); 
                          padding-top: 4px; border-top: 1px dashed rgba(0,0,0,0.1);">
                    {get_text("login_required", "Login required")}
                </div>
            </div>
            """,
                unsafe_allow_html=True,
            )
            return False

        # Check if disabled - enhanced disabled item styling
        if item.disabled:
            st.markdown(
                f"""
            <div style="padding: 12px 15px; margin: 8px 0; border-radius: var(--border-radius-md); 
                       background-color: var(--surface-color); 
                       border: 1px solid var(--border-color);
                       color: var(--text-secondary); opacity: 0.65;
                       transition: all var(--transition-fast);
                       box-shadow: var(--shadow-xs);">
                <div style="display: flex; align-items: center; gap: 12px;">
                    <div style="font-size: 1.3rem; width: 28px; text-align: center; opacity: 0.7;">{
                    item.icon
                }</div>
                    <div style="flex-grow: 1; font-size: 0.95rem; font-weight: 500;">{
                    item.title
                }</div>
                    <div style="background: rgba(255, 143, 0, 0.15); border-radius: 12px; padding: 3px 8px;">
                        <span style="color: var(--accent-color); font-size: 0.7rem; font-weight: 600; text-transform: uppercase;">
                            {get_text("coming_soon", "Coming Soon")}
                        </span>
                    </div>
                </div>
                {
                    f'''
                <div style="font-size: 0.8rem; margin-left: 40px; margin-top: 6px; color: var(--muted-color);">
                    {item.description}
                </div>
                '''
                    if item.description
                    else ""
                }
            </div>
            """,
                unsafe_allow_html=True,
            )
            return False

        # Render clickable item
        is_current = current_page == item.page_type.value
        button_class = "primary" if is_current else "secondary"
        button_label = f"{item.icon} {item.title}"

        if item.badge:
            button_label += f" {item.badge}"

        # Add description as help text
        help_text = item.description if item.description else None

        # Enhanced styling for active navigation item with animation
        if is_current:
            st.markdown(
                f"""
                <style>
                /* Enhanced active navigation item */
                [data-testid="stButton"] button[kind="primary"][data-testid="baseButton-secondary"] {{
                    background: var(--gradient-primary);
                    color: white;
                    font-weight: 600;
                    position: relative;
                    padding-left: 20px;
                    box-shadow: var(--shadow-md);
                    transition: all 0.3s ease;
                    border: none;
                }}
                
                [data-testid="stButton"] button[kind="primary"][data-testid="baseButton-secondary"]::before {{
                    content: '';
                    position: absolute;
                    left: 0;
                    top: 0;
                    height: 100%;
                    width: 4px;
                    background: var(--accent-color);
                    animation: pulse 2s infinite;
                }}
                
                /* Hover effect for active item */
                [data-testid="stButton"] button[kind="primary"][data-testid="baseButton-secondary"]:hover {{
                    transform: translateX(2px);
                    box-shadow: var(--shadow-lg);
                }}
                
                /* Shimmer effect for active item */
                [data-testid="stButton"] button[kind="primary"][data-testid="baseButton-secondary"]::after {{
                    content: '';
                    position: absolute;
                    top: 0;
                    right: 0;
                    width: 100%;
                    height: 100%;
                    background: linear-gradient(
                        to right, 
                        rgba(255, 255, 255, 0) 0%,
                        rgba(255, 255, 255, 0.2) 50%,
                        rgba(255, 255, 255, 0) 100%
                    );
                    transform: translateX(-100%);
                    animation: shimmer 3s infinite;
                    pointer-events: none;
                }}
                
                @keyframes shimmer {{
                    100% {{ transform: translateX(100%); }}
                }}
                
                @keyframes pulse {{
                    0%, 100% {{ opacity: 1; }}
                    50% {{ opacity: 0.6; }}
                }}
                </style>
                """,
                unsafe_allow_html=True,
            )

        if st.button(
            button_label,
            key=f"nav_{item.key}",
            use_container_width=True,
            type="secondary",
            help=help_text,
        ):
            return True

        return False

    def render_navigation_menu(self):
        """Render the main navigation menu"""
        st.markdown(
            f"""
            <h3 style="font-size: 1.1rem; margin: 20px 0 10px 0; color: var(--primary-color); 
                      display: flex; align-items: center; gap: 8px;">
                <span style="font-size: 1.2rem;">🧭</span> 
                {get_text("navigation", "Navigation")}
            </h3>
            """,
            unsafe_allow_html=True,
        )

        current_page = self.state.get("current_page", PageType.HOME.value)

        # Group navigation items
        main_items = self.navigation_items[:4]  # Home, Assessment, Resume, Chat
        secondary_items = self.navigation_items[
            4:
        ]  # Recommendations, Resources, Profile

        # Render main navigation items
        for item in main_items:
            if self.render_navigation_item(item, current_page):
                # Handle navigation
                self.state.set("current_page", item.page_type.value)
                st.rerun()

        # Divider with label for secondary items
        st.markdown(
            f"""
            <div style="display: flex; align-items: center; margin: 15px 0 10px 0; color: var(--text-secondary);">
                <div style="flex: 1; height: 1px; background-color: var(--border-color);"></div>
                <div style="margin: 0 10px; font-size: 0.85rem; color: var(--muted-color);">
                    {get_text("more_options", "More Options")}
                </div>
                <div style="flex: 1; height: 1px; background-color: var(--border-color);"></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Render secondary navigation items
        for item in secondary_items:
            if self.render_navigation_item(item, current_page):
                # Handle navigation
                self.state.set("current_page", item.page_type.value)
                st.rerun()

    def render_language_selector(self):
        """Render language selection with enhanced styling"""
        st.markdown(
            f"""
            <div style="margin: 25px 0 15px 0; border-top: 1px solid var(--border-color); padding-top: 20px;">
                <h3 style="font-size: 1rem; margin-bottom: 12px; color: var(--primary-color); 
                         display: flex; align-items: center; gap: 8px;">
                    <span style="font-size: 1.2rem; opacity: 0.85;">🌐</span> 
                    {get_text("language", "Language")}
                </h3>
            </div>
            """,
            unsafe_allow_html=True,
        )

        languages = [
            {"code": "en", "name": "English", "flag": "🇺🇸"},
            {"code": "hi", "name": "हिंदी", "flag": "🇮🇳"},
            {"code": "hi-en", "name": "Hinglish", "flag": "🇮🇳"},
        ]

        current_lang = self.state.get("language", "en")
        current_index = next(
            (i for i, lang in enumerate(languages) if lang["code"] == current_lang), 0
        )

        # Enhanced language selector styling
        st.markdown(
            """
            <style>
            /* Enhanced language selector */
            div[data-testid="stSelectbox"] > div > div > div {
                padding: 8px 12px;
                font-size: 0.95rem;
            }
            
            div[data-testid="stSelectbox"] > div[data-baseweb="select"] > div:first-child {
                background-color: var(--surface-color);
                border-color: var(--border-color);
                border-radius: var(--border-radius-md);
                box-shadow: var(--shadow-xs);
                transition: all var(--transition-fast);
            }
            
            div[data-testid="stSelectbox"] > div[data-baseweb="select"] > div:first-child:hover {
                border-color: var(--primary-color);
                box-shadow: var(--shadow-sm);
            }
            
            /* Style the dropdown menu */
            ul[data-baseweb="menu"] {
                border-radius: var(--border-radius-md) !important;
                overflow: hidden;
                box-shadow: var(--shadow-lg) !important;
                border: 1px solid var(--border-color) !important;
            }
            
            ul[data-baseweb="menu"] li {
                transition: background-color 0.2s ease;
            }
            
            ul[data-baseweb="menu"] li:hover {
                background-color: rgba(30, 136, 229, 0.1) !important;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

        selected_index = st.selectbox(
            get_text("choose_language", "Choose language:"),
            range(len(languages)),
            index=current_index,
            format_func=lambda i: f"{languages[i]['flag']} {languages[i]['name']}",
            key="language_selector",
        )

        selected_lang = languages[selected_index]["code"]
        if selected_lang != current_lang:
            self.state.set("language", selected_lang)
            st.rerun()

        # Add a stylish footer to the sidebar
        st.markdown(
            """
        <div style="position: absolute; bottom: 0; left: 0; right: 0; padding: 1rem; 
                   background: linear-gradient(180deg, rgba(255,255,255,0) 0%, var(--surface-color) 100%); 
                   text-align: center; margin-top: 2rem;">
            <div style="font-size: 0.75rem; color: var(--text-secondary); margin-bottom: 0.5rem;">
                © 2023 Margadarsaka
            </div>
            <div style="font-size: 0.7rem; color: var(--muted-color);">
                Your AI-powered career guidance partner
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    def render_progress_summary(self):
        """Render user progress summary"""
        if not self._is_user_authenticated():
            return

        st.markdown("### 📊 " + get_text("your_progress", "Your Progress"))

        # Mock progress data - replace with real data
        # Simplified progress data to reduce DOM complexity
        progress_data = {
            "assessment_completion": 75,
            "career_matches": 5,
            "resources_viewed": 12,
            "chat_sessions": 8,
        }

        # Simplified progress display
        st.write("**Assessment Progress**")
        st.progress(0.75)
        st.caption("75% complete")

        # Compact stats display
        st.write(
            f"🎯 {progress_data['career_matches']} matches | 📚 {progress_data['resources_viewed']} resources"
        )

        st.metric(
            get_text("chat_sessions", "Chat Sessions"), progress_data["chat_sessions"]
        )

    def render_quick_actions(self):
        """Render quick action buttons"""
        st.markdown("### ⚡ " + get_text("quick_actions", "Quick Actions"))

        if st.button(
            "🎯 " + get_text("take_assessment", "Take Assessment"),
            use_container_width=True,
        ):
            self.state.set("current_page", PageType.ASSESSMENT.value)
            st.rerun()

        if st.button("💬 " + get_text("ask_ai", "Ask AI"), use_container_width=True):
            self.state.set("current_page", PageType.CHAT.value)
            st.rerun()

        if st.button(
            "📄 " + get_text("analyze_resume", "Analyze Resume"),
            use_container_width=True,
        ):
            self.state.set("current_page", PageType.RESUME.value)
            st.rerun()

    def render_help_section(self):
        """Render help and support section"""
        st.markdown("---")
        st.markdown("### ❓ " + get_text("help_support", "Help & Support"))

        # Simplified help section to reduce DOM complexity
        with st.expander("🆘 " + get_text("need_help", "Need Help?")):
            st.write("**Contact Support:**")
            st.write("📧 support@margadarsaka.com | 💬 24/7 Chat | 📞 +91-XXXX-XXXXXX")

        with st.expander("🔄 " + get_text("app_info", "App Information")):
            st.write("**Margadarsaka v1.0** | 🟢 Online | 👥 1,234 users")

    def render(self):
        """Main render method for the sidebar"""
        with st.sidebar:
            # App logo and title with enhanced styling
            st.markdown(
                f"""
            <div style="text-align: center; padding: var(--spacing-md) 0; animation: fadeIn 0.5s ease-out;">
                <div style="display: flex; justify-content: center; align-items: center; 
                           margin-bottom: var(--spacing-sm);">
                    <div style="background: var(--gradient-primary); width: 50px; height: 50px; 
                             border-radius: 12px; display: flex; align-items: center; 
                             justify-content: center; font-size: 1.8rem;
                             box-shadow: var(--shadow-md);">
                        🚀
                    </div>
                </div>
                <h3 style="margin: 0.5rem 0 0.2rem 0; font-weight: 600; 
                          background: var(--gradient-primary); 
                          -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                          background-clip: text; font-size: 1.4rem;">
                    {get_text("app_title", "Margadarsaka")}
                </h3>
                <p style="margin: 0; color: var(--text-secondary); font-size: 0.85rem;">
                    {get_text("ai_career_advisor", "AI Career Advisor")}
                </p>
            </div>
            """,
                unsafe_allow_html=True,
            )

            # Custom divider
            st.markdown(
                """
                <div style="height: 1px; background: linear-gradient(to right, rgba(0,0,0,0), var(--border-color), rgba(0,0,0,0)); 
                            margin: 1.2rem 0;"></div>
                """,
                unsafe_allow_html=True,
            )

            # User section
            self.render_user_section()

            # Custom divider
            st.markdown(
                """
                <div style="height: 1px; background: linear-gradient(to right, rgba(0,0,0,0), var(--border-color), rgba(0,0,0,0)); 
                            margin: 1.2rem 0;"></div>
                """,
                unsafe_allow_html=True,
            )

            # Navigation menu
            self.render_navigation_menu()

            # Custom divider
            st.markdown(
                """
                <div style="height: 1px; background: linear-gradient(to right, rgba(0,0,0,0), var(--border-color), rgba(0,0,0,0)); 
                            margin: 1.2rem 0;"></div>
                """,
                unsafe_allow_html=True,
            )

            # Language selector
            self.render_language_selector()

            # Custom divider
            st.markdown(
                """
                <div style="height: 1px; background: linear-gradient(to right, rgba(0,0,0,0), var(--border-color), rgba(0,0,0,0)); 
                            margin: 1.2rem 0;"></div>
                """,
                unsafe_allow_html=True,
            )

            # Progress summary (for authenticated users)
            self.render_progress_summary()

            if self._is_user_authenticated():
                # Custom divider
                st.markdown(
                    """
                    <div style="height: 1px; background: linear-gradient(to right, rgba(0,0,0,0), var(--border-color), rgba(0,0,0,0)); 
                                margin: 1.2rem 0;"></div>
                    """,
                    unsafe_allow_html=True,
                )

            # Quick actions
            self.render_quick_actions()

            # Help section
            self.render_help_section()

            # Footer
            st.markdown(
                f"""
                <div style="text-align: center; padding: var(--spacing-md) 0; 
                           margin-top: var(--spacing-xl); font-size: 0.75rem;
                           color: var(--text-secondary);">
                    © 2023 Margadarsaka<br>
                    <a href="#" style="color: var(--primary-color); text-decoration: none; 
                                      font-size: 0.75rem;">Privacy</a> · 
                    <a href="#" style="color: var(--primary-color); text-decoration: none; 
                                      font-size: 0.75rem;">Terms</a> · 
                    <a href="#" style="color: var(--primary-color); text-decoration: none; 
                                      font-size: 0.75rem;">Contact</a>
                </div>
                """,
                unsafe_allow_html=True,
            )


class Navigation:
    """Main navigation controller"""

    def __init__(self):
        self.state = get_state_manager()
        self.sidebar = Sidebar()

    def get_current_page(self) -> PageType:
        """Get the current page"""
        page_str = self.state.get("current_page", PageType.HOME.value)
        try:
            return PageType(page_str)
        except ValueError:
            return PageType.HOME

    def navigate_to(self, page: PageType):
        """Navigate to a specific page"""
        self.state.set("current_page", page.value)

    def render_breadcrumb(self):
        """Render breadcrumb navigation"""
        current_page = self.get_current_page()

        # Get navigation item for current page
        nav_items = NavigationConfig.get_default_navigation()
        current_item = next(
            (item for item in nav_items if item.page_type == current_page), None
        )

        if current_item:
            st.markdown(
                f"""
            <div style="padding: 0.75rem 0; color: var(--text-secondary); 
                       font-size: 0.9em; display: flex; align-items: center;
                       background-color: var(--surface-color); border-radius: var(--border-radius-md);
                       padding: 8px 12px; margin-bottom: 15px; border: 1px solid var(--border-color);
                       box-shadow: var(--shadow-xs);">
                <a href="#" style="color: var(--primary-color); text-decoration: none; 
                                  display: flex; align-items: center; font-weight: 500;">
                    <span style="margin-right: 4px;">🏠</span>
                    <span>{get_text("home", "Home")}</span>
                </a>
                <span style="margin: 0 8px; color: var(--text-secondary);">›</span>
                <span style="font-weight: 500; color: var(--text-primary); 
                           display: flex; align-items: center;">
                    <span style="margin-right: 6px;">{current_item.icon}</span>
                    <span>{current_item.title}</span>
                </span>
            </div>
            """,
                unsafe_allow_html=True,
            )

    def render_page_header(
        self, title: Optional[str] = None, subtitle: Optional[str] = None
    ):
        """Render page header with title and subtitle"""
        if not title:
            current_page = self.get_current_page()
            nav_items = NavigationConfig.get_default_navigation()
            current_item = next(
                (item for item in nav_items if item.page_type == current_page), None
            )

            if current_item:
                title = current_item.title
                subtitle = current_item.description

        if title:
            # Enhanced section header with icon if available
            icon = ""
            for item in NavigationConfig.get_default_navigation():
                if item.title == title:
                    icon = item.icon
                    break

            icon_html = (
                f'<span style="margin-right: 12px; font-size: 1.8rem;">{icon}</span>'
                if icon
                else ""
            )

            st.markdown(
                f"""
                <div class="section-header-container" style="margin: 1.5rem 0 1rem 0;">
                    <h1 class="section-header" style="display: flex; align-items: center;">
                        {icon_html}
                        {title}
                    </h1>
                    <div style="width: 80px; height: 4px; background: var(--gradient-primary); 
                                border-radius: var(--border-radius-pill); margin-top: 8px;"></div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        if subtitle:
            st.markdown(
                f"""
                <p class="subtitle" style="opacity: 0.85; margin-bottom: 2rem;">
                    {subtitle}
                </p>
                """,
                unsafe_allow_html=True,
            )

    def render(self):
        """Render the complete navigation system"""
        # Render sidebar
        self.sidebar.render()

        # Render breadcrumb in main area
        self.render_breadcrumb()


# Convenience functions
def create_navigation() -> Navigation:
    """Create a navigation instance"""
    return Navigation()


def render_navigation():
    """Render the navigation system"""
    nav = create_navigation()
    nav.render()
    return nav.get_current_page()
