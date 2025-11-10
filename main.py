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
from appwrite.client import Client
from appwrite.services.account import Account
from appwrite.id import ID
from appwrite.exception import AppwriteException

# ============================================
# APPWRITE SETUP
# ============================================
def init_appwrite():
    """Initialize Appwrite client"""
    client = Client()
    client.set_endpoint(sl.secrets["APPWRITE_ENDPOINT"])
    client.set_project(sl.secrets["APPWRITE_PROJECT_ID"])
    
    account = Account(client)
    return client, account

# ============================================
# SESSION STATE MANAGEMENT (No cookies needed!)
# ============================================
def init_session_state():
    """Initialize session state variables"""
    if "authenticated" not in sl.session_state:
        sl.session_state.authenticated = False
    if "user_id" not in sl.session_state:
        sl.session_state.user_id = None
    if "user_name" not in sl.session_state:
        sl.session_state.user_name = None
    if "user_email" not in sl.session_state:
        sl.session_state.user_email = None
    if "auth_checked" not in sl.session_state:
        sl.session_state.auth_checked = False

def check_authentication():
    """Check if user is authenticated via Appwrite session"""
    if sl.session_state.auth_checked and sl.session_state.authenticated:
        return True, sl.session_state.user_id
    
    try:
        client, account = init_appwrite()
        user = account.get()
        
        # User is authenticated
        sl.session_state.authenticated = True
        sl.session_state.user_id = user["$id"]
        sl.session_state.user_name = user.get("name", "User")
        sl.session_state.user_email = user.get("email", "")
        sl.session_state.auth_checked = True
        
        return True, user["$id"]
    except AppwriteException:
        # Not authenticated
        sl.session_state.authenticated = False
        sl.session_state.auth_checked = True
        return False, None
    except Exception as e:
        sl.error(f"Authentication check error: {str(e)}")
        return False, None

# ============================================
# AUTHENTICATION FUNCTIONS
# ============================================
def login_page():
    """Display login page with Google OAuth"""
    sl.set_page_config(
        page_title="Margadarsaka - Login",
        page_icon="🎯",
        layout="centered"
    )
    
    # Center the content
    col1, col2, col3 = sl.columns([1, 2, 1])
    
    with col2:
        sl.title("🌟 Welcome to Margadarsaka")
        sl.markdown("### Your AI-Powered Career Guide")
        
        # Lottie animation
        url = "https://lottie.host/179fa302-85e8-4b84-86ff-d6d44b671ae2/yuf3ctwVdH.json"
        try:
            response = requests.get(url)
            animation_json = response.json()
            st_lottie(animation_json, height=200, key="login_lottie")
        except:
            pass
        
        sl.markdown("---")
        
        sl.info("👋 Sign in to get personalized career guidance")
        
        # Google Sign-In Button
        if sl.button("🔐 Sign in with Google", type="primary", use_container_width=True):
            # Generate OAuth URL
            success_url = sl.secrets.get('APP_URL', 'http://localhost:8501')
            failure_url = f"{success_url}?auth=failed"
            
            oauth_url = (
                f"{sl.secrets['APPWRITE_ENDPOINT']}/account/sessions/oauth2/google"
                f"?project={sl.secrets['APPWRITE_PROJECT_ID']}"
                f"&success={success_url}"
                f"&failure={failure_url}"
            )
            
            # Show clickable link
            sl.markdown(f"[Click here if not redirected automatically]({oauth_url})")
            
            # JavaScript redirect
            js = f"""
            <script>
                window.location.href = "{oauth_url}";
            </script>
            """
            sl.markdown(js, unsafe_allow_html=True)
        
        sl.markdown("---")
        sl.caption("🔒 Your data is secure and private")

def handle_oauth_callback():
    """Handle OAuth callback after Google sign-in"""
    # Check for auth failure in URL params
    query_params = sl.query_params
    
    if "auth" in query_params and query_params["auth"] == "failed":
        sl.error("❌ Authentication failed. Please try again.")
        if sl.button("Try Again"):
            query_params.clear()
            sl.rerun()
        return False
    
    # Try to get user session
    try:
        client, account = init_appwrite()
        user = account.get()
        
        # Store user info in session state
        sl.session_state.authenticated = True
        sl.session_state.user_id = user["$id"]
        sl.session_state.user_name = user.get("name", "User")
        sl.session_state.user_email = user.get("email", "")
        sl.session_state.auth_checked = True
        
        # Clear query params
        query_params.clear()
        
        return True
    except AppwriteException:
        return False
    except Exception:
        return False

