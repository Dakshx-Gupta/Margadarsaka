from typing import List, Optional, Dict, Any, Literal
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum


class LanguagePreference(str, Enum):
    """Language preference options"""

    ENGLISH = "english"
    HINDI = "hindi"
    HINGLISH = "hinglish"


class FamilyBackground(str, Enum):
    """Family background categories relevant to Indian context"""

    BUSINESS = "business"
    GOVERNMENT = "government"
    PRIVATE_SECTOR = "private_sector"
    AGRICULTURE = "agriculture"
    EDUCATION = "education"
    HEALTHCARE = "healthcare"
    ARTS_CULTURE = "arts_culture"
    MILITARY = "military"
    OTHER = "other"


class FinancialStatus(str, Enum):
    """Financial status categories"""

    LOW_INCOME = "low_income"  # < 3 LPA
    LOWER_MIDDLE = "lower_middle"  # 3-6 LPA
    MIDDLE_CLASS = "middle_class"  # 6-15 LPA
    UPPER_MIDDLE = "upper_middle"  # 15-30 LPA
    HIGH_INCOME = "high_income"  # > 30 LPA


class RIASECCode(str, Enum):
    """Holland's RIASEC career codes"""

    REALISTIC = "realistic"  # Doers
    INVESTIGATIVE = "investigative"  # Thinkers
    ARTISTIC = "artistic"  # Creators
    SOCIAL = "social"  # Helpers
    ENTERPRISING = "enterprising"  # Persuaders
    CONVENTIONAL = "conventional"  # Organizers


class MentalSkill(str, Enum):
    """Mental and psychological skills"""

    ANALYTICAL_THINKING = "analytical_thinking"
    DEDUCTIVE_REASONING = "deductive_reasoning"
    PATTERN_RECOGNITION = "pattern_recognition"
    STRATEGIC_PLANNING = "strategic_planning"
    EMOTIONAL_INTELLIGENCE = "emotional_intelligence"
    STRESS_MANAGEMENT = "stress_management"
    DECISION_MAKING = "decision_making"
    PROBLEM_SOLVING = "problem_solving"
    CRITICAL_THINKING = "critical_thinking"
    CREATIVE_THINKING = "creative_thinking"
    MEMORY_RETENTION = "memory_retention"
    ATTENTION_TO_DETAIL = "attention_to_detail"


class UserProfile(BaseModel):
    """Enhanced user profile with psychological and cultural context"""

    # Basic Information
    name: Optional[str] = Field(None, description="User's name")
    age: Optional[int] = Field(None, ge=13, le=80, description="User's age")
    location: Optional[str] = Field(None, description="City/State in India")
    language_preference: LanguagePreference = LanguagePreference.ENGLISH

    # Educational Background
    education_level: Optional[str] = Field(None, description="Current education level")
    field_of_study: Optional[str] = Field(None, description="Field of study/major")
    academic_performance: Optional[str] = Field(
        None, description="Academic performance level"
    )

    # Cultural and Social Context
    family_background: Optional[FamilyBackground] = None
    financial_status: Optional[FinancialStatus] = None
    parental_expectations: List[str] = Field(
        default_factory=list, description="Career expectations from family"
    )
    cultural_values: List[str] = Field(
        default_factory=list, description="Important cultural values"
    )

    # Skills and Interests
    interests: List[str] = Field(
        default_factory=list, description="Personal interests and hobbies"
    )
    skills: List[str] = Field(
        default_factory=list, description="Current technical/soft skills"
    )
    mental_skills: List[MentalSkill] = Field(
        default_factory=list, description="Identified mental abilities"
    )
    goals: List[str] = Field(
        default_factory=list, description="Career goals and aspirations"
    )

    # Experience
    experience_years: Optional[float] = Field(
        None, ge=0, description="Years of relevant experience"
    )
    work_experience: List[str] = Field(
        default_factory=list, description="Previous work experiences"
    )

    # Psychological Profile
    riasec_scores: Dict[RIASECCode, float] = Field(
        default_factory=dict, description="RIASEC assessment scores"
    )
    personality_traits: Dict[str, float] = Field(
        default_factory=dict, description="Big Five personality scores"
    )
    learning_style: Optional[str] = Field(None, description="Preferred learning style")
    stress_tolerance: Optional[int] = Field(
        None, ge=1, le=10, description="Stress tolerance level (1-10)"
    )

    # Preferences
    work_environment_preferences: List[str] = Field(default_factory=list)
    geographical_mobility: Optional[bool] = Field(
        None, description="Willing to relocate"
    )
    salary_expectations: Optional[str] = Field(
        None, description="Expected salary range"
    )


