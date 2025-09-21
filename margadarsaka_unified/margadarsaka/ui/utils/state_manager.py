"""
Advanced State Management for Streamlit Applications
Provides centralized state management with persistence and type safety
"""

import streamlit as st
from typing import Any, Dict, Optional, TypeVar, Generic, Callable
import json
import pickle
import logging
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from enum import Enum

logger = logging.getLogger(__name__)

T = TypeVar("T")


class StateScope(Enum):
    """Different scopes for state persistence"""

    SESSION = "session"  # Current session only
    USER = "user"  # Per user (requires authentication)
    GLOBAL = "global"  # Shared across all users


@dataclass
class StateConfig:
    """Configuration for state management"""

    persist: bool = True
    scope: StateScope = StateScope.SESSION
    ttl: Optional[timedelta] = None  # Time to live
    serialize: bool = False  # Whether to serialize complex objects
    encrypt: bool = False  # Whether to encrypt sensitive data


class SessionState:
    """Enhanced session state management with type safety and persistence"""

    def __init__(self):
        self._state = st.session_state
        self._configs: Dict[str, StateConfig] = {}
        self._initialize_default_state()

    def _initialize_default_state(self):
        """Initialize default application state"""
        self.set_default("user_authenticated", False)
        self.set_default("current_user", None)
        self.set_default("current_page", "home")
        self.set_default("language", "en")
        self.set_default("theme", "light")
        self.set_default("assessment_progress", {})
        self.set_default("chat_history", [])
        self.set_default("user_preferences", {})
        self.set_default("last_activity", datetime.now())

    def set_default(self, key: str, value: Any, config: Optional[StateConfig] = None):
        """Set a default value if the key doesn't exist"""
        if key not in self._state:
            self._state[key] = value

        if config:
            self._configs[key] = config

    def get(self, key: str, default: Any = None) -> Any:
        """Get a value from state with optional default"""
        return self._state.get(key, default)

    def set(self, key: str, value: Any, config: Optional[StateConfig] = None):
        """Set a value in state with optional configuration"""
        self._state[key] = value

        if config:
            self._configs[key] = config

        # Update last activity
        self._state["last_activity"] = datetime.now()

    def update(self, updates: Dict[str, Any]):
        """Update multiple state values at once"""
        for key, value in updates.items():
            self.set(key, value)

    def delete(self, key: str):
        """Delete a key from state"""
        if key in self._state:
            del self._state[key]
        if key in self._configs:
            del self._configs[key]

    def clear(self):
        """Clear all state except essential system state"""
        protected_keys = {"user_authenticated", "current_user", "language", "theme"}
        keys_to_delete = [k for k in self._state.keys() if k not in protected_keys]

        for key in keys_to_delete:
            self.delete(str(key))

    def exists(self, key: str) -> bool:
        """Check if a key exists in state"""
        return key in self._state

    def serialize_state(self) -> str:
        """Serialize current state to JSON string"""
        serializable_state = {}

        for key, value in self._state.items():
            try:
                # Skip non-serializable values
                json.dumps(value)
                serializable_state[key] = value
            except (TypeError, ValueError):
                logger.warning(f"Skipping non-serializable state key: {key}")

        return json.dumps(serializable_state, default=str)

    def load_from_json(self, json_str: str):
        """Load state from JSON string"""
        try:
            data = json.loads(json_str)
            for key, value in data.items():
                self.set(key, value)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to load state from JSON: {e}")


class StateManager:
    """Advanced state management with persistence and user context"""

    def __init__(self):
        self.session = SessionState()
        self._user_states: Dict[str, Dict[str, Any]] = {}
        self._global_state: Dict[str, Any] = {}

    def get_user_id(self) -> Optional[str]:
        """Get current user ID from authentication state"""
        user = self.session.get("current_user")
        if user and isinstance(user, dict):
            return user.get("$id") or user.get("email")
        return None

    def get(
        self, key: str, default: Any = None, scope: StateScope = StateScope.SESSION
    ) -> Any:
        """Get value from specified scope"""
        if scope == StateScope.SESSION:
            return self.session.get(key, default)
        elif scope == StateScope.USER:
            user_id = self.get_user_id()
            if user_id and user_id in self._user_states:
                return self._user_states[user_id].get(key, default)
            return default
        elif scope == StateScope.GLOBAL:
            return self._global_state.get(key, default)

        return default

    def set(self, key: str, value: Any, scope: StateScope = StateScope.SESSION):
        """Set value in specified scope"""
        if scope == StateScope.SESSION:
            self.session.set(key, value)
        elif scope == StateScope.USER:
            user_id = self.get_user_id()
            if user_id:
                if user_id not in self._user_states:
                    self._user_states[user_id] = {}
                self._user_states[user_id][key] = value
        elif scope == StateScope.GLOBAL:
            self._global_state[key] = value

    def get_user_preference(self, key: str, default: Any = None) -> Any:
        """Get user-specific preference"""
        preferences = self.get("user_preferences", {}, StateScope.USER)
        return preferences.get(key, default)

    def set_user_preference(self, key: str, value: Any):
        """Set user-specific preference"""
        preferences = self.get("user_preferences", {}, StateScope.USER)
        preferences[key] = value
        self.set("user_preferences", preferences, StateScope.USER)

    def increment_counter(
        self, key: str, scope: StateScope = StateScope.SESSION
    ) -> int:
        """Increment a counter and return new value"""
        current = self.get(key, 0, scope)
        new_value = current + 1
        self.set(key, new_value, scope)
        return new_value

    def add_to_list(
        self,
        key: str,
        item: Any,
        max_length: Optional[int] = None,
        scope: StateScope = StateScope.SESSION,
    ):
        """Add item to a list state"""
        current_list = self.get(key, [], scope)
        current_list.append(item)

        if max_length and len(current_list) > max_length:
            current_list = current_list[-max_length:]

        self.set(key, current_list, scope)

    def remove_from_list(
        self, key: str, item: Any, scope: StateScope = StateScope.SESSION
    ):
        """Remove item from a list state"""
        current_list = self.get(key, [], scope)
        if item in current_list:
            current_list.remove(item)
            self.set(key, current_list, scope)

    def toggle_boolean(self, key: str, scope: StateScope = StateScope.SESSION) -> bool:
        """Toggle a boolean value and return new state"""
        current = self.get(key, False, scope)
        new_value = not current
        self.set(key, new_value, scope)
        return new_value

    def update_dict(
        self, key: str, updates: Dict[str, Any], scope: StateScope = StateScope.SESSION
    ):
        """Update a dictionary in state"""
        current_dict = self.get(key, {}, scope)
        current_dict.update(updates)
        self.set(key, current_dict, scope)

    def clear_user_state(self):
        """Clear all user-specific state"""
        user_id = self.get_user_id()
        if user_id and user_id in self._user_states:
            del self._user_states[user_id]

    def get_state_summary(self) -> Dict[str, Any]:
        """Get summary of current state for debugging"""
        return {
            "session_keys": list(self.session._state.keys()),
            "user_count": len(self._user_states),
            "global_keys": list(self._global_state.keys()),
            "current_user": self.get_user_id(),
            "last_activity": self.session.get("last_activity"),
        }


