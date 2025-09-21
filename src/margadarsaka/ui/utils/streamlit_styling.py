"""
Streamlit-Compatible Styling System
Simplified styling that works well with Streamlit's native theming and components.
"""

import streamlit as st
from typing import Optional


def apply_streamlit_theme():
    """Apply custom CSS that's compatible with Streamlit's theming system"""
    
    css = """
    <style>
    /* Streamlit-compatible color variables */
    :root {
        --primary-color: #1f88e5;
        --secondary-color: #42a5f5;
        --success-color: #4caf50;
        --warning-color: #ff9800;
        --error-color: #f44336;
        --info-color: #2196f3;
        
        /* Neutral colors that work with both light and dark themes */
        --text-primary: var(--text-color);
        --text-secondary: rgba(49, 51, 63, 0.6);
        --border-color: rgba(49, 51, 63, 0.2);
        --surface-color: rgba(255, 255, 255, 0.05);
        
        /* Spacing */
        --spacing-xs: 0.25rem;
        --spacing-sm: 0.5rem;
        --spacing-md: 1rem;
        --spacing-lg: 1.5rem;
        --spacing-xl: 2rem;
        
        /* Border radius */
        --border-radius: 0.5rem;
        --border-radius-sm: 0.25rem;
        --border-radius-lg: 0.75rem;
        
        /* Shadows */
        --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        
        /* Transitions */
        --transition: all 0.2s ease;
    }
    
    /* Hide Streamlit UI elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Improve default Streamlit styling */
    .stApp {
        background-color: var(--background-color);
    }
    
    /* Better text contrast */
    .stMarkdown, .stText {
        color: var(--text-color) !important;
    }
    
    /* Improved buttons */
    .stButton > button {
        background-color: var(--primary-color);
        color: white;
        border: none;
        border-radius: var(--border-radius);
        padding: 0.5rem 1rem;
        font-weight: 500;
        transition: var(--transition);
        min-height: 2.5rem;
    }
    
    .stButton > button:hover {
        background-color: var(--secondary-color);
        transform: translateY(-1px);
        box-shadow: var(--shadow-md);
    }
    
    /* Improved cards */
    .element-container {
        margin-bottom: var(--spacing-md);
    }
    
    /* Better form elements */
    .stTextInput input,
    .stTextArea textarea,
    .stSelectbox select {
        border-radius: var(--border-radius);
        border: 1px solid var(--border-color);
        padding: 0.5rem;
        transition: var(--transition);
    }
    
    .stTextInput input:focus,
    .stTextArea textarea:focus,
    .stSelectbox select:focus {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 2px rgba(31, 136, 229, 0.2);
    }
    
    /* Improved containers */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    
    /* Success/Warning/Error styling */
    .stAlert {
        border-radius: var(--border-radius);
        margin: var(--spacing-sm) 0;
    }
    
    /* Sidebar improvements */
    .css-1d391kg {
        background-color: var(--surface-color);
    }
    
    /* Metrics styling */
    .metric-container {
        background: var(--surface-color);
        padding: var(--spacing-md);
        border-radius: var(--border-radius);
        border: 1px solid var(--border-color);
        text-align: center;
        transition: var(--transition);
    }
    
    .metric-container:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-md);
    }
    
    /* Custom classes for enhanced components */
    .custom-card {
        background: var(--surface-color);
        padding: var(--spacing-lg);
        border-radius: var(--border-radius);
        border: 1px solid var(--border-color);
        margin: var(--spacing-md) 0;
        box-shadow: var(--shadow-sm);
        transition: var(--transition);
    }
    
    .custom-card:hover {
        box-shadow: var(--shadow-md);
        transform: translateY(-1px);
    }
    
    .feature-highlight {
        border-left: 4px solid var(--primary-color);
        background: linear-gradient(90deg, rgba(31, 136, 229, 0.1) 0%, transparent 100%);
    }
    
    .success-highlight {
        border-left: 4px solid var(--success-color);
        background: linear-gradient(90deg, rgba(76, 175, 80, 0.1) 0%, transparent 100%);
    }
    
    .warning-highlight {
        border-left: 4px solid var(--warning-color);
        background: linear-gradient(90deg, rgba(255, 152, 0, 0.1) 0%, transparent 100%);
    }
    
    .error-highlight {
        border-left: 4px solid var(--error-color);
        background: linear-gradient(90deg, rgba(244, 67, 54, 0.1) 0%, transparent 100%);
    }
    
    /* Typography improvements */
    h1, h2, h3, h4, h5, h6 {
        color: var(--text-color) !important;
        font-weight: 600;
        margin-bottom: var(--spacing-sm);
    }
    
    h1 {
        font-size: 2.5rem;
        background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    h2 {
        font-size: 2rem;
        color: var(--primary-color) !important;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }
        
        h1 {
            font-size: 2rem;
        }
        
        h2 {
            font-size: 1.5rem;
        }
        
        .custom-card {
            padding: var(--spacing-md);
        }
    }
    
    /* Loading animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .fade-in {
        animation: fadeIn 0.3s ease-out;
    }
    
    /* High contrast mode support */
    @media (prefers-contrast: high) {
        :root {
            --border-color: #000;
            --text-secondary: var(--text-color);
        }
        
        .stButton > button {
            border: 2px solid #000;
        }
    }
    
    /* Reduced motion support */
    @media (prefers-reduced-motion: reduce) {
        * {
            animation-duration: 0.01ms !important;
            animation-iteration-count: 1 !important;
            transition-duration: 0.01ms !important;
        }
        
        .stButton > button:hover {
            transform: none;
        }
        
        .custom-card:hover {
            transform: none;
        }
    }
    </style>
    """
    
    st.markdown(css, unsafe_allow_html=True)