class PsychologicalTest(BaseModel):
    """Psychological test structure"""

    test_id: str
    test_name: str
    test_type: Literal["riasec", "personality", "aptitude", "interest", "mental_skills"]
    questions: List[Dict[str, Any]]
    scoring_method: str
    description: str
    duration_minutes: int


class TestResponse(BaseModel):
    """User's response to a psychological test"""

    test_id: str
    user_id: Optional[str] = None
    responses: Dict[str, Any]
    scores: Dict[str, float] = Field(default_factory=dict)
    completed_at: datetime = Field(default_factory=datetime.now)


class CareerPath(BaseModel):
    """Enhanced career path with Indian context"""

    role: str
    industry: str
    description: str
    score: float = Field(..., ge=0, le=1)
    match_reason: str

    # Skills and Requirements
    required_skills: List[str] = []
    mental_skills_needed: List[MentalSkill] = []
    education_requirements: List[str] = []

    # Indian Market Context
    growth_potential_india: str
    salary_range_india: str
    job_availability: str
    cultural_acceptance: str

    # Career Progression
    entry_level_roles: List[str] = []
    mid_level_roles: List[str] = []
    senior_level_roles: List[str] = []

    # Next Steps
    immediate_steps: List[str] = []
    short_term_goals: List[str] = []
    long_term_goals: List[str] = []


class LearningResource(BaseModel):
    """Learning resource with Indian context"""

    id: str
    title: str
    title_hindi: Optional[str] = None
    url: str
    description: str
    description_hindi: Optional[str] = None

    # Resource Details
    provider: str
    cost: str
    duration: str
    difficulty_level: Literal["beginner", "intermediate", "advanced"]
    language: List[str] = ["english"]

    # Context
    tags: List[str] = []
    target_audience: List[str] = []
    indian_relevance: bool = True
    certification: bool = False

    # Content Type
    resource_type: Literal[
        "course",
        "book",
        "video",
        "practice",
        "certification",
        "internship",
        "competition",
    ]


class ResumeAnalysis(BaseModel):
    """Resume analysis results"""

    ats_score: float = Field(..., ge=0, le=100)
    strengths: List[str] = []
    weaknesses: List[str] = []
    missing_keywords: List[str] = []
    formatting_issues: List[str] = []
    suggestions: List[str] = []
    project_recommendations: List[str] = []
    skill_gaps: List[str] = []


class Roadmap(BaseModel):
    """Career roadmap structure"""

    title: str
    target_role: str
    duration_months: int
    phases: List[Dict[str, Any]]
    milestones: List[Dict[str, Any]]
    resources: List[LearningResource]
    assessments: List[str]
    gamification_elements: Dict[str, Any] = Field(default_factory=dict)


class AIRecommendation(BaseModel):
    """AI-generated recommendation"""

    career_paths: List[CareerPath] = []
    learning_resources: List[LearningResource] = []
    psychological_insights: Dict[str, Any] = Field(default_factory=dict)
    cultural_considerations: List[str] = []
    mental_skill_development: List[str] = []
    roadmap: Optional[Roadmap] = None
    confidence_score: float = Field(..., ge=0, le=1)
    reasoning: str
    alternative_paths: List[CareerPath] = []


class ChatMessage(BaseModel):
    """Chat message for AI interaction"""

    message: str
    language: LanguagePreference = LanguagePreference.ENGLISH
    timestamp: datetime = Field(default_factory=datetime.now)
    message_type: Literal["user", "ai"] = "user"


class RecommendRequest(BaseModel):
    """Request for AI career recommendations"""

    profile: UserProfile
    test_results: List[TestResponse] = []
    chat_context: List[ChatMessage] = []
    focus_areas: List[str] = []


class RecommendResponse(BaseModel):
    """Response with AI career recommendations"""

    recommendations: AIRecommendation
    timestamp: datetime = Field(default_factory=datetime.now)
    session_id: str


class Resource(BaseModel):
    """Learning resource or opportunity"""

    title: str
    description: str
    url: Optional[str] = None
    type: str  # course, article, video, book, etc.
    level: str = "beginner"  # beginner, intermediate, advanced
    duration: Optional[str] = None
    cost: str = "free"  # free, paid, subscription
    provider: Optional[str] = None
    tags: List[str] = []
    rating: Optional[float] = Field(None, ge=0, le=5)
    language: LanguagePreference = LanguagePreference.ENGLISH


class Recommendation(BaseModel):
    """Career or learning recommendation"""

    title: str
    description: str
    type: str  # career_path, skill, resource, etc.
    priority: int = Field(..., ge=1, le=5)  # 1 = highest priority
    confidence: float = Field(..., ge=0, le=1)
    reasoning: str
    resources: List[Resource] = []
    action_items: List[str] = []
    timeline: Optional[str] = None
