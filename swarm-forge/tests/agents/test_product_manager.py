import pytest
from pathlib import Path
from swarm_forge.agents.roles import ProductManager
from swarm_forge.core.config import ProjectConfig
from tests.utils import AgentTestContext, compare_json_structures

def test_product_manager_initialization():
    """Test ProductManager initialization"""
    agent = ProductManager()
    assert agent.name == "Product Manager"
    assert isinstance(agent.model, str)
    assert isinstance(agent.temperature, float)

def test_gather_requirements(test_project_config, mock_requirements):
    """Test requirements gathering"""
    agent = ProductManager()
    
    # Mock the agent's response
    agent_responses = {
        "gather_requirements": mock_requirements
    }
    
    with AgentTestContext({"ProductManager": agent_responses}):
        requirements = agent.gather_requirements(test_project_config)
        
        # Verify the structure of the requirements
        assert "features" in requirements
        assert "user_stories" in requirements
        assert "acceptance_criteria" in requirements
        
        # Verify the content matches our mock data
        compare_json_structures(requirements, mock_requirements)

def test_gather_requirements_validation(test_project_config):
    """Test requirements validation"""
    agent = ProductManager()
    
    # Test with invalid project config
    with pytest.raises(ValueError):
        agent.gather_requirements(None)
    
    # Test with empty project description
    invalid_config = ProjectConfig(
        name="test",
        description="",
        type="web"
    )
    with pytest.raises(ValueError):
        agent.gather_requirements(invalid_config)

def test_requirements_format(test_project_config, mock_requirements):
    """Test the format of gathered requirements"""
    agent = ProductManager()
    
    agent_responses = {
        "gather_requirements": mock_requirements
    }
    
    with AgentTestContext({"ProductManager": agent_responses}):
        requirements = agent.gather_requirements(test_project_config)
        
        # Check features
        assert isinstance(requirements["features"], list)
        for feature in requirements["features"]:
            assert isinstance(feature, str)
        
        # Check user stories
        assert isinstance(requirements["user_stories"], list)
        for story in requirements["user_stories"]:
            assert isinstance(story, str)
            assert story.startswith("As a")
        
        # Check acceptance criteria
        assert isinstance(requirements["acceptance_criteria"], dict)
        for feature, criteria in requirements["acceptance_criteria"].items():
            assert isinstance(feature, str)
            assert isinstance(criteria, list)
            for criterion in criteria:
                assert isinstance(criterion, str)

def test_requirements_consistency(test_project_config, mock_requirements):
    """Test consistency between multiple calls"""
    agent = ProductManager()
    
    agent_responses = {
        "gather_requirements": mock_requirements
    }
    
    with AgentTestContext({"ProductManager": agent_responses}):
        requirements1 = agent.gather_requirements(test_project_config)
        requirements2 = agent.gather_requirements(test_project_config)
        
        # Both calls should return the same structure
        assert requirements1 == requirements2
        
        # Verify the content hasn't changed
        compare_json_structures(requirements1, mock_requirements)
        compare_json_structures(requirements2, mock_requirements)
