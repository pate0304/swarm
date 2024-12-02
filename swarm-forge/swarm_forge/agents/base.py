from typing import Any, Dict, List, Optional
from abc import ABC, abstractmethod
import re
from swarm_forge.core.settings import get_settings

class BaseAgent(ABC):
    """Base class for all agents"""

    def __init__(
        self,
        name: str,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        custom_instructions: Optional[str] = None
    ):
        """Initialize the agent with name and optional parameters"""
        self.name = name
        self.settings = get_settings()
        self.model = model if model is not None else self.settings.default_model
        self.temperature = temperature if temperature is not None else 0.7
        self.custom_instructions = custom_instructions

    @abstractmethod
    def get_base_instructions(self) -> str:
        """Get the base instructions for this agent"""
        pass

    @abstractmethod
    def process(self, input_data: Any) -> Any:
        """Process input data and return result"""
        pass

    def execute(self, input_data: Any) -> Any:
        """Execute the agent's process on input data"""
        return self.process(input_data)

class RequirementsAgent(BaseAgent):
    """Agent for handling requirements analysis"""

    def __init__(
        self,
        name: str = "Requirements Agent",
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        custom_instructions: Optional[str] = None
    ):
        """Initialize the requirements agent"""
        super().__init__(
            name=name,
            model=model,
            temperature=temperature,
            custom_instructions=custom_instructions
        )

    def get_base_instructions(self) -> str:
        return """
        You are a requirements analysis expert. Your role is to:
        1. Analyze and validate requirements
        2. Format and parse user stories
        3. Prioritize features based on impact and effort
        """

    def validate_requirements(self, requirements: Dict) -> bool:
        """Validate the structure and content of requirements"""
        try:
            # Check for required keys
            required_keys = ["features", "user_stories", "acceptance_criteria"]
            if not all(key in requirements for key in required_keys):
                return False

            # Validate types
            if not isinstance(requirements["features"], list):
                return False
            if not isinstance(requirements["user_stories"], list):
                return False
            if not isinstance(requirements["acceptance_criteria"], dict):
                return False

            # Validate relationships
            for feature in requirements["features"]:
                if feature not in requirements["acceptance_criteria"]:
                    return False
                if not isinstance(requirements["acceptance_criteria"][feature], list):
                    return False

            return True
        except Exception:
            return False

    def format_user_story(self, role: str, action: str, benefit: str) -> str:
        """Format a user story from components"""
        return f"As a {role}, I want to {action}, so that {benefit}"

    def parse_user_story(self, story: str) -> Dict[str, str]:
        """Parse a user story into components"""
        pattern = r"As a (?P<role>.*?), I want to (?P<action>.*?), so that (?P<benefit>.*)"
        match = re.match(pattern, story)
        
        if match:
            return match.groupdict()
        return {"role": "", "action": "", "benefit": ""}

    def prioritize_features(self, features: List[str], criteria: Dict) -> List[Dict]:
        """Prioritize features based on impact and effort"""
        priorities = []
        
        for feature in features:
            impact = criteria["impact"].get(feature, 0)
            effort = criteria["effort"].get(feature, 1)  # Avoid division by zero
            priority = impact / effort
            
            priorities.append({
                "feature": feature,
                "priority": priority
            })
        
        # Sort by priority score in descending order
        return sorted(priorities, key=lambda x: x["priority"], reverse=True)

    def process(self, input_data: Any) -> Any:
        """Process requirements related input"""
        return self.analyze_requirements(input_data)

    def analyze_requirements(self, requirements: Dict) -> Dict:
        """Analyze requirements and return processed results"""
        results = {
            "is_valid": self.validate_requirements(requirements),
            "prioritized_features": [],
            "parsed_stories": []
        }
        
        if results["is_valid"]:
            # Process features if criteria are provided
            if "criteria" in requirements:
                results["prioritized_features"] = self.prioritize_features(
                    requirements["features"],
                    requirements["criteria"]
                )
            
            # Parse user stories
            results["parsed_stories"] = [
                self.parse_user_story(story)
                for story in requirements["user_stories"]
            ]
        
        return results
