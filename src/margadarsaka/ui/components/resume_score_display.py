"""
Resume Score Display Component
Integrates custom JS components for visualizing resume scores
"""

import streamlit as st
from typing import Dict, Any, List, Optional
import logging

# Import the custom component
from .custom_components.rating_component import rating_component

logger = logging.getLogger(__name__)

def render_resume_score_section(resume_analysis: Dict[str, Any]) -> None:
    """
    Render the resume score section with interactive components
    
    Args:
        resume_analysis: Dictionary containing resume analysis results
    """
    st.header("📊 Resume Score Analysis")
    
    # Extract scores from analysis
    ats_score = resume_analysis.get("ats_score", 0)
    keyword_match = resume_analysis.get("keyword_match_percentage", 0)
    readability_score = resume_analysis.get("readability_score", 0)
    format_score = resume_analysis.get("format_score", 0)
    overall_score = resume_analysis.get("overall_score", 0)
    
    # Scale scores to 0-5 range for the rating component
    scaled_ats = min(round(ats_score * 5 / 100), 5)
    scaled_keyword = min(round(keyword_match * 5 / 100), 5)
    scaled_readability = min(round(readability_score * 5 / 100), 5)
    scaled_format = min(round(format_score * 5 / 100), 5)
    scaled_overall = min(round(overall_score * 5 / 100), 5)
    
    # Create two columns for layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("ATS Compatibility")
        st.write(f"Score: {ats_score}/100")
        # Display as read-only rating
        rating_component(key="ats_score", initial_value=scaled_ats)
        
        st.subheader("Keyword Match")
        st.write(f"Match: {keyword_match:.1f}%")
        rating_component(key="keyword_match", initial_value=scaled_keyword)
        
        st.subheader("Readability")
        st.write(f"Score: {readability_score:.1f}/100")
        rating_component(key="readability_score", initial_value=scaled_readability)
    
    with col2:
        st.subheader("Format & Structure")
        st.write(f"Score: {format_score}/100")
        rating_component(key="format_score", initial_value=scaled_format)
        
        st.subheader("Overall Rating")
        st.write(f"Score: {overall_score}/100")
        rating_component(key="overall_score", initial_value=scaled_overall, max_stars=5)
        
        # Add feedback request
        st.subheader("Rate Our Analysis")
        user_rating = rating_component(key="feedback_rating", initial_value=0)
        if user_rating > 0:
            st.success(f"Thank you for your feedback! You rated our analysis {user_rating}/5 stars.")
    
    # Display improvement recommendations
    if "recommendations" in resume_analysis and resume_analysis["recommendations"]:
        st.subheader("📝 Recommendations")
        for i, rec in enumerate(resume_analysis["recommendations"], 1):
            st.markdown(f"{i}. {rec}")

def render_skill_match_visualization(
    job_skills: List[str], 
    resume_skills: List[str]
) -> None:
    """
    Render an interactive visualization of skill matches
    
    Args:
        job_skills: List of skills from job description
        resume_skills: List of skills from resume
    """
    st.subheader("🎯 Skill Match Visualization")
    
    # Find matching skills
    matching_skills = set(job_skills).intersection(set(resume_skills))
    missing_skills = set(job_skills).difference(set(resume_skills))
    additional_skills = set(resume_skills).difference(set(job_skills))
    
    # Create columns for the visualization
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### ✅ Matching Skills")
        if matching_skills:
            for skill in matching_skills:
                st.success(skill)
        else:
            st.info("No matching skills found")
    
    with col2:
        st.markdown("### ❌ Missing Skills")
        if missing_skills:
            for skill in missing_skills:
                st.error(skill)
        else:
            st.success("No missing skills!")
    
    with col3:
        st.markdown("### 🔍 Additional Skills")
        if additional_skills:
            for skill in additional_skills:
                st.info(skill)
        else:
            st.info("No additional skills found")
    
    # Calculate match percentage
    if job_skills:
        match_percentage = len(matching_skills) / len(job_skills) * 100
        
        # Display as progress bar
        st.subheader("Overall Skill Match")
        st.progress(match_percentage / 100)
        st.write(f"{match_percentage:.1f}% of job requirements matched")