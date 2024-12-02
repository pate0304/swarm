from pydantic import BaseModel
from typing import Optional, List, Dict

class ProjectConfig(BaseModel):
    name: str
    description: str
    type: Optional[str] = "web"  # web, mobile, cli, etc.
    features: Optional[List[str]] = []
    technical_requirements: Optional[Dict[str, str]] = {}
    output_directory: Optional[str] = "./projects"
