"""
Internationalization (i18n) support for Margadarsaka
Supports English, Hindi, and Hinglish with cultural adaptations
"""

import streamlit as st
from typing import Dict, Any, Optional, List
import json
import logging
from enum import Enum
from dataclasses import dataclass

logger = logging.getLogger(__name__)


class Language(Enum):
    """Supported languages"""

    ENGLISH = "en"
    HINDI = "hi"
    HINGLISH = "hi-en"


@dataclass
class LocaleConfig:
    """Configuration for a locale"""

    code: str
    name: str
    native_name: str
    direction: str = "ltr"  # ltr or rtl
    date_format: str = "%d/%m/%Y"
    time_format: str = "%H:%M"
    currency: str = "₹"
    decimal_separator: str = "."
    thousand_separator: str = ","


# Locale configurations
LOCALES = {
    Language.ENGLISH: LocaleConfig(
        code="en",
        name="English",
        native_name="English",
        date_format="%d/%m/%Y",
        currency="₹",
    ),
    Language.HINDI: LocaleConfig(
        code="hi",
        name="Hindi",
        native_name="हिंदी",
        date_format="%d/%m/%Y",
        currency="₹",
    ),
    Language.HINGLISH: LocaleConfig(
        code="hi-en",
        name="Hinglish",
        native_name="हिंग्लिश",
        date_format="%d/%m/%Y",
        currency="₹",
    ),
}

