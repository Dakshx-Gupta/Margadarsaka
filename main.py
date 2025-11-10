import streamlit as sl
from google import genai 
import requests
from streamlit_lottie import st_lottie
import PyPDF2
import os
import re
from typing import List, Dict, Any, Optional
from docx import Document
import spacy
from PyPDF2 import PdfReader
from models import ResumeAnalysis, UserProfile
from career_test import career_questions

def display_career_test():
    sl.header("📊 Career Test — Discover Your Path")

    # Initialize answers
    if "career_answers" not in sl.session_state:
        sl.session_state.career_answers = [None] * len(career_questions)

    # Display each question
    for i, q in enumerate(career_questions):
        answer = sl.radio(
            f"{i+1}. {q['question']}",
            q['options'],
            key=f"q{i}"
        )
        sl.session_state.career_answers[i] = answer

    # Submit button
    if sl.button("Submit Answers"):
        if None in sl.session_state.career_answers:
            sl.warning("Please answer all questions before submitting.")
        else:
            user_responses = "\n".join(
                f"{i+1}. {ans}" for i, ans in enumerate(sl.session_state.career_answers)
            )

            prompt = f"""
            I am a career advisor AI. Analyze the following user responses and suggest the most suitable career paths.
            Answer concisely and provide 3 career recommendations with brief explanations.
            
            User Responses:
            {user_responses}
            """
            with sl.spinner("Analyzing your responses..."):
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )
            career_suggestion = response.text
            sl.success("🎯 Recommended Careers:")
            sl.markdown(career_suggestion)

def extract_pdf_text(uploaded_file):
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text

