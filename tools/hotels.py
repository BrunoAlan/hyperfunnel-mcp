"""
Hotel-related tools for the HyperFunnel MCP Server.

This module contains all tools related to hotel operations including
getting hotel lists, individual hotel details, and hotel room information.
"""

import httpx
from typing import Optional
from fastmcp import FastMCP
from config import get_api_base_url


class HotelTools:
    """Hotel-related tools using class-based approach with dependency injection."""

    def __init__(self, mcp: FastMCP):
        self.mcp = mcp
        self.base_url = get_api_base_url()
        # Auto-register all tools when class is instantiated
        self._register_tools()

    def _register_tools(self):
        """Automatically register all tool methods."""
        self.mcp.tool()(self.search_hotels)
        self.mcp.tool()(self.get_hotel_by_id)
        self.mcp.tool()(self.get_hotel_details_with_rooms)

    async def search_hotels(
        self, country: Optional[str] = None, city: Optional[str] = None
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
        base_url = f"{self.base_url}/hotels"

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

    async def get_hotel_by_id(self, hotel_id: str) -> dict:
        """
        Retrieves a specific hotel's details using its unique identifier.

        This tool is best used when the user is asking for information about a single, known hotel.

        Args:
            hotel_id (str): The unique identifier of the hotel.

        Returns:
            dict: A dictionary with the complete hotel's details.
        """
        url = f"{self.base_url}/hotels/{hotel_id}"

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

    async def get_hotel_details_with_rooms(self, hotel_id: str) -> dict:
        """
        Retrieves complete details for a specific hotel, including information for all of its rooms.

        This tool is ideal when you need comprehensive information about a specific hotel
        to display on a product page or during a booking process.

        Args:
            hotel_id (str): The unique identifier of the hotel.

        Returns:
            dict: A dictionary containing the hotel's details and a list of its rooms.
        """
        url = f"{self.base_url}/hotels/{hotel_id}/with-rooms"

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
