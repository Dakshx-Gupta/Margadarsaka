"""
AI Integration for Margadarsaka
Includes Gemini AI for intelligent recommendations and Hindi language support
"""

from typing import List, Dict, Any, Optional
import google.generativeai as genai
from deep_translator import GoogleTranslator
from .models import (
    UserProfile,
    AIRecommendation,
    CareerPath,
    LearningResource,
    ChatMessage,
    LanguagePreference,
    RIASECCode,
    MentalSkill,
)
from .psychology import TestingFramework
from .secrets import get_gemini_api_key
import json


class LanguageProcessor:
    """Handle Hindi-English translation and language processing"""

    def __init__(self):
        self.translator_hi_to_en = GoogleTranslator(source="hindi", target="english")
        self.translator_en_to_hi = GoogleTranslator(source="english", target="hindi")

    def translate_to_english(self, text: str) -> str:
        """Translate Hindi text to English"""
        try:
            return self.translator_hi_to_en.translate(text)
        except Exception as e:
            print(f"Translation error: {e}")
            return text

    def translate_to_hindi(self, text: str) -> str:
        """Translate English text to Hindi"""
        try:
            return self.translator_en_to_hi.translate(text)
        except Exception as e:
            print(f"Translation error: {e}")
            return text

    def process_message(self, message: str, target_language: LanguagePreference) -> str:
        """Process message based on target language preference"""
        if target_language == LanguagePreference.HINDI:
            return self.translate_to_hindi(message)
        elif target_language == LanguagePreference.HINGLISH:
            # For Hinglish, keep technical terms in English
            hindi_translation = self.translate_to_hindi(message)
            return self._create_hinglish(message, hindi_translation)
        else:
            return message

    def _create_hinglish(self, english_text: str, hindi_text: str) -> str:
        """Create Hinglish by mixing English and Hindi"""
        # Simple approach: keep technical terms in English
        technical_terms = [
            "data science",
            "machine learning",
            "artificial intelligence",
            "software engineer",
            "product manager",
            "startup",
            "internship",
            "resume",
            "skill",
            "career",
            "job",
        ]

        result = hindi_text
        for term in technical_terms:
            if term.lower() in english_text.lower():
                result = result.replace(self.translate_to_hindi(term), term)

        return result


