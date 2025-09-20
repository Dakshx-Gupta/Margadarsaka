"""Tests for Margadarsaka career recommendation engine"""

import pytest
from src.margadarsaka.engine import CareerRecommendationEngine
from src.margadarsaka.models import UserProfile, CareerPath, Resource


class TestCareerRecommendationEngine:
    """Test suite for the recommendation engine"""

    def setup_method(self):
        """Set up test fixtures"""
        self.engine = CareerRecommendationEngine()

    def test_engine_initialization(self):
        """Test that engine initializes correctly"""
        assert self.engine is not None
        assert hasattr(self.engine, "career_paths")
        assert hasattr(self.engine, "resources")
        assert len(self.engine.career_paths) > 0
        assert len(self.engine.resources) > 0

    def test_basic_recommendation_generation(self):
        """Test basic recommendation generation"""
        profile = UserProfile(
            name="Test User",
            interests=["technology", "programming"],
            skills=["python", "communication"],
            goals=["become a software engineer"],
            experience_years=2.0,
        )

        recommendations = self.engine.get_recommendations(profile)

        assert recommendations is not None
        assert hasattr(recommendations, "career_paths")
        assert hasattr(recommendations, "learning_resources")
        assert hasattr(recommendations, "skills_to_develop")
        assert isinstance(recommendations.career_paths, list)
        assert isinstance(recommendations.learning_resources, list)
        assert isinstance(recommendations.skills_to_develop, list)

    def test_programming_profile_recommendations(self):
        """Test recommendations for programming-focused profile"""
        profile = UserProfile(
            interests=["programming", "technology", "problem-solving"],
            skills=["python", "javascript"],
            goals=["software development", "coding"],
            experience_years=1.0,
        )

        recommendations = self.engine.get_recommendations(profile)

        # Should recommend software engineering roles
        career_roles = [path.role for path in recommendations.career_paths]
        assert any("Software Engineer" in role for role in career_roles)

        # Should have relevant learning resources
        assert len(recommendations.learning_resources) > 0

        # Should suggest relevant skills
        skills_lower = [skill.lower() for skill in recommendations.skills_to_develop]
        programming_skills = ["javascript", "python", "programming", "problem-solving"]
        assert any(skill in " ".join(skills_lower) for skill in programming_skills)

    def test_data_science_profile_recommendations(self):
        """Test recommendations for data science profile"""
        profile = UserProfile(
            interests=["data analysis", "statistics", "machine learning"],
            skills=["python", "statistics", "data analysis"],
            goals=["data scientist", "analytics"],
            experience_years=3.0,
        )

        recommendations = self.engine.get_recommendations(profile)

        # Should recommend data science roles
        career_roles = [path.role for path in recommendations.career_paths]
        assert any("Data Scientist" in role for role in career_roles)

        # Should have high-scoring matches
        assert any(path.score > 0.5 for path in recommendations.career_paths)

    def test_empty_profile_handling(self):
        """Test handling of minimal profile data"""
        profile = UserProfile()  # Empty profile

        recommendations = self.engine.get_recommendations(profile)

        # Should still return recommendations (general ones)
        assert recommendations is not None
        assert isinstance(recommendations.career_paths, list)
        assert isinstance(recommendations.learning_resources, list)

    def test_experience_level_consideration(self):
        """Test that experience level affects recommendations"""
        # Beginner profile
        beginner_profile = UserProfile(
            interests=["technology"], skills=["basic programming"], experience_years=0.5
        )

        # Senior profile
        senior_profile = UserProfile(
            interests=["technology"],
            skills=["programming", "leadership", "architecture"],
            experience_years=8.0,
        )

        beginner_recs = self.engine.get_recommendations(beginner_profile)
        senior_recs = self.engine.get_recommendations(senior_profile)

        # Both should get recommendations
        assert len(beginner_recs.career_paths) > 0
        assert len(senior_recs.career_paths) > 0

        # Learning resources should be provided
        assert len(beginner_recs.learning_resources) > 0
        assert len(senior_recs.learning_resources) > 0

    def test_career_match_score_calculation(self):
        """Test career path scoring logic"""
        profile = UserProfile(
            interests=["programming"],
            skills=["python", "javascript"],
            goals=["software development"],
        )

        recommendations = self.engine.get_recommendations(profile)

        # Check that scores are valid
        for path in recommendations.career_paths:
            assert 0 <= path.score <= 1
            assert isinstance(path.score, float)
            assert len(path.match_reason) > 0

    def test_skills_gap_identification(self):
        """Test skills gap identification"""
        profile = UserProfile(
            interests=["data science"],
            skills=["python"],  # Limited skills
            goals=["become data scientist"],
            experience_years=1.0,
        )

        recommendations = self.engine.get_recommendations(profile)

        # Should identify missing skills for data science
        skills_to_develop = [
            skill.lower() for skill in recommendations.skills_to_develop
        ]
        expected_skills = ["statistics", "machine learning", "data analysis"]

        # At least some expected skills should be suggested
        assert any(
            expected in " ".join(skills_to_develop) for expected in expected_skills
        )

    def test_resource_relevance(self):
        """Test that recommended resources are relevant"""
        profile = UserProfile(
            interests=["web development"],
            skills=["html", "css"],
            goals=["full stack developer"],
        )

        recommendations = self.engine.get_recommendations(profile)

        # Resources should be relevant to profile
        assert len(recommendations.learning_resources) > 0

        # Check that resources have required fields
        for resource in recommendations.learning_resources:
            assert hasattr(resource, "title")
            assert hasattr(resource, "url")
            assert hasattr(resource, "description")
            assert isinstance(resource.tags, list)

    def test_mentorship_and_job_resources(self):
        """Test that mentorship and job resources are included"""
        profile = UserProfile(
            interests=["career growth"],
            skills=["communication"],
            goals=["leadership role"],
        )

        recommendations = self.engine.get_recommendations(profile)

        # Should include mentorship opportunities
        assert len(recommendations.mentorship_opportunities) > 0

        # Should include job search resources
        assert len(recommendations.job_opportunities) > 0

        # Check structure of these resources
        for mentor in recommendations.mentorship_opportunities:
            assert hasattr(mentor, "title")
            assert hasattr(mentor, "url")

        for job in recommendations.job_opportunities:
            assert hasattr(job, "title")
            assert hasattr(job, "url")

    def test_recommendation_consistency(self):
        """Test that recommendations are consistent across multiple calls"""
        profile = UserProfile(
            interests=["technology", "innovation"],
            skills=["python", "project management"],
            goals=["tech leadership"],
            experience_years=5.0,
        )

        # Get recommendations twice
        recs1 = self.engine.get_recommendations(profile)
        recs2 = self.engine.get_recommendations(profile)

        # Should be identical (deterministic)
        assert len(recs1.career_paths) == len(recs2.career_paths)
        assert len(recs1.learning_resources) == len(recs2.learning_resources)

        # Career path scores should be the same
        for i, path in enumerate(recs1.career_paths):
            if i < len(recs2.career_paths):
                assert path.score == recs2.career_paths[i].score

    def test_edge_cases(self):
        """Test edge cases and error handling"""
        # Very long lists
        long_profile = UserProfile(
            interests=["tech"] * 100,
            skills=["programming"] * 50,
            goals=["success"] * 20,
        )

        recommendations = self.engine.get_recommendations(long_profile)
        assert recommendations is not None

        # Very high experience
        experienced_profile = UserProfile(
            interests=["leadership"], skills=["management"], experience_years=50.0
        )

        recommendations = self.engine.get_recommendations(experienced_profile)
        assert recommendations is not None

        # Special characters in input
        special_profile = UserProfile(
            interests=["AI/ML", "deep-learning", "NLP & text processing"],
            skills=["C++", ".NET", "Node.js"],
            goals=["VP of Engineering"],
        )

        recommendations = self.engine.get_recommendations(special_profile)
        assert recommendations is not None
