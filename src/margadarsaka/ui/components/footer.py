"""
Modern Footer Component for Margadarsaka
A comprehensive footer with links, social media, and utilities
"""

import streamlit as st
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

# Import local modules with fallbacks
try:
    from margadarsaka.ui.utils.i18n import get_text
    from margadarsaka.ui.utils.state_manager import get_state_manager
    IMPORTS_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Import error in footer: {e}")
    IMPORTS_AVAILABLE = False
    
    def get_text(key: str, default: str = "", **kwargs) -> str:
        return default or key
    
    class MockStateManager:
        def get(self, key: str, default=None):
            return default
        def set(self, key: str, value):
            pass
    
    def get_state_manager():
        return MockStateManager()


def render_modern_footer(
    show_social: bool = True,
    show_newsletter: bool = True,
    show_theme_toggle: bool = True,
    custom_links: Optional[Dict[str, List[Dict[str, str]]]] = None
) -> None:
    """
    Render a modern, comprehensive footer
    
    Args:
        show_social: Whether to show social media links
        show_newsletter: Whether to show newsletter signup
        show_theme_toggle: Whether to show dark/light mode toggle
        custom_links: Custom footer links organized by section
    """
    
    # Default footer links
    default_links = {
        "Product": [
            {"name": "Features", "url": "#features"},
            {"name": "Assessments", "url": "#assessments"},
            {"name": "AI Chat", "url": "#chat"},
            {"name": "Resume Builder", "url": "#resume"},
            {"name": "Pricing", "url": "#pricing"}
        ],
        "Resources": [
            {"name": "Career Guide", "url": "#guide"},
            {"name": "Skill Library", "url": "#skills"},
            {"name": "Industry Insights", "url": "#insights"},
            {"name": "Blog", "url": "#blog"},
            {"name": "Success Stories", "url": "#stories"}
        ],
        "Company": [
            {"name": "About Us", "url": "#about"},
            {"name": "Careers", "url": "#careers"},
            {"name": "Contact", "url": "#contact"},
            {"name": "Privacy Policy", "url": "#privacy"},
            {"name": "Terms of Service", "url": "#terms"}
        ],
        "Support": [
            {"name": "Help Center", "url": "#help"},
            {"name": "Documentation", "url": "#docs"},
            {"name": "API Reference", "url": "#api"},
            {"name": "Community", "url": "#community"},
            {"name": "Status", "url": "#status"}
        ]
    }
    
    footer_links = custom_links or default_links
    
    # Footer CSS styling
    st.markdown("""
    <style>
    .modern-footer {
        background: linear-gradient(135deg, #263238 0%, #37474F 100%);
        color: #ECEFF1;
        margin: 4rem -1rem -1rem -1rem;
        padding: 3rem 0 1rem 0;
        position: relative;
        overflow: hidden;
    }
    
    .modern-footer::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent 0%, rgba(30, 136, 229, 0.5) 50%, transparent 100%);
    }
    
    .footer-container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 1rem;
    }
    
    .footer-main {
        display: grid;
        grid-template-columns: 2fr 1fr 1fr 1fr 1fr;
        gap: 2rem;
        margin-bottom: 2rem;
    }
    
    .footer-brand {
        padding-right: 2rem;
    }
    
    .footer-brand h2 {
        margin: 0 0 1rem 0;
        font-size: 1.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #64B5F6 0%, #BA68C8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .footer-brand p {
        color: #B0BEC5;
        line-height: 1.6;
        margin-bottom: 1.5rem;
        font-size: 0.9rem;
    }
    
    .social-links {
        display: flex;
        gap: 0.75rem;
        margin-bottom: 1.5rem;
    }
    
    .social-link {
        width: 40px;
        height: 40px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #B0BEC5;
        text-decoration: none;
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
    }
    
    .social-link:hover {
        background: linear-gradient(135deg, #1E88E5 0%, #8E24AA 100%);
        color: white;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(30, 136, 229, 0.3);
    }
    
    .footer-section h3 {
        color: #ECEFF1;
        font-size: 1rem;
        font-weight: 600;
        margin: 0 0 1rem 0;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .footer-links {
        list-style: none;
        padding: 0;
        margin: 0;
    }
    
    .footer-links li {
        margin-bottom: 0.5rem;
    }
    
    .footer-links a {
        color: #B0BEC5;
        text-decoration: none;
        font-size: 0.9rem;
        transition: all 0.2s ease;
        display: inline-block;
    }
    
    .footer-links a:hover {
        color: #64B5F6;
        transform: translateX(4px);
    }
    
    .newsletter-signup {
        background: rgba(255, 255, 255, 0.05);
        padding: 1.5rem;
        border-radius: 12px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .newsletter-signup h4 {
        color: #ECEFF1;
        margin: 0 0 0.5rem 0;
        font-size: 1rem;
        font-weight: 600;
    }
    
    .newsletter-signup p {
        color: #B0BEC5;
        font-size: 0.85rem;
        margin-bottom: 1rem;
        line-height: 1.4;
    }
    
    .newsletter-form {
        display: flex;
        gap: 0.5rem;
    }
    
    .newsletter-input {
        flex: 1;
        padding: 0.75rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 8px;
        background: rgba(255, 255, 255, 0.1);
        color: #ECEFF1;
        font-size: 0.875rem;
        backdrop-filter: blur(5px);
    }
    
    .newsletter-input::placeholder {
        color: #78909C;
    }
    
    .newsletter-input:focus {
        outline: none;
        border-color: #1E88E5;
        box-shadow: 0 0 0 3px rgba(30, 136, 229, 0.2);
    }
    
    .newsletter-btn {
        background: linear-gradient(135deg, #1E88E5 0%, #8E24AA 100%);
        color: white;
        border: none;
        padding: 0.75rem 1rem;
        border-radius: 8px;
        font-size: 0.875rem;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.2s ease;
        white-space: nowrap;
    }
    
    .newsletter-btn:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(30, 136, 229, 0.3);
    }
    
    .footer-bottom {
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        padding-top: 1.5rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 1rem;
    }
    
    .footer-bottom p {
        color: #78909C;
        font-size: 0.85rem;
        margin: 0;
    }
    
    .footer-utilities {
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    .theme-toggle {
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 20px;
        padding: 0.5rem 1rem;
        color: #B0BEC5;
        font-size: 0.85rem;
        cursor: pointer;
        transition: all 0.2s ease;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .theme-toggle:hover {
        background: rgba(255, 255, 255, 0.15);
        border-color: #1E88E5;
    }
    
    .lang-toggle {
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 6px;
        padding: 0.5rem 0.75rem;
        color: #B0BEC5;
        font-size: 0.85rem;
        cursor: pointer;
        transition: all 0.2s ease;
    }
    
    .lang-toggle:hover {
        background: rgba(255, 255, 255, 0.15);
        border-color: #1E88E5;
    }
    
    @media (max-width: 768px) {
        .footer-main {
            grid-template-columns: 1fr;
            gap: 2rem;
        }
        
        .footer-brand {
            padding-right: 0;
            text-align: center;
        }
        
        .footer-bottom {
            flex-direction: column;
            text-align: center;
        }
        
        .newsletter-form {
            flex-direction: column;
        }
        
        .social-links {
            justify-content: center;
        }
    }
    
    @media (max-width: 1024px) and (min-width: 769px) {
        .footer-main {
            grid-template-columns: 2fr 1fr 1fr 1fr;
        }
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Generate footer HTML
    footer_html = f"""
    <footer class="modern-footer">
        <div class="footer-container">
            <div class="footer-main">
                <!-- Brand Section -->
                <div class="footer-brand">
                    <h2>🚀 {get_text('app_name', 'Margadarsaka')}</h2>
                    <p>{get_text('footer_description', 'Empowering careers through AI-driven insights, personalized guidance, and comprehensive skill development.')}</p>
    """
    
    # Add social links if enabled
    if show_social:
        footer_html += f"""
                    <div class="social-links">
                        <a href="#" class="social-link" title="LinkedIn">
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                                <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
                            </svg>
                        </a>
                        <a href="#" class="social-link" title="Twitter">
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                                <path d="M23.953 4.57a10 10 0 01-2.825.775 4.958 4.958 0 002.163-2.723c-.951.555-2.005.959-3.127 1.184a4.92 4.92 0 00-8.384 4.482C7.69 8.095 4.067 6.13 1.64 3.162a4.822 4.822 0 00-.666 2.475c0 1.71.87 3.213 2.188 4.096a4.904 4.904 0 01-2.228-.616v.06a4.923 4.923 0 003.946 4.827 4.996 4.996 0 01-2.212.085 4.936 4.936 0 004.604 3.417 9.867 9.867 0 01-6.102 2.105c-.39 0-.779-.023-1.17-.067a13.995 13.995 0 007.557 2.209c9.053 0 13.998-7.496 13.998-13.985 0-.21 0-.42-.015-.63A9.935 9.935 0 0024 4.59z"/>
                            </svg>
                        </a>
                        <a href="#" class="social-link" title="YouTube">
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                                <path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/>
                            </svg>
                        </a>
                        <a href="#" class="social-link" title="GitHub">
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                                <path d="M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12"/>
                            </svg>
                        </a>
                    </div>
        """
    
    # Add newsletter if enabled
    if show_newsletter:
        footer_html += f"""
                    <div class="newsletter-signup">
                        <h4>{get_text('newsletter_title', 'Stay Updated')}</h4>
                        <p>{get_text('newsletter_description', 'Get career insights and tips delivered to your inbox.')}</p>
                        <div class="newsletter-form">
                            <input 
                                type="email" 
                                class="newsletter-input" 
                                placeholder="{get_text('email_placeholder', 'Enter your email')}"
                                id="newsletter-email"
                            />
                            <button class="newsletter-btn" onclick="subscribeNewsletter()">
                                {get_text('subscribe', 'Subscribe')}
                            </button>
                        </div>
                    </div>
        """
    
    footer_html += """
                </div>
    """
    
    # Add footer link sections
    for section_name, links in footer_links.items():
        footer_html += f"""
                <div class="footer-section">
                    <h3>{get_text(f'footer_section_{section_name.lower()}', section_name)}</h3>
                    <ul class="footer-links">
        """
        
        for link in links:
            footer_html += f"""
                        <li><a href="{link['url']}">{get_text(f'footer_link_{link["name"].lower().replace(" ", "_")}', link['name'])}</a></li>
            """
        
        footer_html += """
                    </ul>
                </div>
        """
    
    # Footer bottom section
    footer_html += f"""
            </div>
            
            <div class="footer-bottom">
                <p>&copy; 2024 {get_text('app_name', 'Margadarsaka')}. {get_text('rights_reserved', 'All rights reserved.')}</p>
                
                <div class="footer-utilities">
    """
    
    # Add theme toggle if enabled
    if show_theme_toggle:
        footer_html += f"""
                    <button class="theme-toggle" onclick="toggleTheme()">
                        <span id="theme-icon">🌙</span>
                        <span id="theme-text">{get_text('dark_mode', 'Dark Mode')}</span>
                    </button>
        """
    
    # Add language toggle
    footer_html += f"""
                    <button class="lang-toggle" onclick="toggleLanguage()">
                        🌐 {get_text('language_code', 'EN')}
                    </button>
                </div>
            </div>
        </div>
    </footer>
    """
    
    # Render the footer
    st.markdown(footer_html, unsafe_allow_html=True)
    
    # Add JavaScript functionality
    st.markdown("""
    <script>
    // Newsletter subscription
    function subscribeNewsletter() {
        const email = document.getElementById('newsletter-email');
        if (email && email.value) {
            if (validateEmail(email.value)) {
                // TODO: Implement actual newsletter subscription
                alert('Thank you for subscribing! We\\'ll send you our latest career insights.');
                email.value = '';
            } else {
                alert('Please enter a valid email address.');
            }
        }
    }
    
    // Email validation
    function validateEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    }
    
    // Theme toggle functionality
    function toggleTheme() {
        const currentTheme = localStorage.getItem('theme') || 'light';
        const newTheme = currentTheme === 'light' ? 'dark' : 'light';
        
        localStorage.setItem('theme', newTheme);
        
        // Update icon and text
        const icon = document.getElementById('theme-icon');
        const text = document.getElementById('theme-text');
        
        if (newTheme === 'dark') {
            if (icon) icon.textContent = '☀️';
            if (text) text.textContent = 'Light Mode';
        } else {
            if (icon) icon.textContent = '🌙';
            if (text) text.textContent = 'Dark Mode';
        }
        
        // Apply theme (this would be handled by your theme system)
        document.body.setAttribute('data-theme', newTheme);
    }
    
    // Language toggle functionality
    function toggleLanguage() {
        // TODO: Implement language switching
        console.log('Language toggle clicked');
    }
    
    // Initialize theme on load
    document.addEventListener('DOMContentLoaded', function() {
        const savedTheme = localStorage.getItem('theme') || 'light';
        document.body.setAttribute('data-theme', savedTheme);
        
        const icon = document.getElementById('theme-icon');
        const text = document.getElementById('theme-text');
        
        if (savedTheme === 'dark') {
            if (icon) icon.textContent = '☀️';
            if (text) text.textContent = 'Light Mode';
        }
    });
    
    // Enter key support for newsletter
    document.addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && e.target.id === 'newsletter-email') {
            subscribeNewsletter();
        }
    });
    </script>
    """, unsafe_allow_html=True)


def render_mini_footer() -> None:
    """
    Render a minimal footer for pages that need less visual weight
    """
    st.markdown("""
    <style>
    .mini-footer {
        text-align: center;
        padding: 1rem 0;
        margin-top: 2rem;
        border-top: 1px solid rgba(224, 224, 224, 0.3);
        color: #78909C;
        font-size: 0.85rem;
    }
    
    .mini-footer a {
        color: #1E88E5;
        text-decoration: none;
        margin: 0 0.5rem;
    }
    
    .mini-footer a:hover {
        text-decoration: underline;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="mini-footer">
        <p>&copy; 2024 {get_text('app_name', 'Margadarsaka')} | 
        <a href="#privacy">{get_text('privacy', 'Privacy')}</a> |
        <a href="#terms">{get_text('terms', 'Terms')}</a> |
        <a href="#support">{get_text('support', 'Support')}</a>
        </p>
    </div>
    """, unsafe_allow_html=True)