"""
Hotel-related tools for the HyperFunnel MCP Server.

This module contains all tools related to hotel operations including
getting hotel lists, individual hotel details, and hotel room information.
"""

import httpx
from typing import Optional
from fastmcp import FastMCP
from config import get_api_base_url


def register_hotel_tools(mcp: FastMCP):
    """Register all hotel-related tools with the MCP server."""

    @mcp.tool()
    async def search_hotels(
        country: Optional[str] = None, city: Optional[str] = None
    ) -> dict:
        """
        Searches for available hotel information, filtering by country or city.

        Use this tool to find hotels in a specific location, check availability,
        and retrieve their key features.

        Args:
            country (str, optional): The name of the country to filter hotels.
            city (str, optional): The name of the city to filter hotels.
                If both country and city are provided, the search will prioritize the city.

        Returns:
            dict: A dictionary containing the data of the hotels found.
        """
        base_url = f"{get_api_base_url()}/hotels"

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
        url = f"{get_api_base_url()}/hotels/{hotel_id}"

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
    async def get_hotel_details_with_rooms(hotel_id: str) -> dict:
        """
        Retrieves complete details for a specific hotel, including information for all of its rooms.

        This tool is ideal when you need comprehensive information about a specific hotel
        to display on a product page or during a booking process.

        Args:
            hotel_id (str): The unique identifier of the hotel.

        Returns:
            dict: A dictionary containing the hotel's details and a list of its rooms.
        """
        url = f"{get_api_base_url()}/hotels/{hotel_id}/with-rooms"

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
