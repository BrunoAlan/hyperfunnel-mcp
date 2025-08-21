"""
HyperFunnel MCP Server - Main Entry Point

This is the main MCP server file that imports and registers all tools
from the modular tools package structure.
"""

from fastmcp import FastMCP
from tools.hotels import register_hotel_tools
from tools.destinations import register_destination_tools

# Initialize the MCP server
mcp = FastMCP("HyperFunnel Destinations API Client")

# Register all tool modules
register_hotel_tools(mcp)
register_destination_tools(mcp)

if __name__ == "__main__":
    mcp.run()
