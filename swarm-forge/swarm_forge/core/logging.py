import logging
import sys
from pathlib import Path
from datetime import datetime
from rich.logging import RichHandler
from rich.console import Console
from typing import Optional

class ForgeLogger:
    """
    Custom logger for Swarm Forge with rich output and file logging
    """
    
    def __init__(
        self,
        name: str = "swarm_forge",
        log_dir: Optional[Path] = None,
        debug: bool = False
    ):
        self.console = Console()
        
        # Set up log directory
        if log_dir is None:
            log_dir = Path.home() / ".swarm-forge" / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        
        # Create logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG if debug else logging.INFO)
        
        # Remove existing handlers
        self.logger.handlers = []
        
        # Console handler with rich formatting
        console_handler = RichHandler(
            console=self.console,
            show_path=False,
            omit_repeated_times=False,
            rich_tracebacks=True
        )
        console_handler.setLevel(logging.DEBUG if debug else logging.INFO)
        self.logger.addHandler(console_handler)
        
        # File handler for detailed logging
        log_file = log_dir / f"forge_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
    
    def debug(self, message: str, *args, **kwargs):
        """Log debug message"""
        self.logger.debug(message, *args, **kwargs)
    
    def info(self, message: str, *args, **kwargs):
        """Log info message"""
        self.logger.info(message, *args, **kwargs)
    
    def warning(self, message: str, *args, **kwargs):
        """Log warning message"""
        self.logger.warning(message, *args, **kwargs)
    
    def error(self, message: str, *args, **kwargs):
        """Log error message"""
        self.logger.error(message, *args, **kwargs)
    
    def critical(self, message: str, *args, **kwargs):
        """Log critical message"""
        self.logger.critical(message, *args, **kwargs)
    
    def exception(self, message: str, *args, **kwargs):
        """Log exception with traceback"""
        self.logger.exception(message, *args, **kwargs)

# Global logger instance
logger = ForgeLogger()
