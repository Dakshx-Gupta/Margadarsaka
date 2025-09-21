"""FastAPI application for Margadarsaka career advisor"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import logging

from .models import RecommendRequest, RecommendResponse, UserProfile, Resource
from .engine import CareerRecommendationEngine
from .data import (
    JOB_RESOURCES,
    MENTORSHIP_RESOURCES,
    get_all_resources as get_all_resources_data,
    RESOURCES_DISCLAIMER,
)
from .secrets import get_debug_mode, get_environment, get_secret

# Configure logging
log_level = get_secret("LOG_LEVEL", "INFO") or "INFO"
logging.basicConfig(level=getattr(logging, log_level))
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Margadarsaka API",
    description="Intelligent Career Advisor API with Psychological Assessment",
    version="0.2.0",
    debug=get_debug_mode(),
)

# Configure CORS from secrets
cors_origins = get_secret("CORS_ORIGINS", "*")
allowed_origins = cors_origins.split(",") if cors_origins else ["*"]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize recommendation engine
engine = CareerRecommendationEngine()


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "ok",
        "service": "margadarsaka",
        "version": "0.1.0",
        "timestamp": datetime.now().isoformat(),
    }


@app.post("/api/recommend", response_model=RecommendResponse)
async def get_recommendations(request: RecommendRequest):
    """Get personalized career recommendations"""
    try:
        logger.info(f"Generating recommendations for user: {request.profile.name}")

        # Generate recommendations
        recommendations = engine.get_recommendations(request.profile)

        response = RecommendResponse(
            recommendations=recommendations, timestamp=datetime.now().isoformat()
        )

        logger.info(
            f"Generated {len(response.recommendations.career_paths)} career paths"
        )
        return response

    except Exception as e:
        logger.error(f"Error generating recommendations: {str(e)}")
        raise HTTPException(
            status_code=500, detail="Failed to generate recommendations"
        )


@app.get("/api/resources")
async def get_all_resources():
    """Get all available learning resources including roadmap.sh"""
    try:
        all_resources = []

        # Get all resources including roadmap.sh
        for resource_data in get_all_resources_data():
            all_resources.append(Resource(**resource_data))

        # Add job resources
        for resource_data in JOB_RESOURCES:
            all_resources.append(Resource(**resource_data))

        # Add mentorship resources
        for resource_data in MENTORSHIP_RESOURCES:
            all_resources.append(Resource(**resource_data))

        return {"resources": all_resources, "count": len(all_resources)}

    except Exception as e:
        logger.error(f"Error fetching resources: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch resources")


@app.get("/api/resources/{resource_type}")
async def get_resources_by_type(resource_type: str):
    """Get resources filtered by type"""
    try:
        filtered_resources = []

        if resource_type == "learning":
            resource_list = get_all_resources_data()
        elif resource_type == "jobs":
            resource_list = JOB_RESOURCES
        elif resource_type == "mentorship":
            resource_list = MENTORSHIP_RESOURCES
        else:
            raise HTTPException(status_code=404, detail="Resource type not found")

        for resource_data in resource_list:
            filtered_resources.append(Resource(**resource_data))

        return {"resources": filtered_resources, "count": len(filtered_resources)}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching {resource_type} resources: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Failed to fetch {resource_type} resources"
        )


@app.post("/api/profile/validate")
async def validate_profile(profile: UserProfile):
    """Validate user profile data"""
    try:
        # Basic validation logic
        if not profile.interests and not profile.skills and not profile.goals:
            raise HTTPException(
                status_code=400,
                detail="Profile must include at least interests, skills, or goals",
            )

        return {
            "valid": True,
            "message": "Profile is valid",
            "suggestions": _get_profile_suggestions(profile),
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error validating profile: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to validate profile")


def _get_profile_suggestions(profile: UserProfile) -> list:
    """Get suggestions to improve profile completeness"""
    suggestions = []

    if not profile.interests:
        suggestions.append("Add your interests to get better career matches")

    if not profile.skills:
        suggestions.append("List your current skills for accurate recommendations")

    if not profile.goals:
        suggestions.append("Define your career goals for targeted advice")

    if profile.experience_years is None:
        suggestions.append(
            "Include years of experience for level-appropriate resources"
        )

    if not profile.education_level:
        suggestions.append("Add education level for comprehensive guidance")

    return suggestions


@app.get("/api/resources/disclaimer")
async def get_resources_disclaimer():
    """Get legal disclaimer for external resources"""
    return {"disclaimer": RESOURCES_DISCLAIMER}


@app.get("/api/resources/roadmaps")
async def get_roadmap_resources(category: str = "all"):
    """Get roadmap.sh resources by category (role_based, skill_based, or all)"""
    try:
        roadmap_resources = []
        for resource_data in get_all_resources_data():
            if resource_data.get("provider") == "roadmap.sh":
                if category == "all" or resource_data.get("category") == category:
                    roadmap_resources.append(Resource(**resource_data))

        return {
            "roadmaps": roadmap_resources,
            "count": len(roadmap_resources),
            "category": category,
            "disclaimer": RESOURCES_DISCLAIMER,
        }
    except Exception as e:
        logger.error(f"Error fetching roadmap resources: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch roadmap resources")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
