import streamlit as sl
import requests
from streamlit_lottie import st_lottie


def home():
    sl.set_page_config(page_title = "Margadarsaka", page_icon = r"C:\Users\tempe\OneDrive\Documents\Margdarsaka\Margadarsaka\Aldenaire.png")
    sl.logo("Aldenaire.png", size="large")
    url = "https://lottie.host/179fa302-85e8-4b84-86ff-d6d44b671ae2/yuf3ctwVdH.json"
    response = requests.get(url)
    animation_json = response.json()
    st_lottie(animation_json, height=100, key="lottie1")
    sl.title(":red[MARGADARSAKA]")
    sl.subheader(":green[India's First-AI Powered Education Platform!]")
    sl.divider()
    sl.subheader(":orange[The Moat]")

    col1, col2, col3 = sl.columns(3)
    with col1:
            url = "https://lottie.host/08079a40-8ab8-46a2-b930-c0b6a867befe/0viXAHblQr.json"
            response = requests.get(url)
            animation_json = response.json()
            st_lottie(animation_json, height=200, key="lottie2")

    sl.html(
        """
        <p style= "font-size: 22px; color: orange">Margdarsaka is an AI-powered career guidance platform designed for Indian students, combining psychological
        assessments with cultural awareness. Our solutions leverages
        GenAI to provide personalized career roadmaps, addressing the
        critical gap in accessible, culturally-aware career counseling in
        our country's education ecosystem.
        <br>
        <br>

        Below are some key features of our prototype for you to explore — a glimpse of the powerful, scalable, and transformative vision we are building.
        </p>
        """
    )
    
    if sl.button("💼 Career Test"):
        sl.switch_page("pages/test.py")
    if sl.button("🔍 Resume Analyzer"):
        sl.switch_page("pages/resume.py")
    if sl.button("💻 Marg AI"):
         sl.switch_page("pages/ai.py")
    if sl.button("🛣️ Career Roadmap"):
         sl.switch_page("pages/roadmap.py")
home()
