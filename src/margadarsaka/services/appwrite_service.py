"""
Appwrite Service Wrapper for Margadarsaka
Provides abstracted access to Appwrite backend services including authentication,
database operations, and file storage.
"""

import os
import asyncio
from typing import Dict, List, Optional, Any
import logging
from datetime import datetime

from appwrite.client import Client
from appwrite.services.account import Account
from appwrite.services.databases import Databases
from appwrite.services.storage import Storage
from appwrite.services.users import Users
from appwrite.exception import AppwriteException
from appwrite.id import ID

# Import unified secrets management
from margadarsaka.secrets import SecretsManager

logger = logging.getLogger(__name__)


class AppwriteService:
    """
    Comprehensive Appwrite service wrapper for Margadarsaka.
    Handles all backend operations with proper error handling and logging.
    """

    def __init__(self):
        """Initialize Appwrite client with configuration from environment."""
        self.client = None
        self.account = None
        self.databases = None
        self.storage = None
        self.users = None

        # Configuration
        self.endpoint = None
        self.project_id = None
        self.api_key = None
        self.database_id = None
        self.users_collection_id = None
        self.assessments_collection_id = None
        self.recommendations_collection_id = None
        self.storage_bucket_id = None

        self._load_config()
        self._initialize_client()

    def _load_config(self):
        """Load configuration from SecretsManager (Doppler or environment variables)."""
        # Use the unified secrets manager
        secrets_manager = SecretsManager()

        self.endpoint = secrets_manager.get_secret(
            "APPWRITE_ENDPOINT", "https://fra.cloud.appwrite.io/v1"
        )
        self.project_id = secrets_manager.get_secret(
            "APPWRITE_PROJECT_ID", "68cd30a60005e3521af6"
        )
        self.api_key = secrets_manager.get_secret("APPWRITE_API_KEY")
        self.database_id = secrets_manager.get_secret(
            "APPWRITE_DATABASE_ID", "margadarsaka_db"
        )
        self.users_collection_id = secrets_manager.get_secret(
            "APPWRITE_USERS_COLLECTION_ID", "users"
        )
        self.assessments_collection_id = secrets_manager.get_secret(
            "APPWRITE_ASSESSMENTS_COLLECTION_ID", "assessments"
        )
        self.recommendations_collection_id = secrets_manager.get_secret(
            "APPWRITE_RECOMMENDATIONS_COLLECTION_ID", "recommendations"
        )
        self.storage_bucket_id = secrets_manager.get_secret(
            "APPWRITE_BUCKET_ID", "margadarsaka_files"
        )

        logger.info("Loaded Appwrite configuration from SecretsManager")

    def _initialize_client(self):
        """Initialize Appwrite client and services."""
        if not all([self.endpoint, self.project_id, self.api_key]):
            logger.warning(
                "Appwrite configuration incomplete - some features may not work"
            )
            return

        try:
            # Initialize client
            self.client = Client()
            self.client.set_endpoint(self.endpoint)
            self.client.set_project(self.project_id)
            self.client.set_key(self.api_key)

            # Initialize services
            self.account = Account(self.client)
            self.databases = Databases(self.client)
            self.storage = Storage(self.client)
            self.users = Users(self.client)

            logger.info("Appwrite client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Appwrite client: {e}")
            raise

    def is_configured(self) -> bool:
        """Check if Appwrite is properly configured."""
        return all([self.client, self.endpoint, self.project_id, self.api_key])

    # Synchronous wrapper methods for authentication (used by UI components)

    def create_account_sync(
        self, email: str, password: str, name: str
    ) -> Optional[Dict[str, Any]]:
        """
        Synchronous wrapper for create_account.
        Create a new user account using email and password.
        """
        if not self.is_configured():
            logger.warning(
                "Appwrite not configured - using demo mode for account creation"
            )
            # Return a mock user for demo purposes
            return {
                "$id": f"demo_user_{email.replace('@', '_').replace('.', '_')}",
                "name": name,
                "email": email,
                "emailVerification": False,
                "status": True,
                "prefs": {},
                "$createdAt": "2023-09-20T00:00:00.000+00:00",
                "$updatedAt": "2023-09-20T00:00:00.000+00:00",
            }

        try:
            # Create user account (synchronous call)
            result = self.account.create(
                user_id=ID.unique(), email=email, password=password, name=name
            )
            logger.info(f"Account created for user: {email}")
            return result
        except AppwriteException as e:
            logger.error(f"Failed to create account for {email}: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error creating account for {email}: {e}")
            return None

    def create_email_session_sync(
        self, email: str, password: str
    ) -> Optional[Dict[str, Any]]:
        """
        Synchronous wrapper for create_email_session.
        Create an email password session (login).
        """
        if not self.is_configured():
            logger.warning("Appwrite not configured - using demo mode for login")
            # Return a mock session for demo purposes (any email/password works)
            return {
                "$id": f"demo_session_{email.replace('@', '_').replace('.', '_')}",
                "userId": f"demo_user_{email.replace('@', '_').replace('.', '_')}",
                "provider": "email",
                "name": email.split("@")[0].title(),
                "email": email,
                "current": True,
                "$createdAt": "2023-09-20T00:00:00.000+00:00",
            }

        try:
            session = self.account.create_email_password_session(
                email=email, password=password
            )
            logger.info(f"Session created for user: {email}")
            return session
        except AppwriteException as e:
            logger.error(f"Failed to create session for {email}: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error creating session for {email}: {e}")
            return None

    def get_current_user_sync(self) -> Optional[Dict[str, Any]]:
        """
        Synchronous wrapper for get_current_user.
        Get the current authenticated user.
        """
        if not self.is_configured():
            return None

        try:
            user = self.account.get()
            logger.info(f"Retrieved current user: {user.get('email', 'unknown')}")
            return user
        except AppwriteException as e:
            logger.debug(f"No authenticated user: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error getting current user: {e}")
            return None

    def logout_session_sync(self, session_id: Optional[str] = None) -> bool:
        """
        Synchronous wrapper for logout_session.
        Delete a session (logout).
        """
        if not self.is_configured():
            return False

        try:
            if session_id:
                self.account.delete_session(session_id)
            else:
                self.account.delete_session("current")
            logger.info("User logged out successfully")
            return True
        except AppwriteException as e:
            logger.error(f"Failed to logout: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error during logout: {e}")
            return False

    # Compatibility methods for the auth component (delegate to sync versions)
    def create_account(
        self, email: str, password: str, name: str
    ) -> Optional[Dict[str, Any]]:
        """Compatibility method - delegates to synchronous version."""
        return self.create_account_sync(email, password, name)

    def create_email_session(
        self, email: str, password: str
    ) -> Optional[Dict[str, Any]]:
        """Compatibility method - delegates to synchronous version."""
        return self.create_email_session_sync(email, password)

    def get_current_user(self) -> Optional[Dict[str, Any]]:
        """Compatibility method - delegates to synchronous version."""
        return self.get_current_user_sync()

    def logout_session(self, session_id: Optional[str] = None) -> bool:
        """Compatibility method - delegates to synchronous version."""
        return self.logout_session_sync(session_id)

    # Async Authentication Methods (for backward compatibility and async usage)

    async def create_account(
        self, email: str, password: str, name: str
    ) -> Optional[Dict[str, Any]]:
        """
        Create a new user account using email and password.
        Equivalent to: account.create({userId: ID.unique(), email, password})
        """
        if not self.is_configured():
            logger.warning("Appwrite not configured - account creation skipped")
            return None

        try:
            # Create user account
            result = self.account.create(
                user_id=ID.unique(), email=email, password=password, name=name
            )
            logger.info(f"Account created for user: {email}")
            return result
        except AppwriteException as e:
            logger.error(f"Failed to create account for {email}: {e}")
            return None

    async def create_email_session(
        self, email: str, password: str
    ) -> Optional[Dict[str, Any]]:
        """
        Create an email password session (login).
        Equivalent to: account.createEmailPasswordSession({email, password})
        """
        if not self.is_configured():
            logger.warning("Appwrite not configured - session creation skipped")
            return None

        try:
            session = self.account.create_email_password_session(
                email=email, password=password
            )
            logger.info(f"Session created for user: {email}")
            return session
        except AppwriteException as e:
            logger.error(f"Failed to create session for {email}: {e}")
            return None

    async def get_current_user(self) -> Optional[Dict[str, Any]]:
        """
        Get the current authenticated user.
        Equivalent to: account.get()
        """
        if not self.is_configured():
            return None

        try:
            user = self.account.get()
            logger.info(f"Retrieved current user: {user.get('email', 'unknown')}")
            return user
        except AppwriteException as e:
            logger.debug(f"No authenticated user: {e}")
            return None

    async def logout_session(self, session_id: Optional[str] = None) -> bool:
        """
        Delete a session (logout).
        If session_id is None, deletes the current session.
        """
        if not self.is_configured():
            return False

        try:
            if session_id:
                self.account.delete_session(session_id)
            else:
                self.account.delete_session("current")
            logger.info("User logged out successfully")
            return True
        except AppwriteException as e:
            logger.error(f"Failed to logout: {e}")
            return False

    async def logout_all_sessions(self) -> bool:
        """Delete all sessions for the current user."""
        if not self.is_configured():
            return False

        try:
            self.account.delete_sessions()
            logger.info("All sessions deleted successfully")
            return True
        except AppwriteException as e:
            logger.error(f"Failed to delete all sessions: {e}")
            return False

    async def get_user_sessions(self) -> Optional[List[Dict[str, Any]]]:
        """Get all sessions for the current user."""
        if not self.is_configured():
            return None

        try:
            sessions = self.account.list_sessions()
            return sessions.get("sessions", [])
        except AppwriteException as e:
            logger.error(f"Failed to get user sessions: {e}")
            return None

    # OAuth 2 Authentication Methods

    def create_oauth2_session(
        self,
        provider: str,
        success: Optional[str] = None,
        failure: Optional[str] = None,
        scopes: Optional[List[str]] = None,
    ) -> Optional[str]:
        """
        Create OAuth 2 session with specified provider.
        This will redirect the user to the OAuth provider's login page.

        Args:
            provider: OAuth provider (google, github, facebook, etc.)
            success: Success redirect URL
            failure: Failure redirect URL
            scopes: List of OAuth scopes to request

        Returns:
            OAuth session URL or None if failed
        """
        if not self.is_configured():
            logger.warning("Appwrite not configured - OAuth session creation skipped")
            return None

        try:
            # Convert scopes list to comma-separated string if provided
            scopes_str = ",".join(scopes) if scopes else None

            # Create OAuth 2 session - this returns a redirect URL
            oauth_url = self.account.create_o_auth2_session(
                provider=provider, success=success, failure=failure, scopes=scopes_str
            )

            logger.info(f"OAuth 2 session created for provider: {provider}")
            return oauth_url

        except AppwriteException as e:
            logger.error(f"Failed to create OAuth 2 session for {provider}: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error creating OAuth 2 session: {e}")
            return None

    def get_session(self, session_id: str = "current") -> Optional[Dict[str, Any]]:
        """
        Get session information including OAuth provider details.

        Args:
            session_id: Session ID or 'current' for active session

        Returns:
            Session information including provider details
        """
        if not self.is_configured():
            return None

        try:
            session = self.account.get_session(session_id)
            logger.debug(f"Retrieved session: {session_id}")
            return session
        except AppwriteException as e:
            logger.debug(f"Failed to get session {session_id}: {e}")
            return None

    def update_session(self, session_id: str = "current") -> Optional[Dict[str, Any]]:
        """
        Update OAuth 2 session to refresh access tokens.

        Args:
            session_id: Session ID or 'current' for active session

        Returns:
            Updated session information
        """
        if not self.is_configured():
            return None

        try:
            updated_session = self.account.update_session(session_id)
            logger.info(f"OAuth 2 session refreshed: {session_id}")
            return updated_session
        except AppwriteException as e:
            logger.error(f"Failed to refresh OAuth session {session_id}: {e}")
            return None

    def delete_session(self, session_id: str = "current") -> bool:
        """
        Delete a specific session (OAuth or email/password).

        Args:
            session_id: Session ID or 'current' for active session

        Returns:
            True if session was deleted successfully
        """
        if not self.is_configured():
            return False

        try:
            self.account.delete_session(session_id)
            logger.info(f"Session deleted: {session_id}")
            return True
        except AppwriteException as e:
            logger.error(f"Failed to delete session {session_id}: {e}")
            return False

    def get_oauth_provider_info(
        self, session_id: str = "current"
    ) -> Optional[Dict[str, Any]]:
        """
        Get OAuth provider information from session.

        Args:
            session_id: Session ID or 'current' for active session

        Returns:
            OAuth provider information (provider, uid, access token, etc.)
        """
        session = self.get_session(session_id)
        if not session:
            return None

        # Extract OAuth-specific information
        oauth_info = {
            "provider": session.get("provider"),
            "provider_uid": session.get("providerUid"),
            "provider_access_token": session.get("providerAccessToken"),
            "provider_access_token_expiry": session.get("providerAccessTokenExpiry"),
            "provider_refresh_token": session.get("providerRefreshToken"),
        }

        # Only return if this is actually an OAuth session
        if oauth_info["provider"]:
            return oauth_info

        return None

    # User Management Methods

    async def create_user_profile(
        self, user_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Create a new user profile in Appwrite."""
        if not self.is_configured():
            logger.warning("Appwrite not configured - user profile creation skipped")
            return None

        try:
            # Create document in users collection
            result = self.databases.create_document(
                database_id=self.database_id,
                collection_id=self.users_collection_id,
                document_id=ID.unique(),
                data={
                    **user_data,
                    "created_at": datetime.now().isoformat(),
                    "updated_at": datetime.now().isoformat(),
                },
            )
            logger.info(f"User profile created with ID: {result['$id']}")
            return result
        except AppwriteException as e:
            logger.error(f"Failed to create user profile: {e}")
            return None

    async def get_user_profile(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve user profile by ID."""
        if not self.is_configured():
            return None

        try:
            result = self.databases.get_document(
                database_id=self.database_id,
                collection_id=self.users_collection_id,
                document_id=user_id,
            )
            return result
        except AppwriteException as e:
            logger.error(f"Failed to get user profile {user_id}: {e}")
            return None

    async def update_user_profile(
        self, user_id: str, updates: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Update user profile."""
        if not self.is_configured():
            return None

        try:
            updates["updated_at"] = datetime.now().isoformat()
            result = self.databases.update_document(
                database_id=self.database_id,
                collection_id=self.users_collection_id,
                document_id=user_id,
                data=updates,
            )
            logger.info(f"User profile updated: {user_id}")
            return result
        except AppwriteException as e:
            logger.error(f"Failed to update user profile {user_id}: {e}")
            return None

    # Assessment Methods

    async def save_assessment_result(
        self, user_id: str, assessment_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Save assessment results."""
        if not self.is_configured():
            return None

        try:
            result = self.databases.create_document(
                database_id=self.database_id,
                collection_id=self.assessments_collection_id,
                document_id=ID.unique(),
                data={
                    "user_id": user_id,
                    **assessment_data,
                    "created_at": datetime.now().isoformat(),
                },
            )
            logger.info(f"Assessment saved for user {user_id}")
            return result
        except AppwriteException as e:
            logger.error(f"Failed to save assessment: {e}")
            return None

    async def get_user_assessments(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all assessments for a user."""
        if not self.is_configured():
            return []

        try:
            result = self.databases.list_documents(
                database_id=self.database_id,
                collection_id=self.assessments_collection_id,
                queries=[f'equal("user_id", "{user_id}")'],
            )
            return result.get("documents", [])
        except AppwriteException as e:
            logger.error(f"Failed to get assessments for user {user_id}: {e}")
            return []

    # Career Recommendations Methods

    async def save_career_recommendation(
        self, user_id: str, recommendation_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Save career recommendation."""
        if not self.is_configured():
            return None

        try:
            result = self.databases.create_document(
                database_id=self.database_id,
                collection_id=self.recommendations_collection_id,
                document_id=ID.unique(),
                data={
                    "user_id": user_id,
                    **recommendation_data,
                    "created_at": datetime.now().isoformat(),
                },
            )
            logger.info(f"Career recommendation saved for user {user_id}")
            return result
        except AppwriteException as e:
            logger.error(f"Failed to save career recommendation: {e}")
            return None

    async def get_user_recommendations(self, user_id: str) -> List[Dict[str, Any]]:
        """Get career recommendations for a user."""
        if not self.is_configured():
            return []

        try:
            result = self.databases.list_documents(
                database_id=self.database_id,
                collection_id=self.recommendations_collection_id,
                queries=[f'equal("user_id", "{user_id}")'],
            )
            return result.get("documents", [])
        except AppwriteException as e:
            logger.error(f"Failed to get recommendations for user {user_id}: {e}")
            return []

    # File Storage Methods

    async def upload_file(
        self, file_path: str, file_id: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """Upload file to Appwrite storage."""
        if not self.is_configured():
            return None

        try:
            with open(file_path, "rb") as file:
                result = self.storage.create_file(
                    bucket_id=self.storage_bucket_id,
                    file_id=file_id or ID.unique(),
                    file=file,
                )
            logger.info(f"File uploaded: {result['$id']}")
            return result
        except AppwriteException as e:
            logger.error(f"Failed to upload file: {e}")
            return None

    async def get_file_url(self, file_id: str) -> Optional[str]:
        """Get file download URL."""
        if not self.is_configured():
            return None

        try:
            # Get file view URL
            url = f"{self.endpoint}/storage/buckets/{self.storage_bucket_id}/files/{file_id}/view?project={self.project_id}"
            return url
        except Exception as e:
            logger.error(f"Failed to get file URL: {e}")
            return None

    async def delete_file(self, file_id: str) -> bool:
        """Delete file from storage."""
        if not self.is_configured():
            return False

        try:
            self.storage.delete_file(bucket_id=self.storage_bucket_id, file_id=file_id)
            logger.info(f"File deleted: {file_id}")
            return True
        except AppwriteException as e:
            logger.error(f"Failed to delete file {file_id}: {e}")
            return False

    # Health Check Methods

    def health_check(self) -> Dict[str, Any]:
        """Check Appwrite service health."""
        status = {
            "configured": self.is_configured(),
            "endpoint": self.endpoint,
            "project_id": self.project_id,
            "database_id": self.database_id,
            "timestamp": datetime.now().isoformat(),
        }

        if self.is_configured():
            try:
                # Try to get account details as a health check
                self.account.get()
                status["connection"] = "healthy"
            except AppwriteException as e:
                status["connection"] = "error"
                status["error"] = str(e)
        else:
            status["connection"] = "not_configured"

        return status


# Global instance for easy access
appwrite_service = AppwriteService()


# Convenience functions for common operations
async def create_user(user_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Create a new user profile."""
    return await appwrite_service.create_user_profile(user_data)


async def get_user(user_id: str) -> Optional[Dict[str, Any]]:
    """Get user profile by ID."""
    return await appwrite_service.get_user_profile(user_id)


async def save_assessment(
    user_id: str, assessment_data: Dict[str, Any]
) -> Optional[Dict[str, Any]]:
    """Save assessment results."""
    return await appwrite_service.save_assessment_result(user_id, assessment_data)


async def save_recommendation(
    user_id: str, recommendation_data: Dict[str, Any]
) -> Optional[Dict[str, Any]]:
    """Save career recommendation."""
    return await appwrite_service.save_career_recommendation(
        user_id, recommendation_data
    )


def get_appwrite_health() -> Dict[str, Any]:
    """Get Appwrite service health status."""
    return appwrite_service.health_check()
