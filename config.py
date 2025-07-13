"""
Configuration Module

This module handles logging setup and configuration for the Reddit persona generator.
"""

import logging
import os
from typing import Optional


def setup_logging(verbose: bool = False, log_file: Optional[str] = None) -> None:
    """
    Setup logging configuration.
    
    Args:
        verbose: Enable verbose logging
        log_file: Optional log file path
    """
    log_level = logging.DEBUG if verbose else logging.INFO
    
    # Create formatters
    console_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Setup console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(console_formatter)
    
    # Setup root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.addHandler(console_handler)
    
    # Setup file handler if specified
    if log_file:
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
        )
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_level)
        file_handler.setFormatter(file_formatter)
        root_logger.addHandler(file_handler)
    
    # Reduce noise from external libraries
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('prawcore').setLevel(logging.WARNING)
    logging.getLogger('httpx').setLevel(logging.WARNING)


def get_required_env_vars() -> dict:
    """
    Get required environment variables for the application.
    
    Returns:
        Dictionary of environment variables
    """
    return {
        'GEMINI_API_KEY': os.getenv('GEMINI_API_KEY', ''),
        'REDDIT_CLIENT_ID': os.getenv('REDDIT_CLIENT_ID', ''),
        'REDDIT_CLIENT_SECRET': os.getenv('REDDIT_CLIENT_SECRET', ''),
        'REDDIT_USER_AGENT': os.getenv('REDDIT_USER_AGENT', 'PersonaGenerator/1.0'),
        'REDDIT_USERNAME': os.getenv('REDDIT_USERNAME', ''),
        'REDDIT_PASSWORD': os.getenv('REDDIT_PASSWORD', '')
    }


def validate_environment() -> bool:
    """
    Validate that required environment variables are set.
    
    Returns:
        True if all required variables are set, False otherwise
    """
    required_vars = ['GEMINI_API_KEY', 'REDDIT_CLIENT_ID', 'REDDIT_CLIENT_SECRET']
    env_vars = get_required_env_vars()
    
    missing_vars = []
    for var in required_vars:
        if not env_vars.get(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"Missing required environment variables: {', '.join(missing_vars)}")
        print("\nPlease set the following environment variables:")
        print("- GEMINI_API_KEY: Your Gemini API key")
        print("- REDDIT_CLIENT_ID: Your Reddit app client ID")
        print("- REDDIT_CLIENT_SECRET: Your Reddit app client secret")
        print("- REDDIT_USER_AGENT: User agent string (optional)")
        print("- REDDIT_USERNAME: Reddit username (optional, for authenticated access)")
        print("- REDDIT_PASSWORD: Reddit password (optional, for authenticated access)")
        return False
    
    return True


# Application constants
DEFAULT_OUTPUT_DIR = './personas'
DEFAULT_MAX_POSTS = 100
DEFAULT_MAX_COMMENTS = 200
DEFAULT_USER_AGENT = 'PersonaGenerator/1.0'

# API limits and timeouts
REDDIT_API_DELAY = 0.1  # Seconds between API calls
GEMINI_MAX_TOKENS = 4000
GEMINI_TEMPERATURE = 0.3
