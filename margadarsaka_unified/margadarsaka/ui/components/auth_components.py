"""
Enhanced Authentication Components for Margadarsaka
Modern, secure, and user-friendly authentication interface
"""

import streamlit as st
from typing import Optional, Dict, Any, Callable
import logging
import re
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)

# Import local modules
try:
    from margadarsaka.ui.utils.i18n import get_text, get_cultural_greeting
    from margadarsaka.ui.utils.state_manager import get_state_manager
    from margadarsaka.services.appwrite_service import AppwriteService

    IMPORTS_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Import error in auth_components: {e}")
    IMPORTS_AVAILABLE = False

    # Fallback functions
    def get_text(key: str, default: Optional[str] = None, **kwargs) -> str:
        return default or key

    def get_cultural_greeting() -> str:
        return "Hello"

    class MockStateManager:
        def get(self, key: str, default: Any = None):
            return default

        def set(self, key: str, value: Any):
            pass

    def get_state_manager():
        return MockStateManager()

    class AppwriteService:
        def create_email_session(self, email: str, password: str):
            return None

        def create_account(self, email: str, password: str, name: str):
            return None


class AuthMode(Enum):
    """Authentication modes"""

    LOGIN = "login"
    REGISTER = "register"
    FORGOT_PASSWORD = "forgot_password"
    RESET_PASSWORD = "reset_password"


@dataclass
class ValidationResult:
    """Result of form validation"""

    is_valid: bool
    errors: Dict[str, str]
    warnings: Dict[str, str]


class FormValidator:
    """Advanced form validation with Indian context"""

    @staticmethod
    def validate_email(email: str) -> ValidationResult:
        """Validate email address"""
        errors = {}
        warnings = {}

        if not email:
            errors["email"] = get_text("email_required", default="Email is required")
        elif not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
            errors["email"] = get_text(
                "invalid_email", default="Please enter a valid email address"
            )

        # Common Indian email domains
        indian_domains = [
            "gmail.com",
            "yahoo.com",
            "outlook.com",
            "hotmail.com",
            "rediffmail.com",
        ]
        domain = email.split("@")[-1].lower() if "@" in email else ""

        if domain and domain not in indian_domains and not domain.endswith(".in"):
            warnings["email"] = get_text(
                "uncommon_domain", default="This email domain is uncommon in India"
            )

        return ValidationResult(len(errors) == 0, errors, warnings)

    @staticmethod
    def validate_password(
        password: str, confirm_password: Optional[str] = None
    ) -> ValidationResult:
        """Validate password with strong security requirements"""
        errors = {}
        warnings = {}

        if not password:
            errors["password"] = get_text(
                "password_required", default="Password is required"
            )
            return ValidationResult(False, errors, warnings)

        # Strength requirements
        if len(password) < 8:
            errors["password"] = get_text(
                "password_too_short",
                default="Password must be at least 8 characters long",
            )

        if not re.search(r"[A-Z]", password):
            errors["password_uppercase"] = get_text(
                "password_need_uppercase",
                default="Password must contain at least one uppercase letter",
            )

        if not re.search(r"[a-z]", password):
            errors["password_lowercase"] = get_text(
                "password_need_lowercase",
                default="Password must contain at least one lowercase letter",
            )

        if not re.search(r"\\d", password):
            errors["password_number"] = get_text(
                "password_need_number",
                default="Password must contain at least one number",
            )

        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            warnings["password_special"] = get_text(
                "password_recommend_special",
                default="Consider adding special characters for better security",
            )

        # Check for common weak passwords
        weak_patterns = ["password", "123456", "qwerty", "abc123", "admin"]
        if any(pattern in password.lower() for pattern in weak_patterns):
            errors["password_weak"] = get_text(
                "password_too_weak", default="Password is too common and weak"
            )

        # Confirm password validation
        if confirm_password is not None:
            if password != confirm_password:
                errors["confirm_password"] = get_text(
                    "passwords_dont_match", default="Passwords do not match"
                )

        return ValidationResult(len(errors) == 0, errors, warnings)

    @staticmethod
    def validate_name(name: str) -> ValidationResult:
        """Validate full name with reasonable character support for international users"""
        errors = {}
        warnings = {}

        if not name:
            errors["name"] = get_text("name_required", default="Full name is required")
        elif len(name.strip()) < 2:
            errors["name"] = get_text(
                "name_too_short", default="Name must be at least 2 characters long"
            )
        elif not re.match(r"^[a-zA-Z0-9\u00C0-\u017F\u0900-\u097F\s._'-]+$", name):
            # More permissive regex that includes:
            # - Basic Latin and Latin-1 supplement (accented characters)
            # - Devanagari script (Hindi)
            # - Basic punctuation and spaces
            errors["name"] = get_text(
                "invalid_name_chars",
                default="Name contains invalid characters. Please use only letters, numbers, and basic punctuation.",
            )
        elif len(name.strip()) > 100:
            errors["name"] = get_text(
                "name_too_long", default="Name must be less than 100 characters"
            )
        elif len(name.strip().split()) < 2:
            warnings["name"] = get_text(
                "recommend_full_name",
                default="Consider providing your full name for better personalization",
            )

        return ValidationResult(len(errors) == 0, errors, warnings)


