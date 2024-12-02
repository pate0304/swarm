import pytest
import os
from typing import Dict, Any
from swarm_forge.agents.base import BaseAgent, RequirementsAgent
from swarm_forge.core.settings import ForgeSettings, get_settings

@pytest.fixture(autouse=True)
def mock_settings(monkeypatch):
    """Mock settings for tests"""
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setenv("FORGE_PROJECTS_ROOT", "/tmp/forge-test")
    monkeypatch.setenv("FORGE_LOG_LEVEL", "DEBUG")
    monkeypatch.setenv("FORGE_LOG_DIR", "/tmp/forge-test/logs")
    settings = get_settings()
    return settings

# Test implementations (not test cases)
class _TestAgent(BaseAgent):
    """Test implementation of BaseAgent"""
    
    def __init__(self, name="Test Agent", temperature=None):
        super().__init__(name=name, temperature=temperature)
    
    def get_base_instructions(self) -> str:
        return "Test instructions"
    
    def process(self, input_data: Any) -> Any:
        return {"processed": input_data}

class _TestRequirementsAgent(RequirementsAgent):
    """Test implementation of RequirementsAgent"""
    
    def __init__(self, name="Test Requirements Agent", temperature=None):
        super().__init__(name=name, temperature=temperature)
    
    def get_base_instructions(self) -> str:
        return "Test requirements agent instructions"
    
    def process(self, input_data: Any) -> Any:
        return self.analyze_requirements(input_data)

def test_base_agent_initialization():
    """Test BaseAgent initialization"""
    agent = _TestAgent()
    assert agent.name == "Test Agent"
    assert agent.model == "gpt-4"  # Default model from settings
    assert agent.temperature == 0.7  # Default temperature

def test_base_agent_custom_settings():
    """Test BaseAgent with custom settings"""
    agent = _TestAgent(
        name="Custom Agent",
        temperature=0.5
    )
    assert agent.name == "Custom Agent"
    assert agent.temperature == 0.5
    assert agent.get_base_instructions() == "Test instructions"

def test_base_agent_execution():
    """Test BaseAgent execution flow"""
    agent = _TestAgent()
    result = agent.execute("test_input")
    assert result == {"processed": "test_input"}

def test_requirements_agent_validation():
    """Test RequirementsAgent validation"""
    agent = _TestRequirementsAgent()
    
    # Test valid requirements
    valid_requirements = {
        "features": ["Feature 1", "Feature 2"],
        "user_stories": ["Story 1", "Story 2"],
        "acceptance_criteria": {
            "Feature 1": ["Criterion 1", "Criterion 2"],
            "Feature 2": ["Criterion 3", "Criterion 4"]  # Added criteria for Feature 2
        }
    }
    assert agent.validate_requirements(valid_requirements)
    
    # Test invalid requirements
    invalid_requirements = {
        "features": "Not a list",
        "user_stories": ["Story 1"],
        # Missing acceptance_criteria
    }
    assert not agent.validate_requirements(invalid_requirements)

def test_user_story_formatting():
    """Test user story formatting"""
    agent = _TestRequirementsAgent()
    
    story = agent.format_user_story(
        role="user",
        action="perform action",
        benefit="achieve goal"
    )
    assert story == "As a user, I want to perform action, so that achieve goal"

def test_user_story_parsing():
    """Test user story parsing"""
    agent = _TestRequirementsAgent()
    
    # Test valid story
    story = "As a user, I want to login, so that access my account"
    parsed = agent.parse_user_story(story)
    assert parsed["role"] == "user"
    assert parsed["action"] == "login"
    assert parsed["benefit"] == "access my account"
    
    # Test invalid story
    invalid_story = "Invalid story format"
    parsed = agent.parse_user_story(invalid_story)
    assert parsed["role"] == ""
    assert parsed["action"] == ""
    assert parsed["benefit"] == ""

def test_feature_prioritization():
    """Test feature prioritization"""
    agent = _TestRequirementsAgent()
    
    features = ["Feature 1", "Feature 2", "Feature 3"]
    criteria = {
        "impact": {
            "Feature 1": 8,
            "Feature 2": 5,
            "Feature 3": 7
        },
        "effort": {
            "Feature 1": 3,
            "Feature 2": 2,
            "Feature 3": 5
        }
    }
    
    prioritized = agent.prioritize_features(features, criteria)
    
    # Calculate expected priorities
    priorities = {
        feature: criteria["impact"][feature] / criteria["effort"][feature]
        for feature in features
    }
    sorted_features = sorted(
        features,
        key=lambda f: priorities[f],
        reverse=True
    )
    
    # Check prioritization order matches our calculations
    for i, feature in enumerate(sorted_features):
        assert prioritized[i]["feature"] == feature
        assert prioritized[i]["priority"] == priorities[feature]