def main_page():
    #setting up the page
    sl.set_page_config(page_title = "Margadarsaka", page_icon = r"C:\Users\tempe\OneDrive\Documents\Margdarsaka\Margadarsaka\Aldenaire.png")
    sl.logo("Aldenaire.png", size="large")
    url = "https://lottie.host/179fa302-85e8-4b84-86ff-d6d44b671ae2/yuf3ctwVdH.json"
    response = requests.get(url)
    animation_json = response.json()
    st_lottie(animation_json, height=100, key="lottie1")
    sl.title("🏡Home")
    active_tab = sl.radio(
        "Navigation",
        ["📊 Career Test", "🔍 Resume Analyzer", "📈 Marg AI"],
        horizontal=True,
        label_visibility="collapsed"
    )

    if active_tab == "📊 Career Test":
        display_career_test()

    elif active_tab == "🔍 Resume Analyzer":
        user_file = sl.file_uploader("Upload your resume", type = ["pdf", "docx"])
        if user_file is not None:
            # Save uploaded file temporarily
            temp_file_path = f"temp_resume{user_file.name}"
            with open(temp_file_path, "wb") as f:
                f.write(user_file.getbuffer())
            # Extract text using new analyzer class
            analyzer = ResumeAnalyzer()
            try:
                resume_text = analyzer.extract_text_from_file(temp_file_path)
            except Exception as e:
                sl.error(f"Error reading file: {e}")
                resume_text = None   
            if resume_text:
                # Run ATS scoring & analysis
                analysis = analyzer.analyze_resume(resume_text)        
                # Display summary
                sl.success("✅ Resume analyzed successfully!")
                sl.metric("📊 ATS Score", f"{analysis.ats_score:.1f} / 100")
            
                # Strengths
                if analysis.strengths:
                    sl.subheader("💪 Strengths")
                    for s in analysis.strengths:
                        sl.markdown(f"- {s}")
            
                # Weaknesses
                if analysis.weaknesses:  
                    sl.subheader("⚠️ Weaknesses")          
                    for w in analysis.weaknesses:
                        sl.markdown(f"- {w}")
            
                # Missing keywords
                if analysis.missing_keywords:
                    sl.subheader("🔍 Missing Keywords")
                    sl.markdown(", ".join(analysis.missing_keywords))
            
                # Formatting issues
                if analysis.formatting_issues:
                    sl.subheader("📝 Formatting Issues")
                    for f in analysis.formatting_issues:
                        sl.markdown(f"- {f}")
            
                # Project suggestions
                if analysis.project_recommendations:
                    sl.subheader("💡 Suggested Projects")
                    for p in analysis.project_recommendations:
                        sl.markdown(f"- {p}")
            
                # Skill gaps
                if analysis.skill_gaps:
                    sl.subheader("🎯 Skill Gaps")
                    for sg in analysis.skill_gaps:
                        sl.markdown(f"- {sg}")

    elif active_tab == "📈 Marg AI":
            sl.subheader("🚀 Marg — Career Pathfinder AI")
            sl.markdown(
                """
                <p style="
                    background-color: #080808; 
                    padding: 20px; 
                    border-radius: 10px; 
                    font-size: 16px;
                    line-height: 1.5;
                ">
                <strong>Welcome!</strong> Your personal career guide is here — ready to help you:<br><br>
                ✨ Discover side hustles & unconventional career paths<br>
                💡 Identify skill gaps & growth opportunities<br>
                🌏 Navigate the Indian job market with confidence<br>
                📈 Build a personal brand that gets noticed<br><br>
                Upload your resume, share your skills, and let's explore <strong>creative, practical ways to level up your career</strong>!
                </p>
                """, 
                unsafe_allow_html=True
            )
            
            if "messages" not in sl.session_state:
                sl.session_state.messages = [
                    {"role": "system", "content":
                     '''
                     You are an AI career advisor, creative skills mentor, and employment strategist. Your expertise includes helping users discover unconventional career paths, identify side hustles, and grow professionally, with a deep understanding of Indian culture, professional expectations, and market dynamics. You combine practical guidance with imaginative strategies for career growth.
                     Behavior and Approach
                     Initiate Conversation:
                     Acknowledge the user's current career situation or job search.
                     Frame it as an opportunity for self-discovery, skill growth, and experimentation.
                     Ask the user to describe their goals, current strategies, challenges, and constraints (time, finances, location, family expectations).
                     Resume Collection and Contextualization:
                     Ask for the user's resume (CV) via file upload, text paste, or link.
                     Accept additional context on skills, experiences, projects, and aspirations that may not appear on the resume.
                     Treat the resume as a starting point and combine it with the user's narrative for a holistic view.
                     Cultural Awareness:
                     Apply Indian market knowledge, including local job expectations, competitive exams, certifications, and startup culture.
                     Factor in family expectations, social norms, and regional professional etiquette.
                     Consider income potential and cost of living variations in different Indian cities when providing guidance.
                     Analysis and Recommendations
                     Skills Assessment and Gap Analysis:
                     Identify strengths and transferable skills.
                     Highlight gaps relative to the user's career goals or side-hustle potential.
                     Suggest targeted improvements: courses, certifications, micro-projects, self-study, or mentorship.
                     Point out emerging roles and sectors in India that align with their profile.
                     Side Hustle and Income Opportunities:
                     Recommend realistic and imaginative ways to monetize skills in India (freelancing, consulting, digital products, teaching, niche services).
                     Provide rough estimates of earning potential, considering Indian market rates, cost of living, and taxation.
                     Suggest low-risk experiments and actionable first steps.
                     Offer guidance on positioning oneself professionally, including personal branding for side hustles.
                     Unconventional Job Search Strategies:
                     Recommend 3-5 creative approaches beyond standard job applications:
                     Targeted Company Projects: Pitch small projects to potential employers.
                     Niche Community Engagement: Join forums, WhatsApp/Telegram groups, and industry-specific online communities.
                     Content Creation for Visibility: Share blogs, videos, or posts showcasing expertise.
                     Reverse Job Posting: Publicly describe ideal roles and invite companies to reach out.
                     Skills-Based Volunteering: Volunteer with organizations to gain experience and network.
                     Networking with a Twist: Informational interviews, mentorship, or collaborative projects.
                     Tailor each suggestion to the user's skills, goals, and Indian context.
                     Personal Branding and Presentation:
                     Advise on LinkedIn, personal websites, portfolios, GitHub, and online presence.
                     Show how to highlight unconventional experiences and side hustles effectively.
                     Suggest ways to craft a professional story connecting past experience, current skills, and future goals.
                     Behavioral and Mindset Coaching:
                     Encourage proactive, growth-oriented thinking.
                     Provide strategies to handle rejection, setbacks, or uncertainty.
                     Promote reflection and iterative improvement for career decisions.
                     Scenario Planning and Strategic Thinking:
                     Offer short-term (1-year) and long-term (5-year) career path scenarios.
                     Discuss risks, rewards, and fallback strategies for each approach.
                     Suggest stretch opportunities where the user could significantly increase skills, visibility, or income.
                     Continuous Improvement Loop:
                     Encourage tracking results and reflecting on outcomes.
                     Refine strategies based on what works and what doesn't.
                     Recommend documentation of projects and learning for portfolio building.
                     Tone and Style
                     Supportive, encouraging, and empowering.
                     Practical but imaginative, combining visionary guidance with actionable steps.
                     Focus on opportunity, growth, and creative exploration, avoiding fear or limitation.
                     '''}]
         
            # Display previous messages
            for msg in sl.session_state.messages[1:]:  # skip system msg
                with sl.chat_message(msg["role"]):
                    sl.markdown(msg["content"])

        # user input
    if active_tab == "📈 Marg AI":
        user_input = sl.chat_input("Ask Marg for guidance", accept_file = True, file_type = ["pdf", "docx"])
        if user_input:
            if user_input.files:
                uploaded_file = user_input.files[0]
                if uploaded_file.type == "application/pdf":
                    resume_text = extract_pdf_text(uploaded_file)
                
                sl.session_state.messages.append({"role": "user", "content": "Resume Uploaded"})
                with sl.chat_message("user"):
                    sl.markdown("Resume Uploaded")


                # Use the full resume text for AI analysis, but don’t display it
                prompt = "\n".join([f"{msg['role']}: {msg['content']}" for msg in sl.session_state.messages[:-1]] + 
                                   [f"user: {resume_text}"])
            
            else:
                user_text = user_input.text        
                sl.session_state.messages.append({"role": "user", "content": user_text})              
                with sl.chat_message("user"):
                    sl.markdown(user_text)
                    prompt = "\n".join([f"{msg['role']}: {msg['content']}" for msg in sl.session_state.messages])

            with sl.chat_message("assistant"):
                with sl.spinner("Thinking..."):
                    response = client.models.generate_content(
                        model="gemini-2.5-flash", 
                        contents=prompt)
                assistant_reply = response.text
                sl.markdown(assistant_reply)
                sl.session_state.messages.append({"role": "assistant", "content": assistant_reply})
        
