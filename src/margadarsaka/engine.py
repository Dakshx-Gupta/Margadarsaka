"""Career recommendation engine for Margadarsaka"""

from typing import List, Dict, Set
import re
from datetime import datetime

from .models import UserProfile, CareerPath, Resource, Recommendation
from .data import (
    CAREER_PATHS,
    JOB_RESOURCES,
    MENTORSHIP_RESOURCES,
    SKILL_MAPPINGS,
    RESOURCES_DISCLAIMER,
    get_all_resources,
)


class CareerRecommendationEngine:
    """Rule-based career recommendation engine"""

    def __init__(self):
        self.career_paths = CAREER_PATHS
        self.resources = get_all_resources()  # Now includes roadmap.sh resources
        self.job_resources = JOB_RESOURCES
        self.mentorship_resources = MENTORSHIP_RESOURCES
        self.skill_mappings = SKILL_MAPPINGS
        self.resources_disclaimer = RESOURCES_DISCLAIMER

    def get_recommendations(self, profile: UserProfile) -> Recommendation:
        """Generate comprehensive career recommendations"""

        # Get career path recommendations
        career_paths = self._recommend_career_paths(profile)

        # Get learning resources
        learning_resources = self._recommend_learning_resources(profile, career_paths)

        # Identify skills to develop
        skills_to_develop = self._identify_skills_gap(profile, career_paths)

        # Get mentorship opportunities
        mentorship_opportunities = self._get_mentorship_resources(profile)

        # Get job opportunities
        job_opportunities = self._get_job_resources(profile)

        return Recommendation(
            career_paths=career_paths,
            learning_resources=learning_resources,
            skills_to_develop=skills_to_develop,
            mentorship_opportunities=mentorship_opportunities,
            job_opportunities=job_opportunities,
        )

    def _recommend_career_paths(self, profile: UserProfile) -> List[CareerPath]:
        """Recommend career paths based on user profile"""
        recommendations = []

        user_skills = set(skill.lower().replace(" ", "-") for skill in profile.skills)
        user_interests = set(
            interest.lower().replace(" ", "-") for interest in profile.interests
        )
        user_goals = set(goal.lower().replace(" ", "-") for goal in profile.goals)

        for path_id, path_data in self.career_paths.items():
            score = self._calculate_career_match_score(
                path_data,
                user_skills,
                user_interests,
                user_goals,
                profile.experience_years,
            )

            if score > 0.2:  # Threshold for relevance
                match_reason = self._generate_match_reason(
                    path_data, user_skills, user_interests, user_goals
                )

                career_path = CareerPath(
                    role=path_data["role"],
                    industry=path_data["industry"],
                    score=score,
                    match_reason=match_reason,
                    required_skills=path_data["required_skills"],
                    growth_potential=path_data["growth_potential"],
                    salary_range=path_data["salary_range"],
                    next_steps=path_data["next_steps"],
                )
                recommendations.append(career_path)

        # Sort by score and return top 5
        recommendations.sort(key=lambda x: x.score, reverse=True)
        return recommendations[:5]

    def _calculate_career_match_score(
        self,
        path_data: Dict,
        user_skills: Set,
        user_interests: Set,
        user_goals: Set,
        experience_years: float = None,
    ) -> float:
        """Calculate match score between user and career path"""
        score = 0.0

        # Skill matching (40% weight)
        required_skills = set(
            skill.lower().replace(" ", "-") for skill in path_data["required_skills"]
        )
        skill_match = (
            len(user_skills.intersection(required_skills)) / len(required_skills)
            if required_skills
            else 0
        )
        score += skill_match * 0.4

        # Interest matching (30% weight)
        path_keywords = self._extract_keywords_from_path(path_data)
        interest_match = len(user_interests.intersection(path_keywords)) / max(
            len(user_interests), 1
        )
        score += interest_match * 0.3

        # Goal alignment (20% weight)
        goal_match = len(user_goals.intersection(path_keywords)) / max(
            len(user_goals), 1
        )
        score += goal_match * 0.2

        # Experience bonus (10% weight)
        if experience_years is not None:
            # Boost score slightly for relevant experience
            experience_bonus = min(experience_years / 5, 0.1)  # Cap at 0.1
            score += experience_bonus

        return min(score, 1.0)  # Cap at 1.0

    def _extract_keywords_from_path(self, path_data: Dict) -> Set[str]:
        """Extract searchable keywords from career path"""
        keywords = set()

        # Add role and industry keywords
        role_words = re.findall(r"\w+", path_data["role"].lower())
        industry_words = re.findall(r"\w+", path_data["industry"].lower())

        keywords.update(role_words)
        keywords.update(industry_words)
        keywords.update(
            skill.lower().replace(" ", "-") for skill in path_data["required_skills"]
        )

        return keywords

    def _generate_match_reason(
        self, path_data: Dict, user_skills: Set, user_interests: Set, user_goals: Set
    ) -> str:
        """Generate explanation for why this career path matches"""
        reasons = []

        # Check skill matches
        required_skills = set(
            skill.lower().replace(" ", "-") for skill in path_data["required_skills"]
        )
        matching_skills = user_skills.intersection(required_skills)
        if matching_skills:
            skills_str = ", ".join(list(matching_skills)[:3])
            reasons.append(f"Your skills in {skills_str} align well")

        # Check interest matches
        path_keywords = self._extract_keywords_from_path(path_data)
        matching_interests = user_interests.intersection(path_keywords)
        if matching_interests:
            interests_str = ", ".join(list(matching_interests)[:2])
            reasons.append(f"Your interest in {interests_str} is relevant")

        # Check goal matches
        matching_goals = user_goals.intersection(path_keywords)
        if matching_goals:
            goals_str = ", ".join(list(matching_goals)[:2])
            reasons.append(f"Aligns with your goal of {goals_str}")

        if not reasons:
            reasons.append("Good general match based on your profile")

        return ". ".join(reasons) + "."

    def _recommend_learning_resources(
        self, profile: UserProfile, career_paths: List[CareerPath]
    ) -> List[Resource]:
        """Recommend learning resources based on profile and career paths"""
        user_skills = set(skill.lower().replace(" ", "-") for skill in profile.skills)
        user_interests = set(
            interest.lower().replace(" ", "-") for interest in profile.interests
        )

        # Collect skills from recommended career paths
        target_skills = set()
        for path in career_paths:
            target_skills.update(
                skill.lower().replace(" ", "-") for skill in path.required_skills
            )

        recommendations = []
        for resource_data in self.resources:
            resource_tags = set(
                tag.lower().replace(" ", "-") for tag in resource_data["tags"]
            )

            # Score based on relevance to interests, goals, and target skills
            relevance_score = 0

            # Interest match
            if user_interests.intersection(resource_tags):
                relevance_score += 0.4

            # Target skill match
            if target_skills.intersection(resource_tags):
                relevance_score += 0.5

            # Current skill enhancement
            if user_skills.intersection(resource_tags):
                relevance_score += 0.3

            # Level appropriateness
            if profile.experience_years is not None:
                if (
                    profile.experience_years < 2
                    and resource_data["level"] == "beginner"
                ):
                    relevance_score += 0.2
                elif (
                    2 <= profile.experience_years < 5
                    and resource_data["level"] == "intermediate"
                ):
                    relevance_score += 0.2
                elif (
                    profile.experience_years >= 5
                    and resource_data["level"] == "advanced"
                ):
                    relevance_score += 0.2

            if relevance_score > 0.3:  # Threshold for relevance
                resource = Resource(**resource_data)
                recommendations.append(resource)

        # Sort by relevance and return top resources
        return recommendations[:6]

    def _identify_skills_gap(
        self, profile: UserProfile, career_paths: List[CareerPath]
    ) -> List[str]:
        """Identify skills user should develop"""
        user_skills = set(skill.lower().replace(" ", "-") for skill in profile.skills)

        # Collect all recommended skills from career paths
        recommended_skills = set()
        for path in career_paths:
            recommended_skills.update(
                skill.lower().replace(" ", "-") for skill in path.required_skills
            )

        # Find skills gap
        skills_gap = recommended_skills - user_skills

        # Return as list, prioritizing common/important skills
        priority_skills = [
            "python",
            "javascript",
            "communication",
            "leadership",
            "data-analysis",
        ]
        prioritized_gap = []

        # Add priority skills first
        for skill in priority_skills:
            if skill in skills_gap:
                prioritized_gap.append(skill.replace("-", " ").title())
                skills_gap.remove(skill)

        # Add remaining skills
        for skill in list(skills_gap)[:5]:  # Limit to 5 additional
            prioritized_gap.append(skill.replace("-", " ").title())

        return prioritized_gap[:8]  # Max 8 skills

    def _get_mentorship_resources(self, profile: UserProfile) -> List[Resource]:
        """Get mentorship opportunities"""
        return [
            Resource(**resource_data) for resource_data in self.mentorship_resources
        ]

    def _get_job_resources(self, profile: UserProfile) -> List[Resource]:
        """Get job search resources"""
        return [Resource(**resource_data) for resource_data in self.job_resources]

    def get_resources_disclaimer(self) -> str:
        """Get the legal disclaimer for external resources"""
        return self.resources_disclaimer

    def get_roadmap_resources(self, category: str = "all") -> List[Resource]:
        """Get roadmap.sh resources by category (role_based, skill_based, or all)"""
        roadmap_resources = []
        for resource in self.resources:
            if resource.get("provider") == "roadmap.sh":
                if category == "all" or resource.get("category") == category:
                    roadmap_resources.append(Resource(**resource))
        return roadmap_resources