# Translation dictionary
TRANSLATIONS = {
    # Navigation and General
    "app_title": {
        Language.ENGLISH: "Margadarsaka - AI Career Advisor",
        Language.HINDI: "मार्गदर्शक - एआई करियर सलाहकार",
        Language.HINGLISH: "Margadarsaka - AI Career Advisor",
    },
    "app_subtitle": {
        Language.ENGLISH: "AI-Powered Career Guidance with Psychological Assessment",
        Language.HINDI: "मनोवैज्ञानिक मूल्यांकन के साथ एआई-संचालित करियर मार्गदर्शन",
        Language.HINGLISH: "AI-Powered Career Guidance with Psychological Assessment",
    },
    "home": {
        Language.ENGLISH: "Home",
        Language.HINDI: "होम",
        Language.HINGLISH: "Home",
    },
    "psychological_assessment": {
        Language.ENGLISH: "Psychological Assessment",
        Language.HINDI: "मनोवैज्ञानिक मूल्यांकन",
        Language.HINGLISH: "Psychological Assessment",
    },
    "resume_analysis": {
        Language.ENGLISH: "Resume Analysis",
        Language.HINDI: "रिज्यूमे विश्लेषण",
        Language.HINGLISH: "Resume Analysis",
    },
    "ai_career_chat": {
        Language.ENGLISH: "AI Career Chat",
        Language.HINDI: "एआई करियर चैट",
        Language.HINGLISH: "AI Career Chat",
    },
    "career_recommendations": {
        Language.ENGLISH: "Career Recommendations",
        Language.HINDI: "करियर सिफारिशें",
        Language.HINGLISH: "Career Recommendations",
    },
    "learning_resources": {
        Language.ENGLISH: "Learning Resources",
        Language.HINDI: "शिक्षण संसाधन",
        Language.HINGLISH: "Learning Resources",
    },
    "progress_tracker": {
        Language.ENGLISH: "Progress Tracker",
        Language.HINDI: "प्रगति ट्रैकर",
        Language.HINGLISH: "Progress Tracker",
    },
    # Additional UI strings used across modern UI
    "home_desc": {
        Language.ENGLISH: "Welcome to your AI-powered career guide.",
        Language.HINDI: "आपके एआई-संचालित करियर गाइड में स्वागत है।",
        Language.HINGLISH: "Welcome to your AI-powered career guide.",
    },
    "assessment_description": {
        Language.ENGLISH: "Take a psychological assessment to discover your strengths.",
        Language.HINDI: "अपनी ताकतों को जानने के लिए मनोवैज्ञानिक आकलन करें।",
        Language.HINGLISH: "Take a psychological assessment to discover your strengths.",
    },
    "resume_desc": {
        Language.ENGLISH: "Analyze your resume for insights and improvements.",
        Language.HINDI: "अपने रिज्यूमे का विश्लेषण करें और सुधार जानें।",
        Language.HINGLISH: "Analyze your resume for insights and improvements.",
    },
    "chat_desc": {
        Language.ENGLISH: "Chat with the AI career advisor.",
        Language.HINDI: "एआई करियर सलाहकार से चैट करें।",
        Language.HINGLISH: "Chat with the AI career advisor.",
    },
    "recommendations_desc": {
        Language.ENGLISH: "Personalized career recommendations.",
        Language.HINDI: "व्यक्तिगत करियर सिफारिशें।",
        Language.HINGLISH: "Personalized career recommendations.",
    },
    "resources_desc": {
        Language.ENGLISH: "Curated learning resources.",
        Language.HINDI: "चयनित शिक्षण संसाधन।",
        Language.HINGLISH: "Curated learning resources.",
    },
    "profile": {
        Language.ENGLISH: "Profile",
        Language.HINDI: "प्रोफ़ाइल",
        Language.HINGLISH: "Profile",
    },
    "profile_desc": {
        Language.ENGLISH: "View and edit your profile.",
        Language.HINDI: "अपनी प्रोफ़ाइल देखें और संपादित करें।",
        Language.HINGLISH: "View and edit your profile.",
    },
    "ai_career_advisor": {
        Language.ENGLISH: "AI Career Advisor",
        Language.HINDI: "एआई करियर सलाहकार",
        Language.HINGLISH: "AI Career Advisor",
    },
    "user_account": {
        Language.ENGLISH: "User Account",
        Language.HINDI: "यूज़र अकाउंट",
        Language.HINGLISH: "User Account",
    },
    "login_prompt": {
        Language.ENGLISH: "Login to save your progress",
        Language.HINDI: "अपनी प्रगति सहेजने के लिए लॉगिन करें",
        Language.HINGLISH: "Login to save your progress",
    },
    "login_register": {
        Language.ENGLISH: "Login/Register",
        Language.HINDI: "लॉगिन/रजिस्टर",
        Language.HINGLISH: "Login/Register",
    },
    "login_required": {
        Language.ENGLISH: "Login required",
        Language.HINDI: "लॉगिन आवश्यक",
        Language.HINGLISH: "Login required",
    },
    "language": {
        Language.ENGLISH: "Language",
        Language.HINDI: "भाषा",
        Language.HINGLISH: "Language",
    },
    "navigation": {
        Language.ENGLISH: "Navigation",
        Language.HINDI: "नेविगेशन",
        Language.HINGLISH: "Navigation",
    },
    "choose_language": {
        Language.ENGLISH: "Choose language:",
        Language.HINDI: "भाषा चुनें:",
        Language.HINGLISH: "Choose language:",
    },
    "quick_actions": {
        Language.ENGLISH: "Quick Actions",
        Language.HINDI: "त्वरित क्रियाएँ",
        Language.HINGLISH: "Quick Actions",
    },
    "take_assessment": {
        Language.ENGLISH: "Take Assessment",
        Language.HINDI: "आकलन करें",
        Language.HINGLISH: "Take Assessment",
    },
    "ask_ai": {
        Language.ENGLISH: "Ask AI",
        Language.HINDI: "AI से पूछें",
        Language.HINGLISH: "Ask AI",
    },
    "analyze_resume": {
        Language.ENGLISH: "Analyze Resume",
        Language.HINDI: "रिज्यूमे विश्लेषण",
        Language.HINGLISH: "Analyze Resume",
    },
    "help_support": {
        Language.ENGLISH: "Help & Support",
        Language.HINDI: "सहायता और समर्थन",
        Language.HINGLISH: "Help & Support",
    },
    "need_help": {
        Language.ENGLISH: "Need Help?",
        Language.HINDI: "मदद चाहिए?",
        Language.HINGLISH: "Need Help?",
    },
    "contact_support": {
        Language.ENGLISH: "Contact Support",
        Language.HINDI: "सपोर्ट से संपर्क करें",
        Language.HINGLISH: "Contact Support",
    },
    "available_24_7": {
        Language.ENGLISH: "Available 24/7",
        Language.HINDI: "24/7 उपलब्ध",
        Language.HINGLISH: "Available 24/7",
    },
    "useful_links": {
        Language.ENGLISH: "Useful Links",
        Language.HINDI: "उपयोगी लिंक",
        Language.HINGLISH: "Useful Links",
    },
    "app_info": {
        Language.ENGLISH: "App Information",
        Language.HINDI: "ऐप जानकारी",
        Language.HINGLISH: "App Information",
    },
    "last_updated": {
        Language.ENGLISH: "Last Updated",
        Language.HINDI: "आखिरी अपडेट",
        Language.HINGLISH: "Last Updated",
    },
    "today": {
        Language.ENGLISH: "Today",
        Language.HINDI: "आज",
        Language.HINGLISH: "Today",
    },
    "status": {
        Language.ENGLISH: "Status",
        Language.HINDI: "स्थिति",
        Language.HINGLISH: "Status",
    },
    "online": {
        Language.ENGLISH: "Online",
        Language.HINDI: "ऑनलाइन",
        Language.HINGLISH: "Online",
    },
    "users_online": {
        Language.ENGLISH: "Users Online",
        Language.HINDI: "ऑनलाइन उपयोगकर्ता",
        Language.HINGLISH: "Users Online",
    },
    "key_features": {
        Language.ENGLISH: "Key Features",
        Language.HINDI: "मुख्य विशेषताएँ",
        Language.HINGLISH: "Key Features",
    },
    "assessment_desc": {
        Language.ENGLISH: "Scientifically designed assessment to discover your strengths.",
        Language.HINDI: "आपकी ताकतों को खोजने के लिए वैज्ञानिक रूप से डिज़ाइन किया गया आकलन।",
        Language.HINGLISH: "Scientifically designed assessment to discover your strengths.",
    },
    "chat_now": {
        Language.ENGLISH: "Chat Now",
        Language.HINDI: "अभी चैट करें",
        Language.HINGLISH: "Chat Now",
    },
    "success_stories": {
        Language.ENGLISH: "Success Stories",
        Language.HINDI: "सफलता की कहानियाँ",
        Language.HINGLISH: "Success Stories",
    },
    "testimonial_1": {
        Language.ENGLISH: "Margadarsaka helped me find my ideal career path!",
        Language.HINDI: "मार्गदर्शक ने मुझे मेरी आदर्श करियर राह खोजने में मदद की!",
        Language.HINGLISH: "Margadarsaka helped me find my ideal career path!",
    },
    "testimonial_2": {
        Language.ENGLISH: "The AI insights were spot-on and culturally relevant.",
        Language.HINDI: "एआई अंतर्दृष्टि सटीक और सांस्कृतिक रूप से प्रासंगिक थीं।",
        Language.HINGLISH: "The AI insights were spot-on and culturally relevant.",
    },
    "ready_to_start": {
        Language.ENGLISH: "Ready to start your journey?",
        Language.HINDI: "क्या आप अपनी यात्रा शुरू करने के लिए तैयार हैं?",
        Language.HINGLISH: "Ready to start your journey?",
    },
    "cta_message": {
        Language.ENGLISH: "Take the assessment and get personalized guidance.",
        Language.HINDI: "आकलन करें और व्यक्तिगत मार्गदर्शन प्राप्त करें।",
        Language.HINGLISH: "Take the assessment and get personalized guidance.",
    },
    "get_started": {
        Language.ENGLISH: "Get Started",
        Language.HINDI: "शुरू करें",
        Language.HINGLISH: "Get Started",
    },
    "made_with_love": {
        Language.ENGLISH: "Made with ❤️ in India",
        Language.HINDI: "भारत में ❤️ के साथ बनाया गया",
        Language.HINGLISH: "Made with ❤️ in India",
    },
    "privacy": {
        Language.ENGLISH: "Privacy",
        Language.HINDI: "गोपनीयता",
        Language.HINGLISH: "Privacy",
    },
    "terms": {
        Language.ENGLISH: "Terms",
        Language.HINDI: "नियम",
        Language.HINGLISH: "Terms",
    },
    "support": {
        Language.ENGLISH: "Support",
        Language.HINDI: "सहायता",
        Language.HINGLISH: "Support",
    },
    # Authentication
    "login": {
        Language.ENGLISH: "Login",
        Language.HINDI: "लॉग इन",
        Language.HINGLISH: "Login",
    },
    "register": {
        Language.ENGLISH: "Register",
        Language.HINDI: "पंजीकरण",
        Language.HINGLISH: "Register",
    },
    "logout": {
        Language.ENGLISH: "Logout",
        Language.HINDI: "लॉग आउट",
        Language.HINGLISH: "Logout",
    },
    "email": {
        Language.ENGLISH: "Email",
        Language.HINDI: "ईमेल",
        Language.HINGLISH: "Email",
    },
    "password": {
        Language.ENGLISH: "Password",
        Language.HINDI: "पासवर्ड",
        Language.HINGLISH: "Password",
    },
    "full_name": {
        Language.ENGLISH: "Full Name",
        Language.HINDI: "पूरा नाम",
        Language.HINGLISH: "Full Name",
    },
    "confirm_password": {
        Language.ENGLISH: "Confirm Password",
        Language.HINDI: "पासवर्ड की पुष्टि करें",
        Language.HINGLISH: "Confirm Password",
    },
    "sign_in": {
        Language.ENGLISH: "Sign In",
        Language.HINDI: "साइन इन",
        Language.HINGLISH: "Sign In",
    },
    "sign_up": {
        Language.ENGLISH: "Sign Up",
        Language.HINDI: "साइन अप",
        Language.HINGLISH: "Sign Up",
    },
    # Welcome Messages
    "welcome_message": {
        Language.ENGLISH: "Welcome to Margadarsaka! Get personalized career guidance with psychological profiling, resume analysis, and AI-powered recommendations tailored for the Indian job market.",
        Language.HINDI: "मार्गदर्शक में आपका स्वागत है! भारतीय नौकरी बाजार के लिए तैयार किए गए मनोवैज्ञानिक प्रोफाइलिंग, रिज्यूमे विश्लेषण और एआई-संचालित सिफारिशों के साथ व्यक्तिगत करियर मार्गदर्शन प्राप्त करें।",
        Language.HINGLISH: "Margadarsaka mein aapka swagat hai! Indian job market ke liye tailored psychological profiling, resume analysis aur AI-powered recommendations ke saath personalized career guidance paayiye.",
    },
    "welcome_user": {
        Language.ENGLISH: "Welcome, {name}!",
        Language.HINDI: "स्वागत है, {name}!",
        Language.HINGLISH: "Welcome, {name}!",
    },
    # Assessment
    "start_assessment": {
        Language.ENGLISH: "Start Assessment",
        Language.HINDI: "मूल्यांकन शुरू करें",
        Language.HINGLISH: "Assessment Start Kariye",
    },
    "question": {
        Language.ENGLISH: "Question",
        Language.HINDI: "प्रश्न",
        Language.HINGLISH: "Question",
    },
    "next": {
        Language.ENGLISH: "Next",
        Language.HINDI: "अगला",
        Language.HINGLISH: "Next",
    },
    "previous": {
        Language.ENGLISH: "Previous",
        Language.HINDI: "पिछला",
        Language.HINGLISH: "Previous",
    },
    "submit": {
        Language.ENGLISH: "Submit",
        Language.HINDI: "जमा करें",
        Language.HINGLISH: "Submit",
    },
    "skip": {
        Language.ENGLISH: "Skip",
        Language.HINDI: "छोड़ें",
        Language.HINGLISH: "Skip",
    },
    # Chat Interface
    "type_message": {
        Language.ENGLISH: "Type your message here...",
        Language.HINDI: "यहाँ अपना संदेश लिखें...",
        Language.HINGLISH: "Yahan apna message likhiye...",
    },
    "send": {Language.ENGLISH: "Send", Language.HINDI: "भेजें", Language.HINGLISH: "Send"},
    "ai_thinking": {
        Language.ENGLISH: "AI is thinking...",
        Language.HINDI: "एआई सोच रहा है...",
        Language.HINGLISH: "AI soch raha hai...",
    },
    # Career Fields (Indian Context)
    "engineering": {
        Language.ENGLISH: "Engineering",
        Language.HINDI: "इंजीनियरिंग",
        Language.HINGLISH: "Engineering",
    },
    "medicine": {
        Language.ENGLISH: "Medicine",
        Language.HINDI: "चिकित्सा",
        Language.HINGLISH: "Medicine",
    },
    "information_technology": {
        Language.ENGLISH: "Information Technology",
        Language.HINDI: "सूचना प्रौद्योगिकी",
        Language.HINGLISH: "Information Technology",
    },
    "civil_services": {
        Language.ENGLISH: "Civil Services",
        Language.HINDI: "सिविल सेवाएं",
        Language.HINGLISH: "Civil Services",
    },
    "business_management": {
        Language.ENGLISH: "Business Management",
        Language.HINDI: "व्यापार प्रबंधन",
        Language.HINGLISH: "Business Management",
    },
    "teaching": {
        Language.ENGLISH: "Teaching",
        Language.HINDI: "शिक्षण",
        Language.HINGLISH: "Teaching",
    },
    "arts_humanities": {
        Language.ENGLISH: "Arts & Humanities",
        Language.HINDI: "कला और मानविकी",
        Language.HINGLISH: "Arts & Humanities",
    },
    "commerce_finance": {
        Language.ENGLISH: "Commerce & Finance",
        Language.HINDI: "वाणिज्य और वित्त",
        Language.HINGLISH: "Commerce & Finance",
    },
    "agriculture": {
        Language.ENGLISH: "Agriculture",
        Language.HINDI: "कृषि",
        Language.HINGLISH: "Agriculture",
    },
    "defense": {
        Language.ENGLISH: "Defense",
        Language.HINDI: "रक्षा",
        Language.HINGLISH: "Defense",
    },
    # Status Messages
    "loading": {
        Language.ENGLISH: "Loading...",
        Language.HINDI: "लोड हो रहा है...",
        Language.HINGLISH: "Loading...",
    },
    "success": {
        Language.ENGLISH: "Success!",
        Language.HINDI: "सफलता!",
        Language.HINGLISH: "Success!",
    },
    "error": {
        Language.ENGLISH: "Error",
        Language.HINDI: "त्रुटि",
        Language.HINGLISH: "Error",
    },
    "warning": {
        Language.ENGLISH: "Warning",
        Language.HINDI: "चेतावनी",
        Language.HINGLISH: "Warning",
    },
    "info": {
        Language.ENGLISH: "Information",
        Language.HINDI: "जानकारी",
        Language.HINGLISH: "Information",
    },
    # Common Actions
    "save": {
        Language.ENGLISH: "Save",
        Language.HINDI: "सेव करें",
        Language.HINGLISH: "Save",
    },
    "cancel": {
        Language.ENGLISH: "Cancel",
        Language.HINDI: "रद्द करें",
        Language.HINGLISH: "Cancel",
    },
    "edit": {
        Language.ENGLISH: "Edit",
        Language.HINDI: "संपादित करें",
        Language.HINGLISH: "Edit",
    },
    "delete": {
        Language.ENGLISH: "Delete",
        Language.HINDI: "हटाएं",
        Language.HINGLISH: "Delete",
    },
    "download": {
        Language.ENGLISH: "Download",
        Language.HINDI: "डाउनलोड",
        Language.HINGLISH: "Download",
    },
    "upload": {
        Language.ENGLISH: "Upload",
        Language.HINDI: "अपलोड",
        Language.HINGLISH: "Upload",
    },
    "search": {
        Language.ENGLISH: "Search",
        Language.HINDI: "खोजें",
        Language.HINGLISH: "Search",
    },
    "filter": {
        Language.ENGLISH: "Filter",
        Language.HINDI: "फिल्टर",
        Language.HINGLISH: "Filter",
    },
    "sort": {
        Language.ENGLISH: "Sort",
        Language.HINDI: "क्रमबद्ध करें",
        Language.HINGLISH: "Sort",
    },
    # Assessment Questions (Sample)
    "personality_intro": {
        Language.ENGLISH: "Let's understand your personality traits. Please answer honestly - there are no right or wrong answers.",
        Language.HINDI: "आइए आपके व्यक्तित्व के गुणों को समझते हैं। कृपया ईमानदारी से उत्तर दें - कोई सही या गलत उत्तर नहीं है।",
        Language.HINGLISH: "Chaliye aapke personality traits ko samjhte hain. Please honestly answer kariye - koi right ya wrong answer nahi hai.",
    },
    "interests_intro": {
        Language.ENGLISH: "Now let's explore your interests and preferences.",
        Language.HINDI: "अब आइए आपकी रुचियों और प्राथमिकताओं का पता लगाते हैं।",
        Language.HINGLISH: "Ab chaliye aapki interests aur preferences explore karte hain.",
    },
    # Indian Educational Context
    "class_10": {
        Language.ENGLISH: "Class 10",
        Language.HINDI: "कक्षा 10",
        Language.HINGLISH: "Class 10",
    },
    "class_12": {
        Language.ENGLISH: "Class 12",
        Language.HINDI: "कक्षा 12",
        Language.HINGLISH: "Class 12",
    },
    "graduation": {
        Language.ENGLISH: "Graduation",
        Language.HINDI: "स्नातक",
        Language.HINGLISH: "Graduation",
    },
    "post_graduation": {
        Language.ENGLISH: "Post Graduation",
        Language.HINDI: "स्नातकोत्तर",
        Language.HINGLISH: "Post Graduation",
    },
    "diploma": {
        Language.ENGLISH: "Diploma",
        Language.HINDI: "डिप्लोमा",
        Language.HINGLISH: "Diploma",
    },
    "professional_course": {
        Language.ENGLISH: "Professional Course",
        Language.HINDI: "व्यावसायिक पाठ्यक्रम",
        Language.HINGLISH: "Professional Course",
    },
    # Indian Exam Context
    "jee": {
        Language.ENGLISH: "JEE (Joint Entrance Examination)",
        Language.HINDI: "जेईई (संयुक्त प्रवेश परीक्षा)",
        Language.HINGLISH: "JEE (Joint Entrance Examination)",
    },
    "neet": {
        Language.ENGLISH: "NEET (National Eligibility cum Entrance Test)",
        Language.HINDI: "नीट (राष्ट्रीय पात्रता सह प्रवेश परीक्षा)",
        Language.HINGLISH: "NEET (National Eligibility cum Entrance Test)",
    },
    "upsc": {
        Language.ENGLISH: "UPSC (Union Public Service Commission)",
        Language.HINDI: "यूपीएससी (संघ लोक सेवा आयोग)",
        Language.HINGLISH: "UPSC (Union Public Service Commission)",
    },
    "cat": {
        Language.ENGLISH: "CAT (Common Admission Test)",
        Language.HINDI: "कैट (सामान्य प्रवेश परीक्षा)",
        Language.HINGLISH: "CAT (Common Admission Test)",
    },
}