gemini_api = sl.secrets["Gemini_API"]
client = genai.Client(api_key = gemini_api)
model_id = "gemini-2.5-flash"

class ATSScorer:
    """ATS (Applicant Tracking System) Score Calculator"""

    def __init__(self):
        self.technical_keywords = {
            "programming": [
                "python",
                "java",
                "javascript",
                "c++",
                "react",
                "angular",
                "nodejs",
                "sql",
            ],
            "data_science": [
                "machine learning",
                "data analysis",
                "pandas",
                "numpy",
                "tensorflow",
                "pytorch",
            ],
            "business": [
                "project management",
                "agile",
                "scrum",
                "leadership",
                "strategy",
                "analysis",
            ],
            "design": [
                "ui/ux",
                "figma",
                "photoshop",
                "adobe",
                "design thinking",
                "prototyping",
            ],
            "marketing": [
                "digital marketing",
                "seo",
                "sem",
                "social media",
                "content marketing",
            ],
        }

        self.action_verbs = [
            "achieved",
            "managed",
            "led",
            "developed",
            "implemented",
            "created",
            "designed",
            "optimized",
            "improved",
            "increased",
            "decreased",
            "collaborated",
            "coordinated",
        ]

        self.indian_specific_keywords = [
            "iit",
            "iim",
            "nit",
            "bits",
            "iisc",
            "gate",
            "cat",
            "jee",
            "neet",
            "tcs",
            "infosys",
            "wipro",
            "accenture",
            "cognizant",
            "hcl",
            "bangalore",
            "hyderabad",
            "pune",
            "gurgaon",
            "noida",
            "chennai",
        ]

    def calculate_ats_score(
        self, resume_text: str, target_role: Optional[str] = None
    ) -> Dict[str, Any]:
        """Calculate comprehensive ATS score"""

        scores = {
            "keyword_relevance": self._score_keyword_relevance(
                resume_text, target_role
            ),
            "formatting": self._score_formatting(resume_text),
            "content_quality": self._score_content_quality(resume_text),
            "experience_presentation": self._score_experience_presentation(resume_text),
            "education_relevance": self._score_education_relevance(resume_text),
            "indian_context": self._score_indian_context(resume_text),
        }

        # Calculate weighted overall score
        weights = {
            "keyword_relevance": 0.3,
            "formatting": 0.15,
            "content_quality": 0.2,
            "experience_presentation": 0.2,
            "education_relevance": 0.1,
            "indian_context": 0.05,
        }

        overall_score = sum(scores[key] * weights[key] for key in scores)

        return {
            "overall_score": min(overall_score * 100, 100),  # Convert to 0-100 scale
            "component_scores": scores,
            "analysis": self._generate_score_analysis(scores),
        }

    def _score_keyword_relevance(self, text: str, target_role: Optional[str]) -> float:
        """Score based on relevant keywords for target role"""
        text_lower = text.lower()

        if not target_role:
            # General technical keywords scoring
            all_keywords = []
            for category in self.technical_keywords.values():
                all_keywords.extend(category)
        else:
            # Role-specific keyword scoring
            role_lower = target_role.lower()
            relevant_categories = []

            if any(
                term in role_lower
                for term in ["software", "developer", "engineer", "programmer"]
            ):
                relevant_categories.append("programming")
            if any(
                term in role_lower for term in ["data", "scientist", "analyst", "ml"]
            ):
                relevant_categories.append("data_science")
            if any(term in role_lower for term in ["manager", "lead", "business"]):
                relevant_categories.append("business")
            if any(term in role_lower for term in ["design", "ui", "ux"]):
                relevant_categories.append("design")
            if any(term in role_lower for term in ["marketing", "digital"]):
                relevant_categories.append("marketing")

            all_keywords = []
            for category in relevant_categories:
                all_keywords.extend(self.technical_keywords.get(category, []))

        if not all_keywords:
            return 0.5  # Default score if no specific keywords

        # Count matching keywords
        matched_keywords = sum(1 for keyword in all_keywords if keyword in text_lower)
        keyword_score = min(matched_keywords / len(all_keywords), 1.0)

        return keyword_score

    def _score_formatting(self, text: str) -> float:
        """Score resume formatting and structure"""
        score = 0.0

        # Check for common sections
        sections = ["experience", "education", "skills", "projects"]
        section_count = sum(1 for section in sections if section in text.lower())
        score += (section_count / len(sections)) * 0.4

        # Check for bullet points or structured content
        if "•" in text or "-" in text or "\n" in text:
            score += 0.2

        # Check for contact information patterns
        email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        phone_pattern = r"[\+]?[1-9]?[0-9]{7,14}"

        if re.search(email_pattern, text):
            score += 0.2
        if re.search(phone_pattern, text):
            score += 0.2

        return min(score, 1.0)

    def _score_content_quality(self, text: str) -> float:
        """Score content quality based on action verbs and achievements"""
        text_lower = text.lower()

        # Count action verbs
        action_verb_count = sum(1 for verb in self.action_verbs if verb in text_lower)
        action_score = min(action_verb_count / 10, 0.4)  # Up to 0.4 for action verbs

        # Check for quantifiable achievements (numbers, percentages)
        number_pattern = r"\b\d+(?:\.\d+)?%?\b"
        numbers = re.findall(number_pattern, text)
        number_score = min(len(numbers) / 15, 0.3)  # Up to 0.3 for numbers

        # Check for project descriptions
        project_indicators = ["project", "developed", "built", "created", "designed"]
        project_score = min(
            sum(1 for indicator in project_indicators if indicator in text_lower) / 10,
            0.3,
        )

        return action_score + number_score + project_score

    def _score_experience_presentation(self, text: str) -> float:
        """Score how well experience is presented"""
        text_lower = text.lower()

        score = 0.0

        # Check for company names or work experience indicators
        experience_indicators = [
            "intern",
            "developer",
            "analyst",
            "manager",
            "engineer",
            "consultant",
        ]
        exp_count = sum(
            1 for indicator in experience_indicators if indicator in text_lower
        )
        score += min(exp_count / 5, 0.4)

        # Check for duration indicators
        duration_patterns = [
            r"\b(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)",
            r"\b\d{4}\b",
            r"\b\d+\s*(?:month|year)s?\b",
        ]

        duration_matches = sum(
            1 for pattern in duration_patterns if re.search(pattern, text_lower)
        )
        score += min(duration_matches / 6, 0.3)

        # Check for responsibility descriptions
        if len(text.split(".")) > 5:  # Multiple sentences indicate descriptions
            score += 0.3

        return min(score, 1.0)

    def _score_education_relevance(self, text: str) -> float:
        """Score education section relevance"""
        text_lower = text.lower()

        score = 0.0

        # Check for educational qualifications
        education_terms = [
            "bachelor",
            "master",
            "phd",
            "diploma",
            "degree",
            "b.tech",
            "m.tech",
            "bca",
            "mca",
            "mba",
            "engineering",
            "computer science",
        ]

        edu_count = sum(1 for term in education_terms if term in text_lower)
        score += min(edu_count / 5, 0.6)

        # Check for Indian educational institutions
        indian_edu = sum(
            1 for term in self.indian_specific_keywords[:9] if term in text_lower
        )
        score += min(indian_edu / 3, 0.4)

        return min(score, 1.0)

    def _score_indian_context(self, text: str) -> float:
        """Score relevance to Indian job market"""
        text_lower = text.lower()

        # Count Indian companies, cities, and educational institutions
        indian_count = sum(
            1 for term in self.indian_specific_keywords if term in text_lower
        )

        return min(indian_count / 5, 1.0)

    def _generate_score_analysis(self, scores: Dict[str, float]) -> Dict[str, str]:
        """Generate analysis of scores"""
        analysis = {}

        for component, score in scores.items():
            if score >= 0.8:
                analysis[component] = "Excellent"
            elif score >= 0.6:
                analysis[component] = "Good"
            elif score >= 0.4:
                analysis[component] = "Average"
            else:
                analysis[component] = "Needs Improvement"

        return analysis


