"""
Logger Module
Handles application logging and debugging
"""

import logging
import os
from datetime import datetime
from pathlib import Path

class Logger:
    def __init__(self, log_file="logs/file_manager.log", level=logging.INFO):
        self.log_file = Path(log_file)
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Configure logging
        logging.basicConfig(
            level=level,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def info(self, message):
        """Log info message"""
        self.logger.info(message)
        
    def error(self, message):
        """Log error message"""
        self.logger.error(message)
        
    def warning(self, message):
        """Log warning message"""
        self.logger.warning(message)
        
    def debug(self, message):
        """Log debug message"""
        self.logger.debug(message)