def create_card(title: str, content: str, card_type: str = "default") -> None:
    """Create a simple, accessible card using Streamlit components"""
    
    # Map card types to CSS classes
    highlight_classes = {
        "feature": "feature-highlight",
        "success": "success-highlight", 
        "warning": "warning-highlight",
        "error": "error-highlight",
        "default": ""
    }
    
    css_class = f"custom-card {highlight_classes.get(card_type, '')}"
    
    with st.container():
        st.markdown(f'<div class="{css_class}">', unsafe_allow_html=True)
        if title:
            st.subheader(title)
        st.markdown(content)
        st.markdown('</div>', unsafe_allow_html=True)


def create_metric_card(title: str, value: str, delta: Optional[str] = None) -> None:
    """Create a metric card using Streamlit's built-in metric component"""
    
    with st.container():
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.metric(label=title, value=value, delta=delta)
        st.markdown('</div>', unsafe_allow_html=True)


def create_hero_section(title: str, subtitle: str, description: str) -> None:
    """Create a hero section with proper typography"""
    
    with st.container():
        st.markdown(f'<div class="fade-in">', unsafe_allow_html=True)
        st.markdown(f"# {title}")
        if subtitle:
            st.markdown(f"## {subtitle}")
        if description:
            st.markdown(description)
        st.markdown('</div>', unsafe_allow_html=True)


def show_success_message(message: str) -> None:
    """Show a success message with proper styling"""
    st.success(message)


def show_warning_message(message: str) -> None:
    """Show a warning message with proper styling"""
    st.warning(message)


def show_error_message(message: str) -> None:
    """Show an error message with proper styling"""
    st.error(message)


def show_info_message(message: str) -> None:
    """Show an info message with proper styling"""
    st.info(message)


def create_button(label: str, key: Optional[str] = None, button_type: str = "primary") -> bool:
    """Create a styled button"""
    return st.button(label, key=key)


def create_columns(ratios: list = None) -> list:
    """Create responsive columns"""
    if ratios:
        return st.columns(ratios)
    else:
        return st.columns(2)


def apply_fade_in_animation():
    """Apply fade-in animation to the current container"""
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)


def close_animation():
    """Close the animation container"""
    st.markdown('</div>', unsafe_allow_html=True)