import pytest
from pathlib import Path
from pydantic import ValidationError
from swarm_forge.core.settings import (
    AgentConfig,
    ProjectSettings,
    ForgeSettings
)

def test_agent_config():
    """Test AgentConfig validation"""
    # Test default values
    config = AgentConfig()
    assert config.model == "gpt-4"
    assert config.temperature == 0.7
    
    # Test custom values
    config = AgentConfig(
        model="gpt-3.5-turbo",
        temperature=0.5,
        max_tokens=1000,
        custom_instructions="Be creative"
    )
    assert config.model == "gpt-3.5-turbo"
    assert config.temperature == 0.5
    assert config.max_tokens == 1000
    assert config.custom_instructions == "Be creative"
    
    # Test temperature validation
    with pytest.raises(ValidationError):
        AgentConfig(temperature=1.5)

def test_project_settings(tmp_path):
    """Test ProjectSettings validation and directory creation"""
    project_dir = tmp_path / "test_project"
    
    settings = ProjectSettings(
        name="test_project",
        description="Test project",
        output_dir=project_dir
    )
    
    assert settings.name == "test_project"
    assert settings.description == "Test project"
    assert settings.type == "web"
    assert project_dir.exists()

def test_forge_settings(tmp_path, monkeypatch):
    """Test ForgeSettings with environment variables"""
    # Set environment variables
    monkeypatch.setenv("OPENAI_API_KEY", "test_key")
    monkeypatch.setenv("FORGE_PROJECTS_ROOT", str(tmp_path / "projects"))
    monkeypatch.setenv("FORGE_LOG_LEVEL", "DEBUG")
    
    settings = ForgeSettings()
    
    assert settings.openai_api_key == "test_key"
    assert settings.log_level == "DEBUG"
    assert settings.projects_root == tmp_path / "projects"
    assert settings.projects_root.exists()

def test_project_settings_file_operations(tmp_path):
    """Test saving and loading project settings"""
    settings = ForgeSettings()
    settings.projects_root = tmp_path / "projects"
    
    project_settings = ProjectSettings(
        name="test_project",
        description="Test project",
        output_dir=settings.get_project_dir("test_project")
    )
    
    # Save settings
    settings.save_project_settings(project_settings)
    
    # Load settings
    loaded_settings = settings.load_project_settings("test_project")
    
    assert loaded_settings.name == project_settings.name
    assert loaded_settings.description == project_settings.description
    assert loaded_settings.output_dir == project_settings.output_dir
