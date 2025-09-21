"""
Appwrite OAuth 2 Authentication for Margadarsaka
Implements OAuth 2 authentication using Appwrite's OAuth providers
"""

import streamlit as st
import logging
from typing import Optional, Dict, Any, List
from datetime import datetime
import json

logger = logging.getLogger(__name__)

# Import local modules
try:
    from margadarsaka.ui.utils.i18n import get_text
    from margadarsaka.ui.utils.state_manager import get_state_manager
    from margadarsaka.services.appwrite_service import AppwriteService

    IMPORTS_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Import error in oauth_auth: {e}")
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

    class AppwriteService:
        def create_oauth2_session(self, provider: str, scopes: List[str] = None):
            return None


class OAuth2Provider:
    """OAuth 2 Provider definitions"""

    GOOGLE = "google"
    GITHUB = "github"
    FACEBOOK = "facebook"
    TWITTER = "twitter"
    LINKEDIN = "linkedin"
    MICROSOFT = "microsoft"
    DISCORD = "discord"


class AppwriteOAuth2Manager:
    """
    Appwrite OAuth 2 Authentication Manager
    Handles OAuth 2 authentication using Appwrite's authentication service
    """

    def __init__(self, appwrite_service: Optional[AppwriteService] = None):
        self.state = get_state_manager()
        self.appwrite_service = appwrite_service
        self.success_url = st.secrets.get("oauth", {}).get(
            "success_url", "https://margadarsaka.com/auth/success"
        )
        self.failure_url = st.secrets.get("oauth", {}).get(
            "failure_url", "https://margadarsaka.com/auth/failure"
        )

    def is_user_logged_in(self) -> bool:
        """Check if user is currently logged in via OAuth 2"""
        try:
            session = self.get_current_session()
            return session is not None and session.get("provider") is not None
        except Exception as e:
            logger.debug(f"Error checking OAuth login status: {e}")
            return False

    def get_current_session(self) -> Optional[Dict[str, Any]]:
        """Get the current OAuth 2 session information"""
        try:
            if self.appwrite_service:
                session = self.appwrite_service.get_session("current")
                return session
            return None
        except Exception as e:
            logger.debug(f"No active OAuth session: {e}")
            return None

    def get_user_info(self) -> Optional[Dict[str, Any]]:
        """Get OAuth 2 user profile information"""
        try:
            session = self.get_current_session()
            if session:
                # Extract user information from OAuth session
                user_info = {
                    "id": session.get("userId"),
                    "provider": session.get("provider"),
                    "provider_uid": session.get("providerUid"),
                    "email": session.get("providerEmail"),
                    "name": session.get("providerName"),
                    "picture": session.get("providerAvatar"),
                    "verified": True,  # OAuth providers are typically verified
                    "access_token": session.get("providerAccessToken"),
                    "token_expiry": session.get("providerAccessTokenExpiry"),
                }
                return user_info
            return None
        except Exception as e:
            logger.error(f"Error getting OAuth user info: {e}")
            return None

    def create_oauth2_token(
        self, provider: str, scopes: Optional[List[str]] = None
    ) -> bool:
        """
        Create OAuth 2 token with specified provider, which redirects the user.

        Args:
            provider: OAuth provider (google, github, etc.)
            scopes: List of OAuth scopes to request

        Returns:
            bool: True if the redirect was initiated successfully.
        """
        try:
            if not self.appwrite_service:
                st.error("Authentication service not available")
                return False

            # Default scopes based on provider
            if not scopes:
                scopes = self._get_default_scopes(provider)

            # Create OAuth 2 token - this will trigger a redirect
            self.appwrite_service.create_oauth2_token(
                provider=provider,
                success=self.success_url,
                failure=self.failure_url,
                scopes=scopes,
            )
            
            # If the above call doesn't raise an exception, it means the redirect is happening.
            st.success(f"Redirecting to {provider.title()} for authentication...")
            # We might not even see this message as the browser will be redirected.
            return True

        except Exception as e:
            logger.error(f"Error creating OAuth 2 token: {e}")
            st.error(f"Authentication error: {str(e)}")
            return False

    def _get_default_scopes(self, provider: str) -> List[str]:
        """Get default OAuth scopes for each provider"""
        default_scopes = {
            OAuth2Provider.GOOGLE: ["openid", "email", "profile"],
            OAuth2Provider.GITHUB: ["user:email", "read:user"],
            OAuth2Provider.FACEBOOK: ["email", "public_profile"],
            OAuth2Provider.TWITTER: ["tweet.read", "users.read"],
            OAuth2Provider.LINKEDIN: ["r_liteprofile", "r_emailaddress"],
            OAuth2Provider.MICROSOFT: ["openid", "email", "profile"],
            OAuth2Provider.DISCORD: ["identify", "email"],
        }
        return default_scopes.get(provider, [])

    def refresh_oauth_session(self) -> bool:
        """Refresh the OAuth 2 session to update access tokens"""
        try:
            if not self.appwrite_service:
                return False

            session = self.appwrite_service.update_session(session_id="current")
            if session:
                logger.info("OAuth 2 session refreshed successfully")
                return True
            return False
        except Exception as e:
            logger.error(f"Error refreshing OAuth session: {e}")
            return False

    def logout(self) -> None:
        """Logout the current OAuth 2 user"""
        try:
            if self.appwrite_service:
                self.appwrite_service.delete_session(session_id="current")

            # Clear local state
            self.state.set("oauth_user", None)
            self.state.set("oauth_session", None)

            st.success("Successfully logged out")
            st.rerun()
        except Exception as e:
            logger.error(f"Error during OAuth logout: {e}")
            st.error("Logout failed")

    def render_oauth_login_buttons(self) -> None:
        """Render OAuth 2 login buttons for multiple providers"""
        st.markdown("### 🔐 " + get_text("oauth_login", "Social Login"))

        # Define available providers with their display information
        providers = [
            {
                "id": OAuth2Provider.GOOGLE,
                "name": "Google",
                "icon": "🔍",
                "color": "#4285F4",
                "scopes": ["openid", "email", "profile"],
            },
            {
                "id": OAuth2Provider.GITHUB,
                "name": "GitHub",
                "icon": "🐙",
                "color": "#333333",
                "scopes": ["user:email", "read:user"],
            },
            {
                "id": OAuth2Provider.MICROSOFT,
                "name": "Microsoft",
                "icon": "🪟",
                "color": "#0078D4",
                "scopes": ["openid", "email", "profile"],
            },
        ]

        # Render provider buttons
        for provider in providers:
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button(
                    f"{provider['icon']} Continue with {provider['name']}",
                    key=f"oauth_{provider['id']}",
                    use_container_width=True,
                    type="secondary",
                ):
                    self.create_oauth2_token(provider["id"], provider["scopes"])

    def render_user_profile(self) -> None:
        """Render OAuth 2 user profile information"""
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
                            ✅ Verified via {user_info.get("provider", "OAuth").title()}
                        </span>
                        <span style="color: var(--text-secondary); font-size: 0.85rem;">
                            ID: {user_info.get("provider_uid", "")[:8]}...
                        </span>
                    </div>
                </div>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        # Show token expiry warning if needed
        if user_info.get("token_expiry"):
            expiry_date = datetime.fromisoformat(
                user_info["token_expiry"].replace("Z", "+00:00")
            )
            if (expiry_date - datetime.now()).days < 7:
                st.warning(
                    "⚠️ Your access token expires soon. Please refresh your session."
                )
                if st.button("🔄 Refresh Session", key="refresh_oauth"):
                    self.refresh_oauth_session()

    def render_logout_button(self, label: Optional[str] = None) -> None:
        """Render OAuth 2 logout button"""
        button_label = label or get_text("logout", "Sign Out")

        if st.button(
            f"🚪 {button_label}", use_container_width=True, key="oauth_logout"
        ):
            self.logout()

    def render_auth_section(self) -> None:
        """Render the complete OAuth 2 authentication section"""
        if self.is_user_logged_in():
            # User is logged in - show profile and logout
            st.markdown(f"### 👤 {get_text('welcome', 'Welcome')}")
            self.render_user_profile()

            col1, col2 = st.columns(2)
            with col1:
                if st.button("⚙️ Settings", use_container_width=True):
                    st.info("Settings page coming soon!")
            with col2:
                self.render_logout_button()
        else:
            # User not logged in - show login options
            self.render_oauth_login_buttons()


