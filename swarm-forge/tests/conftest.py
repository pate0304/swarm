import pytest
from pathlib import Path
from unittest.mock import Mock
from swarm import Agent
from swarm_forge.core.settings import ForgeSettings, ProjectSettings, get_settings
from swarm_forge.core.config import ProjectConfig

@pytest.fixture(autouse=True)
def mock_settings(monkeypatch):
    """Mock settings for tests"""
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setenv("FORGE_PROJECTS_ROOT", "/tmp/forge-test")
    monkeypatch.setenv("FORGE_LOG_LEVEL", "DEBUG")
    monkeypatch.setenv("FORGE_LOG_DIR", "/tmp/forge-test/logs")
    settings = get_settings()
    return settings

@pytest.fixture
def mock_agent():
    """Create a mock agent for testing"""
    agent = Mock(spec=Agent)
    agent.name = "Mock Agent"
    agent.model = "gpt-4"
    agent.temperature = 0.7
    return agent

@pytest.fixture
def test_project_config():
    """Create a test project configuration"""
    return ProjectConfig(
        name="test_project",
        description="A test project",
        type="web"
    )

@pytest.fixture
def test_project_settings(tmp_path):
    """Create test project settings"""
    return ProjectSettings(
        name="test_project",
        description="A test project",
        output_dir=tmp_path / "test_project",
        type="web"
    )

@pytest.fixture
def mock_requirements():
    """Create mock requirements data"""
    return {
        "features": [
            "User authentication",
            "Data storage",
            "API endpoints"
        ],
        "user_stories": [
            "As a user, I want to sign up",
            "As a user, I want to log in",
            "As a user, I want to store data"
        ],
        "acceptance_criteria": {
            "auth": ["Must support email/password", "Must validate email format"],
            "data": ["Must encrypt sensitive data", "Must backup regularly"]
        }
    }

@pytest.fixture
def mock_architecture():
    """Create mock architecture data"""
    return {
        "backend": {
            "framework": "FastAPI",
            "database": "PostgreSQL",
            "cache": "Redis"
        },
        "frontend": {
            "framework": "React",
            "ui_library": "Material-UI",
            "state_management": "Redux"
        },
        "dependencies": {
            "python": {
                "fastapi": "^0.68.0",
                "sqlalchemy": "^1.4.23"
            },
            "javascript": {
                "react": "^17.0.2",
                "material-ui": "^5.0.0"
            }
        }
    }

@pytest.fixture
def mock_deployment_config():
    """Create mock deployment configuration"""
    return {
        "docker": {
            "backend": "python:3.10-slim",
            "frontend": "node:16-alpine"
        },
        "kubernetes": {
            "replicas": 3,
            "resources": {
                "requests": {
                    "cpu": "100m",
                    "memory": "128Mi"
                }
            }
        },
        "environment_variables": [
            "DATABASE_URL",
            "REDIS_URL",
            "SECRET_KEY"
        ]
    }