class I18nManager:
    """Internationalization manager for the application"""

    def __init__(self):
        self.current_language = Language.ENGLISH
        self.fallback_language = Language.ENGLISH

    def set_language(self, language: Language):
        """Set the current language"""
        self.current_language = language

        # Store in session state for persistence
        if hasattr(st, "session_state"):
            st.session_state.language = language.value

    def get_current_language(self) -> Language:
        """Get current language from session state or default"""
        if hasattr(st, "session_state") and hasattr(st.session_state, "language"):
            try:
                return Language(st.session_state.language)
            except ValueError:
                return self.current_language
        return self.current_language

    def get_text(self, key: str, **kwargs) -> str:
        """Get translated text for a key with optional formatting"""
        current_lang = self.get_current_language()

        if key not in TRANSLATIONS:
            logger.warning(f"Translation key '{key}' not found")
            return key  # Return key as fallback

        translations = TRANSLATIONS[key]

        # Try current language first
        if current_lang in translations:
            text = translations[current_lang]
        # Fall back to fallback language
        elif self.fallback_language in translations:
            text = translations[self.fallback_language]
        # Last resort: return first available translation
        else:
            text = next(iter(translations.values()))

        # Apply formatting if kwargs provided
        if kwargs:
            try:
                text = text.format(**kwargs)
            except (KeyError, ValueError) as e:
                logger.warning(f"Text formatting failed for key '{key}': {e}")

        return text

    def get_locale_config(self) -> LocaleConfig:
        """Get current locale configuration"""
        current_lang = self.get_current_language()
        return LOCALES.get(current_lang, LOCALES[Language.ENGLISH])

    def format_currency(self, amount: float) -> str:
        """Format currency according to current locale"""
        config = self.get_locale_config()
        # Format with Indian numbering system
        if amount >= 10000000:  # 1 crore
            return f"{config.currency}{amount / 10000000:.1f} Cr"
        elif amount >= 100000:  # 1 lakh
            return f"{config.currency}{amount / 100000:.1f} L"
        else:
            return f"{config.currency}{amount:,.0f}"

    def format_number(self, number: float, decimal_places: int = 0) -> str:
        """Format number according to current locale"""
        config = self.get_locale_config()
        formatted = f"{number:,.{decimal_places}f}"

        # Replace separators according to locale
        if config.decimal_separator != ".":
            formatted = formatted.replace(".", "TEMP_DECIMAL")
        if config.thousand_separator != ",":
            formatted = formatted.replace(",", config.thousand_separator)
        if config.decimal_separator != ".":
            formatted = formatted.replace("TEMP_DECIMAL", config.decimal_separator)

        return formatted

    def get_available_languages(self) -> List[Dict[str, str]]:
        """Get list of available languages"""
        return [
            {"code": lang.value, "name": config.name, "native_name": config.native_name}
            for lang, config in LOCALES.items()
        ]

    def is_rtl(self) -> bool:
        """Check if current language is right-to-left"""
        config = self.get_locale_config()
        return config.direction == "rtl"


