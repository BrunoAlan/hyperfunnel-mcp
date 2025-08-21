"""
Configuration module for HyperFunnel MCP Server.

This module handles loading environment variables and providing
configuration values to the application.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()


def get_api_base_url() -> str:
    """
    Get the HyperFunnel API base URL from environment variables.

    Returns:
        str: The base URL for the HyperFunnel API. Defaults to http://127.0.0.1:8000
             if HYPERFUNNEL_API_BASE_URL is not set in environment.
    """
    return os.getenv("HYPERFUNNEL_API_BASE_URL", "http://127.0.0.1:8000")
