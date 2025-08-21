import httpx
from fastmcp import FastMCP
from config import get_api_base_url


class RoomTools:
    """Room-related tools using class-based approach with dependency injection."""

    def __init__(self, mcp: FastMCP):
        self.mcp = mcp
        self.base_url = get_api_base_url()
        # Auto-register all tools when class is instantiated
        self._register_tools()

    def _register_tools(self):
        """Automatically register all tool methods."""
        self.mcp.tool()(self.get_rooms_by_hotel_id)

    async def get_rooms_by_hotel_id(self, hotel_id: str) -> dict:
        """
        Retrieves all rooms available for a specific hotel from the HyperFunnel API.

        This tool connects to the rooms service running on localhost:8000
        to fetch complete room inventory for a specific hotel using its unique identifier.
        The tool provides detailed information about all rooms including types, availability,
        pricing, and amenities for the specified hotel.

        Typical use cases:
        - Get all available rooms for a specific hotel
        - Display room inventory for booking purposes
        - Check room availability and pricing for a hotel
        - Access detailed room information including amenities and features
        - Verify room options and capacity for hotel guests
        - Compare different room types within the same hotel

        The tool automatically handles connection errors and response parsing,
        returning structured responses with comprehensive error handling.

        Args:
            hotel_id (str): The unique UUID identifier of the hotel to get rooms for

        Returns:
            dict: Complete API response that includes:
                - status_code (int): HTTP status code (200, 400, 404, 500, etc.)
                - headers (dict): Response headers from the server
                - content (dict|str): Response content (array of Room objects or error)
                - success (bool): True if the response was successful (2xx)
                - error (str, optional): Error message if any problem occurred
                - url (str): The final URL that was requested

        Expected Error Responses:
            - 400: Invalid UUID format provided for hotel_id
            - 404: Hotel not found or no rooms available for the specified hotel
            - 500: Internal server error

        Note: Requires the service to be running on localhost:8000
        """
        url = f"{self.base_url}/rooms/by-hotel/{hotel_id}"

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