# Global state manager instance
_state_manager: Optional[StateManager] = None


def get_state_manager() -> StateManager:
    """Get or create global state manager instance"""
    global _state_manager
    if _state_manager is None:
        _state_manager = StateManager()
    return _state_manager


def init_state():
    """Initialize application state"""
    state = get_state_manager()

    # Initialize page-specific state
    if not state.session.exists("initialized"):
        state.session.set("initialized", True)
        state.session.set("app_start_time", datetime.now())

        # Initialize component states
        state.session.set("sidebar_expanded", True)
        state.session.set("notifications", [])
        state.session.set("loading_states", {})
        state.session.set("error_messages", {})

        logger.info("Application state initialized")

    return state


# Decorators for state management
def with_state(func: Callable) -> Callable:
    """Decorator to inject state manager into function"""

    def wrapper(*args, **kwargs):
        state = get_state_manager()
        return func(state, *args, **kwargs)

    return wrapper


def persistent_state(
    key: str, default: Any = None, scope: StateScope = StateScope.SESSION
):
    """Decorator for persistent state variables"""

    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            state = get_state_manager()

            if not state.get(f"{key}_initialized", False, scope):
                value = func(*args, **kwargs)
                state.set(key, value, scope)
                state.set(f"{key}_initialized", True, scope)

            return state.get(key, default, scope)

        return wrapper

    return decorator


# Context managers for state operations
class StateTransaction:
    """Context manager for atomic state operations"""

    def __init__(self, state_manager: StateManager):
        self.state_manager = state_manager
        self.backup = {}
        self.committed = False

    def __enter__(self):
        # Create backup of current session state
        self.backup = dict(self.state_manager.session._state)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None and not self.committed:
            # Rollback on exception
            self.state_manager.session._state.clear()
            self.state_manager.session._state.update(self.backup)
            logger.warning("State transaction rolled back due to exception")

    def commit(self):
        """Commit the transaction"""
        self.committed = True
        self.backup.clear()


# Utility functions
def safe_state_operation(func: Callable, *args, **kwargs) -> Any:
    """Safely execute a state operation with error handling"""
    try:
        return func(*args, **kwargs)
    except Exception as e:
        logger.error(f"State operation failed: {e}")
        return None


def export_user_data(user_id: str) -> Optional[str]:
    """Export user data for backup/migration"""
    try:
        state = get_state_manager()
        user_data = {
            "user_id": user_id,
            "preferences": state.get("user_preferences", {}, StateScope.USER),
            "assessment_data": state.get("assessment_progress", {}, StateScope.USER),
            "chat_history": state.get("chat_history", [], StateScope.USER),
            "export_timestamp": datetime.now().isoformat(),
        }
        return json.dumps(user_data, default=str)
    except Exception as e:
        logger.error(f"Failed to export user data: {e}")
        return None


def import_user_data(user_id: str, data_json: str) -> bool:
    """Import user data from backup"""
    try:
        data = json.loads(data_json)
        state = get_state_manager()

        if data.get("user_id") != user_id:
            logger.warning("User ID mismatch in import data")
            return False

        state.set("user_preferences", data.get("preferences", {}), StateScope.USER)
        state.set(
            "assessment_progress", data.get("assessment_data", {}), StateScope.USER
        )
        state.set("chat_history", data.get("chat_history", []), StateScope.USER)

        logger.info(f"Successfully imported user data for {user_id}")
        return True
    except Exception as e:
        logger.error(f"Failed to import user data: {e}")
        return False