def logout():
    """Logout user"""
    try:
        client, account = init_appwrite()
        # Delete current session
        account.delete_session('current')
    except:
        pass
    
    # Clear session state
    sl.session_state.authenticated = False
    sl.session_state.user_id = None
    sl.session_state.user_name = None
    sl.session_state.user_email = None
    sl.session_state.auth_checked = False
    
    # Clear any messages
    if "messages" in sl.session_state:
        del sl.session_state.messages
    
    sl.rerun()

# ============================================
# EXISTING FUNCTIONS (keeping them as is)
# ============================================

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
                response = client_gemini.models.generate_content(
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
    """Main application page (after authentication)"""
    
    user_name = sl.session_state.get("user_name", "User")
    
    # Setting up the page
    sl.set_page_config(
        page_title="Margadarsaka", 
        page_icon="🎯",
        layout="wide"
    )
    
    # User info and logout in sidebar
    with sl.sidebar:
        sl.markdown(f"### 👋 Welcome, {user_name}!")
        sl.markdown(f"📧 {sl.session_state.get('user_email', '')}")
        sl.markdown("---")
        if sl.button("🚪 Logout", type="secondary", use_container_width=True):
            logout()
    
    url = "https://lottie.host/179fa302-85e8-4b84-86ff-d6d44b671ae2/yuf3ctwVdH.json"
    try:
        response = requests.get(url)
        animation_json = response.json()
        st_lottie(animation_json, height=100, key="lottie1")
    except:
        pass
    
    sl.title("🏡 Home")
    active_tab = sl.radio(
        "Navigation",
        ["📊 Career Test", "🔍 Resume Analyzer", "📈 Marg AI"],
        horizontal=True,
        label_visibility="collapsed"
    )

    if active_tab == "📊 Career Test":
        display_career_test()

    elif active_tab == "🔍 Resume Analyzer":
        user_file = sl.file_uploader("Upload your resume", type=["pdf", "docx"])
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
            
            # Clean up temp file
            try:
                os.remove(temp_file_path)
            except:
                pass
                
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
        user_input = sl.chat_input("Ask Marg for guidance")
        
        # File uploader for resume
        uploaded_resume = sl.file_uploader("Or upload your resume", type=["pdf", "docx"], key="resume_uploader")
        
        if uploaded_resume:
            if uploaded_resume.type == "application/pdf":
                resume_text = extract_pdf_text(uploaded_resume)
            else:
                # Handle DOCX
                from docx import Document
                doc = Document(uploaded_resume)
                resume_text = "\n".join([para.text for para in doc.paragraphs])
        
            sl.session_state.messages.append({"role": "user", "content": "Resume Uploaded"})
            with sl.chat_message("user"):
                sl.markdown("✅ Resume Uploaded")

            # Use the full resume text for AI analysis
            prompt = "\n".join([f"{msg['role']}: {msg['content']}" for msg in sl.session_state.messages[:-1]] + 
                               [f"user: Here is my resume:\n{resume_text}"])
            
            with sl.chat_message("assistant"):
                with sl.spinner("Analyzing your resume..."):
                    response = client_gemini.models.generate_content(
                        model="gemini-2.5-flash", 
                        contents=prompt)
                assistant_reply = response.text
                sl.markdown(assistant_reply)
                sl.session_state.messages.append({"role": "assistant", "content": assistant_reply})
        
        elif user_input:
            sl.session_state.messages.append({"role": "user", "content": user_input})              
            with sl.chat_message("user"):
                sl.markdown(user_input)
            
            prompt = "\n".join([f"{msg['role']}: {msg['content']}" for msg in sl.session_state.messages])

            with sl.chat_message("assistant"):
                with sl.spinner("Thinking..."):
                    response = client_gemini.models.generate_content(
                        model="gemini-2.5-flash", 
                        contents=prompt)
                assistant_reply = response.text
                sl.markdown(assistant_reply)
                sl.session_state.messages.append({"role": "assistant", "content": assistant_reply})

# ============================================
# INITIALIZE GEMINI
# ============================================
gemini_api = sl.secrets["Gemini_API"]
client_gemini = genai.Client(api_key=gemini_api)
model_id = "gemini-2.5-flash"

# ============================================
# YOUR EXISTING CLASSES (ATSScorer, ResumeAnalyzer)
# Keep all your existing class code here - unchanged
# ============================================

class ATSScorer:
    # ... (keep all your existing code)
    pass

class ResumeAnalyzer:
    # ... (keep all your existing code)
    pass

# ============================================
# MAIN APP ENTRY POINT
# ============================================
if __name__ == "__main__":
    # Initialize session state
    init_session_state()
    
    # Check if user is coming back from OAuth
    if not sl.session_state.authenticated:
        callback_success = handle_oauth_callback()
        if callback_success:
            sl.rerun()
    
    # Check authentication status
    is_authenticated, user_id = check_authentication()
    
    # Show appropriate page
    if is_authenticated:
        main_page()
    else:
        login_page()