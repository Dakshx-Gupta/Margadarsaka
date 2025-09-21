"""
Simple Streamlit-Compatible Header Component
Replaces complex HTML header with Streamlit-native components
"""

import streamlit as st
from typing import Optional, Dict, Any

def render_simple_header(
    show_auth: bool = True,
    user_info: Optional[Dict[str, Any]] = None
) -> None:
    """
    Render a simple header using Streamlit components
    
    Args:
        show_auth: Whether to show authentication buttons
        user_info: User information if authenticated
    """
    
    # Create header layout with columns
    col1, col2, col3 = st.columns([2, 3, 2])
    
    with col1:
        st.markdown("# 🚀 Margadarsaka")
        st.caption("AI Career Advisor")
    
    with col2:
        # Navigation using selectbox in the center
        nav_options = ["Home", "Assessment", "AI Chat", "Resume", "Resources"]
        selected_nav = st.selectbox(
            "Navigate to:",
            nav_options,
            key="header_nav",
            label_visibility="collapsed"
        )
        
        # Update session state based on selection
        if selected_nav != st.session_state.get("current_nav", "Home"):
            st.session_state.current_nav = selected_nav
            if selected_nav == "Assessment":
                st.session_state.current_page = "assessment"
            elif selected_nav == "AI Chat":
                st.session_state.current_page = "chat"
            elif selected_nav == "Resume":
                st.session_state.current_page = "resume"
            elif selected_nav == "Resources":
                st.session_state.current_page = "resources"
            else:
                st.session_state.current_page = "home"
            st.rerun()
    
    with col3:
        if user_info:
            # User is logged in
            user_name = user_info.get('name', 'User')
            st.write(f"👤 Welcome, {user_name}!")
        elif show_auth:
            # Show auth buttons
            col_signin, col_signup = st.columns(2)
            with col_signin:
                if st.button("Sign In", type="secondary", use_container_width=True):
                    st.session_state.show_auth = True
            with col_signup:
                if st.button("Get Started", type="primary", use_container_width=True):
                    st.session_state.show_auth = True
    
    # Add some spacing
    st.markdown("---")


def render_sidebar_rating():
    """Render rating component in sidebar"""
    with st.sidebar:
        st.markdown("### Rate Your Experience")
        
        # Simple rating using radio buttons
        rating = st.radio(
            "How would you rate our service?",
            options=[1, 2, 3, 4, 5],
            format_func=lambda x: "⭐" * x,
            key="user_rating",
            horizontal=True
        )
        
        if rating:
            st.success(f"Thank you for rating us {rating} stars!")
            
        # Feedback text area
        feedback = st.text_area(
            "Any feedback or suggestions?",
            placeholder="Tell us how we can improve...",
            key="user_feedback"
        )
        
        if feedback:
            if st.button("Submit Feedback", type="primary"):
                st.success("Thank you for your feedback!")
                # Here you would normally save the feedback to a database