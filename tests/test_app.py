"""
Test suite for High School Management System API endpoints.

This module contains tests for all API endpoints using the AAA (Arrange-Act-Assert) pattern.
Tests cover happy paths and key error scenarios for activity management functionality.
"""

import pytest
from fastapi.testclient import TestClient
from src.app import activities


class TestRootEndpoint:
    """Tests for the root endpoint (/)."""
    
    def test_root_redirects_to_static_index(self, client):
        """Test that the root endpoint redirects to the static index.html page."""
        # Arrange: client fixture provides the TestClient
        
        # Act: Make GET request to root endpoint
        response = client.get("/", follow_redirects=False)
        
        # Assert: Verify redirect response
        assert response.status_code == 307
        assert response.headers["location"] == "/static/index.html"


class TestGetActivities:
    """Tests for GET /activities endpoint."""
    
    def test_get_all_activities_returns_success(self, client):
        """Test that GET /activities returns all activities with 200 status."""
        # Arrange: client fixture provides TestClient with pre-populated activities
        
        # Act: Make GET request to /activities
        response = client.get("/activities")
        
        # Assert: Verify successful response
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert len(data) == 9  # Should have all 9 activities
    
    def test_get_activities_returns_correct_structure(self, client):
        """Test that activities have the correct fields and data structure."""
        # Arrange: client fixture provides TestClient
        
        # Act: Make GET request to /activities
        response = client.get("/activities")
        data = response.json()
        
        # Assert: Verify structure of returned activities
        assert "Chess Club" in data
        chess_club = data["Chess Club"]
        assert "description" in chess_club
        assert "schedule" in chess_club
        assert "max_participants" in chess_club
        assert "participants" in chess_club
        assert isinstance(chess_club["participants"], list)
        assert chess_club["max_participants"] == 12


class TestSignupEndpoint:
    """Tests for POST /activities/{activity_name}/signup endpoint."""
    
    def test_signup_adds_participant_successfully(self, client):
        """Test that signing up a new student adds them to the participants list."""
        # Arrange: Choose an activity and a new student email
        activity_name = "Chess Club"
        new_email = "newstudent@mergington.edu"
        initial_participants = len(activities[activity_name]["participants"])
        
        # Act: Make POST request to signup endpoint
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": new_email}
        )
        
        # Assert: Verify successful signup
        assert response.status_code == 200
        assert response.json() == {"message": f"Signed up {new_email} for {activity_name}"}
        assert new_email in activities[activity_name]["participants"]
        assert len(activities[activity_name]["participants"]) == initial_participants + 1
    
    def test_signup_for_nonexistent_activity_returns_404(self, client):
        """Test that signing up for a non-existent activity returns 404 error."""
        # Arrange: Use a non-existent activity name
        activity_name = "Nonexistent Club"
        email = "student@mergington.edu"
        
        # Act: Make POST request with invalid activity name
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert: Verify 404 error response
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()
    
    def test_signup_duplicate_student_returns_400(self, client):
        """Test that signing up an already registered student returns 400 error."""
        # Arrange: Use an existing participant email from Chess Club
        activity_name = "Chess Club"
        existing_email = "michael@mergington.edu"  # Already in Chess Club
        
        # Act: Make POST request with already registered email
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": existing_email}
        )
        
        # Assert: Verify 400 error response
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"].lower()
    
    def test_signup_handles_activity_names_with_spaces(self, client):
        """Test that activity names with spaces are handled correctly with URL encoding."""
        # Arrange: Use activity name with spaces
        activity_name = "Programming Class"
        new_email = "coder@mergington.edu"
        
        # Act: Make POST request (TestClient handles URL encoding automatically)
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": new_email}
        )
        
        # Assert: Verify successful signup
        assert response.status_code == 200
        assert new_email in activities[activity_name]["participants"]


class TestUnregisterEndpoint:
    """Tests for DELETE /activities/{activity_name}/unregister endpoint."""
    
    def test_unregister_removes_participant_successfully(self, client):
        """Test that unregistering removes a student from the participants list."""
        # Arrange: Use an existing participant from Chess Club
        activity_name = "Chess Club"
        existing_email = "michael@mergington.edu"
        initial_participants = len(activities[activity_name]["participants"])
        assert existing_email in activities[activity_name]["participants"]
        
        # Act: Make DELETE request to unregister endpoint
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": existing_email}
        )
        
        # Assert: Verify successful unregistration
        assert response.status_code == 200
        assert response.json() == {"message": f"Unregistered {existing_email} from {activity_name}"}
        assert existing_email not in activities[activity_name]["participants"]
        assert len(activities[activity_name]["participants"]) == initial_participants - 1
    
    def test_unregister_from_nonexistent_activity_returns_404(self, client):
        """Test that unregistering from a non-existent activity returns 404 error."""
        # Arrange: Use a non-existent activity name
        activity_name = "Fake Club"
        email = "student@mergington.edu"
        
        # Act: Make DELETE request with invalid activity name
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        
        # Assert: Verify 404 error response
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()
    
    def test_unregister_non_participant_returns_400(self, client):
        """Test that unregistering a student who isn't registered returns 400 error."""
        # Arrange: Use an email not in Chess Club's participants
        activity_name = "Chess Club"
        non_participant_email = "notinclub@mergington.edu"
        assert non_participant_email not in activities[activity_name]["participants"]
        
        # Act: Make DELETE request for non-registered student
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": non_participant_email}
        )
        
        # Assert: Verify 400 error response
        assert response.status_code == 400
        assert "is not signed up" in response.json()["detail"].lower()