# Global instance
_i18n_manager: Optional[I18nManager] = None


def get_i18n_manager() -> I18nManager:
    """Get or create global i18n manager instance"""
    global _i18n_manager
    if _i18n_manager is None:
        _i18n_manager = I18nManager()
    return _i18n_manager


def get_text(key: str, default: Optional[str] = None, **kwargs) -> str:
    """Convenience function to get translated text"""
    try:
        return get_i18n_manager().get_text(key, **kwargs)
    except Exception:
        # If translation fails, return default or key
        return default if default is not None else key


def set_language(language: Language):
    """Convenience function to set language"""
    get_i18n_manager().set_language(language)


def get_available_languages() -> List[Dict[str, str]]:
    """Convenience function to get available languages"""
    return get_i18n_manager().get_available_languages()


def create_language_selector(key: str = "language_selector") -> Language:
    """Create a language selector widget"""
    i18n = get_i18n_manager()
    languages = get_available_languages()

    current_lang = i18n.get_current_language()
    current_index = next(
        (i for i, lang in enumerate(languages) if lang["code"] == current_lang.value), 0
    )

    selected_index = st.selectbox(
        get_text("language"),
        range(len(languages)),
        index=current_index,
        format_func=lambda i: f"{languages[i]['native_name']} ({languages[i]['name']})",
        key=key,
    )

    selected_language = Language(languages[selected_index]["code"])

    # Update language if changed
    if selected_language != current_lang:
        set_language(selected_language)
        st.rerun()

    return selected_language


