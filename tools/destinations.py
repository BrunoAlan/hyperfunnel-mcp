"""
Destination-related tools for the HyperFunnel MCP Server.

This module contains all tools related to destination operations.
"""

import httpx
from fastmcp import FastMCP
from config import get_api_base_url


class DestinationTools:
    """Destination-related tools using class-based approach with dependency injection."""
    
    def __init__(self, mcp: FastMCP):
        self.mcp = mcp
        self.base_url = get_api_base_url()
        # Auto-register all tools when class is instantiated
        self._register_tools()
    
    def _register_tools(self):
        """Automatically register all tool methods."""
        self.mcp.tool()(self.get_available_destinations)
    
    async def get_available_destinations(self) -> dict:
        """
        Retrieves information on available travel destinations from the HyperFunnel service.
        This tool is used to answer questions about which destinations can be booked,
        their specific features, or to check if a specific destination exists in the system.
        Args:
            None. This tool does not require any arguments.
        Returns:
             dict: The complete API response, including destination data.
        """
        url = f"{self.base_url}/destinations"

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url)

                # Try to parse as JSON, fallback to text if it fails
                try:
                    content = response.json()
                except:
                    content = response.text

                return {
                    "status_code": response.status_code,
                    "headers": dict(response.headers),
                    "content": content,
                    "success": response.is_success,
                }

        except httpx.ConnectError:
            return {
                "error": "Could not connect to localhost:8000. Make sure the API is running.",
                "status_code": None,
                "success": False,
            }
        except Exception as e:
            return {
                "error": f"Unexpected error: {str(e)}",
                "status_code": None,
                "success": False,
            }
