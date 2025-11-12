import streamlit as sl
from google import genai 
import requests
from streamlit_lottie import st_lottie
import PyPDF2

url = "https://lottie.host/b0c9c03c-2ed7-41b9-81ab-3059b116cfbc/SGfbf7WJGU.json"
response = requests.get(url)
animation_json = response.json()
st_lottie(animation_json, height=250, key="lottie1")


gemini_api = sl.secrets["Gemini_API"]
roadmap_client = genai.Client(api_key = gemini_api)
model_id = "gemini-2.5-flash"

def extract_pdf_text(uploaded_file):
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text
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
                     Tone should be Youth-friendly, motivating, Indian context
                     '''}]
         
            # Display previous messages
for msg in sl.session_state.messages[1:]:  # skip system msg
                with sl.chat_message(msg["role"]):
                    sl.markdown(msg["content"])

        # user input
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
                    response = roadmap_client.models.generate_content(
                        model="gemini-2.5-flash", 
                        contents=prompt)
                assistant_reply = response.text
                sl.markdown(assistant_reply)
                sl.session_state.messages.append({"role": "assistant", "content": assistant_reply})
