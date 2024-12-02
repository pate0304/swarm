from pathlib import Path
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field, validator
from pydantic_settings import BaseSettings
import os

class AgentConfig(BaseModel):
    """Configuration for an individual agent"""
    model: str = "gpt-4"
    temperature: float = Field(default=0.7, ge=0, le=1)
    max_tokens: Optional[int] = None
    custom_instructions: Optional[str] = None
    tools: Optional[List[str]] = None

class ProjectSettings(BaseModel):
    """Project-specific settings"""
    name: str
    description: str
    type: str = "web"
    output_dir: Path
    template: Optional[str] = None
    features: List[str] = Field(default_factory=list)
    dependencies: Dict[str, str] = Field(default_factory=dict)
    
    @validator('output_dir')
    def create_output_dir(cls, v):
        v.mkdir(parents=True, exist_ok=True)
        return v

class ForgeSettings(BaseSettings):
    """Global settings for Swarm Forge"""
    # OpenAI settings
    openai_api_key: str = Field(..., env='OPENAI_API_KEY')
    
    # Agent configurations
    default_model: str = "gpt-4"
    product_manager: AgentConfig = Field(default_factory=AgentConfig)
    system_architect: AgentConfig = Field(default_factory=AgentConfig)
    backend_developer: AgentConfig = Field(default_factory=AgentConfig)
    frontend_developer: AgentConfig = Field(default_factory=AgentConfig)
    devops_engineer: AgentConfig = Field(default_factory=AgentConfig)
    technical_writer: AgentConfig = Field(default_factory=AgentConfig)
    
    # Project settings
    projects_root: Path = Field(
        default=Path.home() / ".swarm-forge" / "projects",
        env='FORGE_PROJECTS_ROOT'
    )
    templates_dir: Path = Field(
        default=Path.home() / ".swarm-forge" / "templates",
        env='FORGE_TEMPLATES_DIR'
    )
    
    # Logging settings
    log_level: str = Field(default="INFO", env='FORGE_LOG_LEVEL')
    log_dir: Path = Field(
        default=Path.home() / ".swarm-forge" / "logs",
        env='FORGE_LOG_DIR'
    )
    
    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
    
    @validator('projects_root', 'templates_dir', 'log_dir')
    def create_directory(cls, v):
        v.mkdir(parents=True, exist_ok=True)
        return v
    
    def get_project_dir(self, project_name: str) -> Path:
        """Get the directory for a specific project"""
        return self.projects_root / project_name
    
    def load_project_settings(self, project_name: str) -> ProjectSettings:
        """Load settings for a specific project"""
        project_dir = self.get_project_dir(project_name)
        settings_file = project_dir / "forge.json"
        
        if settings_file.exists():
            return ProjectSettings.parse_file(settings_file)
        
        return ProjectSettings(
            name=project_name,
            description="",
            output_dir=project_dir
        )
    
    def save_project_settings(self, settings: ProjectSettings):
        """Save project settings to file"""
        settings_file = settings.output_dir / "forge.json"
        with settings_file.open('w') as f:
            f.write(settings.json(indent=2))

# Initialize settings only when explicitly requested
def get_settings() -> ForgeSettings:
    """Get the global settings instance"""
    return ForgeSettings()
