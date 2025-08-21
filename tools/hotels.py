"""
Hotel-related tools for the HyperFunnel MCP Server.

This module contains all tools related to hotel operations including
getting hotel lists, individual hotel details, and hotel room information.
"""

import httpx
from fastmcp import FastMCP


def register_hotel_tools(mcp: FastMCP):
    """Register all hotel-related tools with the MCP server."""

    @mcp.tool()
    async def get_hotels(country: str = None, city: str = None) -> dict:
        """
        Retrieves hotel information from the HyperFunnel API.

        This tool connects to the hotels service running on localhost:8000
        to fetch data about available hotels. You can filter by country or city,
        or get all available hotels if no filters are provided.
        Dont show the ids to the user.

        Typical use cases:
        - Get all available hotels in the system
        - Filter hotels by specific country
        - Filter hotels by specific city
        - Check hotel availability and details

        The tool automatically handles connection errors and response parsing,
        returning both JSON responses and plain text depending on what the API returns.

        Args:
            country (str, optional): Filter hotels by country (e.g., "mexico", "spain")
            city (str, optional): Filter hotels by city (e.g., "cancun", "madrid")

        Note: If both country and city are provided, city takes precedence.

        Returns:
            dict: Complete API response that includes:
                - status_code (int): HTTP status code (200, 404, 500, etc.)
                - headers (dict): Response headers from the server
                - content (dict|str): Response content (parsed JSON or text)
                - success (bool): True if the response was successful (2xx)
                - error (str, optional): Error message if any problem occurred

        Note: Requires the service to be running on localhost:8000
        """
        base_url = "http://127.0.0.1:8000/hotels"

        # Build query parameters
        params = {}
        if city:
            params["city"] = city
        elif country:
            params["country"] = country

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(base_url, params=params)

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
                    "url": str(response.url),  # Include the final URL with parameters
                }

        except httpx.ConnectError:
            return {
                "error": "Could not connect to 127.0.0.1:8000. Make sure the API is running.",
                "status_code": None,
                "success": False,
            }
        except Exception as e:
            return {
                "error": f"Unexpected error: {str(e)}",
                "status_code": None,
                "success": False,
            }

    @mcp.tool()
    async def get_hotel_by_id(hotel_id: str) -> dict:
        """
        Retrieves detailed information for a specific hotel by its ID from the HyperFunnel API.

        This tool connects to the hotels service running on localhost:8000
        to fetch complete details about a specific hotel using its unique identifier.

        Typical use cases:
        - Get complete details of a specific hotel
        - Retrieve hotel information for booking or display purposes
        - Access detailed hotel data including amenities, location, and pricing
        - Verify hotel existence and availability

        The tool automatically handles connection errors and response parsing,
        returning both JSON responses and plain text depending on what the API returns.

        Args:
            hotel_id (str): The unique UUID identifier of the hotel

        Returns:
            dict: Complete API response that includes:
                - status_code (int): HTTP status code (200, 404, 500, etc.)
                - headers (dict): Response headers from the server
                - content (dict|str): Response content (complete Hotel object or error)
                - success (bool): True if the response was successful (2xx)
                - error (str, optional): Error message if any problem occurred
                - url (str): The final URL that was requested

        Note: Requires the service to be running on localhost:8000
        """
        url = f"http://127.0.0.1:8000/hotels/{hotel_id}"

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
                    "url": url,
                }

        except httpx.ConnectError:
            return {
                "error": "Could not connect to 127.0.0.1:8000. Make sure the API is running.",
                "status_code": None,
                "success": False,
                "url": url,
            }
        except Exception as e:
            return {
                "error": f"Unexpected error: {str(e)}",
                "status_code": None,
                "success": False,
                "url": url,
            }

    @mcp.tool()
    async def get_hotel_with_rooms(hotel_id: str) -> dict:
        """
        Retrieves detailed information for a specific hotel including all its rooms from the HyperFunnel API.

        This tool connects to the hotels service running on localhost:8000
        to fetch complete details about a specific hotel along with all available rooms
        using the hotel's unique identifier.

        Typical use cases:
        - Get complete hotel details with room inventory
        - Retrieve hotel and room information for booking systems
        - Access detailed hotel data including all room types, availability, and pricing
        - Display comprehensive hotel information with room options
        - Verify hotel existence and room availability

        The tool automatically handles connection errors and response parsing,
        returning both JSON responses and plain text depending on what the API returns.

        Args:
            hotel_id (str): The unique UUID identifier of the hotel

        Returns:
            dict: Complete API response that includes:
                - status_code (int): HTTP status code (200, 400, 404, 500, etc.)
                - headers (dict): Response headers from the server
                - content (dict|str): Response content (Hotel object with rooms array included or error)
                - success (bool): True if the response was successful (2xx)
                - error (str, optional): Error message if any problem occurred
                - url (str): The final URL that was requested

        Expected Error Responses:
            - 400: Invalid UUID format provided
            - 404: Hotel not found with the specified ID
            - 500: Internal server error

        Note: Requires the service to be running on localhost:8000
        """
        url = f"http://127.0.0.1:8000/hotels/{hotel_id}/with-rooms"

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
                    "url": url,
                }

        except httpx.ConnectError:
            return {
                "error": "Could not connect to 127.0.0.1:8000. Make sure the API is running.",
                "status_code": None,
                "success": False,
                "url": url,
            }
        except Exception as e:
            return {
                "error": f"Unexpected error: {str(e)}",
                "status_code": None,
                "success": False,
                "url": url,
            }