class ResumeAnalyzer:
    """Complete resume analysis system"""

    def __init__(self):
        self.ats_scorer = ATSScorer()
        # Try to load spaCy model for NLP analysis
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            self.nlp = None
            print(
                "Warning: spaCy English model not found. Some features will be limited."
            )

    def analyze_resume(
        self,
        resume_content: str,
        target_role: Optional[str] = None,
        user_profile: Optional[UserProfile] = None,
    ) -> ResumeAnalysis:
        """Perform comprehensive resume analysis"""

        # Calculate ATS score
        ats_data = self.ats_scorer.calculate_ats_score(resume_content, target_role)

        # Analyze strengths and weaknesses
        strengths = self._identify_strengths(resume_content, ats_data)
        weaknesses = self._identify_weaknesses(resume_content, ats_data)

        # Find missing keywords
        missing_keywords = self._find_missing_keywords(resume_content, target_role)

        # Check formatting issues
        formatting_issues = self._check_formatting_issues(resume_content)

        # Generate suggestions
        suggestions = self._generate_suggestions(ats_data, target_role, user_profile)

        # Recommend projects
        project_recommendations = self._recommend_projects(
            resume_content, target_role, user_profile
        )

        # Identify skill gaps
        skill_gaps = self._identify_skill_gaps(
            resume_content, target_role, user_profile
        )

        return ResumeAnalysis(
            ats_score=ats_data["overall_score"],
            strengths=strengths,
            weaknesses=weaknesses,
            missing_keywords=missing_keywords,
            formatting_issues=formatting_issues,
            suggestions=suggestions,
            project_recommendations=project_recommendations,
            skill_gaps=skill_gaps,
        )

    def extract_text_from_file(self, file_path: str) -> str:
        """Extract text from PDF or DOCX files"""
        _, ext = os.path.splitext(file_path.lower())

        if ext == ".pdf":
            return self._extract_from_pdf(file_path)
        elif ext in [".docx", ".doc"]:
            return self._extract_from_docx(file_path)
        else:
            raise ValueError(f"Unsupported file format: {ext}")

    def _extract_from_pdf(self, file_path: str) -> str:
        """Extract text from PDF file"""
        text = ""
        try:
            with open(file_path, "rb") as file:
                pdf_reader = PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() or ""
        except Exception as e:
            raise ValueError(f"Error reading PDF: {str(e)}")

        return text

    def _extract_from_docx(self, file_path: str) -> str:
        """Extract text from DOCX file"""
        try:
            doc = Document(file_path)
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            return text
        except Exception as e:
            raise ValueError(f"Error reading DOCX: {str(e)}")

    def _identify_strengths(
        self, resume_content: str, ats_data: Dict[str, Any]
    ) -> List[str]:
        """Identify resume strengths"""
        strengths = []

        component_scores = ats_data["component_scores"]

        if component_scores["keyword_relevance"] >= 0.7:
            strengths.append("Strong keyword relevance for target role")

        if component_scores["formatting"] >= 0.7:
            strengths.append("Well-structured and formatted resume")

        if component_scores["content_quality"] >= 0.7:
            strengths.append("Good use of action verbs and quantifiable achievements")

        if component_scores["experience_presentation"] >= 0.7:
            strengths.append("Clear presentation of work experience")

        if component_scores["indian_context"] >= 0.5:
            strengths.append("Good relevance to Indian job market")

        # Check for specific content strengths
        if "project" in resume_content.lower():
            strengths.append("Includes project experience")

        if re.search(r"\b\d+(?:\.\d+)?%\b", resume_content):
            strengths.append("Contains quantifiable achievements")

        return strengths

    def _identify_weaknesses(
        self, resume_content: str, ats_data: Dict[str, Any]
    ) -> List[str]:
        """Identify resume weaknesses"""
        weaknesses = []

        component_scores = ats_data["component_scores"]

        if component_scores["keyword_relevance"] < 0.5:
            weaknesses.append("Lacks relevant keywords for target role")

        if component_scores["formatting"] < 0.5:
            weaknesses.append("Poor formatting and structure")

        if component_scores["content_quality"] < 0.5:
            weaknesses.append("Limited use of action verbs and achievements")

        if component_scores["experience_presentation"] < 0.5:
            weaknesses.append("Unclear work experience presentation")

        if len(resume_content) < 500:
            weaknesses.append("Resume appears too short")

        if not re.search(
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", resume_content
        ):
            weaknesses.append("Missing or unclear contact information")

        return weaknesses

    def _find_missing_keywords(
        self, resume_content: str, target_role: Optional[str]
    ) -> List[str]:
        """Find missing keywords for target role"""
        if not target_role:
            return []

        text_lower = resume_content.lower()
        role_lower = target_role.lower()

        # Determine relevant keyword categories
        missing_keywords = []

        if "software" in role_lower or "developer" in role_lower:
            programming_keywords = self.ats_scorer.technical_keywords["programming"]
            missing = [kw for kw in programming_keywords if kw not in text_lower]
            missing_keywords.extend(missing[:5])  # Top 5 missing

        if "data" in role_lower or "analyst" in role_lower:
            data_keywords = self.ats_scorer.technical_keywords["data_science"]
            missing = [kw for kw in data_keywords if kw not in text_lower]
            missing_keywords.extend(missing[:5])

        return missing_keywords

    def _check_formatting_issues(self, resume_content: str) -> List[str]:
        """Check for formatting issues"""
        issues = []

        # Check for inconsistent spacing
        if "  " in resume_content:  # Multiple spaces
            issues.append("Inconsistent spacing detected")

        # Check for missing sections
        required_sections = ["experience", "education", "skills"]
        missing_sections = [
            section
            for section in required_sections
            if section not in resume_content.lower()
        ]

        if missing_sections:
            issues.append(f"Missing sections: {', '.join(missing_sections)}")

        # Check length
        if len(resume_content) > 4000:
            issues.append("Resume may be too long for ATS systems")
        elif len(resume_content) < 800:
            issues.append("Resume may be too short")

        return issues

    def _generate_suggestions(
        self,
        ats_data: Dict[str, Any],
        target_role: Optional[str],
        user_profile: Optional[UserProfile],
    ) -> List[str]:
        """Generate improvement suggestions"""
        suggestions = []

        component_scores = ats_data["component_scores"]

        if component_scores["keyword_relevance"] < 0.6:
            suggestions.append("Add more relevant keywords for your target role")

        if component_scores["content_quality"] < 0.6:
            suggestions.append("Use more action verbs and quantify your achievements")

        if component_scores["formatting"] < 0.6:
            suggestions.append(
                "Improve resume structure with clear sections and bullet points"
            )

        suggestions.append("Tailor your resume for each job application")
        suggestions.append("Include 2-3 relevant projects with technical details")
        suggestions.append("Add a professional summary at the top")

        return suggestions

    def _recommend_projects(
        self,
        resume_content: str,
        target_role: Optional[str],
        user_profile: Optional[UserProfile],
    ) -> List[str]:
        """Recommend projects to add to resume"""
        projects = []

        if not target_role:
            return [
                "Build a portfolio website",
                "Complete an online certification project",
            ]

        role_lower = target_role.lower()

        if "software" in role_lower or "developer" in role_lower:
            projects.extend(
                [
                    "Build a full-stack web application with user authentication",
                    "Create a mobile app using React Native or Flutter",
                    "Contribute to an open-source project on GitHub",
                    "Build a REST API with database integration",
                ]
            )

        if "data" in role_lower:
            projects.extend(
                [
                    "Create a data analysis project using real-world datasets",
                    "Build a machine learning model for prediction",
                    "Develop a data visualization dashboard",
                    "Analyze social media sentiment using NLP",
                ]
            )

        if "business" in role_lower:
            projects.extend(
                [
                    "Lead a team project or volunteer initiative",
                    "Create a business analysis case study",
                    "Organize a college event or competition",
                ]
            )

        return projects[:4]  # Return top 4 suggestions

    def _identify_skill_gaps(
        self,
        resume_content: str,
        target_role: Optional[str],
        user_profile: Optional[UserProfile],
    ) -> List[str]:
        """Identify skill gaps based on role requirements"""
        skill_gaps = []

        if not target_role:
            return skill_gaps

        text_lower = resume_content.lower()
        role_lower = target_role.lower()

        # Common skills for different roles
        role_skills = {
            "software_developer": ["git", "testing", "debugging", "agile", "ci/cd"],
            "data_scientist": [
                "statistics",
                "sql",
                "visualization",
                "machine learning",
                "python",
            ],
            "product_manager": [
                "market research",
                "user stories",
                "roadmap",
                "stakeholder management",
            ],
            "business_analyst": [
                "requirements gathering",
                "process mapping",
                "stakeholder analysis",
            ],
        }

        # Determine role category
        if any(term in role_lower for term in ["software", "developer", "engineer"]):
            required_skills = role_skills["software_developer"]
        elif any(term in role_lower for term in ["data", "scientist", "analyst"]):
            required_skills = role_skills["data_scientist"]
        elif "product" in role_lower and "manager" in role_lower:
            required_skills = role_skills["product_manager"]
        elif "business" in role_lower and "analyst" in role_lower:
            required_skills = role_skills["business_analyst"]
        else:
            return skill_gaps

        # Find missing skills
        missing_skills = [skill for skill in required_skills if skill not in text_lower]
        skill_gaps.extend(missing_skills)

        return skill_gaps[:5]  # Top 5 skill gaps
main_page()