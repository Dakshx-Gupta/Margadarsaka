"""Sample career data and resources for Margadarsaka"""

# Career pathways with skills and requirements
CAREER_PATHS = {
    "software_engineer": {
        "role": "Software Engineer",
        "industry": "Technology",
        "required_skills": ["programming", "python", "javascript", "problem-solving"],
        "growth_potential": "High - Growing demand in tech industry",
        "salary_range": "$70k - $180k+",
        "next_steps": [
            "Build portfolio projects",
            "Learn frameworks",
            "Practice algorithms",
        ],
    },
    "data_scientist": {
        "role": "Data Scientist",
        "industry": "Technology/Analytics",
        "required_skills": [
            "python",
            "statistics",
            "machine-learning",
            "data-analysis",
        ],
        "growth_potential": "Very High - AI/ML revolution driving demand",
        "salary_range": "$80k - $200k+",
        "next_steps": [
            "Learn SQL and pandas",
            "Build ML projects",
            "Get familiar with cloud platforms",
        ],
    },
    "product_manager": {
        "role": "Product Manager",
        "industry": "Technology/Business",
        "required_skills": ["strategy", "communication", "analytics", "leadership"],
        "growth_potential": "High - Digital transformation needs",
        "salary_range": "$90k - $220k+",
        "next_steps": [
            "Learn product frameworks",
            "Build cross-functional skills",
            "Understand user research",
        ],
    },
    "ux_designer": {
        "role": "UX Designer",
        "industry": "Design/Technology",
        "required_skills": ["design", "user-research", "prototyping", "creativity"],
        "growth_potential": "High - User experience focus increasing",
        "salary_range": "$60k - $150k+",
        "next_steps": [
            "Build design portfolio",
            "Learn design tools",
            "Practice user research",
        ],
    },
    "marketing_specialist": {
        "role": "Digital Marketing Specialist",
        "industry": "Marketing/Business",
        "required_skills": ["marketing", "analytics", "creativity", "communication"],
        "growth_potential": "Medium-High - Digital marketing growth",
        "salary_range": "$45k - $120k+",
        "next_steps": [
            "Learn digital tools",
            "Build campaign portfolio",
            "Get certified in platforms",
        ],
    },
}

# Legal disclaimer for external resources
RESOURCES_DISCLAIMER = """
⚖️ **Legal Disclaimer**: All guidance resources provided are external third-party materials. 
These resources are curated for educational purposes and are suitable for various skill levels (beginner to advanced). 
Margadarsaka does not own, control, or guarantee the accuracy, completeness, or availability of external content. 
Users should verify information independently and use resources at their own discretion.
"""

# Roadmap.sh integration - Role-based and Skill-based roadmaps
ROADMAP_SH_BASE_URL = "https://roadmap.sh/"

ROADMAP_SH_ROADMAPS = {
    "role_based": {
        "Frontend Beginner": "frontend?r=frontend-beginner",
        "Backend Beginner": "backend?r=backend-beginner",
        "DevOps Beginner": "devops?r=devops-beginner",
        "Frontend": "frontend",
        "Backend": "backend",
        "Full Stack": "full-stack",
        "API Design": "api-design",
        "QA": "qa",
        "DevOps": "devops",
        "Android": "android",
        "iOS": "ios",
        "PostgreSQL": "postgresql-dba",
        "Software Architect": "software-architect",
        "Technical Writer": "technical-writer",
        "DevRel Engineer": "devrel",
        "Machine Learning": "mlops",
        "AI and Data Scientist": "ai-data-scientist",
        "AI Engineer": "ai-engineer",
        "AI Agents": "ai-agents",
        "Data Analyst": "data-analyst",
        "BI Analyst": "bi-analyst",
        "Data Engineer": "data-engineer",
        "MLOps": "mlops",
        "Product Manager": "product-manager",
        "Engineering Manager": "engineering-manager",
        "Client Side Game Dev.": "game-developer",
        "Server Side Game Dev.": "server-side-game-developer",
        "UX Design": "ux-design",
        "Blockchain": "blockchain",
        "Cyber Security": "cyber-security",
    },
    "skill_based": {
        "GraphQL": "graphql",
        "Git and GitHub": "git-github",
        "React": "react",
        "Vue": "vue",
        "Angular": "angular",
        "Next.js": "nextjs",
        "Spring Boot": "spring-boot",
        "ASP.NET Core": "aspnet-core",
        "JavaScript": "javascript",
        "TypeScript": "typescript",
        "Node.js": "nodejs",
        "PHP": "php",
        "C++": "cpp",
        "Go": "golang",
        "Rust": "rust",
        "Python": "python",
        "Java": "java",
        "SQL": "sql",
        "Docker": "docker",
        "Kubernetes": "kubernetes",
        "AWS": "aws",
        "Cloudflare": "cloudflare",
        "Linux": "linux",
        "Terraform": "terraform",
        "React Native": "react-native",
        "Flutter": "flutter",
        "MongoDB": "mongodb",
        "Redis": "redis",
        "Computer Science": "computer-science",
        "Data Structures": "datastructures-and-algorithms",
        "System Design": "system-design",
        "Design and Architecture": "software-design-architecture",
        "Code Review": "code-review",
        "AI Red Teaming": "ai-red-teaming",
        "Prompt Engineering": "prompt-engineering",
        "Design System": "design-system",
    },
}

