"""
HyperFunnel MCP Server - Main Entry Point

This is the main MCP server file that imports and registers all tools
using the class-based approach with dependency injection.
"""

from fastmcp import FastMCP
from tools.hotels import HotelTools
from tools.destinations import DestinationTools
from tools.rooms import RoomTools

# Initialize the MCP server
mcp = FastMCP("HyperFunnel Destinations API Client")

# Initialize tool classes - they auto-register when instantiated
HotelTools(mcp)
DestinationTools(mcp)
RoomTools(mcp)

if __name__ == "__main__":
    mcp.run()
