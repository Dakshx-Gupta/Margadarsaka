"""
Streamlit Native OIDC Authentication for Margadarsaka
Uses Streamlit's built-in authentication features with OpenID Connect
"""

import streamlit as st
import logging
from typing import Optional, Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)

# Import local modules
try:
    from margadarsaka.ui.utils.i18n import get_text
    from margadarsaka.ui.utils.state_manager import get_state_manager

    IMPORTS_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Import error in oidc_auth: {e}")
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


class OIDCAuthManager:
    """
    Streamlit Native OIDC Authentication Manager
    Provides a clean interface for authentication using Streamlit's built-in features
    """

    def __init__(self):
        self.state = get_state_manager()

    def is_user_logged_in(self) -> bool:
        """Check if user is currently logged in using Streamlit's native auth"""
        try:
            return st.user.is_logged_in if hasattr(st, "user") else False
        except Exception as e:
            logger.debug(f"Error checking login status: {e}")
            return False

    def get_user_info(self) -> Optional[Dict[str, Any]]:
        """Get current user information from Streamlit's auth system"""
        try:
            if self.is_user_logged_in():
                user_data = dict(st.user)
                return {
                    "id": user_data.get("sub", ""),
                    "name": user_data.get("name", ""),
                    "email": user_data.get("email", ""),
                    "picture": user_data.get("picture", ""),
                    "provider": user_data.get("iss", ""),
                    "verified": user_data.get("email_verified", False),
                    "raw": user_data,
                }
            return None
        except Exception as e:
            logger.error(f"Error getting user info: {e}")
            return None

    def render_login_button(self, label: Optional[str] = None) -> None:
        """Render the login button using Streamlit's native auth"""
        button_label = label or get_text("login", "Sign In")

        # Add custom styling for the login button
        st.markdown(
            """
        <style>
        /* Style for Streamlit's native login button */
        .stButton > button[data-testid="baseButton-primary"] {
            background: var(--gradient-primary, linear-gradient(135deg, #1E88E5 0%, #8E24AA 100%));
            color: white;
            border: none;
            border-radius: 12px;
            padding: 0.75rem 2rem;
            font-weight: 600;
            font-size: 1rem;
            transition: all 0.3s ease;
            box-shadow: 0 4px 12px rgba(30, 136, 229, 0.3);
        }
        
        .stButton > button[data-testid="baseButton-primary"]:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(30, 136, 229, 0.4);
        }
        </style>
        """,
            unsafe_allow_html=True,
        )

        if st.button(f"🔑 {button_label}", type="primary", use_container_width=True):
            st.login()

    def render_logout_button(self, label: Optional[str] = None) -> None:
        """Render the logout button using Streamlit's native auth"""
        button_label = label or get_text("logout", "Sign Out")

        if st.button(f"🚪 {button_label}", use_container_width=True):
            st.logout()

    def render_user_profile(self) -> None:
        """Render user profile information"""
        user_info = self.get_user_info()

        if not user_info:
            return

        st.markdown(
            f"""
        <div class="feature-card" style="background: var(--surface-color); border: 1px solid var(--border-color);">
            <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 15px;">
                <div style="width: 60px; height: 60px; border-radius: 50%; overflow: hidden; 
                          border: 3px solid var(--primary-color); display: flex; align-items: center; justify-content: center;
                          background: var(--gradient-primary);">
                    {
                f'<img src="{user_info["picture"]}" style="width: 100%; height: 100%; object-fit: cover;" />'
                if user_info.get("picture")
                else f'<span style="color: white; font-size: 1.5rem; font-weight: bold;">{user_info.get("name", "U")[0].upper()}</span>'
            }
                </div>
                <div>
                    <h3 style="margin: 0; color: var(--text-primary); font-size: 1.3rem; font-weight: 600;">
                        {user_info.get("name", "User")}
                    </h3>
                    <p style="margin: 4px 0; color: var(--text-secondary); font-size: 0.95rem;">
                        {user_info.get("email", "")}
                    </p>
                    <div style="display: flex; align-items: center; gap: 8px; margin-top: 8px;">
                        <span style="background: var(--success-color); color: white; padding: 2px 8px; 
                                   border-radius: 12px; font-size: 0.8rem; font-weight: 500;">
                            {
                "✅ Verified" if user_info.get("verified") else "⏳ Pending"
            }
                        </span>
                        <span style="color: var(--text-secondary); font-size: 0.85rem;">
                            via {
                user_info.get("provider", "OAuth").replace("https://", "").split("/")[0]
            }
                        </span>
                    </div>
                </div>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    def render_auth_section(self) -> None:
        """Render the complete authentication section"""
        if self.is_user_logged_in():
            # User is logged in - show profile and logout
            st.markdown(f"### 👤 {get_text('welcome', 'Welcome')}")

            self.render_user_profile()

            st.markdown("---")

            col1, col2 = st.columns([3, 1])
            with col2:
                self.render_logout_button()

        else:
            # User is not logged in - show login option
            st.markdown(
                f"""
            <div class="info-card fade-in" style="padding: var(--spacing-lg); margin-bottom: var(--spacing-md); text-align: center;">
                <div style="font-size: 3rem; margin-bottom: 15px;">🔐</div>
                <h3 style="color: var(--primary-color); margin-bottom: 10px;">
                    {get_text("secure_login", "Secure Authentication")}
                </h3>
                <p style="color: var(--text-secondary); margin-bottom: 20px;">
                    {get_text("login_description", "Sign in securely with your preferred provider to access all features and save your progress.")}
                </p>
            </div>
            """,
                unsafe_allow_html=True,
            )

            self.render_login_button()

            # Additional info about supported providers
            st.markdown(
                f"""
            <div style="text-align: center; margin-top: 15px; color: var(--text-secondary); font-size: 0.9rem;">
                {get_text("supported_providers", "Supports Google, Microsoft, GitHub, and other OAuth providers")}
            </div>
            """,
                unsafe_allow_html=True,
            )


def create_oidc_auth_manager() -> OIDCAuthManager:
    """Create an OIDC authentication manager instance"""
    return OIDCAuthManager()


def render_authentication_section() -> OIDCAuthManager:
    """Render the authentication section and return the auth manager"""
    auth_manager = create_oidc_auth_manager()
    auth_manager.render_auth_section()
    return auth_manager


# Route guard decorator
def require_authentication(func):
    """Decorator to require authentication for a page/function"""

    def wrapper(*args, **kwargs):
        auth_manager = create_oidc_auth_manager()

        if not auth_manager.is_user_logged_in():
            st.warning(
                "🔒 " + get_text("login_required", "Please log in to access this page.")
            )
            auth_manager.render_auth_section()
            st.stop()

        return func(*args, **kwargs)

    return wrapper


# Context manager for protected sections
class ProtectedSection:
    """Context manager for protecting sections of code"""

    def __init__(self, message: Optional[str] = None):
        self.message = message or get_text(
            "login_required", "Please log in to access this section."
        )
        self.auth_manager = create_oidc_auth_manager()

    def __enter__(self):
        if not self.auth_manager.is_user_logged_in():
            st.warning(f"🔒 {self.message}")
            self.auth_manager.render_auth_section()
            st.stop()
        return self.auth_manager

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
