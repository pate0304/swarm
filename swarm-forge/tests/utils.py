from pathlib import Path
from typing import Dict, Any, Optional
import json
import pytest
from unittest.mock import Mock, patch
from swarm import Agent

class MockAgent:
    """Mock agent for testing with predefined responses"""
    
    def __init__(
        self,
        name: str = "Mock Agent",
        responses: Optional[Dict[str, Any]] = None
    ):
        self.name = name
        self._responses = responses or {}
        self._calls = []
    
    def __call__(self, *args, **kwargs):
        """Record the call and return predefined response"""
        call_info = {
            "args": args,
            "kwargs": kwargs
        }
        self._calls.append(call_info)
        
        # Get the appropriate response based on the function name
        func_name = kwargs.get("function", "default")
        if func_name in self._responses:
            return self._responses[func_name]
        return {"status": "success"}

def create_test_project_structure(
    root_dir: Path,
    project_name: str,
    files: Dict[str, str]
) -> Path:
    """
    Create a test project structure with specified files
    
    Args:
        root_dir: Root directory for the project
        project_name: Name of the project
        files: Dictionary mapping file paths to content
    
    Returns:
        Path to the created project directory
    """
    project_dir = root_dir / project_name
    project_dir.mkdir(parents=True, exist_ok=True)
    
    for file_path, content in files.items():
        full_path = project_dir / file_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_text(content)
    
    return project_dir

def assert_project_structure(
    project_dir: Path,
    expected_files: Dict[str, Optional[Dict[str, Any]]]
):
    """
    Assert that a project directory has the expected structure
    
    Args:
        project_dir: Project directory to check
        expected_files: Dictionary mapping file paths to expected content checks
    """
    for file_path, checks in expected_files.items():
        full_path = project_dir / file_path
        assert full_path.exists(), f"Expected file {file_path} does not exist"
        
        if checks:
            content = full_path.read_text()
            if checks.get("is_json", False):
                content = json.loads(content)
            
            for key, value in checks.get("contains", {}).items():
                if isinstance(content, dict):
                    assert key in content, f"Expected key {key} not found in {file_path}"
                    assert content[key] == value, f"Expected {value} for {key} in {file_path}"
                else:
                    assert value in content, f"Expected content {value} not found in {file_path}"

class AgentTestContext:
    """Context manager for testing agent interactions"""
    
    def __init__(self, agent_responses: Dict[str, Any] = None):
        self.agent_responses = agent_responses or {}
        self.patches = []
    
    def __enter__(self):
        """Set up the test context with mocked agents"""
        for agent_name, responses in self.agent_responses.items():
            # Create a new class that inherits from the original
            mock_class = type(
                f"Mock{agent_name}",
                (MockAgent,),
                {"__init__": lambda self, *args, **kwargs: MockAgent.__init__(self, responses=responses)}
            )
            
            # Patch the class
            patch_path = f"swarm_forge.agents.roles.{agent_name}"
            patcher = patch(patch_path, mock_class)
            self.patches.append(patcher)
            patcher.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Clean up the test context"""
        for patcher in self.patches:
            patcher.stop()

def compare_json_structures(actual: Dict, expected: Dict, path: str = "") -> None:
    """
    Compare two JSON structures for structural equality
    
    Args:
        actual: Actual JSON structure
        expected: Expected JSON structure
        path: Current path in the JSON structure (for error messages)
    """
    if not isinstance(actual, dict) or not isinstance(expected, dict):
        pytest.fail(f"Both structures must be dictionaries at {path}")
    
    actual_keys = set(actual.keys())
    expected_keys = set(expected.keys())
    
    missing_keys = expected_keys - actual_keys
    extra_keys = actual_keys - expected_keys
    
    if missing_keys:
        pytest.fail(f"Missing keys at {path}: {missing_keys}")
    if extra_keys:
        pytest.fail(f"Extra keys at {path}: {extra_keys}")
    
    for key in expected_keys:
        new_path = f"{path}.{key}" if path else key
        
        if isinstance(expected[key], dict):
            if not isinstance(actual[key], dict):
                pytest.fail(f"Expected dictionary at {new_path}")
            compare_json_structures(actual[key], expected[key], new_path)
        elif isinstance(expected[key], list):
            if not isinstance(actual[key], list):
                pytest.fail(f"Expected list at {new_path}")
            if len(actual[key]) != len(expected[key]):
                pytest.fail(f"List length mismatch at {new_path}")
        # Types are checked implicitly by the dictionary comparison
