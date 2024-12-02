import pytest
from pathlib import Path
import logging
from swarm_forge.core.logging import ForgeLogger

def test_forge_logger_initialization():
    """Test basic logger initialization"""
    logger = ForgeLogger(name="test_logger")
    assert logger.logger.name == "test_logger"
    assert len(logger.logger.handlers) == 2  # Console and file handler

def test_forge_logger_debug_mode():
    """Test logger in debug mode"""
    logger = ForgeLogger(name="test_logger", debug=True)
    assert logger.logger.level == logging.DEBUG
    
def test_forge_logger_custom_log_dir(tmp_path):
    """Test logger with custom log directory"""
    log_dir = tmp_path / "test_logs"
    logger = ForgeLogger(name="test_logger", log_dir=log_dir)
    assert log_dir.exists()
    assert len(list(log_dir.glob("*.log"))) == 1

def test_forge_logger_methods(tmp_path, caplog):
    """Test all logging methods"""
    logger = ForgeLogger(name="test_logger", log_dir=tmp_path)
    
    test_messages = {
        "debug": "Debug message",
        "info": "Info message",
        "warning": "Warning message",
        "error": "Error message",
        "critical": "Critical message"
    }
    
    for level, message in test_messages.items():
        getattr(logger, level)(message)
        assert message in caplog.text

def test_forge_logger_exception_handling(tmp_path):
    """Test exception logging"""
    logger = ForgeLogger(name="test_logger", log_dir=tmp_path)
    
    try:
        raise ValueError("Test exception")
    except ValueError:
        logger.exception("Caught an error")
    
    log_file = next(tmp_path.glob("*.log"))
    log_content = log_file.read_text()
    assert "Caught an error" in log_content
    assert "ValueError: Test exception" in log_content