# Learning resources database
RESOURCES = [
    {
        "id": "py_basics",
        "title": "Python for Beginners",
        "url": "https://docs.python.org/3/tutorial/",
        "description": "Official Python tutorial covering fundamentals",
        "tags": ["python", "programming", "beginner"],
        "level": "beginner",
        "type": "course",
        "provider": "Python.org",
        "duration": "2-3 weeks",
        "cost": "Free",
    },
    {
        "id": "ds_course",
        "title": "Data Science Fundamentals",
        "url": "https://www.kaggle.com/learn",
        "description": "Comprehensive data science learning path",
        "tags": ["data-science", "python", "machine-learning"],
        "level": "intermediate",
        "type": "course",
        "provider": "Kaggle",
        "duration": "4-6 weeks",
        "cost": "Free",
    },
    {
        "id": "pm_guide",
        "title": "Product Management Guide",
        "url": "https://www.productplan.com/learn/",
        "description": "Complete guide to product management",
        "tags": ["product-management", "strategy", "business"],
        "level": "beginner",
        "type": "article",
        "provider": "ProductPlan",
        "duration": "1-2 weeks",
        "cost": "Free",
    },
    {
        "id": "ux_design",
        "title": "UX Design Specialization",
        "url": "https://www.coursera.org/specializations/ui-ux-design",
        "description": "Comprehensive UX design program",
        "tags": ["ux-design", "design", "user-research"],
        "level": "beginner",
        "type": "course",
        "provider": "Coursera",
        "duration": "6 months",
        "cost": "$49/month",
    },
    {
        "id": "digital_marketing",
        "title": "Google Digital Marketing Course",
        "url": "https://skillshop.withgoogle.com/",
        "description": "Google's official digital marketing training",
        "tags": ["marketing", "digital-marketing", "analytics"],
        "level": "beginner",
        "type": "certification",
        "provider": "Google",
        "duration": "3-4 weeks",
        "cost": "Free",
    },
    {
        "id": "coding_bootcamp",
        "title": "Free Code Camp",
        "url": "https://www.freecodecamp.org/",
        "description": "Full-stack web development curriculum",
        "tags": ["programming", "web-development", "javascript"],
        "level": "beginner",
        "type": "course",
        "provider": "FreeCodeCamp",
        "duration": "6-12 months",
        "cost": "Free",
    },
]

# Job search resources
JOB_RESOURCES = [
    {
        "id": "linkedin_jobs",
        "title": "LinkedIn Jobs",
        "url": "https://www.linkedin.com/jobs/",
        "description": "Professional networking and job search platform",
        "tags": ["job-search", "networking"],
        "type": "job",
        "provider": "LinkedIn",
    },
    {
        "id": "indeed",
        "title": "Indeed Job Search",
        "url": "https://www.indeed.com/",
        "description": "Comprehensive job search engine",
        "tags": ["job-search"],
        "type": "job",
        "provider": "Indeed",
    },
    {
        "id": "glassdoor",
        "title": "Glassdoor",
        "url": "https://www.glassdoor.com/",
        "description": "Job search with company reviews and salary data",
        "tags": ["job-search", "salary-research"],
        "type": "job",
        "provider": "Glassdoor",
    },
]

# Mentorship platforms
MENTORSHIP_RESOURCES = [
    {
        "id": "adplist",
        "title": "ADPList",
        "url": "https://adplist.org/",
        "description": "Free mentorship platform for career growth",
        "tags": ["mentorship", "career-guidance"],
        "type": "mentor",
        "provider": "ADPList",
    },
    {
        "id": "mentorcruise",
        "title": "MentorCruise",
        "url": "https://mentorcruise.com/",
        "description": "1-on-1 mentorship with industry experts",
        "tags": ["mentorship", "career-coaching"],
        "type": "mentor",
        "provider": "MentorCruise",
    },
]


# Generate roadmap.sh resources dynamically
def get_roadmap_sh_resources():
    """Generate roadmap.sh resources from the roadmap data"""
    resources = []

    # Add role-based roadmaps
    for role, path in ROADMAP_SH_ROADMAPS["role_based"].items():
        resources.append(
            {
                "id": f"roadmap_role_{role.lower().replace(' ', '_').replace('.', '')}",
                "title": f"{role} Roadmap",
                "url": f"{ROADMAP_SH_BASE_URL}{path}",
                "description": f"Complete {role} learning roadmap with step-by-step guidance",
                "tags": ["roadmap", "career-path", role.lower().replace(" ", "-")],
                "level": "all_levels",
                "type": "roadmap",
                "provider": "roadmap.sh",
                "category": "role_based",
            }
        )

    # Add skill-based roadmaps
    for skill, path in ROADMAP_SH_ROADMAPS["skill_based"].items():
        resources.append(
            {
                "id": f"roadmap_skill_{skill.lower().replace(' ', '_').replace('.', '').replace('#', 'sharp')}",
                "title": f"{skill} Learning Path",
                "url": f"{ROADMAP_SH_BASE_URL}{path}",
                "description": f"Comprehensive {skill} learning roadmap from basics to advanced",
                "tags": [
                    "roadmap",
                    "skill-development",
                    skill.lower().replace(" ", "-"),
                ],
                "level": "all_levels",
                "type": "roadmap",
                "provider": "roadmap.sh",
                "category": "skill_based",
            }
        )

    return resources


# Combine original resources with roadmap.sh resources
def get_all_resources():
    """Get all resources including roadmap.sh roadmaps"""
    return RESOURCES + get_roadmap_sh_resources()


# Industry-specific skill mappings
SKILL_MAPPINGS = {
    "technology": [
        "programming",
        "python",
        "javascript",
        "data-analysis",
        "machine-learning",
        "cloud",
    ],
    "design": ["design", "creativity", "user-research", "prototyping", "visual-design"],
    "business": [
        "strategy",
        "communication",
        "leadership",
        "analytics",
        "project-management",
    ],
    "marketing": [
        "marketing",
        "creativity",
        "analytics",
        "communication",
        "digital-marketing",
    ],
    "data": [
        "python",
        "statistics",
        "data-analysis",
        "machine-learning",
        "sql",
        "visualization",
    ],
}
