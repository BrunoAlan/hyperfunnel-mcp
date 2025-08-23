"""
HyperFunnel MCP Server - Main Entry Point

This is the main MCP server file that imports and registers all tools
using the class-based approach with dependency injection.
"""

import argparse
import sys
from fastmcp import FastMCP
from tools.hotels import HotelTools
from tools.destinations import DestinationTools
from tools.rooms import RoomTools
from tools.availability import AvailabilityTools
from tools.bookings import BookingTools


def parse_arguments():
    """Parse command line arguments for transport selection."""
    parser = argparse.ArgumentParser(
        description="HyperFunnel MCP Server - Select transport type",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python my_server.py --transport http     # HTTP transport on port 8001
  python my_server.py --transport sse      # SSE transport on port 8001  
  python my_server.py --transport stdio    # STDIO transport (default)
  python my_server.py -t http              # Short form
  python my_server.py                      # Uses STDIO by default
        """,
    )

    parser.add_argument(
        "-t",
        "--transport",
        choices=["http", "sse", "stdio"],
        default="stdio",
        help="Transport type: http, sse, or stdio (default: stdio)",
    )

    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Host for HTTP/SSE transport (default: 127.0.0.1)",
    )

    parser.add_argument(
        "--port",
        type=int,
        default=8001,
        help="Port for HTTP/SSE transport (default: 8001)",
    )

    return parser.parse_args()


# Initialize the MCP server
mcp = FastMCP("HyperFunnel Destinations MCP Server")

# Initialize tool classes - they auto-register when instantiated
HotelTools(mcp)
DestinationTools(mcp)
RoomTools(mcp)
AvailabilityTools(mcp)
BookingTools(mcp)

if __name__ == "__main__":
    args = parse_arguments()

    print(
        f"🚀 Starting HyperFunnel MCP Server with {args.transport.upper()} transport..."
    )

    if args.transport == "http":
        print(f"🌐 HTTP server starting on {args.host}:{args.port}")
        mcp.run(transport="http", host=args.host, port=args.port)
    elif args.transport == "sse":
        print(f"📡 SSE server starting on {args.host}:{args.port}")
        mcp.run(transport="sse", host=args.host, port=args.port)
    else:  # stdio
        print("📝 Using STDIO transport (default)")
        mcp.run()  # Uses STDIO transport by default
