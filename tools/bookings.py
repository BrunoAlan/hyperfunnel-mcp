"""
Booking-related tools for the HyperFunnel MCP Server.

This module contains all tools related to booking operations including
getting quotes and creating reservations.
"""

import httpx
from typing import Optional
from fastmcp import FastMCP
from config import get_api_base_url


class BookingTools:
    """Booking-related tools using class-based approach with dependency injection."""

    def __init__(self, mcp: FastMCP):
        self.mcp = mcp
        self.base_url = get_api_base_url()
        # Auto-register all tools when class is instantiated
        self._register_tools()

    def _register_tools(self):
        """Automatically register all tool methods."""
        self.mcp.tool()(self.get_booking_quote)
        self.mcp.tool()(self.create_booking)

    async def get_booking_quote(
        self,
        room_id: str,
        check_in_date: str,
        check_out_date: str,
        guests: int,
    ) -> dict:
        """
        Gets a booking quotation without creating an actual reservation.

        This is a KEY ENDPOINT that provides complete pricing information for a potential booking.
        It calculates total costs, validates availability, and provides detailed price breakdowns
        without committing to a reservation.

        Args:
            room_id (str): The unique identifier of the room to quote.
            check_in_date (str): Check-in date in YYYY-MM-DD format.
            check_out_date (str): Check-out date in YYYY-MM-DD format.
            guests (int): Number of guests (1-10).

        Returns:
            dict: Complete API response that includes:
                - status_code (int): HTTP status code (200, 400, 404, 409, 500)
                - headers (dict): Response headers from the server
                - content (dict|str): Complete quote object with:
                  * room_id, room_name
                  * check_in_date, check_out_date, guests
                  * nights: integer
                  * total_price: float
                  * average_price_per_night: float
                  * price_breakdown: array with daily prices
                  * currency: string
                  * availability_confirmed: boolean
                - success (bool): True if the response was successful (2xx)
                - error (str, optional): Error message if any problem occurred
                - url (str): The final URL that was requested
        """
        url = f"{self.base_url}/bookings/quote"

        # Build the request body following the BookingQuoteRequest schema
        request_body = {
            "room_id": room_id,
            "check_in_date": check_in_date,
            "check_out_date": check_out_date,
            "guests": guests,
        }

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
                    "request_body": request_body,
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

    async def create_booking(
        self,
        hotel_id: str,
        room_id: str,
        check_in_date: str,
        check_out_date: str,
        guests: int,
        price: Optional[float] = None,
        status: Optional[str] = None,
    ) -> dict:
        """
        Creates a new booking reservation in the system.

        This is a KEY ENDPOINT that handles the complete booking creation process.
        It automatically verifies availability, calculates pricing if not provided,
        reduces room availability, and manages transactions with rollback capability.

        Args:
            hotel_id (str): The unique identifier of the hotel.
            room_id (str): The unique identifier of the room to book.
            check_in_date (str): Check-in date in YYYY-MM-DD format.
            check_out_date (str): Check-out date in YYYY-MM-DD format.
            guests (int): Number of guests (1-10).
            price (float, optional): Total price. If not provided, will be calculated automatically.
            status (str, optional): Booking status. Defaults to PENDING if not specified.

        Returns:
            dict: Complete API response that includes:
                - status_code (int): HTTP status code (200, 400, 404, 409, 500)
                - headers (dict): Response headers from the server
                - content (dict|str): Created Booking object or error message
                - success (bool): True if the response was successful (2xx)
                - error (str, optional): Error message if any problem occurred
                - url (str): The final URL that was requested
        """
        url = f"{self.base_url}/bookings"

        # Build the request body following the BookingCreate schema
        request_body = {
            "hotel_id": hotel_id,
            "room_id": room_id,
            "check_in_date": check_in_date,
            "check_out_date": check_out_date,
            "guests": guests,
        }

        # Add optional parameters only if provided
        if price is not None:
            request_body["price"] = price
        if status is not None:
            request_body["status"] = status

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
                    "request_body": request_body,
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
