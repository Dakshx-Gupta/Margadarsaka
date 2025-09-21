"""
Modern CSS Styling for Margadarsaka UI
Provides consistent theming, responsive design, and beautiful components
"""

import streamlit as st
from typing import Dict, Any

# Modern Design System - Enhanced color palette and design tokens
DESIGN_TOKENS = {
    # Primary Color System - Professional blue to purple gradient
    "primary": {
        "50": "#E3F2FD",   # Lightest blue
        "100": "#BBDEFB",  # Light blue
        "200": "#90CAF9",  # Medium-light blue
        "300": "#64B5F6",  # Medium blue
        "400": "#42A5F5",  # Medium-dark blue
        "500": "#1E88E5",  # Primary blue
        "600": "#1976D2",  # Dark blue
        "700": "#1565C0",  # Darker blue
        "800": "#0D47A1",  # Very dark blue
        "900": "#0A3A85",  # Darkest blue
    },
    
    # Secondary Color System - Rich purple gradients
    "secondary": {
        "50": "#F3E5F5",   # Lightest purple
        "100": "#E1BEE7",  # Light purple
        "200": "#CE93D8",  # Medium-light purple
        "300": "#BA68C8",  # Medium purple
        "400": "#AB47BC",  # Medium-dark purple
        "500": "#8E24AA",  # Primary purple
        "600": "#8E24AA",  # Same as primary
        "700": "#7B1FA2",  # Dark purple
        "800": "#6A1B9A",  # Darker purple
        "900": "#4A148C",  # Darkest purple
    },
    
    # Neutral/Gray System - Balanced grays for text and backgrounds
    "neutral": {
        "0": "#FFFFFF",    # Pure white
        "50": "#FAFBFC",   # Almost white
        "100": "#F4F6F8",  # Very light gray
        "200": "#E4E7EB",  # Light gray
        "300": "#D1D5DB",  # Medium-light gray
        "400": "#9CA3AF",  # Medium gray
        "500": "#6B7280",  # Balanced gray
        "600": "#4B5563",  # Medium-dark gray
        "700": "#374151",  # Dark gray
        "800": "#1F2937",  # Very dark gray
        "900": "#111827",  # Almost black
    },
    
    # Semantic Colors - Status and feedback colors
    "semantic": {
        "success": {
            "light": "#D4F4DD",
            "main": "#2E7D32",
            "dark": "#1B5E20",
        },
        "warning": {
            "light": "#FFF3CD",
            "main": "#F57F17",
            "dark": "#E65100",
        },
        "error": {
            "light": "#FFEBEE",
            "main": "#D32F2F",
            "dark": "#B71C1C",
        },
        "info": {
            "light": "#E1F5FE",
            "main": "#0288D1",
            "dark": "#01579B",
        },
    },
    
    # Accent Colors - For highlights and special elements
    "accent": {
        "orange": "#FF8F00",
        "teal": "#00ACC1",
        "pink": "#E91E63",
        "green": "#4CAF50",
        "indigo": "#3F51B5",
    },
    
    # Typography Scale - Modern type scale
    "typography": {
        "font_family_primary": "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
        "font_family_heading": "'Poppins', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
        "font_family_mono": "'JetBrains Mono', 'SF Mono', Consolas, monospace",
        
        "font_size": {
            "xs": "0.75rem",    # 12px
            "sm": "0.875rem",   # 14px
            "base": "1rem",     # 16px
            "lg": "1.125rem",   # 18px
            "xl": "1.25rem",    # 20px
            "2xl": "1.5rem",    # 24px
            "3xl": "1.875rem",  # 30px
            "4xl": "2.25rem",   # 36px
            "5xl": "3rem",      # 48px
            "6xl": "3.75rem",   # 60px
        },
        
        "font_weight": {
            "light": "300",
            "normal": "400",
            "medium": "500",
            "semibold": "600",
            "bold": "700",
            "extrabold": "800",
        },
        
        "line_height": {
            "tight": "1.25",
            "snug": "1.375",
            "normal": "1.5",
            "relaxed": "1.625",
            "loose": "2",
        },
    },
    
    # Spacing Scale - Consistent spacing system
    "spacing": {
        "0": "0",
        "1": "0.25rem",   # 4px
        "2": "0.5rem",    # 8px
        "3": "0.75rem",   # 12px
        "4": "1rem",      # 16px
        "5": "1.25rem",   # 20px
        "6": "1.5rem",    # 24px
        "8": "2rem",      # 32px
        "10": "2.5rem",   # 40px
        "12": "3rem",     # 48px
        "16": "4rem",     # 64px
        "20": "5rem",     # 80px
        "24": "6rem",     # 96px
        "32": "8rem",     # 128px
    },
    
    # Border Radius System
    "border_radius": {
        "none": "0",
        "sm": "0.125rem",   # 2px
        "base": "0.25rem",  # 4px
        "md": "0.375rem",   # 6px
        "lg": "0.5rem",     # 8px
        "xl": "0.75rem",    # 12px
        "2xl": "1rem",      # 16px
        "3xl": "1.5rem",    # 24px
        "full": "9999px",   # Fully rounded
    },
    
    # Shadow System - Elevation and depth
    "shadows": {
        "xs": "0 1px 2px 0 rgba(0, 0, 0, 0.05)",
        "sm": "0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)",
        "base": "0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)",
        "md": "0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)",
        "lg": "0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)",
        "xl": "0 25px 50px -12px rgba(0, 0, 0, 0.25)",
        "2xl": "0 25px 50px -12px rgba(0, 0, 0, 0.25)",
        "inner": "inset 0 2px 4px 0 rgba(0, 0, 0, 0.06)",
    },
    
    # Gradients - Beautiful gradient combinations
    "gradients": {
        "primary": "linear-gradient(135deg, #1E88E5 0%, #8E24AA 100%)",
        "secondary": "linear-gradient(135deg, #8E24AA 0%, #E91E63 100%)",
        "accent": "linear-gradient(135deg, #FF8F00 0%, #F57F17 100%)",
        "success": "linear-gradient(135deg, #4CAF50 0%, #2E7D32 100%)",
        "info": "linear-gradient(135deg, #0288D1 0%, #01579B 100%)",
        "warm": "linear-gradient(135deg, #FF8F00 0%, #E91E63 100%)",
        "cool": "linear-gradient(135deg, #00ACC1 0%, #1E88E5 100%)",
        "neutral": "linear-gradient(135deg, #6B7280 0%, #374151 100%)",
        "glass": "linear-gradient(135deg, rgba(255, 255, 255, 0.25) 0%, rgba(255, 255, 255, 0.1) 100%)",
    },
}

