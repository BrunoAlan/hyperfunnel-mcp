"""
Destination-related tools for the HyperFunnel MCP Server.

This module contains all tools related to destination operations.
"""

import httpx
from fastmcp import FastMCP


def register_destination_tools(mcp: FastMCP):
    """Register all destination-related tools with the MCP server."""
    
    @mcp.tool()
    async def destination_request() -> dict:
        """
        Retrieves destination information from the HyperFunnel API.

        This tool connects to the destinations service running on localhost:8000
        to fetch data about available destinations, route configurations,
        or any information related to the /destinations endpoint.

        Typical use cases:
        - Query available destinations in the system
        - Check the status of the destinations service
        - Get routing configurations
        - Monitor connectivity with the destinations service

        The tool automatically handles connection errors and response parsing,
        returning both JSON responses and plain text depending on what the API returns.

        Returns:
            dict: Complete API response that includes:
                - status_code (int): HTTP status code (200, 404, 500, etc.)
                - headers (dict): Response headers from the server
                - content (dict|str): Response content (parsed JSON or text)
                - success (bool): True if the response was successful (2xx)
                - error (str, optional): Error message if any problem occurred

        Note: Requires the service to be running on localhost:8000
        """
        url = "http://localhost:8000/destinations"

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
