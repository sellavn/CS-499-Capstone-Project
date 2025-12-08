# CS-499 Nick Valles
# Enhancement 3+ - Module 6

"""
logging configuration for Course Planner application

provides centralized logging with configurable levels and file output

"""

import logging
import sys
from pathlib import Path
from typing import Optional


class LoggerConfig:
    """
    manages application-wide logging configuration
    
    provides structured logging with console and file handlers,
    configurable log levels, and proper formatting
    
    """
    
    _logger: Optional[logging.Logger] = None
    _initialized: bool = False
    
    @classmethod
    def get_logger(cls, name: str = "course_planner") -> logging.Logger:
        """
        get or create the application logger
        
        Args:
            name: logger name (default: course_planner)
            
        Returns:
            configured logger instance

        """

        if not cls._initialized:
            cls.setup_logging()
        
        return logging.getLogger(name)
    
    @classmethod
    def setup_logging(
        cls,
        level: str = "INFO",
        log_to_file: bool = False,
        log_file: str = "course_planner.log",
        format_style: str = "detailed"
    ):
        """
        configure application logging
        
        Args:
            level: log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            log_to_file: enable file logging
            log_file: path to log file
            format_style: 'simple' or 'detailed' formatting

        """

        if cls._initialized:
            return
        
        # convert string level to logging constant
        numeric_level = getattr(logging, level.upper(), logging.INFO)
        
        # create logger
        logger = logging.getLogger("course_planner")
        logger.setLevel(numeric_level)
        logger.handlers.clear()  # removes existing headers
        
        # define formats
        if format_style == "detailed":
            format_string = "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s"
            date_format = "%Y-%m-%d %H:%M:%S"
        else:  # simple
            format_string = "%(levelname)s: %(message)s"
            date_format = None
        
        formatter = logging.Formatter(format_string, datefmt=date_format)
        
        # console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(numeric_level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        # optional file handler
        if log_to_file:
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(numeric_level)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        
        cls._logger = logger
        cls._initialized = True
        
        logger.debug(f"Logging initialized - Level: {level}, File logging: {log_to_file}")
    
    @classmethod
    def set_level(cls, level: str):
        """
        change logging level dynamically
        
        Args:
            level: new log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        """
        if not cls._initialized:
            cls.setup_logging(level=level)
            return
        
        numeric_level = getattr(logging, level.upper(), logging.INFO)
        logger = logging.getLogger("course_planner")
        logger.setLevel(numeric_level)
        
        for handler in logger.handlers:
            handler.setLevel(numeric_level)
        
        logger.debug(f"Log level changed to {level}")
    
    @classmethod
    def enable_verbose(cls):
        """Enable verbose (DEBUG level) logging"""
        cls.set_level("DEBUG")
    
    @classmethod
    def disable_verbose(cls):
        """Disable verbose logging (back to INFO level)"""
        cls.set_level("INFO")


# convenience for quick logger access
def get_logger(name: str = "course_planner") -> logging.Logger:
    """
    get application logger
    
    Args:
        name: logger name
        
    Returns:
        configured logger instance
    """
    return LoggerConfig.get_logger(name)