# Legacy color system for backward compatibility
THEME_COLORS = {
    "primary": DESIGN_TOKENS["primary"]["500"],
    "secondary": DESIGN_TOKENS["secondary"]["500"],
    "accent": DESIGN_TOKENS["accent"]["orange"],
    "success": DESIGN_TOKENS["semantic"]["success"]["main"],
    "warning": DESIGN_TOKENS["semantic"]["warning"]["main"],
    "error": DESIGN_TOKENS["semantic"]["error"]["main"],
    "info": DESIGN_TOKENS["semantic"]["info"]["main"],
    "light": DESIGN_TOKENS["neutral"]["100"],
    "dark": DESIGN_TOKENS["neutral"]["800"],
    "muted": DESIGN_TOKENS["neutral"]["500"],
    "background": DESIGN_TOKENS["neutral"]["0"],
    "surface": DESIGN_TOKENS["neutral"]["50"],
    "text_primary": DESIGN_TOKENS["neutral"]["900"],
    "text_secondary": DESIGN_TOKENS["neutral"]["600"],
    "border": DESIGN_TOKENS["neutral"]["200"],
    "shadow": "rgba(0,0,0,0.08)",
    "gradient_primary": DESIGN_TOKENS["gradients"]["primary"],
    "gradient_accent": DESIGN_TOKENS["gradients"]["accent"],
}


def get_theme_colors() -> Dict[str, str]:
    """Get the current theme color palette"""
    return THEME_COLORS.copy()


def get_design_tokens() -> Dict[str, Any]:
    """Get the complete design token system"""
    return DESIGN_TOKENS.copy()


def get_color(color_name: str, shade: str = "500") -> str:
    """
    Get a color from the design system
    
    Args:
        color_name: Name of the color (primary, secondary, neutral, etc.)
        shade: Shade number (50-900) or semantic name (light, main, dark)
    
    Returns:
        Color hex code or CSS value
    """
    tokens = DESIGN_TOKENS
    
    # Handle semantic colors
    if color_name in tokens["semantic"]:
        return tokens["semantic"][color_name].get(shade, tokens["semantic"][color_name]["main"])
    
    # Handle accent colors
    if color_name in tokens["accent"]:
        return tokens["accent"][color_name]
    
    # Handle gradients
    if color_name in tokens["gradients"]:
        return tokens["gradients"][color_name]
    
    # Handle primary/secondary/neutral colors with shades
    if color_name in tokens and isinstance(tokens[color_name], dict):
        return tokens[color_name].get(shade, tokens[color_name].get("500", "#000000"))
    
    # Fallback to legacy colors
    return THEME_COLORS.get(color_name, "#000000")


def get_spacing(size: str) -> str:
    """Get spacing value from design tokens"""
    return DESIGN_TOKENS["spacing"].get(size, "1rem")


def get_typography(property_name: str, value: str) -> str:
    """Get typography value from design tokens"""
    return DESIGN_TOKENS["typography"].get(property_name, {}).get(value, "")


def get_shadow(level: str) -> str:
    """Get shadow value from design tokens"""
    return DESIGN_TOKENS["shadows"].get(level, "none")


def get_border_radius(size: str) -> str:
    """Get border radius value from design tokens"""
    return DESIGN_TOKENS["border_radius"].get(size, "0.25rem")


