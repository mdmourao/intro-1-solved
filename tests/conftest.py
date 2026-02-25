"""
Pytest configuration and fixtures for FastAPI application tests.

This module provides shared fixtures for testing the High School Management System API.
"""

import pytest
from fastapi.testclient import TestClient
from copy import deepcopy
from src.app import app, activities


# Store the original activities state for reset
ORIGINAL_ACTIVITIES = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Soccer Team": {
        "description": "Join the varsity soccer team and compete in regional tournaments",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 6:00 PM",
        "max_participants": 25,
        "participants": ["lucas@mergington.edu", "mia@mergington.edu"]
    },
    "Basketball Club": {
        "description": "Practice basketball skills and play pickup games",
        "schedule": "Wednesdays, 3:30 PM - 5:30 PM",
        "max_participants": 20,
        "participants": ["liam@mergington.edu"]
    },
    "Drama Club": {
        "description": "Participate in theater productions and acting workshops",
        "schedule": "Mondays and Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 30,
        "participants": ["ava@mergington.edu", "noah@mergington.edu"]
    },
    "Art Studio": {
        "description": "Explore painting, drawing, and sculpture techniques",
        "schedule": "Fridays, 2:30 PM - 4:30 PM",
        "max_participants": 15,
        "participants": ["isabella@mergington.edu"]
    },
    "Debate Team": {
        "description": "Develop critical thinking and public speaking skills through competitive debates",
        "schedule": "Tuesdays, 3:30 PM - 5:00 PM",
        "max_participants": 16,
        "participants": ["ethan@mergington.edu", "charlotte@mergington.edu"]
    },
    "Science Club": {
        "description": "Conduct experiments and explore STEM topics through hands-on projects",
        "schedule": "Wednesdays, 3:00 PM - 4:30 PM",
        "max_participants": 18,
        "participants": ["james@mergington.edu"]
    }
}


@pytest.fixture
def client():
    """
    Fixture that provides a TestClient for making requests to the FastAPI application.
    
    Returns:
        TestClient: Configured test client for the FastAPI app
    """
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """
    Fixture that automatically resets the activities dictionary to its original state
    after each test, ensuring test isolation.
    
    This fixture runs automatically for every test (autouse=True) and executes
    cleanup after the test completes (yield pattern).
    """
    # Setup: code before yield runs before the test
    # (nothing needed before test runs)
    
    # Test runs here
    yield
    
    # Teardown: code after yield runs after the test
    activities.clear()
    activities.update(deepcopy(ORIGINAL_ACTIVITIES))
