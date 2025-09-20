"""Tests for Margadarsaka API endpoints"""

import pytest
from fastapi.testclient import TestClient
from src.margadarsaka.api import app

client = TestClient(app)


class TestAPI:
    """Test suite for API endpoints"""

    def test_root_endpoint(self):
        """Test the root health check endpoint"""
        response = client.get("/")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert data["service"] == "margadarsaka"
        assert "timestamp" in data

    def test_recommendations_endpoint_valid_profile(self):
        """Test recommendations endpoint with valid profile"""
        profile_data = {
            "profile": {
                "name": "Test User",
                "interests": ["programming", "technology"],
                "skills": ["python", "javascript"],
                "goals": ["software engineer"],
                "experience_years": 2.0,
                "education_level": "Bachelor's Degree",
                "location": "San Francisco",
            }
        }

        response = client.post("/api/recommend", json=profile_data)

        assert response.status_code == 200
        data = response.json()
        assert "recommendations" in data
        assert "timestamp" in data

        recommendations = data["recommendations"]
        assert "career_paths" in recommendations
        assert "learning_resources" in recommendations
        assert "skills_to_develop" in recommendations
        assert isinstance(recommendations["career_paths"], list)

    def test_recommendations_endpoint_minimal_profile(self):
        """Test recommendations with minimal profile data"""
        profile_data = {"profile": {"interests": ["technology"]}}

        response = client.post("/api/recommend", json=profile_data)

        assert response.status_code == 200
        data = response.json()
        assert "recommendations" in data

    def test_recommendations_endpoint_empty_profile(self):
        """Test recommendations with empty profile"""
        profile_data = {"profile": {}}

        response = client.post("/api/recommend", json=profile_data)

        assert response.status_code == 200
        data = response.json()
        assert "recommendations" in data

    def test_recommendations_endpoint_invalid_data(self):
        """Test recommendations endpoint with invalid data"""
        invalid_data = {
            "profile": {
                "experience_years": -5  # Invalid negative experience
            }
        }

        response = client.post("/api/recommend", json=invalid_data)
        assert response.status_code == 422  # Validation error

    def test_get_all_resources_endpoint(self):
        """Test getting all resources"""
        response = client.get("/api/resources")

        assert response.status_code == 200
        data = response.json()
        assert "resources" in data
        assert "count" in data
        assert isinstance(data["resources"], list)
        assert data["count"] > 0

    def test_get_resources_by_type_learning(self):
        """Test getting learning resources"""
        response = client.get("/api/resources/learning")

        assert response.status_code == 200
        data = response.json()
        assert "resources" in data
        assert isinstance(data["resources"], list)

    def test_get_resources_by_type_jobs(self):
        """Test getting job resources"""
        response = client.get("/api/resources/jobs")

        assert response.status_code == 200
        data = response.json()
        assert "resources" in data
        assert isinstance(data["resources"], list)

    def test_get_resources_by_type_mentorship(self):
        """Test getting mentorship resources"""
        response = client.get("/api/resources/mentorship")

        assert response.status_code == 200
        data = response.json()
        assert "resources" in data
        assert isinstance(data["resources"], list)

    def test_get_resources_invalid_type(self):
        """Test getting resources with invalid type"""
        response = client.get("/api/resources/invalid_type")

        assert response.status_code == 404

    def test_profile_validation_endpoint(self):
        """Test profile validation endpoint"""
        valid_profile = {
            "name": "Test User",
            "interests": ["technology"],
            "skills": ["python"],
            "goals": ["software engineer"],
        }

        response = client.post("/api/profile/validate", json=valid_profile)

        assert response.status_code == 200
        data = response.json()
        assert data["valid"] is True
        assert "message" in data
        assert "suggestions" in data

    def test_profile_validation_empty_profile(self):
        """Test validation of empty profile"""
        empty_profile = {}

        response = client.post("/api/profile/validate", json=empty_profile)

        assert response.status_code == 400
        data = response.json()
        assert "Profile must include" in data["detail"]
