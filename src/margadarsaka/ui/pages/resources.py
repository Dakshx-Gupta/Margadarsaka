"""
Resources Page - Integrated Learning Resources Interface
Connects backend API with resources recommendation engine
"""

import streamlit as st
import requests
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

# Import backend services
try:
    from margadarsaka.engine import CareerRecommendationEngine
    from margadarsaka.models import UserProfile, Resource
    from margadarsaka.secrets import get_api_base_url
    ENGINE_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Resources backend not available: {e}")
    ENGINE_AVAILABLE = False

class ResourcesPage:
    """Integrated resources page with backend connection"""

    def __init__(self):
        self.api_base_url = get_api_base_url() if ENGINE_AVAILABLE else "/api"
        self.engine = CareerRecommendationEngine() if ENGINE_AVAILABLE else None
        
        # Initialize session state for resources
        if "resources_filter" not in st.session_state:
            st.session_state.resources_filter = "All Resources"
        if "resources_cache" not in st.session_state:
            st.session_state.resources_cache = {}

    def render(self):
        """Render the complete resources page"""
        self.render_header()
        self.render_filters()
        self.render_resource_sections()
        self.render_disclaimer()

    def render_header(self):
        """Render modern resources page header"""
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 3rem 2rem; border-radius: 20px; margin-bottom: 2rem; text-align: center;
                    box-shadow: 0 15px 35px rgba(102, 126, 234, 0.3);">
            <h1 style="color: white; margin: 0; font-size: 3rem; font-weight: 700;">
                📚 Learning Resources Hub
            </h1>
            <p style="color: rgba(255,255,255,0.9); margin: 1rem 0 0 0; font-size: 1.3rem; font-weight: 300;">
                Discover curated learning resources, roadmaps, and career development materials
            </p>
            <div style="margin-top: 2rem;">
                <div style="background: rgba(255,255,255,0.2); padding: 1rem; border-radius: 10px; display: inline-block;">
                    <span style="color: white; font-size: 1.1rem;">
                        🎯 Personalized • 🌟 Expert-Curated • 🚀 Career-Focused
                    </span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    def render_filters(self):
        """Render resource type filters"""
        st.markdown("### 🎯 Filter Resources")
        
        col1, col2, col3 = st.columns([2, 2, 1])
        
        with col1:
            resource_type = st.selectbox(
                "Resource Type:",
                [
                    "All Resources",
                    "Learning Courses", 
                    "Career Roadmaps",
                    "Job Search",
                    "Mentorship",
                    "Skills Development"
                ],
                index=0 if st.session_state.resources_filter == "All Resources" else 0,
                key="resource_type_filter"
            )
            st.session_state.resources_filter = resource_type

        with col2:
            skill_level = st.selectbox(
                "Skill Level:",
                ["All Levels", "Beginner", "Intermediate", "Advanced"],
                key="skill_level_filter"
            )

        with col3:
            if st.button("🔄 Refresh", use_container_width=True):
                st.session_state.resources_cache.clear()
                st.rerun()

    def render_resource_sections(self):
        """Render different resource sections"""
        
        if st.session_state.resources_filter == "Career Roadmaps":
            self.render_roadmaps_section()
        else:
            # Try to get resources from API first
            resources = self.get_resources_from_api(st.session_state.resources_filter)
            
            if resources:
                self.render_resources_grid(resources)
            else:
                # Fallback to engine if API fails
                if ENGINE_AVAILABLE:
                    self.render_engine_resources()
                else:
                    self.render_fallback_resources()

    def get_resources_from_api(self, resource_type: str) -> Optional[List[Dict]]:
        """Get resources from the backend API"""
        try:
            # Check cache first
            cache_key = f"{resource_type}_{st.session_state.get('skill_level_filter', 'all')}"
            if cache_key in st.session_state.resources_cache:
                return st.session_state.resources_cache[cache_key]

            # Determine API endpoint
            if resource_type == "All Resources":
                endpoint = f"{self.api_base_url}/resources"
            elif resource_type == "Learning Courses":
                endpoint = f"{self.api_base_url}/resources/learning"
            elif resource_type == "Job Search":
                endpoint = f"{self.api_base_url}/resources/jobs"
            elif resource_type == "Mentorship":
                endpoint = f"{self.api_base_url}/resources/mentorship"
            else:
                return None

            response = requests.get(endpoint, timeout=10)
            if response.status_code == 200:
                data = response.json()
                resources = data.get("resources", [])
                
                # Filter by skill level if specified
                skill_level = st.session_state.get('skill_level_filter', 'All Levels')
                if skill_level != "All Levels":
                    resources = [r for r in resources if r.get('level', '').lower() == skill_level.lower()]
                
                # Cache the results
                st.session_state.resources_cache[cache_key] = resources
                return resources
            else:
                logger.warning(f"API request failed with status {response.status_code}")
                return None

        except Exception as e:
            logger.error(f"Error fetching resources from API: {e}")
            return None

    def render_resources_grid(self, resources: List[Dict]):
        """Render resources in a modern grid layout"""
        st.markdown(f"### 📊 Found {len(resources)} Resources")
        
        if not resources:
            st.info("No resources found for the selected filters. Try adjusting your criteria.")
            return

        # Create grid layout
        for i in range(0, len(resources), 3):
            cols = st.columns(3)
            for j, col in enumerate(cols):
                if i + j < len(resources):
                    resource = resources[i + j]
                    with col:
                        self.render_resource_card(resource)

    def render_resource_card(self, resource: Dict):
        """Render individual resource card"""
        # Determine card style based on resource type
        type_colors = {
            "course": "#4CAF50",
            "article": "#2196F3", 
            "video": "#FF9800",
            "roadmap": "#9C27B0",
            "job_board": "#F44336",
            "tool": "#607D8B"
        }
        
        color = type_colors.get(resource.get('resource_type', 'course'), "#4CAF50")
        
        st.markdown(f"""
        <div style="border: 1px solid #e0e0e0; border-radius: 15px; padding: 1.5rem; 
                    margin-bottom: 1rem; background: white; height: 280px; display: flex; flex-direction: column;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1); transition: transform 0.2s;">
            <div style="border-left: 4px solid {color}; padding-left: 1rem; margin-bottom: 1rem;">
                <h4 style="margin: 0; color: #2c3e50; font-size: 1.1rem; line-height: 1.3;">
                    {resource.get('title', 'Untitled Resource')}
                </h4>
                <span style="background: {color}; color: white; padding: 0.2rem 0.6rem; 
                            border-radius: 12px; font-size: 0.8rem; font-weight: 500;">
                    {resource.get('resource_type', 'course').replace('_', ' ').title()}
                </span>
            </div>
            
            <p style="color: #555; margin: 0 0 1rem 0; flex-grow: 1; overflow: hidden; 
                      display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical;">
                {resource.get('description', 'No description available')}
            </p>
            
            <div style="display: flex; justify-content: space-between; align-items: center; margin-top: auto;">
                <div style="font-size: 0.9rem; color: #777;">
                    <strong>Level:</strong> {resource.get('level', 'All').title()}<br>
                    <strong>Cost:</strong> {resource.get('cost', 'Free')}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Action button
        if st.button(f"🔗 View Resource", key=f"resource_{resource.get('id', hash(resource.get('title', '')))}"):
            if resource.get('url'):
                st.markdown(f"**Opening:** [{resource.get('title')}]({resource.get('url')})")
                st.balloons()
            else:
                st.warning("No URL available for this resource")

    def render_roadmaps_section(self):
        """Render career roadmaps section"""
        st.markdown("### 🗺️ Career Development Roadmaps")
        
        if ENGINE_AVAILABLE and self.engine:
            # Get roadmaps from engine
            roadmaps = self.engine.get_roadmap_resources()
            
            if roadmaps:
                # Categorize roadmaps
                role_based = [r for r in roadmaps if r.tags and 'role_based' in r.tags]
                skill_based = [r for r in roadmaps if r.tags and 'skill_based' in r.tags]
                
                tab1, tab2 = st.tabs(["🎯 Role-Based Roadmaps", "🛠️ Skill-Based Roadmaps"])
                
                with tab1:
                    if role_based:
                        self.render_roadmap_grid(role_based)
                    else:
                        st.info("Role-based roadmaps will be loaded from roadmap.sh")
                
                with tab2:
                    if skill_based:
                        self.render_roadmap_grid(skill_based)
                    else:
                        st.info("Skill-based roadmaps will be loaded from roadmap.sh")
            else:
                self.render_sample_roadmaps()
        else:
            self.render_sample_roadmaps()

    def render_roadmap_grid(self, roadmaps: List[Resource]):
        """Render roadmaps in grid format"""
        for i in range(0, len(roadmaps), 2):
            cols = st.columns(2)
            for j, col in enumerate(cols):
                if i + j < len(roadmaps):
                    roadmap = roadmaps[i + j]
                    with col:
                        st.markdown(f"""
                        <div style="border: 2px solid #9C27B0; border-radius: 15px; padding: 1.5rem; 
                                    margin-bottom: 1rem; background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);">
                            <h4 style="color: #9C27B0; margin: 0 0 1rem 0;">🗺️ {roadmap.title}</h4>
                            <p style="color: #555; margin-bottom: 1rem;">{roadmap.description}</p>
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <span style="background: #9C27B0; color: white; padding: 0.3rem 0.8rem; 
                                            border-radius: 20px; font-size: 0.9rem;">
                                    {roadmap.level.title()}
                                </span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        if st.button(f"📖 View Roadmap", key=f"roadmap_{roadmap.id}"):
                            if roadmap.url:
                                st.markdown(f"**Opening:** [{roadmap.title}]({roadmap.url})")
                            else:
                                st.info("This roadmap will be available soon!")

    def render_sample_roadmaps(self):
        """Render sample roadmaps when engine is not available"""
        sample_roadmaps = [
            {
                "title": "Frontend Developer",
                "description": "Complete roadmap to become a modern frontend developer",
                "url": "https://roadmap.sh/frontend",
                "level": "beginner"
            },
            {
                "title": "Backend Developer", 
                "description": "Comprehensive backend development learning path",
                "url": "https://roadmap.sh/backend",
                "level": "intermediate"
            },
            {
                "title": "DevOps Engineer",
                "description": "DevOps practices and tools mastery roadmap",
                "url": "https://roadmap.sh/devops", 
                "level": "advanced"
            },
            {
                "title": "Data Scientist",
                "description": "Data science and machine learning career path",
                "url": "https://roadmap.sh/data-science",
                "level": "intermediate"
            }
        ]
        
        for i in range(0, len(sample_roadmaps), 2):
            cols = st.columns(2)
            for j, col in enumerate(cols):
                if i + j < len(sample_roadmaps):
                    roadmap = sample_roadmaps[i + j]
                    with col:
                        st.markdown(f"**🗺️ {roadmap['title']}**")
                        st.markdown(roadmap['description'])
                        st.markdown(f"**Level:** {roadmap['level'].title()}")
                        st.markdown(f"🔗 [View Roadmap]({roadmap['url']})")
                        st.markdown("---")

    def render_engine_resources(self):
        """Render resources from the engine when API is unavailable"""
        st.info("🔄 Loading resources from local engine...")
        
        if not self.engine:
            self.render_fallback_resources()
            return
            
        # Create a mock user profile for resource recommendations
        mock_profile = UserProfile(
            age=25,
            location="India",
            education_level="bachelor",
            field_of_study="computer_science",
            interests=["technology", "programming"],
            skills=["python", "web_development"],
            goals=["career_growth"]
        )
        
        try:
            recommendations = self.engine.get_recommendations(mock_profile)
            if recommendations.learning_resources:
                st.markdown("### 📚 Recommended Learning Resources")
                for resource in recommendations.learning_resources:
                    with st.container():
                        st.markdown(f"**{resource.title}**")
                        st.markdown(resource.description)
                        st.markdown(f"**Provider:** {resource.provider} | **Level:** {resource.level}")
                        if resource.url:
                            st.markdown(f"🔗 [Access Resource]({resource.url})")
                        st.markdown("---")
            else:
                self.render_fallback_resources()
        except Exception as e:
            logger.error(f"Error getting resources from engine: {e}")
            self.render_fallback_resources()

    def render_fallback_resources(self):
        """Render fallback resources when both API and engine fail"""
        st.warning("⚠️ Unable to load live resources. Showing curated examples:")
        
        fallback_resources = [
            {
                "title": "Python for Everybody",
                "description": "Comprehensive Python course for beginners",
                "provider": "Coursera",
                "level": "beginner",
                "cost": "Free",
                "url": "https://www.coursera.org/specializations/python"
            },
            {
                "title": "The Complete Web Developer Course",
                "description": "Full-stack web development bootcamp",
                "provider": "Udemy", 
                "level": "intermediate",
                "cost": "$84.99",
                "url": "https://www.udemy.com/course/the-complete-web-developer-course-2/"
            },
            {
                "title": "Machine Learning Yearning",
                "description": "Practical guide to machine learning projects",
                "provider": "Andrew Ng",
                "level": "advanced", 
                "cost": "Free",
                "url": "https://www.mlyearning.org/"
            }
        ]
        
        for resource in fallback_resources:
            with st.container():
                st.markdown(f"**📖 {resource['title']}**")
                st.markdown(resource['description'])
                st.markdown(f"**Provider:** {resource['provider']} | **Level:** {resource['level']} | **Cost:** {resource['cost']}")
                st.markdown(f"🔗 [View Course]({resource['url']})")
                st.markdown("---")

    def render_disclaimer(self):
        """Render legal disclaimer"""
        st.markdown("---")
        st.markdown("""
        ### 📋 Disclaimer
        
        **Legal Notice:** All external resources are provided for educational purposes only. 
        Margadarsaka does not own, control, or guarantee the accuracy, completeness, or availability 
        of third-party content. Users should verify information independently and use resources 
        at their own discretion. We are not responsible for any issues arising from the use of external resources.
        
        **Quality Assurance:** Resources are curated based on community feedback, expert reviews, 
        and educational value. However, content quality and availability may vary.
        """)


def show_resources_page():
    """Main function to display the resources page"""
    resources_page = ResourcesPage()
    resources_page.render()


if __name__ == "__main__":
    show_resources_page()