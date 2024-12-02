from typing import List
from swarm import Swarm, Agent
from ..agents.roles import (
    ProductManager,
    SystemArchitect,
    BackendDeveloper,
    FrontendDeveloper,
    DevOpsEngineer,
    TechnicalWriter
)
from .config import ProjectConfig
from .logging import logger
from .settings import settings, ProjectSettings

class ProjectManager:
    def __init__(self, config: ProjectConfig):
        logger.info(f"Initializing project manager for project: {config.name}")
        self.config = config
        self.swarm = Swarm()
        
        # Create project settings
        self.project_settings = ProjectSettings(
            name=config.name,
            description=config.description,
            output_dir=settings.get_project_dir(config.name)
        )
        
        # Save initial project settings
        settings.save_project_settings(self.project_settings)
        
        self.initialize_agents()
        
    def initialize_agents(self):
        """Initialize all the specialized agents"""
        logger.debug("Initializing specialized agents")
        
        # Initialize agents with their specific configurations
        self.product_manager = ProductManager(
            model=settings.product_manager.model,
            temperature=settings.product_manager.temperature
        )
        
        self.system_architect = SystemArchitect(
            model=settings.system_architect.model,
            temperature=settings.system_architect.temperature
        )
        
        self.backend_developer = BackendDeveloper(
            model=settings.backend_developer.model,
            temperature=settings.backend_developer.temperature
        )
        
        self.frontend_developer = FrontendDeveloper(
            model=settings.frontend_developer.model,
            temperature=settings.frontend_developer.temperature
        )
        
        self.devops_engineer = DevOpsEngineer(
            model=settings.devops_engineer.model,
            temperature=settings.devops_engineer.temperature
        )
        
        self.technical_writer = TechnicalWriter(
            model=settings.technical_writer.model,
            temperature=settings.technical_writer.temperature
        )
        
        logger.info("All agents initialized successfully")
        
    def start_development(self):
        """
        Orchestrate the entire development process through different phases
        """
        logger.info("Starting development process")
        try:
            # Phase 1: Requirements and Planning
            logger.info("Phase 1: Requirements and Planning")
            requirements = self.product_manager.gather_requirements(self.config)
            architecture = self.system_architect.design_architecture(requirements)
            
            # Update project settings with requirements
            self.project_settings.features = requirements.get('features', [])
            self.project_settings.dependencies = architecture.get('dependencies', {})
            settings.save_project_settings(self.project_settings)
            
            # Phase 2: Development
            logger.info("Phase 2: Development")
            backend_code = self.backend_developer.implement_backend(architecture)
            frontend_code = self.frontend_developer.implement_frontend(architecture)
            
            # Phase 3: DevOps and Documentation
            logger.info("Phase 3: DevOps and Documentation")
            deployment_config = self.devops_engineer.setup_deployment(
                backend_code, 
                frontend_code
            )
            documentation = self.technical_writer.create_documentation(
                requirements,
                architecture,
                deployment_config
            )
            
            # Generate the final project
            logger.info("Generating final project files")
            self._generate_project_files(
                backend_code,
                frontend_code,
                deployment_config,
                documentation
            )
            logger.info("Development process completed successfully")
            
        except Exception as e:
            logger.exception("Error during development process")
            raise
    
    def _generate_project_files(self, *args):
        """Generate all project files in the output directory"""
        # TODO: Implement project file generation
        logger.debug("Project file generation not yet implemented")
