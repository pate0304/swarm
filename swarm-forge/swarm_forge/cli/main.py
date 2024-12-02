import typer
from rich.console import Console
from rich.prompt import Prompt, Confirm
from pathlib import Path
from ..core.project_manager import ProjectManager
from ..core.config import ProjectConfig
from ..core.logging import logger
from ..core.settings import settings, ProjectSettings

app = typer.Typer()
console = Console()

def validate_project_name(name: str) -> bool:
    """Validate project name and check if it already exists"""
    if not name.isidentifier():
        console.print("[red]Project name must be a valid Python identifier[/red]")
        return False
        
    project_dir = settings.get_project_dir(name)
    if project_dir.exists():
        console.print("[red]Project already exists[/red]")
        return False
    
    return True

@app.command()
def create():
    """
    Start a new software project with AI-powered development lifecycle
    """
    logger.info("Starting new project creation")
    console.print("[bold green]Welcome to Swarm Forge![/bold green]")
    console.print("Let's create your software project with AI-powered development.\n")
    
    try:
        # Gather project information
        while True:
            project_name = Prompt.ask("What's your project name?")
            if validate_project_name(project_name):
                break
        
        project_description = Prompt.ask("Describe your project idea in detail")
        project_type = Prompt.ask(
            "What type of project is this?",
            choices=["web", "mobile", "cli", "desktop"],
            default="web"
        )
        
        logger.debug(f"Project details - Name: {project_name}, Type: {project_type}")
        logger.debug(f"Project description: {project_description}")
        
        # Create project configuration
        config = ProjectConfig(
            name=project_name,
            description=project_description,
            type=project_type
        )
        
        # Initialize project manager
        manager = ProjectManager(config)
        
        with console.status("[bold green]Initializing development process...") as status:
            # Start the development process
            manager.start_development()
            
        console.print("\n[bold green]✓[/bold green] Project successfully created!")
        console.print(f"\nYour project has been created in: {settings.get_project_dir(project_name)}")
        logger.info(f"Project {project_name} created successfully")
        
    except Exception as e:
        logger.exception("Error during project creation")
        console.print(f"\n[bold red]Error:[/bold red] {str(e)}")
        raise typer.Exit(1)

@app.command()
def list():
    """
    List all projects created with Swarm Forge
    """
    logger.info("Listing all projects")
    console.print("[bold]Your Swarm Forge Projects:[/bold]\n")
    
    try:
        projects = []
        for project_dir in settings.projects_root.iterdir():
            if project_dir.is_dir():
                try:
                    project_settings = settings.load_project_settings(project_dir.name)
                    projects.append(project_settings)
                except Exception as e:
                    logger.warning(f"Could not load settings for project {project_dir.name}: {e}")
        
        if not projects:
            console.print("[yellow]No projects found[/yellow]")
            return
        
        for project in projects:
            console.print(f"[green]• {project.name}[/green]")
            console.print(f"  Description: {project.description}")
            console.print(f"  Type: {project.type}")
            console.print(f"  Location: {project.output_dir}\n")
            
    except Exception as e:
        logger.exception("Error listing projects")
        console.print(f"\n[bold red]Error:[/bold red] {str(e)}")
        raise typer.Exit(1)

@app.command()
def config():
    """
    Show or edit configuration settings
    """
    logger.info("Displaying configuration settings")
    console.print("[bold]Swarm Forge Configuration:[/bold]\n")
    
    console.print(f"[green]Projects Directory:[/green] {settings.projects_root}")
    console.print(f"[green]Templates Directory:[/green] {settings.templates_dir}")
    console.print(f"[green]Log Directory:[/green] {settings.log_dir}")
    console.print(f"[green]Log Level:[/green] {settings.log_level}")
    console.print("\n[green]Agent Configurations:[/green]")
    
    for agent in ["product_manager", "system_architect", "backend_developer",
                 "frontend_developer", "devops_engineer", "technical_writer"]:
        config = getattr(settings, agent)
        console.print(f"\n[bold]{agent.replace('_', ' ').title()}[/bold]")
        console.print(f"  Model: {config.model}")
        console.print(f"  Temperature: {config.temperature}")

if __name__ == "__main__":
    app()
