"""
Example implementation of custom components in Margadarsaka
"""

import streamlit as st
from pathlib import Path
import sys
import logging

# Add the project root to the path to import custom modules
project_root = Path(__file__).parent.parent.parent.parent.parent.parent
sys.path.append(str(project_root))

# Import the custom component
from margadarsaka.ui.components.custom_components.rating_component import rating_component

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    st.set_page_config(
        page_title="Margadarsaka - Custom Components",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("Custom Components Demo")
    st.write("This page demonstrates custom Streamlit components using JavaScript")
    
    # Example usage in a career evaluation form
    st.header("Career Satisfaction Survey")
    
    with st.form("career_survey"):
        st.write("Please rate your satisfaction with the following aspects of your career:")
        
        # Use custom rating components
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Current Role Satisfaction")
            role_rating = rating_component(key="role_rating", initial_value=3)
            
            st.subheader("Work-Life Balance")
            balance_rating = rating_component(key="balance_rating")
            
            st.subheader("Growth Opportunities")
            growth_rating = rating_component(key="growth_rating")
        
        with col2:
            st.subheader("Compensation")
            comp_rating = rating_component(key="comp_rating")
            
            st.subheader("Team Collaboration")
            team_rating = rating_component(key="team_rating")
            
            st.subheader("Overall Job Satisfaction")
            overall_rating = rating_component(key="overall_rating", max_stars=10, initial_value=5)
        
        # Additional form fields
        st.text_area("Additional comments", key="comments", height=100)
        
        # Submit button
        submitted = st.form_submit_button("Submit Ratings")
        
    # Handle form submission
    if submitted:
        st.success("Thank you for your feedback!")
        
        # Show a summary of the ratings
        st.subheader("Your Ratings Summary")
        
        # Create a horizontal bar chart
        data = {
            "Current Role": role_rating,
            "Work-Life Balance": balance_rating,
            "Growth Opportunities": growth_rating,
            "Compensation": comp_rating,
            "Team Collaboration": team_rating,
            "Overall Satisfaction": overall_rating / 2  # Scale to 5 for consistency
        }
        
        # Display as chart
        st.bar_chart(data)
        
        # Personalized recommendation based on ratings
        avg_rating = sum([role_rating, balance_rating, growth_rating, 
                          comp_rating, team_rating]) / 5
        
        if avg_rating < 2:
            st.warning("Your ratings indicate you might want to consider exploring new opportunities.")
        elif avg_rating < 4:
            st.info("Your ratings show there's room for improvement in your current role.")
        else:
            st.success("Your ratings indicate you're quite satisfied with your current position!")
            
if __name__ == "__main__":
    main()