import streamlit as sl
from career_test import career_questions
from google import genai
from streamlit_lottie import st_lottie
import requests

def display_career_test():
    # Lottie Animation
    url = "https://lottie.host/e5f2d1f4-bf3d-4615-9f76-7ad01529b880/9mPRniZPLk.json"
    response = requests.get(url)
    animation_json = response.json()
    st_lottie(animation_json, height=220, key="lottie2")

    sl.markdown(
        """
        <h1 style="text-align:center; color:#4CAF50; margin-top:-20px;">
            📊 Career Test — Discover Your Path
        </h1>
        <p style="text-align:center; font-size:16px; color:#d0d0d0;">
            Answer a few questions and get tailored career suggestions!
        </p>
        """, unsafe_allow_html=True
    )

    sl.write("")  # spacing

    # Initialize answers
    if "career_answers" not in sl.session_state:
        sl.session_state.career_answers = [None] * len(career_questions)

    # Display questions with card-like UI
    for i, q in enumerate(career_questions):
        with sl.container(border=True):
            sl.markdown(f"**Q{i+1}. {q['question']}**")
            answer = sl.radio(
                "",
                q['options'],
                key=f"q{i}",
                horizontal=True
            )
            sl.session_state.career_answers[i] = answer

    sl.write("")  # spacing

    # Submit button
    if sl.button("✨ Get My Career Suggestions", use_container_width=True):
        if None in sl.session_state.career_answers:
            sl.warning("⚠️ Please answer all questions before submitting.")
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

            with sl.spinner("🧠 Analyzing your responses..."):
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )

            career_suggestion = response.text
            sl.success("🎯 Recommended Careers:")
            sl.markdown(career_suggestion)


# Gemini API
gemini_api = sl.secrets["Gemini_API"]
client = genai.Client(api_key=gemini_api)
model_id = "gemini-2.5-flash"

display_career_test()
