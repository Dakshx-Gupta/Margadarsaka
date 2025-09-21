"""
Modern Header Component for Margadarsaka
A sophisticated header with branding, navigation, and user controls
"""

import streamlit as st
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

# Import local modules with fallbacks
try:
    from margadarsaka.ui.utils.i18n import get_text
    from margadarsaka.ui.utils.state_manager import get_state_manager
    IMPORTS_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Import error in header: {e}")
    IMPORTS_AVAILABLE = False
    
    def get_text(key: str, default: str = "", **kwargs) -> str:
        return default or key
    
    class MockStateManager:
        def get(self, key: str, default: Any = None):
            return default
        def set(self, key: str, value: Any):
            pass
    
    def get_state_manager():
        return MockStateManager()


def render_modern_header(
    show_auth: bool = True,
    show_search: bool = True,
    show_language: bool = True,
    user_info: Optional[Dict[str, Any]] = None
) -> None:
    """
    Render a modern, responsive header with branding and navigation
    
    Args:
        show_auth: Whether to show authentication buttons
        show_search: Whether to show search functionality
        show_language: Whether to show language selector
        user_info: User information if authenticated
    """
    
    # Header CSS styling
    st.markdown("""
    <style>
    .modern-header {
        background: linear-gradient(135deg, rgba(30, 136, 229, 0.1) 0%, rgba(142, 36, 170, 0.1) 100%);
        backdrop-filter: blur(10px);
        border-bottom: 1px solid rgba(224, 224, 224, 0.3);
        padding: 0.75rem 0;
        margin: -1rem -1rem 2rem -1rem;
        position: sticky;
        top: 0;
        z-index: 1000;
        box-shadow: 0 2px 20px rgba(0,0,0,0.1);
    }
    
    .header-container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 1rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 1rem;
    }
    
    .header-brand {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        text-decoration: none;
        color: inherit;
    }
    
    .header-brand h1 {
        margin: 0;
        font-size: 1.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #1E88E5 0%, #8E24AA 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .header-brand .tagline {
        font-size: 0.75rem;
        color: #546E7A;
        margin: 0;
        font-weight: 400;
    }
    
    .header-nav {
        display: flex;
        align-items: center;
        gap: 1.5rem;
        flex: 1;
        justify-content: center;
    }
    
    .header-nav a {
        color: #263238;
        text-decoration: none;
        font-weight: 500;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        transition: all 0.2s ease;
        position: relative;
    }
    
    .header-nav a:hover {
        background: rgba(30, 136, 229, 0.1);
        color: #1E88E5;
        transform: translateY(-1px);
    }
    
    .header-actions {
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    .search-container {
        position: relative;
        display: flex;
        align-items: center;
    }
    
    .search-input {
        border: 1px solid rgba(224, 224, 224, 0.5);
        border-radius: 20px;
        padding: 0.5rem 1rem 0.5rem 2.5rem;
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(5px);
        font-size: 0.875rem;
        width: 200px;
        transition: all 0.2s ease;
    }
    
    .search-input:focus {
        outline: none;
        border-color: #1E88E5;
        box-shadow: 0 0 0 3px rgba(30, 136, 229, 0.1);
        width: 250px;
    }
    
    .search-icon {
        position: absolute;
        left: 0.75rem;
        color: #78909C;
        font-size: 0.875rem;
    }
    
    .user-avatar {
        width: 32px;
        height: 32px;
        border-radius: 50%;
        background: linear-gradient(135deg, #1E88E5 0%, #8E24AA 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: 600;
        font-size: 0.875rem;
        cursor: pointer;
        transition: all 0.2s ease;
    }
    
    .user-avatar:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 12px rgba(30, 136, 229, 0.3);
    }
    
    .lang-selector {
        background: rgba(255, 255, 255, 0.8);
        border: 1px solid rgba(224, 224, 224, 0.5);
        border-radius: 6px;
        padding: 0.25rem 0.5rem;
        font-size: 0.75rem;
        color: #546E7A;
        cursor: pointer;
        transition: all 0.2s ease;
    }
    
    .lang-selector:hover {
        background: rgba(30, 136, 229, 0.1);
        border-color: #1E88E5;
    }
    
    .auth-buttons {
        display: flex;
        gap: 0.5rem;
    }
    
    .btn-outline {
        background: transparent;
        border: 1px solid #1E88E5;
        color: #1E88E5;
        padding: 0.5rem 1rem;
        border-radius: 6px;
        font-size: 0.875rem;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.2s ease;
        text-decoration: none;
        display: inline-block;
    }
    
    .btn-outline:hover {
        background: #1E88E5;
        color: white;
        transform: translateY(-1px);
    }
    
    .btn-primary {
        background: linear-gradient(135deg, #1E88E5 0%, #8E24AA 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 6px;
        font-size: 0.875rem;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.2s ease;
        border: none;
        text-decoration: none;
        display: inline-block;
    }
    
    .btn-primary:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(30, 136, 229, 0.3);
    }
    
    @media (max-width: 768px) {
        .header-nav {
            display: none;
        }
        
        .search-input {
            width: 150px;
        }
        
        .search-input:focus {
            width: 180px;
        }
        
        .header-brand h1 {
            font-size: 1.25rem;
        }
        
        .header-actions {
            gap: 0.5rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header structure
    header_html = f"""
    <div class="modern-header">
        <div class="header-container">
            <!-- Brand Section -->
            <div class="header-brand">
                <div>
                    <h1>🚀 {get_text('app_name', 'Margadarsaka')}</h1>
                    <p class="tagline">{get_text('tagline', 'AI Career Advisor')}</p>
                </div>
            </div>
            
            <!-- Navigation -->
            <nav class="header-nav">
                <a href="#home">{get_text('nav_home', 'Home')}</a>
                <a href="#assessment">{get_text('nav_assessment', 'Assessment')}</a>
                <a href="#chat">{get_text('nav_chat', 'AI Chat')}</a>
                <a href="#resume">{get_text('nav_resume', 'Resume')}</a>
                <a href="#resources">{get_text('nav_resources', 'Resources')}</a>
            </nav>
            
            <!-- Actions Section -->
            <div class="header-actions">
    """
    
    # Add search if enabled
    if show_search:
        header_html += f"""
                <div class="search-container">
                    <span class="search-icon">🔍</span>
                    <input 
                        type="text" 
                        class="search-input" 
                        placeholder="{get_text('search_placeholder', 'Search careers, skills...')}"
                        id="header-search"
                    />
                </div>
        """
    
    # Add language selector if enabled
    if show_language:
        header_html += f"""
                <div class="lang-selector" title="{get_text('change_language', 'Change Language')}">
                    🌐 EN
                </div>
        """
    
    # Add user info or auth buttons
    if user_info:
        # User is logged in
        user_name = user_info.get('name', 'User')
        user_initials = ''.join([name[0].upper() for name in user_name.split()[:2]])
        header_html += f"""
                <div class="user-avatar" title="{user_name}">
                    {user_initials}
                </div>
        """
    elif show_auth:
        # Show auth buttons
        header_html += f"""
                <div class="auth-buttons">
                    <a href="#login" class="btn-outline">{get_text('sign_in', 'Sign In')}</a>
                    <a href="#signup" class="btn-primary">{get_text('get_started', 'Get Started')}</a>
                </div>
        """
    
    header_html += """
            </div>
        </div>
    </div>
    """
    
    # Render the header
    st.markdown(header_html, unsafe_allow_html=True)
    
    # Add interactive functionality with JavaScript
    st.markdown("""
    <script>
    // Search functionality
    const searchInput = document.getElementById('header-search');
    if (searchInput) {
        searchInput.addEventListener('input', function(e) {
            const query = e.target.value;
            if (query.length > 2) {
                // Trigger search functionality
                console.log('Searching for:', query);
                // TODO: Implement actual search
            }
        });
        
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                // Trigger search
                const query = e.target.value;
                if (query.trim()) {
                    console.log('Search submitted:', query);
                    // TODO: Navigate to search results
                }
            }
        });
    }
    
    // Smooth scroll for navigation links
    document.querySelectorAll('.header-nav a').forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const target = this.getAttribute('href').substring(1);
            const element = document.getElementById(target);
            if (element) {
                element.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });
    </script>
    """, unsafe_allow_html=True)


def render_breadcrumb(pages: list) -> None:
    """
    Render a breadcrumb navigation below the header
    
    Args:
        pages: List of page names/titles for breadcrumb
    """
    if not pages:
        return
        
    st.markdown("""
    <style>
    .breadcrumb {
        background: rgba(248, 249, 250, 0.8);
        padding: 0.5rem 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        font-size: 0.875rem;
        color: #546E7A;
    }
    
    .breadcrumb a {
        color: #1E88E5;
        text-decoration: none;
    }
    
    .breadcrumb a:hover {
        text-decoration: underline;
    }
    
    .breadcrumb-separator {
        margin: 0 0.5rem;
        color: #78909C;
    }
    </style>
    """, unsafe_allow_html=True)
    
    breadcrumb_html = '<div class="breadcrumb">'
    for i, page in enumerate(pages):
        if i > 0:
            breadcrumb_html += '<span class="breadcrumb-separator">›</span>'
        
        if i == len(pages) - 1:
            # Current page (not clickable)
            breadcrumb_html += f'<span>{page}</span>'
        else:
            # Previous pages (clickable)
            breadcrumb_html += f'<a href="#">{page}</a>'
    
    breadcrumb_html += '</div>'
    st.markdown(breadcrumb_html, unsafe_allow_html=True)