def create_oauth2_auth_manager(
    appwrite_service: Optional[AppwriteService] = None,
) -> AppwriteOAuth2Manager:
    """Factory function to create OAuth 2 auth manager"""
    return AppwriteOAuth2Manager(appwrite_service)


def render_oauth2_authentication_section(
    appwrite_service: Optional[AppwriteService] = None,
) -> AppwriteOAuth2Manager:
    """Convenience function to render OAuth 2 authentication section"""
    auth_manager = create_oauth2_auth_manager(appwrite_service)
    auth_manager.render_auth_section()
    return auth_manager


def oauth2_route_guard(func):
    """
    Decorator to protect routes with OAuth 2 authentication
    Usage: @oauth2_route_guard
    """

    def wrapper(*args, **kwargs):
        auth_manager = create_oauth2_auth_manager()
        if not auth_manager.is_user_logged_in():
            st.warning("🔒 Please log in to access this feature")
            auth_manager.render_oauth_login_buttons()
            return None
        return func(*args, **kwargs)

    return wrapper


class OAuth2Guard:
    """Context manager for OAuth 2 authentication guard"""

    def __init__(
        self,
        appwrite_service: Optional[AppwriteService] = None,
        message: Optional[str] = None,
    ):
        self.auth_manager = create_oauth2_auth_manager(appwrite_service)
        self.message = message or "Please log in to access this feature"

    def __enter__(self):
        if not self.auth_manager.is_user_logged_in():
            st.warning(f"🔒 {self.message}")
            self.auth_manager.render_oauth_login_buttons()
            st.stop()
        return self.auth_manager

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