# Cultural adaptations for Indian context
INDIAN_CULTURAL_CONTEXT = {
    "greeting_times": {
        "morning": {
            Language.ENGLISH: "Good morning",
            Language.HINDI: "सुप्रभात",
            Language.HINGLISH: "Good morning",
        },
        "afternoon": {
            Language.ENGLISH: "Good afternoon",
            Language.HINDI: "नमस्कार",
            Language.HINGLISH: "Good afternoon",
        },
        "evening": {
            Language.ENGLISH: "Good evening",
            Language.HINDI: "शुभ संध्या",
            Language.HINGLISH: "Good evening",
        },
    },
    "formal_titles": {
        "sir": {
            Language.ENGLISH: "Sir",
            Language.HINDI: "श्रीमान",
            Language.HINGLISH: "Sir",
        },
        "madam": {
            Language.ENGLISH: "Madam",
            Language.HINDI: "श्रीमती",
            Language.HINGLISH: "Madam",
        },
        "ji": {Language.ENGLISH: "", Language.HINDI: "जी", Language.HINGLISH: "ji"},
    },
}


def get_cultural_greeting() -> str:
    """Get culturally appropriate greeting based on time"""
    from datetime import datetime

    current_hour = datetime.now().hour

    if 5 <= current_hour < 12:
        time_key = "morning"
    elif 12 <= current_hour < 17:
        time_key = "afternoon"
    else:
        time_key = "evening"

    i18n = get_i18n_manager()
    current_lang = i18n.get_current_language()

    return INDIAN_CULTURAL_CONTEXT["greeting_times"][time_key].get(
        current_lang,
        INDIAN_CULTURAL_CONTEXT["greeting_times"][time_key][Language.ENGLISH],
    )
