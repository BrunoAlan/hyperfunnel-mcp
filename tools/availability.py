"""
Availability-related tools for the HyperFunnel MCP Server.

This module contains all tools related to room availability operations including
searching for available rooms by various criteria and date ranges.
"""

import httpx
from typing import Optional
from fastmcp import FastMCP
from config import get_api_base_url


class AvailabilityTools:
    """Availability-related tools using class-based approach with dependency injection."""

    def __init__(self, mcp: FastMCP):
        self.mcp = mcp
        self.base_url = get_api_base_url()
        # Auto-register all tools when class is instantiated
        self._register_tools()

    def _register_tools(self):
        """Automatically register all tool methods."""
        self.mcp.tool()(self.search_availability)
        self.mcp.tool()(self.get_room_calendar)

    async def search_availability(
        self,
        check_in_date: str,
        check_out_date: str,
        guests: int,
        min_rooms: int,
        hotel_id: Optional[str] = None,
        room_id: Optional[str] = None,
    ) -> dict:
        """
        Finds available rooms for a given date range and number of guests.

        This tool is used to search for rooms across all hotels or within a specific hotel,
        based on check-in/out dates, number of guests, and minimum rooms required.

        Args:
            check_in_date (str): The check-in date in YYYY-MM-DD format.
            check_out_date (str): The check-out date in YYYY-MM-DD format.
            guests (int): The number of guests to accommodate.
            min_rooms (int): The minimum number of rooms required.
            hotel_id (str, optional): The ID of the specific hotel to search within.
            room_id (str, optional): The ID of the specific room type to search for.

        Returns:
            dict: A dictionary of available rooms that match the search criteria.
        """

        url = f"{self.base_url}/availability/search"

        # Build the request body following the AvailabilitySearch schema
        request_body = {
            "check_in_date": check_in_date,
            "check_out_date": check_out_date,
            "guests": guests,
            "min_rooms": min_rooms,
        }

        # Add optional parameters only if provided
        if hotel_id:
            request_body["hotel_id"] = hotel_id
        if room_id:
            request_body["room_id"] = room_id

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=request_body)

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
                    "request_body": request_body,  # Include request body for debugging
                }

        except httpx.ConnectError:
            return {
                "error": "Could not connect to 127.0.0.1:8000. Make sure the API is running.",
                "status_code": None,
                "success": False,
                "url": url,
                "request_body": request_body,
            }
        except Exception as e:
            return {
                "error": f"Unexpected error: {str(e)}",
                "status_code": None,
                "success": False,
                "url": url,
                "request_body": request_body,
            }

    async def get_room_calendar(
        self,
        room_id: str,
        check_in_date: str,
        check_out_date: str,
    ) -> dict:
        """
        Retrieves the availability calendar for a specific room within a date range.

        Use this tool to get the day-by-day availability status of a single room.

        Args:
            room_id (str): The unique identifier of the room.
            check_in_date (str): The start date for the calendar in YYYY-MM-DD format.
            check_out_date (str): The end date for the calendar in YYYY-MM-DD format.

        Returns:
            dict: A dictionary showing the room's availability for each day in the date range.
        """
        url = f"{self.base_url}/availability/room/{room_id}/calendar"

        # Build query parameters
        params = {
            "check_in_date": check_in_date,
            "check_out_date": check_out_date,
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=params)

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
                "url": url,
            }
        except Exception as e:
            return {
                "error": f"Unexpected error: {str(e)}",
                "status_code": None,
                "success": False,
                "url": url,
            }