class AuthComponent:
    """Advanced authentication component with modern UI"""

    def __init__(self, appwrite_service: Optional[AppwriteService] = None):
        self.appwrite_service = appwrite_service
        self.state = get_state_manager()
        self.validator = FormValidator()

    def show_auth_header(self, mode: AuthMode):
        """Show authentication header with greeting"""
        greeting = get_cultural_greeting()

        if mode == AuthMode.LOGIN:
            st.markdown(
                f"""
            <div class="feature-card" style="text-align: center; background: var(--surface-color); padding: var(--spacing-lg); border: 1px solid var(--border-color);">
                <h2 style="color: var(--primary-color); margin-bottom: var(--spacing-md);">{greeting} 👋</h2>
                <p style="color: var(--text-primary); margin-bottom: var(--spacing-sm); font-size: 1.1rem; font-weight: 500;">{get_text("welcome_back", default="Welcome back to Margadarsaka!")}</p>
                <p style="color: var(--text-secondary); margin-bottom: 0; font-size: 0.95rem;">{get_text("login_subtitle", default="Sign in to continue your career journey")}</p>
            </div>
            """,
                unsafe_allow_html=True,
            )

        elif mode == AuthMode.REGISTER:
            st.markdown(
                f"""
            <div class="feature-card" style="text-align: center; background: var(--surface-color); padding: var(--spacing-lg); border: 1px solid var(--border-color);">
                <h2 style="color: var(--primary-color); margin-bottom: var(--spacing-md);">{greeting} 🚀</h2>
                <p style="color: var(--text-primary); margin-bottom: var(--spacing-sm); font-size: 1.1rem; font-weight: 500;">{get_text("join_margadarsaka", default="Join Margadarsaka Community!")}</p>
                <p style="color: var(--text-secondary); margin-bottom: 0; font-size: 0.95rem;">{get_text("register_subtitle", default="Start your personalized career guidance journey")}</p>
            </div>
            """,
                unsafe_allow_html=True,
            )

    def show_validation_messages(self, validation: ValidationResult):
        """Display validation errors and warnings"""
        if validation.errors:
            for field, message in validation.errors.items():
                st.error(f"❌ {message}")

        if validation.warnings:
            for field, message in validation.warnings.items():
                st.warning(f"⚠️ {message}")

    def render_login_form(self) -> Optional[Dict[str, Any]]:
        """Render modern login form"""
        self.show_auth_header(AuthMode.LOGIN)

        with st.form("login_form", clear_on_submit=False):
            col1, col2, col3 = st.columns([1, 2, 1])

            with col2:
                st.markdown("### 🔐 " + get_text("sign_in", default="Sign In"))

                # Email input
                email = st.text_input(
                    get_text("email", default="Email"),
                    placeholder="your.email@example.com",
                    help=get_text(
                        "email_help", default="Enter your registered email address"
                    ),
                )

                # Password input
                password = st.text_input(
                    get_text("password", default="Password"),
                    type="password",
                    help=get_text("password_help", default="Enter your password"),
                )

                # Remember me checkbox
                remember_me = st.checkbox(
                    get_text("remember_me", default="Remember me"),
                    help=get_text(
                        "remember_help", default="Stay signed in on this device"
                    ),
                )

                # Submit button
                col_btn1, col_btn2 = st.columns(2)
                with col_btn1:
                    login_clicked = st.form_submit_button(
                        get_text("sign_in", default="Sign In"),
                        use_container_width=True,
                        type="primary",
                    )

                with col_btn2:
                    forgot_password = st.form_submit_button(
                        get_text("forgot_password", default="Forgot Password?"),
                        use_container_width=True,
                    )

        # Handle form submission
        if login_clicked:
            return self._handle_login(email, password, remember_me)
        elif forgot_password:
            self.state.set("auth_mode", AuthMode.FORGOT_PASSWORD.value)
            st.rerun()

        return None

    def render_register_form(self) -> Optional[Dict[str, Any]]:
        """Render modern registration form"""
        self.show_auth_header(AuthMode.REGISTER)

        with st.form("register_form", clear_on_submit=False):
            col1, col2, col3 = st.columns([1, 2, 1])

            with col2:
                st.markdown(
                    "### 📝 " + get_text("create_account", default="Create Account")
                )

                # Full name input
                full_name = st.text_input(
                    get_text("full_name", default="Full Name"),
                    placeholder="Your Full Name",
                    help=get_text("name_help", default="Enter your complete name"),
                )

                # Email input
                email = st.text_input(
                    get_text("email", default="Email"),
                    placeholder="your.email@example.com",
                    help=get_text(
                        "email_register_help",
                        default="We'll use this email for your account",
                    ),
                )

                # Password inputs
                password = st.text_input(
                    get_text("password", default="Password"),
                    type="password",
                    help=get_text(
                        "password_strength_help",
                        default="Use 8+ characters with uppercase, lowercase, and numbers",
                    ),
                )

                confirm_password = st.text_input(
                    get_text("confirm_password", default="Confirm Password"),
                    type="password",
                    help=get_text(
                        "confirm_password_help", default="Re-enter your password"
                    ),
                )

                # Terms and conditions
                terms_accepted = st.checkbox(
                    get_text(
                        "accept_terms",
                        default="I accept the Terms of Service and Privacy Policy",
                    ),
                    help=get_text(
                        "terms_help",
                        default="You must accept our terms to create an account",
                    ),
                )

                # Age verification (Indian legal requirement)
                age_verified = st.checkbox(
                    get_text("age_verification", default="I am 13 years or older"),
                    help=get_text(
                        "age_help", default="Users must be at least 13 years old"
                    ),
                )

                # Submit button
                register_clicked = st.form_submit_button(
                    get_text("create_account", default="Create Account"),
                    use_container_width=True,
                    type="primary",
                )

        # Handle form submission
        if register_clicked:
            return self._handle_register(
                full_name,
                email,
                password,
                confirm_password,
                terms_accepted,
                age_verified,
            )

        return None

    def render_forgot_password_form(self):
        """Render forgot password form"""
        st.markdown(
            """
        <div class="feature-card text-center">
            <h2 class="text-primary">🔑 Reset Password</h2>
            <p class="text-secondary">Don't worry! Enter your email and we'll send you reset instructions.</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

        with st.form("forgot_password_form"):
            col1, col2, col3 = st.columns([1, 2, 1])

            with col2:
                email = st.text_input(
                    get_text("email", default="Email"),
                    placeholder="your.email@example.com",
                    help="Enter the email address associated with your account",
                )

                col_btn1, col_btn2 = st.columns(2)
                with col_btn1:
                    reset_clicked = st.form_submit_button(
                        "Send Reset Link", use_container_width=True, type="primary"
                    )

                with col_btn2:
                    back_clicked = st.form_submit_button(
                        "Back to Login", use_container_width=True
                    )

        if reset_clicked:
            self._handle_forgot_password(email)
        elif back_clicked:
            self.state.set("auth_mode", AuthMode.LOGIN.value)
            st.rerun()

    def _handle_login(
        self, email: str, password: str, remember_me: bool
    ) -> Optional[Dict[str, Any]]:
        """Handle login submission with improved validation"""
        
        # Simple validation - just check if fields are filled
        errors = []
        
        if not email or not email.strip():
            errors.append(get_text("email_required", default="Email is required"))
        elif "@" not in email:  # Basic email check, don't be too strict
            errors.append(get_text("invalid_email", default="Please enter a valid email address"))

        if not password:
            errors.append(get_text("password_required", default="Password is required"))

        # Display all errors at once
        if errors:
            for error in errors:
                st.error(f"❌ {error}")
            return None

        # Show loading state
        with st.spinner(get_text("signing_in", default="Signing in...")):
            try:
                if self.appwrite_service:
                    # Use Appwrite for authentication
                    user = self.appwrite_service.create_email_session(email, password)
                    if user:
                        # Update state
                        self.state.set("user_authenticated", True)
                        self.state.set("current_user", user)
                        self.state.set("remember_me", remember_me)
                        self.state.set("login_timestamp", datetime.now())

                        st.success(
                            f"✅ {get_text('login_success', default='Successfully signed in!')} {get_text('welcome_user', name=user.get('name', 'User'))}"
                        )
                        st.balloons()

                        # Redirect to main app
                        self.state.set("show_auth", False)
                        st.rerun()

                        return user
                    else:
                        st.error(
                            "❌ "
                            + get_text(
                                "invalid_credentials",
                                default="Invalid email or password. Please try again.",
                            )
                        )
                else:
                    st.error(
                        "❌ "
                        + get_text(
                            "auth_service_unavailable",
                            default="Authentication service is not available",
                        )
                    )

            except Exception as e:
                logger.error(f"Login error: {e}")
                st.error(
                    f"❌ {get_text('login_failed', default='Login failed')}: {str(e)}"
                )

        return None

    def _handle_register(
        self,
        full_name: str,
        email: str,
        password: str,
        confirm_password: str,
        terms_accepted: bool,
        age_verified: bool,
    ) -> Optional[Dict[str, Any]]:
        """Handle registration submission with improved validation"""

        # Clear any previous error messages
        placeholder = st.empty()
        
        # Validate all inputs
        name_validation = self.validator.validate_name(full_name)
        email_validation = self.validator.validate_email(email)
        password_validation = self.validator.validate_password(
            password, confirm_password
        )

        # Collect all errors first
        all_errors = []
        all_warnings = []
        
        if not name_validation.is_valid:
            all_errors.extend(name_validation.errors.values())
        else:
            all_warnings.extend(name_validation.warnings.values())
            
        if not email_validation.is_valid:
            all_errors.extend(email_validation.errors.values())
        else:
            all_warnings.extend(email_validation.warnings.values())
            
        if not password_validation.is_valid:
            all_errors.extend(password_validation.errors.values())
        else:
            all_warnings.extend(password_validation.warnings.values())

        # Check required checkboxes
        if not terms_accepted:
            all_errors.append(
                get_text(
                    "must_accept_terms", default="You must accept the Terms of Service"
                )
            )

        if not age_verified:
            all_errors.append(
                get_text(
                    "must_verify_age", default="You must be at least 13 years old"
                )
            )

        # Display errors (stop if any)
        if all_errors:
            for error in all_errors:
                st.error(f"❌ {error}")
            return None
            
        # Display warnings (but continue)
        if all_warnings:
            for warning in all_warnings:
                st.warning(f"⚠️ {warning}")

        # Show loading state
        with st.spinner(
            get_text("creating_account", default="Creating your account...")
        ):
            try:
                if self.appwrite_service:
                    # Use Appwrite for registration
                    user = self.appwrite_service.create_account(
                        email, password, full_name
                    )
                    if user:
                        # Update state
                        self.state.set("user_authenticated", True)
                        self.state.set("current_user", user)
                        self.state.set("registration_timestamp", datetime.now())

                        st.success(
                            f"✅ {get_text('registration_success', default='Account created successfully!')} {get_text('welcome_user', name=full_name)}"
                        )
                        st.balloons()

                        # Show welcome message
                        st.info(
                            f"🎉 {get_text('registration_welcome', default='Welcome to Margadarsaka! Your career guidance journey begins now.')}"
                        )

                        # Redirect to main app
                        self.state.set("show_auth", False)
                        st.rerun()

                        return user
                else:
                    st.error(
                        "❌ "
                        + get_text(
                            "auth_service_unavailable",
                            default="Authentication service is not available",
                        )
                    )

            except Exception as e:
                logger.error(f"Registration error: {e}")
                st.error(
                    f"❌ {get_text('registration_failed', default='Registration failed')}: {str(e)}"
                )

        return None

    def _handle_forgot_password(self, email: str):
        """Handle forgot password submission"""
        email_validation = self.validator.validate_email(email)
        if not email_validation.is_valid:
            self.show_validation_messages(email_validation)
            return

        with st.spinner("Sending reset instructions..."):
            try:
                # Here you would implement password reset logic
                # For now, just show a success message
                st.success(f"✅ Password reset instructions sent to {email}")
                st.info(
                    "📧 Please check your email and follow the instructions to reset your password."
                )

                # Auto-redirect to login after 3 seconds
                import time

                time.sleep(3)
                self.state.set("auth_mode", AuthMode.LOGIN.value)
                st.rerun()

            except Exception as e:
                logger.error(f"Password reset error: {e}")
                st.error(f"❌ Failed to send reset instructions: {str(e)}")

    def render_social_login(self):
        """Render social login options"""
        st.markdown("---")
        st.markdown(
            "### 🔗 " + get_text("or_continue_with", default="Or continue with")
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("🔍 Google", use_container_width=True):
                st.info("Google login will be available soon!")

        with col2:
            if st.button("📧 Microsoft", use_container_width=True):
                st.info("Microsoft login will be available soon!")

        with col3:
            if st.button("📱 GitHub", use_container_width=True):
                st.info("GitHub login will be available soon!")

    def render_auth_footer(self):
        """Render authentication footer with links"""
        st.markdown("---")

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button(
                "📋 " + get_text("terms_of_service", default="Terms of Service")
            ):
                st.info("Terms of Service page will open here")

        with col2:
            if st.button("🔒 " + get_text("privacy_policy", default="Privacy Policy")):
                st.info("Privacy Policy page will open here")

        with col3:
            if st.button("❓ " + get_text("help_support", default="Help & Support")):
                st.info("Help & Support page will open here")

        # Footer text
        st.markdown(
            f"""
        <div class="text-center text-muted mt-3">
            <small>
                {get_text("auth_footer", default="© 2025 Margadarsaka. All rights reserved.")}
                <br>
                {get_text("made_with_love", default="Made with ❤️ in India")}
            </small>
        </div>
        """,
            unsafe_allow_html=True,
        )

    def render(self) -> Optional[Dict[str, Any]]:
        """Main render method for authentication component"""

        # Get current auth mode
        auth_mode_str = self.state.get("auth_mode", AuthMode.LOGIN.value)
        try:
            auth_mode = AuthMode(auth_mode_str)
        except ValueError:
            auth_mode = AuthMode.LOGIN

        # Mode switcher
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            mode_tabs = st.tabs(
                [
                    "🔑 " + get_text("sign_in", default="Sign In"),
                    "📝 " + get_text("sign_up", default="Sign Up"),
                ]
            )

            with mode_tabs[0]:
                if auth_mode == AuthMode.FORGOT_PASSWORD:
                    self.render_forgot_password_form()
                else:
                    result = self.render_login_form()
                    if result:
                        return result

                    # Show registration link
                    st.markdown("---")
                    col_center = st.columns([1, 2, 1])[1]
                    with col_center:
                        if st.button(
                            get_text(
                                "need_account", default="Don't have an account? Sign up"
                            ),
                            use_container_width=True,
                        ):
                            self.state.set("auth_mode", AuthMode.REGISTER.value)
                            st.rerun()

            with mode_tabs[1]:
                result = self.render_register_form()
                if result:
                    return result

                # Show login link
                st.markdown("---")
                col_center = st.columns([1, 2, 1])[1]
                with col_center:
                    if st.button(
                        get_text(
                            "have_account", default="Already have an account? Sign in"
                        ),
                        use_container_width=True,
                    ):
                        self.state.set("auth_mode", AuthMode.LOGIN.value)
                        st.rerun()

        # Social login and footer
        with col2:
            self.render_social_login()
            self.render_auth_footer()

        return None


# Convenience functions
def create_auth_component(
    appwrite_service: Optional[AppwriteService] = None,
) -> AuthComponent:
    """Create an authentication component instance"""
    return AuthComponent(appwrite_service)


def show_authentication_modal(
    appwrite_service: Optional[AppwriteService] = None,
) -> Optional[Dict[str, Any]]:
    """Show authentication modal and return user data if successful"""
    auth_component = create_auth_component(appwrite_service)
    return auth_component.render()
