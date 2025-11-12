import streamlit as sl
from google import genai 
from fpdf import FPDF
import requests
from streamlit_lottie import st_lottie

url = "https://lottie.host/e1f2f8ef-741c-4b1d-8fc3-03df060f4667/nQh6bnynn8.json"
response = requests.get(url)
animation_json = response.json()
st_lottie(animation_json, height=200, key="lottie1")

sl.subheader("🚀 Generate a detailed roadmap for your goal")
sl.markdown(
    """
    <p style="
    background-color: #080808; 
    padding: 20px; 
    border-radius: 10px; 
    font-size: 16px;
    line-height: 1.5;
    color: white;
    ">
    <strong>Welcome!</strong> Your personal career/skill roadmap generator is here — ready to help you:<br><br>
    ✨ Discover practical way to reach your goal<br>
    💡 Identify skill gaps & growth opportunities<br>
    🌏 Navigate the Indian job market with confidence<br>
    📈 Build a personal brand that gets noticed<br><br>
    </p>
    """,
    unsafe_allow_html=True
)

gemini_api = sl.secrets["Gemini_API"]
roadmap_client = genai.Client(api_key=gemini_api)
model_id = "gemini-2.5-flash"

BASE_PROMPT = """
You are Marg, an AI Career Roadmap Architect for Indian students and professionals. 
Create a detailed yet practical roadmap tailored for the user's goal.

RULES:
- Tone: Youth-friendly, motivating, Indian context
- Structure phases with timelines and clear action steps
- No generic advice; be specific and actionable
- If experience level unclear, assume beginner

FORMAT TO FOLLOW:

**Goal Summary (2–3 lines)**  
Brief explanation of the goal and feasibility in India.

**Phase 1: Foundation (Month 1–2)**  
- Skills to learn  
- Course links (India + global; free + paid)  
- Time per week  

**Phase 2: Skill Building & Projects (Month 3–4)**  
- 3–5 project ideas  
- Tools & tech to learn  
- GitHub/portfolio work  

**Phase 3: Experience & Internships (Month 5–7)**  
- How to get internships (India-specific)  
- Resume + LinkedIn upgrades  
- Outreach templates  

**Phase 4: Personal Brand & Networking (Month 8–9)**  
- Social platforms strategy (LinkedIn, X, GitHub)  
- Proof-of-work ideas  

**Phase 5: Job Prep & Applications (Month 10–12)**  
- Interview prep  
- Mock interview resources  
- Companies to target (India + remote)  

**Alternate Paths (2–3)**  
**Salary in India**  
Beginner, intermediate, experienced  
**Bonus Accelerators**  
Books, podcasts, communities
"""


user_text = sl.chat_input("Write the job, skill, or role you want to achieve")

if user_text:

    with sl.chat_message("user"):
        sl.markdown(user_text)

    prompt = BASE_PROMPT + f"\n\nUser Goal: {user_text}\n\nGenerate the roadmap now."

    with sl.chat_message("assistant"):
        with sl.spinner("🧠 Generating the perfect roadmap for you..."):
            response = roadmap_client.models.generate_content(
                model=model_id, 
                contents=prompt
            )

        assistant_reply = response.text
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.multi_cell(0, 10, "Your Career Roadmap", align='C')
        pdf.ln(5)
        pdf.set_font("Arial", size=11)
        safe_text = assistant_reply.encode("latin-1", "replace").decode("latin-1")
        pdf.multi_cell(0, 7, txt=safe_text)

        pdf.output("Roadmap.pdf")
        with open("Roadmap.pdf", "rb") as file:
            sl.download_button(
                label="📄 Download Your Roadmap (PDF)",
                data=file,
                file_name="Career_Roadmap.pdf",
                mime="application/pdf"
            )
