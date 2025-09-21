"""
Resume Builder Page - AI-Powered Resume Creation
"""

import streamlit as st
from typing import Dict, List, Any, Optional
import logging

logger = logging.getLogger(__name__)

# Import components with fallbacks
try:
    from margadarsaka.ui.utils.i18n import get_text
    from margadarsaka.ui.utils.state_manager import get_state_manager
    from margadarsaka.ui.components.cards import BaseCard

    COMPONENTS_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Resume page components not available: {e}")
    COMPONENTS_AVAILABLE = False

    def get_text(key, default):
        return default


class ResumeBuilder:
    """AI-powered resume builder"""

    def __init__(self):
        self.state = get_state_manager() if COMPONENTS_AVAILABLE else None

    def render_header(self):
        """Render page header"""
        st.markdown(
            f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 2rem; border-radius: 20px; margin-bottom: 2rem; text-align: center;
                    box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);">
            <h1 style="color: white; margin: 0; font-size: 2.5rem;">
                📄 {get_text("resume_builder", "AI Resume Builder")}
            </h1>
            <p style="color: rgba(255,255,255,0.9); margin: 1rem 0 0 0; font-size: 1.2rem;">
                {get_text("resume_subtitle", "Create professional resumes tailored to your career goals")}
            </p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    def render_templates_section(self):
        """Render resume templates"""
        st.markdown(f"### 🎨 {get_text('choose_template', 'Choose a Template')}")

        templates = [
            {
                "name": get_text("classic_template", "Classic Professional"),
                "description": get_text(
                    "classic_desc",
                    "Clean, traditional layout perfect for corporate roles",
                ),
                "icon": "📋",
                "color": "#2E86AB",
            },
            {
                "name": get_text("modern_template", "Modern Creative"),
                "description": get_text(
                    "modern_desc", "Contemporary design with visual elements"
                ),
                "icon": "🎨",
                "color": "#A23B72",
            },
            {
                "name": get_text("tech_template", "Tech Focused"),
                "description": get_text(
                    "tech_desc", "Optimized for technical and IT positions"
                ),
                "icon": "💻",
                "color": "#F18F01",
            },
            {
                "name": get_text("executive_template", "Executive"),
                "description": get_text(
                    "exec_desc", "Sophisticated design for senior leadership roles"
                ),
                "icon": "👔",
                "color": "#C73E1D",
            },
        ]

        cols = st.columns(2)
        for i, template in enumerate(templates):
            with cols[i % 2]:
                with st.container():
                    st.markdown(
                        f"""
                    <div style="border: 2px solid {template["color"]}; border-radius: 10px; 
                                padding: 1rem; margin-bottom: 1rem; cursor: pointer;
                                transition: all 0.3s ease;">
                        <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 8px;">
                            <span style="font-size: 2em;">{template["icon"]}</span>
                            <h4 style="margin: 0; color: {template["color"]};">{template["name"]}</h4>
                        </div>
                        <p style="margin: 0; color: #666;">{template["description"]}</p>
                    </div>
                    """,
                        unsafe_allow_html=True,
                    )

                    if st.button(
                        f"Use {template['name']}",
                        key=f"template_{i}",
                        use_container_width=True,
                    ):
                        if self.state:
                            self.state.set("selected_template", template["name"])
                        st.success(f"✅ Selected: {template['name']}")

    def render_personal_info_form(self):
        """Render personal information form"""
        st.markdown(f"### 👤 {get_text('personal_info', 'Personal Information')}")

        col1, col2 = st.columns(2)

        with col1:
            full_name = st.text_input(
                get_text("full_name", "Full Name"), key="resume_name"
            )
            email = st.text_input(get_text("email", "Email"), key="resume_email")
            phone = st.text_input(get_text("phone", "Phone"), key="resume_phone")
            location = st.text_input(
                get_text("location", "Location"), key="resume_location"
            )

        with col2:
            linkedin = st.text_input(
                get_text("linkedin", "LinkedIn Profile"), key="resume_linkedin"
            )
            portfolio = st.text_input(
                get_text("portfolio", "Portfolio/Website"), key="resume_portfolio"
            )
            github = st.text_input(
                get_text("github", "GitHub Profile"), key="resume_github"
            )

            professional_title = st.text_input(
                get_text("professional_title", "Professional Title"),
                placeholder=get_text(
                    "title_placeholder", "e.g., Software Engineer, Marketing Manager"
                ),
                key="resume_title",
            )

        # Professional summary
        st.markdown(
            f"#### ✨ {get_text('professional_summary', 'Professional Summary')}"
        )
        summary = st.text_area(
            get_text(
                "summary_label", "Write a brief summary of your professional background"
            ),
            placeholder=get_text(
                "summary_placeholder",
                "Describe your experience, key skills, and career objectives in 2-3 sentences...",
            ),
            height=100,
            key="resume_summary",
        )

        return {
            "full_name": full_name,
            "email": email,
            "phone": phone,
            "location": location,
            "linkedin": linkedin,
            "portfolio": portfolio,
            "github": github,
            "professional_title": professional_title,
            "summary": summary,
        }

    def render_experience_section(self):
        """Render work experience section"""
        st.markdown(f"### 💼 {get_text('work_experience', 'Work Experience')}")

        # Initialize experience entries
        if "experience_entries" not in st.session_state:
            st.session_state.experience_entries = [{}]

        experiences = []

        for i, exp in enumerate(st.session_state.experience_entries):
            with st.expander(
                f"{get_text('experience', 'Experience')} {i + 1}", expanded=True
            ):
                col1, col2 = st.columns(2)

                with col1:
                    job_title = st.text_input(
                        get_text("job_title", "Job Title"), key=f"exp_title_{i}"
                    )
                    company = st.text_input(
                        get_text("company", "Company"), key=f"exp_company_{i}"
                    )
                    start_date = st.date_input(
                        get_text("start_date", "Start Date"), key=f"exp_start_{i}"
                    )

                with col2:
                    location = st.text_input(
                        get_text("job_location", "Location"), key=f"exp_location_{i}"
                    )
                    employment_type = st.selectbox(
                        get_text("employment_type", "Employment Type"),
                        [
                            get_text("full_time", "Full-time"),
                            get_text("part_time", "Part-time"),
                            get_text("contract", "Contract"),
                            get_text("internship", "Internship"),
                        ],
                        key=f"exp_type_{i}",
                    )

                    current_job = st.checkbox(
                        get_text("current_position", "Current Position"),
                        key=f"exp_current_{i}",
                    )
                    if not current_job:
                        end_date = st.date_input(
                            get_text("end_date", "End Date"), key=f"exp_end_{i}"
                        )
                    else:
                        end_date = None

                # Job description
                description = st.text_area(
                    get_text("job_description", "Job Description & Achievements"),
                    placeholder=get_text(
                        "desc_placeholder",
                        "Describe your responsibilities and achievements...",
                    ),
                    height=100,
                    key=f"exp_desc_{i}",
                )

                # Key achievements
                achievements = st.text_area(
                    get_text("key_achievements", "Key Achievements (one per line)"),
                    placeholder=get_text(
                        "achievements_placeholder",
                        "• Increased sales by 25%\n• Led team of 5 developers\n• Implemented new process that saved $50K annually",
                    ),
                    height=80,
                    key=f"exp_achievements_{i}",
                )

                if st.button(
                    get_text("remove_experience", "Remove This Experience"),
                    key=f"remove_exp_{i}",
                ):
                    st.session_state.experience_entries.pop(i)
                    st.rerun()

                experiences.append(
                    {
                        "job_title": job_title,
                        "company": company,
                        "location": location,
                        "employment_type": employment_type,
                        "start_date": start_date,
                        "end_date": end_date,
                        "current_job": current_job,
                        "description": description,
                        "achievements": achievements,
                    }
                )

        # Add new experience button
        if st.button(
            f"➕ {get_text('add_experience', 'Add Another Experience')}",
            type="secondary",
        ):
            st.session_state.experience_entries.append({})
            st.rerun()

        return experiences

    def render_education_section(self):
        """Render education section"""
        st.markdown(f"### 🎓 {get_text('education', 'Education')}")

        # Initialize education entries
        if "education_entries" not in st.session_state:
            st.session_state.education_entries = [{}]

        education = []

        for i, edu in enumerate(st.session_state.education_entries):
            with st.expander(
                f"{get_text('education_entry', 'Education')} {i + 1}", expanded=True
            ):
                col1, col2 = st.columns(2)

                with col1:
                    degree = st.text_input(
                        get_text("degree", "Degree"), key=f"edu_degree_{i}"
                    )
                    institution = st.text_input(
                        get_text("institution", "Institution"),
                        key=f"edu_institution_{i}",
                    )
                    graduation_year = st.number_input(
                        get_text("graduation_year", "Graduation Year"),
                        min_value=1950,
                        max_value=2030,
                        key=f"edu_year_{i}",
                    )

                with col2:
                    field_of_study = st.text_input(
                        get_text("field_of_study", "Field of Study"),
                        key=f"edu_field_{i}",
                    )
                    gpa = st.text_input(
                        get_text("gpa", "GPA (optional)"), key=f"edu_gpa_{i}"
                    )
                    honors = st.text_input(
                        get_text("honors", "Honors/Awards (optional)"),
                        key=f"edu_honors_{i}",
                    )

                if st.button(
                    get_text("remove_education", "Remove This Education"),
                    key=f"remove_edu_{i}",
                ):
                    st.session_state.education_entries.pop(i)
                    st.rerun()

                education.append(
                    {
                        "degree": degree,
                        "institution": institution,
                        "field_of_study": field_of_study,
                        "graduation_year": graduation_year,
                        "gpa": gpa,
                        "honors": honors,
                    }
                )

        if st.button(
            f"➕ {get_text('add_education', 'Add Another Education')}", type="secondary"
        ):
            st.session_state.education_entries.append({})
            st.rerun()

        return education

    def render_skills_section(self):
        """Render skills section"""
        st.markdown(f"### 🛠️ {get_text('skills', 'Skills')}")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"#### {get_text('technical_skills', 'Technical Skills')}")
            technical_skills = st.text_area(
                get_text(
                    "technical_skills_label",
                    "List your technical skills (one per line)",
                ),
                placeholder=get_text(
                    "tech_skills_placeholder", "Python\nJavaScript\nSQL\nAWS\nDocker"
                ),
                height=100,
                key="tech_skills",
            )

        with col2:
            st.markdown(f"#### {get_text('soft_skills', 'Soft Skills')}")
            soft_skills = st.text_area(
                get_text("soft_skills_label", "List your soft skills (one per line)"),
                placeholder=get_text(
                    "soft_skills_placeholder",
                    "Leadership\nCommunication\nProblem Solving\nTeam Collaboration",
                ),
                height=100,
                key="soft_skills",
            )

        # Languages
        st.markdown(f"#### 🌐 {get_text('languages', 'Languages')}")
        languages = st.text_area(
            get_text("languages_label", "Languages and proficiency levels"),
            placeholder=get_text(
                "languages_placeholder",
                "English - Native\nHindi - Fluent\nSpanish - Intermediate",
            ),
            height=60,
            key="languages",
        )

        # Certifications
        st.markdown(f"#### 🏆 {get_text('certifications', 'Certifications')}")
        certifications = st.text_area(
            get_text("cert_label", "Professional certifications (one per line)"),
            placeholder=get_text(
                "cert_placeholder",
                "AWS Certified Solutions Architect\nPMP Certification\nGoogle Analytics Certified",
            ),
            height=80,
            key="certifications",
        )

        return {
            "technical_skills": technical_skills,
            "soft_skills": soft_skills,
            "languages": languages,
            "certifications": certifications,
        }

    def render_ai_enhancement_section(self):
        """Render AI enhancement options"""
        st.markdown(f"### 🤖 {get_text('ai_enhancement', 'AI Enhancement')}")

        enhancement_options = [
            {
                "title": get_text("optimize_keywords", "Optimize for Keywords"),
                "description": get_text(
                    "keywords_desc",
                    "Add industry-specific keywords to improve ATS compatibility",
                ),
                "icon": "🔍",
            },
            {
                "title": get_text("improve_descriptions", "Improve Job Descriptions"),
                "description": get_text(
                    "descriptions_desc",
                    "Enhance job descriptions with action verbs and quantified achievements",
                ),
                "icon": "✨",
            },
            {
                "title": get_text("generate_summary", "Generate Professional Summary"),
                "description": get_text(
                    "summary_desc",
                    "Create a compelling professional summary based on your experience",
                ),
                "icon": "📝",
            },
            {
                "title": get_text("tailor_job", "Tailor for Specific Job"),
                "description": get_text(
                    "tailor_desc", "Customize resume content for a specific job posting"
                ),
                "icon": "🎯",
            },
        ]

        selected_enhancements = []

        for option in enhancement_options:
            col1, col2 = st.columns([3, 1])

            with col1:
                st.markdown(
                    f"""
                <div style="display: flex; align-items: center; gap: 12px;">
                    <span style="font-size: 1.5em;">{option["icon"]}</span>
                    <div>
                        <h4 style="margin: 0; color: var(--primary-color);">{option["title"]}</h4>
                        <p style="margin: 4px 0 0 0; color: var(--text-secondary); font-size: 0.9em;">{option["description"]}</p>
                    </div>
                </div>
                """,
                    unsafe_allow_html=True,
                )

            with col2:
                if st.checkbox(
                    get_text("enable", "Enable"),
                    key=f"ai_{option['title'].lower().replace(' ', '_')}",
                ):
                    selected_enhancements.append(option["title"])

        # Job posting input for tailoring
        if get_text("tailor_job", "Tailor for Specific Job") in selected_enhancements:
            st.markdown(f"#### {get_text('job_posting', 'Job Posting')}")
            job_posting = st.text_area(
                get_text("paste_job_posting", "Paste the job posting here"),
                placeholder=get_text(
                    "job_posting_placeholder", "Paste the complete job description..."
                ),
                height=150,
                key="job_posting",
            )
        else:
            job_posting = ""

        return selected_enhancements, job_posting

    def render_preview_and_download(self):
        """Render resume preview and download options"""
        st.markdown(f"### 👀 {get_text('preview_download', 'Preview & Download')}")

        col1, col2 = st.columns([2, 1])

        with col1:
            if st.button(
                f"🔄 {get_text('generate_resume', 'Generate Resume')}",
                type="primary",
                use_container_width=True,
            ):
                with st.spinner(get_text("generating", "Generating your resume...")):
                    # Simulate resume generation
                    import time

                    time.sleep(2)
                    st.success(
                        get_text("resume_generated", "Resume generated successfully!")
                    )

                    # Show preview
                    st.markdown("#### " + get_text("preview", "Preview"))
                    st.markdown(
                        f"""
                    <div style="border: 1px solid #ddd; border-radius: 8px; padding: 2rem; 
                                background: white; min-height: 500px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                        <div style="text-align: center; margin-bottom: 2rem;">
                            <h2 style="color: #333; margin: 0;">[Your Name]</h2>
                            <p style="color: #666; margin: 5px 0;">[Professional Title]</p>
                            <p style="color: #666; font-size: 0.9em;">[Email] | [Phone] | [Location]</p>
                        </div>
                        
                        <div style="margin-bottom: 1.5rem;">
                            <h3 style="color: #2E86AB; border-bottom: 2px solid #2E86AB; padding-bottom: 5px;">
                                {get_text("professional_summary", "Professional Summary")}
                            </h3>
                            <p style="line-height: 1.6; color: #444;">
                                [Your professional summary will appear here...]
                            </p>
                        </div>
                        
                        <div style="margin-bottom: 1.5rem;">
                            <h3 style="color: #2E86AB; border-bottom: 2px solid #2E86AB; padding-bottom: 5px;">
                                {get_text("work_experience", "Work Experience")}
                            </h3>
                            <div style="margin-bottom: 1rem;">
                                <h4 style="margin: 0; color: #333;">[Job Title] - [Company]</h4>
                                <p style="margin: 2px 0; color: #666; font-size: 0.9em;">[Dates] | [Location]</p>
                                <ul style="margin: 8px 0; color: #444;">
                                    <li>[Achievement or responsibility]</li>
                                    <li>[Achievement or responsibility]</li>
                                </ul>
                            </div>
                        </div>
                        
                        <div style="margin-bottom: 1.5rem;">
                            <h3 style="color: #2E86AB; border-bottom: 2px solid #2E86AB; padding-bottom: 5px;">
                                {get_text("education", "Education")}
                            </h3>
                            <p style="color: #444;">[Degree] in [Field] - [Institution] ([Year])</p>
                        </div>
                        
                        <div>
                            <h3 style="color: #2E86AB; border-bottom: 2px solid #2E86AB; padding-bottom: 5px;">
                                {get_text("skills", "Skills")}
                            </h3>
                            <p style="color: #444;">[Your skills will be displayed here...]</p>
                        </div>
                    </div>
                    """,
                        unsafe_allow_html=True,
                    )

        with col2:
            st.markdown("#### " + get_text("download_options", "Download Options"))

            download_options = [
                {"format": "PDF", "icon": "📄", "recommended": True},
                {"format": "Word", "icon": "📝", "recommended": False},
                {"format": "HTML", "icon": "🌐", "recommended": False},
            ]

            for option in download_options:
                label = f"{option['icon']} {option['format']}"
                if option["recommended"]:
                    label += f" ({get_text('recommended', 'Recommended')})"

                if st.button(
                    label,
                    key=f"download_{option['format'].lower()}",
                    use_container_width=True,
                ):
                    st.info(
                        f"{get_text('download_ready', 'Download ready!')} {option['format']} {get_text('format', 'format')}"
                    )

    def render(self):
        """Main render method"""
        self.render_header()

        # Create tabs for different sections
        tabs = st.tabs(
            [
                f"🎨 {get_text('templates', 'Templates')}",
                f"👤 {get_text('personal_info', 'Personal Info')}",
                f"💼 {get_text('experience', 'Experience')}",
                f"🎓 {get_text('education', 'Education')}",
                f"🛠️ {get_text('skills', 'Skills')}",
                f"🤖 {get_text('ai_enhancement', 'AI Enhancement')}",
                f"📄 {get_text('preview', 'Preview')}",
            ]
        )

        with tabs[0]:
            self.render_templates_section()

        with tabs[1]:
            personal_info = self.render_personal_info_form()

        with tabs[2]:
            experiences = self.render_experience_section()

        with tabs[3]:
            education = self.render_education_section()

        with tabs[4]:
            skills = self.render_skills_section()

        with tabs[5]:
            enhancements, job_posting = self.render_ai_enhancement_section()

        with tabs[6]:
            self.render_preview_and_download()


def show_resume_page():
    """Function to show the resume page"""
    resume_builder = ResumeBuilder()
    resume_builder.render()