class GeminiAI:
    """Gemini AI integration for intelligent career recommendations"""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or get_gemini_api_key()
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel("gemini-1.5-flash")
        else:
            self.model = None
            print("Warning: Gemini API key not provided. AI features will be limited.")

        self.language_processor = LanguageProcessor()
        self.testing_framework = TestingFramework()

    def generate_career_recommendations(
        self,
        profile: UserProfile,
        test_results: Optional[List[Dict[str, Any]]] = None,
    ) -> AIRecommendation:
        """Generate comprehensive AI-powered career recommendations"""

        if not self.model:
            return self._generate_fallback_recommendations(profile)

        try:
            # Prepare context for AI
            context = self._prepare_context(profile, test_results)

            # Generate recommendations using Gemini
            prompt = self._create_recommendation_prompt(context)
            response = self.model.generate_content(prompt)

            # Parse AI response and create structured recommendation
            ai_data = self._parse_ai_response(response.text)

            return self._create_ai_recommendation(ai_data, profile, test_results)

        except Exception as e:
            print(f"AI generation error: {e}")
            return self._generate_fallback_recommendations(profile)

    def chat_with_user(
        self,
        message: str,
        profile: UserProfile,
        chat_history: Optional[List[ChatMessage]] = None,
    ) -> str:
        """Chat with user in their preferred language"""

        if not self.model:
            return self._generate_fallback_chat_response(message, profile)

        try:
            # Translate message to English if needed
            if profile.language_preference != LanguagePreference.ENGLISH:
                english_message = self.language_processor.translate_to_english(message)
            else:
                english_message = message

            # Prepare chat context
            chat_context = self._prepare_chat_context(profile, chat_history)

            # Generate response
            prompt = f"""
            You are Margadarsaka, an AI career advisor specializing in Indian cultural context.
            
            User Profile: {self._profile_summary(profile)}
            
            Chat History: {self._format_chat_history(chat_history)}
            
            User Message: {english_message}
            
            Provide a helpful, culturally sensitive response about career guidance.
            Be empathetic and consider Indian family dynamics and cultural values.
            Keep responses conversational and supportive.
            """

            response = self.model.generate_content(prompt)

            # Translate response back to user's preferred language
            return self.language_processor.process_message(
                response.text, profile.language_preference
            )

        except Exception as e:
            print(f"Chat error: {e}")
            return self._generate_fallback_chat_response(message, profile)

    def analyze_skills_for_career_mapping(
        self, interests: List[str], mental_skills: List[MentalSkill]
    ) -> Dict[str, Any]:
        """Map interests and mental skills to potential careers (like football -> lawyer example)"""

        if not self.model:
            return self._fallback_skill_mapping(interests, mental_skills)

        try:
            prompt = f"""
            Analyze the following interests and mental skills to suggest career paths:
            
            Interests: {", ".join(interests)}
            Mental Skills: {", ".join([skill.value for skill in mental_skills])}
            
            For each interest, identify the underlying mental skills and map them to potential careers.
            For example: Football involves prediction, adrenaline management, sharp mental abilities 
            which can map to careers like Lawyer (quick thinking, strategy), Sports Analyst, etc.
            
            Consider Indian job market and cultural context.
            
            Return analysis in JSON format:
            {{
                "skill_mappings": [
                    {{
                        "interest": "football",
                        "underlying_skills": ["prediction", "strategic_thinking", "pressure_management"],
                        "career_matches": [
                            {{"career": "Lawyer", "reasoning": "Quick strategic thinking and pressure management"}},
                            {{"career": "Sports Analyst", "reasoning": "Pattern recognition and prediction skills"}}
                        ]
                    }}
                ],
                "overall_recommendations": ["career1", "career2"]
            }}
            """

            response = self.model.generate_content(prompt)
            return json.loads(response.text)

        except Exception as e:
            print(f"Skills mapping error: {e}")
            return self._fallback_skill_mapping(interests, mental_skills)

    def _prepare_context(
        self,
        profile: UserProfile,
        test_results: Optional[List[Dict[str, Any]]] = None,
    ) -> Dict[str, Any]:
        """Prepare context for AI recommendation generation"""
        context = {
            "profile": {
                "age": profile.age,
                "education": profile.education_level,
                "field_of_study": profile.field_of_study,
                "location": profile.location,
                "family_background": profile.family_background.value
                if profile.family_background
                else None,
                "financial_status": profile.financial_status.value
                if profile.financial_status
                else None,
                "interests": profile.interests,
                "skills": profile.skills,
                "goals": profile.goals,
                "experience_years": profile.experience_years,
                "parental_expectations": profile.parental_expectations,
                "cultural_values": profile.cultural_values,
            },
            "test_results": test_results or [],
            "indian_context": True,
            "language_preference": profile.language_preference.value,
        }
        return context

    def _create_recommendation_prompt(self, context: Dict[str, Any]) -> str:
        """Create AI prompt for career recommendations"""
        return f"""
        You are Margadarsaka, an expert AI career advisor specializing in the Indian job market 
        and cultural context. Analyze the following user profile and provide comprehensive career guidance.
        
        User Profile:
        {json.dumps(context["profile"], indent=2)}
        
        Psychological Test Results:
        {json.dumps(context["test_results"], indent=2)}
        
        Consider the following factors:
        1. Indian family dynamics and cultural expectations
        2. Financial background and its impact on career choices
        3. Regional job market opportunities
        4. Mental skills and psychological profile
        5. Educational system and career pathways in India
        6. Work-life balance expectations in Indian culture
        
        Provide recommendations in JSON format with:
        - 3-5 primary career paths with detailed reasoning
        - Learning resources relevant to Indian context
        - Skill development roadmap
        - Cultural considerations and family discussion points
        - Alternative career options
        - Confidence score (0-1) for recommendations
        
        Focus on practical, actionable advice that considers both individual aspirations 
        and cultural realities.
        """

    def _parse_ai_response(self, response_text: str) -> Dict[str, Any]:
        """Parse AI response and extract structured data"""
        try:
            # Try to extract JSON from response
            start_idx = response_text.find("{")
            end_idx = response_text.rfind("}") + 1
            if start_idx != -1 and end_idx != -1:
                json_str = response_text[start_idx:end_idx]
                return json.loads(json_str)
        except:
            pass

        # Fallback: return structured response from text
        return {
            "career_paths": [],
            "learning_resources": [],
            "cultural_considerations": [],
            "confidence_score": 0.7,
            "reasoning": response_text,
        }

    def _create_ai_recommendation(
        self,
        ai_data: Dict[str, Any],
        profile: UserProfile,
        test_results: Optional[List[Dict[str, Any]]],
    ) -> AIRecommendation:
        """Create structured AI recommendation from parsed data"""

        # Create career paths
        career_paths = []
        for path_data in ai_data.get("career_paths", []):
            career_path = CareerPath(
                role=path_data.get("role", "Unknown Role"),
                industry=path_data.get("industry", "General"),
                description=path_data.get("description", ""),
                score=path_data.get("score", 0.7),
                match_reason=path_data.get("reasoning", "AI recommendation"),
                required_skills=path_data.get("required_skills", []),
                mental_skills_needed=[
                    MentalSkill(skill)
                    for skill in path_data.get("mental_skills", [])
                    if skill in [s.value for s in MentalSkill]
                ],
                education_requirements=path_data.get("education_requirements", []),
                growth_potential_india=path_data.get("growth_potential", "Moderate"),
                salary_range_india=path_data.get("salary_range", "Varies"),
                job_availability=path_data.get("job_availability", "Moderate"),
                cultural_acceptance=path_data.get("cultural_acceptance", "Good"),
                entry_level_roles=path_data.get("entry_level_roles", []),
                mid_level_roles=path_data.get("mid_level_roles", []),
                senior_level_roles=path_data.get("senior_level_roles", []),
                immediate_steps=path_data.get("immediate_steps", []),
                short_term_goals=path_data.get("short_term_goals", []),
                long_term_goals=path_data.get("long_term_goals", []),
            )
            career_paths.append(career_path)

        # Create learning resources
        learning_resources = []
        for resource_data in ai_data.get("learning_resources", []):
            resource = LearningResource(
                id=f"ai_{len(learning_resources)}",
                title=resource_data.get("title", "Learning Resource"),
                url=resource_data.get("url", "#"),
                description=resource_data.get("description", ""),
                provider=resource_data.get("provider", "Various"),
                cost=resource_data.get("cost", "Free"),
                duration=resource_data.get("duration", "Self-paced"),
                difficulty_level=resource_data.get("level", "beginner"),
                resource_type=resource_data.get("type", "course"),
                tags=resource_data.get("tags", []),
                indian_relevance=True,
            )
            learning_resources.append(resource)

        return AIRecommendation(
            career_paths=career_paths,
            learning_resources=learning_resources,
            psychological_insights=ai_data.get("psychological_insights", {}),
            cultural_considerations=ai_data.get("cultural_considerations", []),
            mental_skill_development=ai_data.get("skill_development", []),
            confidence_score=ai_data.get("confidence_score", 0.7),
            reasoning=ai_data.get("reasoning", "AI-powered analysis"),
            alternative_paths=[],  # Can be populated from AI data
        )

    def _generate_fallback_recommendations(
        self, profile: UserProfile
    ) -> AIRecommendation:
        """Generate basic recommendations when AI is unavailable"""

        # Basic rule-based recommendations
        career_paths = [
            CareerPath(
                role="Software Developer",
                industry="Technology",
                description="Software development opportunities in India",
                score=0.7,
                match_reason="High demand in Indian tech sector",
                growth_potential_india="Very High",
                salary_range_india="₹4-25 LPA",
                job_availability="High",
                cultural_acceptance="Very Good",
                immediate_steps=["Learn programming", "Build projects"],
                short_term_goals=["Complete certification"],
                long_term_goals=["Senior developer role"],
            )
        ]

        learning_resources = [
            LearningResource(
                id="fallback_1",
                title="Programming Fundamentals",
                url="https://www.freecodecamp.org",
                description="Learn programming basics",
                provider="FreeCodeCamp",
                cost="Free",
                duration="3 months",
                difficulty_level="beginner",
                resource_type="course",
                indian_relevance=True,
            )
        ]

        return AIRecommendation(
            career_paths=career_paths,
            learning_resources=learning_resources,
            confidence_score=0.5,
            reasoning="Basic recommendation (AI unavailable)",
        )

    def _generate_fallback_chat_response(
        self, message: str, profile: UserProfile
    ) -> str:
        """Generate basic chat response when AI is unavailable"""
        responses = {
            "hindi": "मैं आपकी मदद करने की कोशिश कर रहा हूं। कृपया अपने करियर के लक्ष्यों के बारे में बताएं।",
            "english": "I'm here to help you with your career guidance. Please tell me more about your goals.",
            "hinglish": "Main aapki career guidance में help करने के लिए यहां हूं। Please अपने goals के बारे में बताइए।",
        }

        return responses.get(profile.language_preference.value, responses["english"])

    def _fallback_skill_mapping(
        self, interests: List[str], mental_skills: List[MentalSkill]
    ) -> Dict[str, Any]:
        """Basic skill mapping when AI is unavailable"""
        basic_mappings = {
            "football": {
                "underlying_skills": [
                    "strategic_thinking",
                    "pressure_management",
                    "quick_decision_making",
                ],
                "career_matches": [
                    {
                        "career": "Sports Management",
                        "reasoning": "Direct sports industry connection",
                    },
                    {
                        "career": "Event Management",
                        "reasoning": "Team coordination and pressure management",
                    },
                ],
            },
            "chess": {
                "underlying_skills": [
                    "strategic_planning",
                    "analytical_thinking",
                    "pattern_recognition",
                ],
                "career_matches": [
                    {
                        "career": "Business Analyst",
                        "reasoning": "Strategic thinking and pattern analysis",
                    },
                    {
                        "career": "Investment Banking",
                        "reasoning": "Strategic planning and analysis skills",
                    },
                ],
            },
        }

        skill_mappings = []
        for interest in interests:
            if interest.lower() in basic_mappings:
                mapping = basic_mappings[interest.lower()]
                mapping["interest"] = interest
                skill_mappings.append(mapping)

        return {
            "skill_mappings": skill_mappings,
            "overall_recommendations": ["Business Analyst", "Project Manager"],
        }

    def _profile_summary(self, profile: UserProfile) -> str:
        """Create a brief profile summary for chat context"""
        summary = f"Age: {profile.age}, Education: {profile.education_level}"
        if profile.interests:
            summary += f", Interests: {', '.join(profile.interests[:3])}"
        if profile.goals:
            summary += f", Goals: {', '.join(profile.goals[:2])}"
        return summary

    def _format_chat_history(
        self, chat_history: Optional[List[ChatMessage]]
    ) -> str:
        """Format chat history for AI context"""
        if not chat_history:
            return "No previous conversation"

        formatted = []
        for msg in chat_history[-5:]:  # Last 5 messages
            formatted.append(f"{msg.message_type}: {msg.message}")

        return "\n".join(formatted)

    def _prepare_chat_context(
        self, profile: UserProfile, chat_history: Optional[List[ChatMessage]]
    ) -> str:
        """Prepare context for chat AI"""
        return f"Profile: {self._profile_summary(profile)}\nHistory: {self._format_chat_history(chat_history)}"