def apply_custom_css():
    """Apply comprehensive custom CSS styling with modern design tokens"""

    # Get design tokens
    tokens = get_design_tokens()
    colors = get_theme_colors()
    
    # Performance-optimized CSS with font-display and resource hints
    css = f"""
    <style>
    /* Performance optimizations */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Poppins:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');
    
    /* Font face declarations with font-display for performance */
    @font-face {{
        font-family: 'Inter';
        font-display: swap;
        src: local('Inter');
    }}
    
    @font-face {{
        font-family: 'Poppins';
        font-display: swap;
        src: local('Poppins');
    }}
    
    @font-face {{
        font-family: 'JetBrains Mono';
        font-display: swap;
        src: local('JetBrains Mono');
    }}
    
    /* Modern Design Token System */
    :root {{
        /* Primary Color Scale */
        --primary-50: {tokens["primary"]["50"]};
        --primary-100: {tokens["primary"]["100"]};
        --primary-200: {tokens["primary"]["200"]};
        --primary-300: {tokens["primary"]["300"]};
        --primary-400: {tokens["primary"]["400"]};
        --primary-500: {tokens["primary"]["500"]};
        --primary-600: {tokens["primary"]["600"]};
        --primary-700: {tokens["primary"]["700"]};
        --primary-800: {tokens["primary"]["800"]};
        --primary-900: {tokens["primary"]["900"]};
        
        /* Secondary Color Scale */
        --secondary-50: {tokens["secondary"]["50"]};
        --secondary-100: {tokens["secondary"]["100"]};
        --secondary-200: {tokens["secondary"]["200"]};
        --secondary-300: {tokens["secondary"]["300"]};
        --secondary-400: {tokens["secondary"]["400"]};
        --secondary-500: {tokens["secondary"]["500"]};
        --secondary-600: {tokens["secondary"]["600"]};
        --secondary-700: {tokens["secondary"]["700"]};
        --secondary-800: {tokens["secondary"]["800"]};
        --secondary-900: {tokens["secondary"]["900"]};
        
        /* Neutral/Gray Scale */
        --neutral-0: {tokens["neutral"]["0"]};
        --neutral-50: {tokens["neutral"]["50"]};
        --neutral-100: {tokens["neutral"]["100"]};
        --neutral-200: {tokens["neutral"]["200"]};
        --neutral-300: {tokens["neutral"]["300"]};
        --neutral-400: {tokens["neutral"]["400"]};
        --neutral-500: {tokens["neutral"]["500"]};
        --neutral-600: {tokens["neutral"]["600"]};
        --neutral-700: {tokens["neutral"]["700"]};
        --neutral-800: {tokens["neutral"]["800"]};
        --neutral-900: {tokens["neutral"]["900"]};
        
        /* Semantic Colors */
        --success-light: {tokens["semantic"]["success"]["light"]};
        --success-main: {tokens["semantic"]["success"]["main"]};
        --success-dark: {tokens["semantic"]["success"]["dark"]};
        --warning-light: {tokens["semantic"]["warning"]["light"]};
        --warning-main: {tokens["semantic"]["warning"]["main"]};
        --warning-dark: {tokens["semantic"]["warning"]["dark"]};
        --error-light: {tokens["semantic"]["error"]["light"]};
        --error-main: {tokens["semantic"]["error"]["main"]};
        --error-dark: {tokens["semantic"]["error"]["dark"]};
        --info-light: {tokens["semantic"]["info"]["light"]};
        --info-main: {tokens["semantic"]["info"]["main"]};
        --info-dark: {tokens["semantic"]["info"]["dark"]};
        
        /* Accent Colors */
        --accent-orange: {tokens["accent"]["orange"]};
        --accent-teal: {tokens["accent"]["teal"]};
        --accent-pink: {tokens["accent"]["pink"]};
        --accent-green: {tokens["accent"]["green"]};
        --accent-indigo: {tokens["accent"]["indigo"]};
        
        /* Gradients */
        --gradient-primary: {tokens["gradients"]["primary"]};
        --gradient-secondary: {tokens["gradients"]["secondary"]};
        --gradient-accent: {tokens["gradients"]["accent"]};
        --gradient-success: {tokens["gradients"]["success"]};
        --gradient-info: {tokens["gradients"]["info"]};
        --gradient-warm: {tokens["gradients"]["warm"]};
        --gradient-cool: {tokens["gradients"]["cool"]};
        --gradient-neutral: {tokens["gradients"]["neutral"]};
        --gradient-glass: {tokens["gradients"]["glass"]};
        
        /* Typography System */
        --font-family-primary: {tokens["typography"]["font_family_primary"]};
        --font-family-heading: {tokens["typography"]["font_family_heading"]};
        --font-family-mono: {tokens["typography"]["font_family_mono"]};
        
        /* Font Sizes */
        --font-size-xs: {tokens["typography"]["font_size"]["xs"]};
        --font-size-sm: {tokens["typography"]["font_size"]["sm"]};
        --font-size-base: {tokens["typography"]["font_size"]["base"]};
        --font-size-lg: {tokens["typography"]["font_size"]["lg"]};
        --font-size-xl: {tokens["typography"]["font_size"]["xl"]};
        --font-size-2xl: {tokens["typography"]["font_size"]["2xl"]};
        --font-size-3xl: {tokens["typography"]["font_size"]["3xl"]};
        --font-size-4xl: {tokens["typography"]["font_size"]["4xl"]};
        --font-size-5xl: {tokens["typography"]["font_size"]["5xl"]};
        --font-size-6xl: {tokens["typography"]["font_size"]["6xl"]};
        
        /* Font Weights */
        --font-weight-light: {tokens["typography"]["font_weight"]["light"]};
        --font-weight-normal: {tokens["typography"]["font_weight"]["normal"]};
        --font-weight-medium: {tokens["typography"]["font_weight"]["medium"]};
        --font-weight-semibold: {tokens["typography"]["font_weight"]["semibold"]};
        --font-weight-bold: {tokens["typography"]["font_weight"]["bold"]};
        --font-weight-extrabold: {tokens["typography"]["font_weight"]["extrabold"]};
        
        /* Line Heights */
        --line-height-tight: {tokens["typography"]["line_height"]["tight"]};
        --line-height-snug: {tokens["typography"]["line_height"]["snug"]};
        --line-height-normal: {tokens["typography"]["line_height"]["normal"]};
        --line-height-relaxed: {tokens["typography"]["line_height"]["relaxed"]};
        --line-height-loose: {tokens["typography"]["line_height"]["loose"]};
        
        /* Spacing Scale */
        --spacing-0: {tokens["spacing"]["0"]};
        --spacing-1: {tokens["spacing"]["1"]};
        --spacing-2: {tokens["spacing"]["2"]};
        --spacing-3: {tokens["spacing"]["3"]};
        --spacing-4: {tokens["spacing"]["4"]};
        --spacing-5: {tokens["spacing"]["5"]};
        --spacing-6: {tokens["spacing"]["6"]};
        --spacing-8: {tokens["spacing"]["8"]};
        --spacing-10: {tokens["spacing"]["10"]};
        --spacing-12: {tokens["spacing"]["12"]};
        --spacing-16: {tokens["spacing"]["16"]};
        --spacing-20: {tokens["spacing"]["20"]};
        --spacing-24: {tokens["spacing"]["24"]};
        --spacing-32: {tokens["spacing"]["32"]};
        
        /* Border Radius */
        --border-radius-none: {tokens["border_radius"]["none"]};
        --border-radius-sm: {tokens["border_radius"]["sm"]};
        --border-radius-base: {tokens["border_radius"]["base"]};
        --border-radius-md: {tokens["border_radius"]["md"]};
        --border-radius-lg: {tokens["border_radius"]["lg"]};
        --border-radius-xl: {tokens["border_radius"]["xl"]};
        --border-radius-2xl: {tokens["border_radius"]["2xl"]};
        --border-radius-3xl: {tokens["border_radius"]["3xl"]};
        --border-radius-full: {tokens["border_radius"]["full"]};
        
        /* Shadow System */
        --shadow-xs: {tokens["shadows"]["xs"]};
        --shadow-sm: {tokens["shadows"]["sm"]};
        --shadow-base: {tokens["shadows"]["base"]};
        --shadow-md: {tokens["shadows"]["md"]};
        --shadow-lg: {tokens["shadows"]["lg"]};
        --shadow-xl: {tokens["shadows"]["xl"]};
        --shadow-2xl: {tokens["shadows"]["2xl"]};
        --shadow-inner: {tokens["shadows"]["inner"]};
        
        /* Legacy Variables for Backward Compatibility */
        --primary-color: var(--primary-500);
        --secondary-color: var(--secondary-500);
        --accent-color: var(--accent-orange);
        --success-color: var(--success-main);
        --warning-color: var(--warning-main);
        --error-color: var(--error-main);
        --info-color: var(--info-main);
        --light-color: var(--neutral-100);
        --dark-color: var(--neutral-800);
        --muted-color: var(--neutral-500);
        --background-color: var(--neutral-0);
        --surface-color: var(--neutral-50);
        --text-primary: var(--neutral-900);
        --text-secondary: var(--neutral-600);
        --border-color: var(--neutral-200);
        --shadow-color: rgba(0,0,0,0.08);
        
        /* Typography Legacy */
        --font-primary: var(--font-family-primary);
        --font-heading: var(--font-family-heading);
        --line-height-normal: var(--line-height-normal);
        --line-height-heading: var(--line-height-snug);
        --spacing-md: 1rem;      /* 16px */
        --spacing-lg: 1.5rem;    /* 24px */
        --spacing-xl: 2rem;      /* 32px */
        --spacing-xxl: 2.5rem;   /* 40px */
        --spacing-xxxl: 3rem;    /* 48px */
        
        /* Border Radius */
        --border-radius-xs: 4px;
        --border-radius-sm: 8px; 
        --border-radius-md: 12px;
        --border-radius-lg: 16px;
        --border-radius-xl: 24px;
        --border-radius-pill: 9999px;
        
        /* Shadows */
        --shadow-xs: 0 1px 2px rgba(0,0,0,0.05);
        --shadow-sm: 0 1px 3px rgba(0,0,0,0.1), 0 1px 2px rgba(0,0,0,0.06);
        --shadow-md: 0 4px 6px -1px rgba(0,0,0,0.1), 0 2px 4px -1px rgba(0,0,0,0.06);
        --shadow-lg: 0 10px 15px -3px rgba(0,0,0,0.1), 0 4px 6px -2px rgba(0,0,0,0.05);
        --shadow-xl: 0 20px 25px -5px rgba(0,0,0,0.1), 0 10px 10px -5px rgba(0,0,0,0.04);
        
        /* Transitions */
        --transition-fast: 150ms ease;
        --transition-normal: 250ms ease;
        --transition-slow: 350ms ease;
    }}
    
    /* Global Styles */
    .stApp {{
        font-family: var(--font-primary);
        background: var(--background-color);
        color: var(--text-primary);
        line-height: var(--line-height-normal);
    }}
    
    /* Ensure all text is visible - WCAG contrast fix */
    p, span, div, label, h1, h2, h3, h4, h5, h6 {{
        color: var(--text-primary) !important;
    }}
    
    .text-secondary {{
        color: var(--text-secondary) !important;
    }}
    
    .text-muted {{
        color: var(--muted-color) !important;
    }}
    
    .text-primary {{
        color: var(--primary-color) !important;
    }}
    
    /* Hide Streamlit branding */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    
    /* Typography */
    h1, h2, h3, h4, h5, h6 {{
        font-family: var(--font-heading);
        line-height: var(--line-height-heading);
        font-weight: 600;
        margin-bottom: var(--spacing-md);
    }}
    
    p {{
        margin-bottom: var(--spacing-md);
        line-height: var(--line-height-normal);
    }}
    
    /* Custom Headers */
    .main-header {{
        font-family: var(--font-heading);
        font-weight: 700;
        font-size: 2.75rem;
        text-align: center;
        background: var(--gradient-primary);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: var(--spacing-lg);
        line-height: 1.2;
        letter-spacing: -0.02em;
    }}
    
    .section-header {{
        font-family: var(--font-heading);
        font-weight: 600;
        font-size: 1.75rem;
        color: var(--primary-color);
        margin: var(--spacing-xl) 0 var(--spacing-md) 0;
        border-bottom: 3px solid var(--accent-color);
        padding-bottom: var(--spacing-xs);
        letter-spacing: -0.01em;
    }}
    
    .subtitle {{
        font-size: 1.1rem;
        color: var(--text-secondary);
        text-align: center;
        margin: -0.5rem 0 var(--spacing-xl) 0;
        font-weight: 400;
        line-height: 1.6;
        max-width: 700px;
        margin-left: auto;
        margin-right: auto;
    }}
    
    /* Card Components with Layout Shift Prevention */
    .feature-card {{
        background: var(--surface-color);
        padding: var(--spacing-lg);
        border-radius: var(--border-radius-md);
        border: 1px solid var(--border-color);
        margin: var(--spacing-md) 0;
        box-shadow: var(--shadow-sm);
        transition: all var(--transition-normal);
        position: relative;
        overflow: hidden;
        min-height: 120px; /* Prevent layout shift */
        display: flex;
        flex-direction: column;
        backdrop-filter: blur(5px);
        contain: layout style; /* CSS containment for performance */
    }}
    
    /* Layout Shift Prevention - Fixed scroll issues */
    .stMainBlockContainer {{
        /* Removed min-height: 100vh to fix scroll */
        contain: layout style;
    }}
    
    .stSidebar {{
        /* Removed min-height: 100vh to fix scroll */
        contain: layout style;
    }}
    
    /* Form and Modal Improvements */
    .stForm {{
        background: var(--surface-color);
        padding: var(--spacing-lg);
        border-radius: var(--border-radius-md);
        border: 1px solid var(--border-color);
        margin: var(--spacing-md) 0;
        box-shadow: var(--shadow-sm);
        max-width: 100%;
        overflow: visible;
    }}
    
    /* Tab content improvements */
    .stTabs [data-baseweb="tab-list"] {{
        gap: var(--spacing-sm);
    }}
    
    .stTabs [data-baseweb="tab"] {{
        height: auto;
        padding: var(--spacing-sm) var(--spacing-md);
        border-radius: var(--border-radius-sm);
    }}
    
    /* Error and warning message improvements */
    .stAlert {{
        margin: var(--spacing-xs) 0;
        border-radius: var(--border-radius-sm);
        border-left: 4px solid;
    }}
    
    .stAlert[data-testid="alertError"] {{
        border-left-color: var(--error-color);
        background-color: rgba(211, 47, 47, 0.1);
    }}
    
    .stAlert[data-testid="alertWarning"] {{
        border-left-color: var(--warning-color);
        background-color: rgba(245, 127, 23, 0.1);
    }}
    
    /* Improve input spacing */
    .stTextInput > div > div > input {{
        margin-bottom: var(--spacing-xs);
    }}
    
    /* Checkbox improvements */
    .stCheckbox {{
        margin: var(--spacing-sm) 0;
    }}
    
    /* Button containers with fixed dimensions */
    .stButton > button {{
        min-height: 40px;
        min-width: 120px;
        contain: layout style;
    }}
    
    .feature-card::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: var(--gradient-primary);
    }}
    
    /* Enhanced card animations and effects */
    .feature-card::after {{
        content: '';
        position: absolute;
        top: 0;
        right: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(to right, rgba(255,255,255,0.03), rgba(255,255,255,0.1));
        transform: translateX(-100%);
        transition: transform 0.6s ease;
        pointer-events: none;
    }}
    
    .feature-card:hover {{
        transform: translateY(-2px);
        box-shadow: var(--shadow-md);
        border-color: var(--primary-color);
    }}
    
    .feature-card:hover::after {{
        transform: translateX(100%);
    }}
    
    .metric-card {{
        background: linear-gradient(135deg, var(--light-color) 0%, #ffffff 100%);
        padding: var(--spacing-lg);
        border-radius: var(--border-radius-md);
        text-align: center;
        box-shadow: var(--shadow-sm);
        border: 1px solid var(--border-color);
        transition: all var(--transition-normal);
        height: 100%;
    }}
    
    .metric-card:hover {{
        transform: scale(1.02);
        box-shadow: var(--shadow-md);
    }}
    
    .success-card {{
        background: linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 100%);
        border-color: var(--success-color);
        color: #1B5E20;
        border-radius: var(--border-radius-md);
        padding: var(--spacing-lg);
        box-shadow: var(--shadow-sm);
        margin: var(--spacing-md) 0;
    }}
    
    .warning-card {{
        background: linear-gradient(135deg, #FFF8E1 0%, #FFECB3 100%);
        border-color: var(--warning-color);
        color: #F57F17;
        border-radius: var(--border-radius-md);
        padding: var(--spacing-lg);
        box-shadow: var(--shadow-sm);
        margin: var(--spacing-md) 0;
    }}
    
    .error-card {{
        background: linear-gradient(135deg, #FFEBEE 0%, #FFCDD2 100%);
        border-color: var(--error-color);
        color: #B71C1C;
        border-radius: var(--border-radius-md);
        padding: var(--spacing-lg);
        box-shadow: var(--shadow-sm);
        margin: var(--spacing-md) 0;
    }}
    
    .info-card {{
        background: linear-gradient(135deg, #E1F5FE 0%, #B3E5FC 100%);
        border-color: var(--info-color);
        color: #01579B;
        border-radius: var(--border-radius-md);
        padding: var(--spacing-lg);
        box-shadow: var(--shadow-sm);
        margin: var(--spacing-md) 0;
    }}
    
    /* Button Styles */
    .stButton > button {{
        background: var(--primary-color);
        color: white;
        border: none;
        border-radius: var(--border-radius-md);
        padding: 0.5rem 1rem;
        font-weight: 500;
        font-family: var(--font-primary);
        transition: all var(--transition-fast);
        box-shadow: var(--shadow-sm);
        height: 2.5rem;
    }}
    
    .stButton > button:hover {{
        transform: translateY(-1px);
        box-shadow: var(--shadow-md);
        background: var(--gradient-primary);
        opacity: 0.9;
    }}
    
    .stButton > button:active {{
        transform: translateY(0);
        box-shadow: var(--shadow-xs);
        opacity: 1;
    }}
    
    /* Primary action button */
    .stButton.primary > button {{
        background: var(--gradient-primary);
        font-weight: 600;
    }}
    
    /* Secondary action button */
    .stButton.secondary > button {{
        background: transparent;
        border: 1px solid var(--primary-color);
        color: var(--primary-color);
    }}
    
    .stButton.secondary > button:hover {{
        background: rgba(30, 136, 229, 0.1);
        transform: translateY(-1px);
    }}
    
    /* Form Elements */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select {{
        border-radius: var(--border-radius-md);
        border: 1px solid var(--border-color);
        padding: var(--spacing-sm) var(--spacing-md);
        font-family: var(--font-primary);
        transition: all var(--transition-fast);
        font-size: 1rem;
        box-shadow: var(--shadow-xs);
    }}
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stSelectbox > div > div > select:focus {{
        border-color: var(--primary-color);
        box-shadow: 0 0 0 2px rgba(30, 136, 229, 0.2);
        transform: translateY(-1px);
    }}
    
    /* Enhanced Form Styling */
    .form-question-container {{
        background: var(--surface-color);
        border-radius: var(--border-radius-md);
        padding: 1.2rem;
        margin-bottom: 1.5rem;
        border: 1px solid var(--border-color);
        box-shadow: var(--shadow-sm);
        transition: all var(--transition-normal);
    }}
    
    .form-question-container:hover {{
        box-shadow: var(--shadow-md);
        border-color: rgba(30, 136, 229, 0.3);
    }}
    
    .question-text {{
        font-weight: 600;
        font-size: 1.1rem;
        color: var(--primary-color);
        margin-bottom: 0.8rem;
    }}
    
    .question-help {{
        color: var(--text-secondary);
        font-size: 0.9rem;
        font-style: italic;
        margin-bottom: 1rem;
        opacity: 0.8;
    }}
    
    .required-indicator {{
        color: var(--error-color);
        margin-left: 0.3rem;
    }}
    
    /* Radio button styling */
    .stRadio > div {{
        background: var(--surface-color);
        padding: 0.75rem;
        border-radius: var(--border-radius-md);
        border: 1px solid var(--border-color);
    }}
    
    .stRadio > div > label {{
        background: white;
        border-radius: var(--border-radius-sm);
        padding: 0.5rem 1rem;
        margin: 0.25rem 0;
        border: 1px solid transparent;
        transition: all var(--transition-fast);
    }}
    
    .stRadio > div > label:hover {{
        background: rgba(30, 136, 229, 0.05);
        border-color: rgba(30, 136, 229, 0.2);
    }}
    
    /* Checkbox and Radio buttons */
    .stCheckbox > label > div[role="checkbox"],
    .stRadio > div > label > div[role="radio"] {{
        border-color: var(--primary-color);
    }}
    
    .stCheckbox > label > div[data-baseweb="checkbox"] > div,
    .stRadio > div > label > div[data-baseweb="radio"] > div {{
        background-color: var(--primary-color);
    }}
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {{
        background: var(--surface-color);
        border-right: 1px solid var(--border-color);
        padding: var(--spacing-md);
    }}
    
    section[data-testid="stSidebar"] .stButton > button {{
        width: 100%;
        margin-bottom: var(--spacing-xs);
    }}
    
    /* Progress Components */
    .progress-container {{
        background: var(--light-color);
        border-radius: var(--border-radius-lg);
        padding: var(--spacing-sm);
        margin: var(--spacing-md) 0;
    }}
    
    .progress-bar {{
        background: var(--gradient-primary);
        height: 8px;
        border-radius: var(--border-radius-pill);
        transition: width 0.5s ease;
    }}
    
    /* Chat Interface */
    .chat-container {{
        max-height: 500px;
        overflow-y: auto;
        padding: var(--spacing-md);
        background: var(--surface-color);
        border-radius: var(--border-radius-md);
        border: 1px solid var(--border-color);
    }}
    
    .message-bubble {{
        padding: var(--spacing-sm) var(--spacing-md);
        margin: var(--spacing-sm) 0;
        border-radius: var(--border-radius-md);
        max-width: 85%;
    }}
    
    .message-user {{
        background: var(--gradient-primary);
        color: white;
        margin-left: auto;
        border-top-right-radius: var(--border-radius-xs);
        border-bottom-right-radius: var(--border-radius-md);
        border-top-left-radius: var(--border-radius-md);
        border-bottom-left-radius: var(--border-radius-md);
        box-shadow: var(--shadow-sm);
    }}
    
    .message-assistant {{
        background: var(--light-color);
        color: var(--text-primary);
        border: 1px solid var(--border-color);
        border-top-left-radius: var(--border-radius-xs);
        border-bottom-left-radius: var(--border-radius-md);
        border-top-right-radius: var(--border-radius-md);
        border-bottom-right-radius: var(--border-radius-md);
        box-shadow: var(--shadow-sm);
    }}
    
    /* Data Tables */
    .stDataFrame {{
        border: 1px solid var(--border-color);
        border-radius: var(--border-radius-md);
        overflow: hidden;
    }}
    
    .stDataFrame [data-testid="stTable"] {{
        border-collapse: collapse;
    }}
    
    .stDataFrame thead tr th {{
        background-color: var(--primary-color);
        color: white;
        padding: var(--spacing-sm) var(--spacing-md);
    }}
    
    .stDataFrame tbody tr:nth-child(even) {{
        background-color: rgba(0,0,0,0.02);
    }}
    
    .stDataFrame tbody tr:hover {{
        background-color: rgba(30, 136, 229, 0.05);
    }}
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 2px;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        padding: var(--spacing-sm) var(--spacing-md);
        border-radius: var(--border-radius-md) var(--border-radius-md) 0 0;
    }}
    
    .stTabs [aria-selected="true"] {{
        background-color: var(--primary-color) !important;
        color: white !important;
    }}
    
    /* Expanders */
    .streamlit-expanderHeader {{
        font-weight: 600;
        color: var(--primary-color);
    }}
    
    /* Animation Classes */
    .fade-in {{
        animation: fadeIn 0.5s ease-out forwards;
    }}
    
    .scale-in {{
        animation: scaleIn 0.3s ease-out forwards;
    }}
    
    .slide-in {{
        animation: slideIn 0.5s ease-out forwards;
    }}
    
    /* Utilities */
    .text-center {{
        text-align: center;
    }}
    
    .margin-top {{
        margin-top: var(--spacing-lg);
    }}
    
    .margin-bottom {{
        margin-bottom: var(--spacing-lg);
    }}
    
    .no-margin {{
        margin: 0 !important;
    }}
    
    .strong {{
        font-weight: 600;
    }}
    
    .text-muted {{
        color: var(--text-secondary);
    }}
    
    .shadow {{
        box-shadow: var(--shadow-md);
    }}
    
    .rounded {{
        border-radius: var(--border-radius-md);
    }}
    
    /* Responsive design */
    @media (max-width: 992px) {{
        .main-header {{
            font-size: 2.2rem;
        }}
        
        .section-header {{
            font-size: 1.6rem;
        }}
        
        .feature-card,
        .metric-card,
        .success-card,
        .warning-card,
        .error-card,
        .info-card {{
            padding: var(--spacing-md);
        }}
    }}
    
    @media (max-width: 768px) {{
        .main-header {{
            font-size: 2rem;
        }}
        
        .section-header {{
            font-size: 1.5rem;
        }}
        
        section[data-testid="stSidebar"] {{
            width: 100% !important;
        }}
        
        /* Improve stacked columns on mobile */
        [data-testid="column"] {{
            width: 100% !important;
            margin-bottom: var(--spacing-md);
        }}
    }}
    
    @media (max-width: 576px) {{
        .main-header {{
            font-size: 1.8rem;
        }}
        
        .section-header {{
            font-size: 1.4rem;
        }}
        
        .feature-card,
        .metric-card,
        .success-card,
        .warning-card,
        .error-card,
        .info-card {{
            padding: var(--spacing-sm);
        }}
        
        /* Better mobile form controls */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stSelectbox > div > div > select {{
            font-size: 16px; /* Prevents iOS zoom on focus */
        }}
        
        .stButton > button {{
            width: 100%;
            height: 3rem; /* Larger touch targets */
        }}
    }}
    
    /* Animations */
    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(20px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    
    @keyframes scaleIn {{
        from {{ opacity: 0; transform: scale(0.9); }}
        to {{ opacity: 1; transform: scale(1); }}
    }}
    
    @keyframes slideIn {{
        from {{ opacity: 0; transform: translateX(-20px); }}
        to {{ opacity: 1; transform: translateX(0); }}
    }}
    
    @keyframes pulse {{
        0%, 100% {{ opacity: 1; }}
        50% {{ opacity: 0.7; }}
    }}
    
    .fade-in {{
        animation: fadeIn 0.5s ease-out;
    }}
    
    .pulse {{
        animation: pulse 2s infinite;
    }}
    
    /* Responsive Design */
    @media (max-width: 768px) {{
        .main-header {{
            font-size: 2.5rem;
        }}
        
        .section-header {{
            font-size: 1.5rem;
        }}
        
        .feature-card {{
            padding: var(--spacing-md);
        }}
        
        .metric-card {{
            padding: var(--spacing-md);
        }}
    }}
    
    /* Custom Streamlit Component Overrides */
    .stExpander {{
        border: 1px solid var(--border-color);
        border-radius: var(--border-radius);
        box-shadow: var(--shadow-sm);
    }}
    
    .stTabs [data-baseweb="tab-list"] {{
        gap: var(--spacing-sm);
    }}
    
    .stTabs [data-baseweb="tab"] {{
        background: var(--surface-color);
        border-radius: var(--border-radius-sm);
        padding: var(--spacing-sm) var(--spacing-md);
        border: 1px solid var(--border-color);
    }}
    
    .stTabs [aria-selected="true"] {{
        background: var(--gradient-primary);
        color: white;
        border-color: var(--primary-color);
    }}
    
    /* Utility Classes */
    .text-center {{ text-align: center; }}
    .text-left {{ text-align: left; }}
    .text-right {{ text-align: right; }}
    
    .mt-1 {{ margin-top: var(--spacing-xs); }}
    .mt-2 {{ margin-top: var(--spacing-sm); }}
    .mt-3 {{ margin-top: var(--spacing-md); }}
    .mt-4 {{ margin-top: var(--spacing-lg); }}
    .mt-5 {{ margin-top: var(--spacing-xl); }}
    
    .mb-1 {{ margin-bottom: var(--spacing-xs); }}
    .mb-2 {{ margin-bottom: var(--spacing-sm); }}
    .mb-3 {{ margin-bottom: var(--spacing-md); }}
    .mb-4 {{ margin-bottom: var(--spacing-lg); }}
    .mb-5 {{ margin-bottom: var(--spacing-xl); }}
    
    .p-1 {{ padding: var(--spacing-xs); }}
    .p-2 {{ padding: var(--spacing-sm); }}
    .p-3 {{ padding: var(--spacing-md); }}
    .p-4 {{ padding: var(--spacing-lg); }}
    .p-5 {{ padding: var(--spacing-xl); }}
    
    .rounded {{ border-radius: var(--border-radius); }}
    .rounded-sm {{ border-radius: var(--border-radius-sm); }}
    .rounded-lg {{ border-radius: var(--border-radius-lg); }}
    
    .shadow {{ box-shadow: var(--shadow-sm); }}
    .shadow-md {{ box-shadow: var(--shadow-md); }}
    .shadow-lg {{ box-shadow: var(--shadow-lg); }}
    
    .border {{ border: 1px solid var(--border-color); }}
    .border-primary {{ border: 2px solid var(--primary-color); }}
    .border-success {{ border: 2px solid var(--success-color); }}
    .border-warning {{ border: 2px solid var(--warning-color); }}
    .border-error {{ border: 2px solid var(--error-color); }}
    
    .bg-primary {{ background: var(--primary-color); }}
    .bg-secondary {{ background: var(--secondary-color); }}
    .bg-accent {{ background: var(--accent-color); }}
    .bg-success {{ background: var(--success-color); }}
    .bg-warning {{ background: var(--warning-color); }}
    .bg-error {{ background: var(--error-color); }}
    .bg-light {{ background: var(--light-color); }}
    .bg-surface {{ background: var(--surface-color); }}
    
    .text-primary {{ color: var(--primary-color); }}
    .text-secondary {{ color: var(--text-secondary); }}
    .text-success {{ color: var(--success-color); }}
    .text-warning {{ color: var(--warning-color); }}
    .text-error {{ color: var(--error-color); }}
    .text-muted {{ color: var(--muted-color); }}
    
    .font-weight-light {{ font-weight: 300; }}
    .font-weight-normal {{ font-weight: 400; }}
    .font-weight-medium {{ font-weight: 500; }}
    .font-weight-semibold {{ font-weight: 600; }}
    .font-weight-bold {{ font-weight: 700; }}
    
    /* Performance Optimizations */
    * {{
        box-sizing: border-box; /* Reduce reflow calculations */
    }}
    
    /* GPU acceleration for animations */
    .feature-card:hover,
    .stButton > button:hover {{
        transform: translateZ(0); /* Force GPU layer */
        will-change: transform; /* Optimize for animations */
    }}
    
    /* Reduce paint complexity */
    .stApp {{
        contain: layout style paint; /* CSS containment */
    }}
    
    /* Optimize images and media */
    img {{
        max-width: 100%;
        height: auto;
        loading: lazy; /* Lazy load images */
    }}
    
    /* Critical resource hints */
    @media (prefers-reduced-motion: reduce) {{
        * {{
            animation-duration: 0.01ms !important;
            animation-iteration-count: 1 !important;
            transition-duration: 0.01ms !important;
        }}
    }}
    
    /* Reduce complexity on mobile */
    @media (max-width: 768px) {{
        .feature-card::after {{
            display: none; /* Remove hover effects on mobile */
        }}
        
        .shadow,
        .shadow-md,
        .shadow-lg {{
            box-shadow: none; /* Reduce shadows on mobile */
        }}
    }}
    
    </style>
    """

    st.markdown(css, unsafe_allow_html=True)


