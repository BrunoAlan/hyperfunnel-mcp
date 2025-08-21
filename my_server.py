from fastmcp import FastMCP
import httpx
import asyncio

mcp = FastMCP("HyperFunnel Destinations API Client")


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


if __name__ == "__main__":
    mcp.run()
