# CS-499 Nick Valles
# Enhancement 3 - Module 5

""" 
configuration management for Course Planner application

handles reading/parsing configuration from config.ini

"""

import configparser
from pathlib import Path
from typing import Optional

class ConfigManager:
    """
    manages application configuration settings

    reads configuration from config.ini, provides
    access to settings throughout application
    
    """

    def __init__(self, config_file: str = 'config.ini'):
        """
        initialize config manager

        Args:
            config_file: path to config file, relative to project root path

        """

        self.config = configparser.ConfigParser()
        self.config_path = self._find_config_file(config_file)

        if self.config_path and self.config_path.exists():
            self.config.read(self.config_path)
        else:
            # use default config if file not found
            self._load_defaults()

    def _find_config_file(self, config_file: str) -> Optional[Path]:
        """
        locate config file

        searches in current directory and parent directories

        Args:
            config_file: Name of config file to find
        
        Returns:
            path to config file if found, none if otherwise
        
        """

        # look in current directory
        current = Path.cwd() / config_file
        if current.exists():
            return current

        # try parent directory (when running from src/)
        parent = Path.cwd().parent / config_file
        if parent.exists():
            return parent

        # try root
        root = Path(__file__).parent.parent / config_file
        if root.exists():
            return root
        
        return None

    def _load_defaults(self):
        """ load default config values """
        
        self.config['files'] = {
            'default_csv_path': 'data/CS_300_ABCU_Advising_Program_Input.csv'
        }
        self.config['app'] = {
            'name': 'Course Planner',
            'version': '1.0'
        }

    def get_default_csv_path(self) -> str:
        """
        gets default CSV file path from config

        Returns:
            path to default CSV file
        
        """

        return self.config.get('files', 'default_csv_path', fallback='data/CS_300_ABCU_Advising_Program_Input.csv')

    def get_version(self) -> str:
        """
        gets application version

        Returns:
            application version string
        
        """

        return self.config.get('app', 'version', fallback='1.0')

    def get_app_name(self) -> str:
        """
        get application name

        Returns:
            application name string
        
        """

        return self.config.get('app', 'name', fallback='Course Planner')

    def get_log_level(self) -> str:
        """
        get logging level from config
    
        Returns:
            log level string (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        
        """
        
        return self.config.get('logging', 'level', fallback='INFO').upper()

    def get_log_to_file(self) -> bool:
        """
        check if file logging is enabled
    
        Returns:
            true if file logging enabled
        """
        
        return self.config.getboolean('logging', 'log_to_file', fallback=False)

    def get_log_file(self) -> str:
        """
        get log file path from config
    
        Returns:
            path to log file
        """
        
        return self.config.get('logging', 'log_file', fallback='logs/course_planner.log')

    def get_log_format_style(self) -> str:
        """
        Get log format style
    
        Returns:
            formatting ('simple' or 'detailed')
        """
        return self.config.get('logging', 'format_style', fallback='simple')