def inject_custom_js():
    """Inject custom JavaScript for enhanced functionality"""

    js = """
    <script>
    // Apply custom scrollbar styling
    document.addEventListener('DOMContentLoaded', function() {
        const style = document.createElement('style');
        style.innerHTML = `
            ::-webkit-scrollbar {
                width: 8px;
                height: 8px;
            }
            ::-webkit-scrollbar-track {
                background: #f5f5f5;
                border-radius: 10px;
            }
            ::-webkit-scrollbar-thumb {
                background: #c1c1c1;
                border-radius: 10px;
            }
            ::-webkit-scrollbar-thumb:hover {
                background: #888;
            }
        `;
        document.head.appendChild(style);
    });
    
    // Smooth scrolling for anchor links
    document.addEventListener('DOMContentLoaded', function() {
        const links = document.querySelectorAll('a[href^="#"]');
        for (const link of links) {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({ behavior: 'smooth' });
                }
            });
        }
    });
    
    // Auto-resize textareas
    function autoResize(textarea) {
        textarea.style.height = 'auto';
        textarea.style.height = textarea.scrollHeight + 'px';
    }
    
    // Add loading states to buttons
    function addLoadingState(button, text = 'Loading...') {
        const originalText = button.textContent;
        button.textContent = text;
        button.disabled = true;
        
        return function() {
            button.textContent = originalText;
            button.disabled = false;
        };
    }
    
    // Enhanced form validation
    function validateForm(form) {
        const inputs = form.querySelectorAll('input[required], textarea[required], select[required]');
        let isValid = true;
        
        inputs.forEach(input => {
            if (!input.value.trim()) {
                input.classList.add('border-error');
                isValid = false;
            } else {
                input.classList.remove('border-error');
            }
        });
        
        return isValid;
    }
    
    // Copy to clipboard functionality
    function copyToClipboard(text) {
        navigator.clipboard.writeText(text).then(function() {
            // Show success message
            const toast = document.createElement('div');
            toast.textContent = 'Copied to clipboard!';
            toast.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                background: var(--success-color);
                color: white;
                padding: 10px 20px;
                border-radius: 8px;
                z-index: 1000;
                box-shadow: var(--shadow-md);
            `;
            document.body.appendChild(toast);
            setTimeout(() => document.body.removeChild(toast), 3000);
        });
    }
    
    // Add animation classes to elements
    document.addEventListener('DOMContentLoaded', function() {
        setTimeout(() => {
            const fadeElements = document.querySelectorAll('.fade-in');
            fadeElements.forEach((el, index) => {
                setTimeout(() => {
                    el.style.opacity = '1';
                    el.style.transform = 'translateY(0)';
                }, index * 100);
            });
        }, 300);
    });
    
    // Enhanced typing effect for chat
    function typeWriter(element, text, speed = 50) {
        let i = 0;
        element.textContent = '';
        
        function type() {
            if (i < text.length) {
                element.textContent += text.charAt(i);
                i++;
                setTimeout(type, speed);
            }
        }
        
        type();
    }
    
    // Theme persistence
    function saveThemePreference(theme) {
        localStorage.setItem('margadarsaka_theme', theme);
    }
    
    function loadThemePreference() {
        return localStorage.getItem('margadarsaka_theme') || 'light';
    }
    
    // Keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + K for search
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            const searchInput = document.querySelector('input[type="search"], input[placeholder*="search" i]');
            if (searchInput) {
                searchInput.focus();
            }
        }
        
        // Escape to close modals
        if (e.key === 'Escape') {
            const modals = document.querySelectorAll('.modal, .dialog');
            modals.forEach(modal => {
                if (modal.style.display !== 'none') {
                    modal.style.display = 'none';
                }
            });
        }
    });
    
    // Performance optimization - lazy load images
    document.addEventListener('DOMContentLoaded', function() {
        const lazyImages = document.querySelectorAll('img[data-src]');
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    observer.unobserve(img);
                }
            });
        }, { rootMargin: '100px' });
        
        lazyImages.forEach(img => observer.observe(img));
    });
    </script>
    """

    st.markdown(js, unsafe_allow_html=True)
