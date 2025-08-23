# HyperFunnel MCP Server

A Model Context Protocol (MCP) server for the HyperFunnel travel booking API. This server provides tools for hotel searches, room availability checks, booking management, and destination queries through the MCP protocol.

## Overview

HyperFunnel MCP Server acts as a bridge between MCP clients (like Claude Desktop) and the HyperFunnel travel booking API. It provides a comprehensive set of tools for:

- **Hotel Management**: Search hotels by location, get detailed hotel information
- **Room Operations**: Retrieve room details and availability for specific hotels
- **Availability Search**: Find available rooms based on dates, guests, and requirements
- **Booking Management**: Get price quotes and create new bookings
- **Destination Discovery**: Explore available travel destinations

## Features

### Hotel Tools
- `search_hotels`: Search for hotels by country or city
- `get_hotel_by_id`: Get detailed information for a specific hotel
- `get_hotel_details_with_rooms`: Get complete hotel details including all room information

### Room Tools
- `get_rooms_by_hotel_id`: Retrieve all rooms for a specific hotel

### Availability Tools
- `search_availability`: Find available rooms for specific dates and requirements
- `get_room_calendar`: Get day-by-day availability calendar for a room

### Booking Tools
- `get_booking_quote`: Calculate pricing for potential bookings
- `create_booking`: Create new room reservations

### Destination Tools
- `get_available_destinations`: List all available travel destinations

## Prerequisites

- Python 3.11 or higher
- [uv](https://docs.astral.sh/uv/) package manager (recommended)
- Access to a running HyperFunnel API server (default: `http://127.0.0.1:8000`)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd hyperfunnel-mcp
```

2. Install dependencies using uv:
```bash
uv sync
```

## Configuration

The server uses environment variables for configuration. Create a `.env` file in the project root:

```env
# HyperFunnel API Configuration
HYPERFUNNEL_API_BASE_URL=http://127.0.0.1:8000
```

### Configuration Options

- `HYPERFUNNEL_API_BASE_URL`: Base URL for the HyperFunnel API (default: `http://127.0.0.1:8000`)

## Usage

### Running the Server

The MCP server supports multiple transport types and can be run with either `uv` or `python`.

#### Using uv (Recommended)

**STDIO Transport (Default - for MCP clients):**
```bash
uv run my_server.py
# or explicitly:
uv run my_server.py --transport stdio
```

**HTTP Transport:**
```bash
uv run my_server.py --transport http
# or short form:
uv run my_server.py -t http
```

**SSE Transport:**
```bash
uv run my_server.py --transport sse
# or short form:
uv run my_server.py -t sse
```

**Custom host/port:**
```bash
uv run my_server.py --transport http --host 0.0.0.0 --port 8080
```

#### Using Python Directly

**STDIO Transport (Default - for MCP clients):**
```bash
python my_server.py
# or explicitly:
python my_server.py --transport stdio
```

**HTTP Transport:**
```bash
python my_server.py --transport http
# or short form:
python my_server.py -t http
```

**SSE Transport:**
```bash
python my_server.py --transport sse
# or short form:
python my_server.py -t sse
```

**Custom host/port:**
```bash
python my_server.py --transport http --host 0.0.0.0 --port 8080
```

#### Transport Types Explained

- **STDIO**: Standard input/output transport (default) - best for MCP client integration
- **HTTP**: HTTP server transport - useful for testing and development
- **SSE**: Server-Sent Events transport - alternative to HTTP for real-time communication

#### Help and Options

View all available options:
```bash
# With uv
uv run my_server.py --help

# With python
python my_server.py --help
```

### Integration with Claude Desktop

To use this server with Claude Desktop, add the following configuration to your Claude Desktop config file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%/Claude/claude_desktop_config.json`

#### Using uv (Recommended):
```json
{
  "mcpServers": {
    "hyperfunnel": {
      "command": "uv",
      "args": ["run", "my_server.py"],
      "cwd": "/path/to/hyperfunnel-mcp"
    }
  }
}
```

#### Using Python directly:
```json
{
  "mcpServers": {
    "hyperfunnel": {
      "command": "python",
      "args": ["my_server.py"],
      "cwd": "/path/to/hyperfunnel-mcp"
    }
  }
}
```

Replace `/path/to/hyperfunnel-mcp` with the actual path to your project directory.

## API Dependencies

This MCP server requires a running HyperFunnel API service. The API should provide the following endpoints:

- `GET /hotels` - Search hotels
- `GET /hotels/{id}` - Get hotel details
- `GET /hotels/{id}/with-rooms` - Get hotel with rooms
- `GET /rooms/by-hotel/{hotel_id}` - Get rooms by hotel
- `GET /destinations` - Get available destinations
- `POST /availability/search` - Search room availability
- `GET /availability/room/{room_id}/calendar` - Get room calendar
- `POST /bookings/quote` - Get booking quote
- `POST /bookings` - Create booking

## Project Structure

```
hyperfunnel-mcp/
├── config.py              # Configuration management
├── main.py                # Simple main entry point
├── my_server.py           # MCP server implementation with transport selection
├── pyproject.toml         # Project dependencies and metadata
├── tools/                 # MCP tool implementations
│   ├── __init__.py
│   ├── availability.py    # Room availability tools
│   ├── bookings.py        # Booking management tools
│   ├── destinations.py    # Destination discovery tools
│   ├── hotels.py          # Hotel search and details tools
│   └── rooms.py           # Room information tools
└── uv.lock               # Dependency lock file
```

## Development

### Architecture

The server uses a class-based approach with dependency injection:

1. **FastMCP**: Core MCP server framework
2. **Tool Classes**: Each domain (hotels, rooms, bookings, etc.) has its own tool class
3. **Auto-registration**: Tools are automatically registered when classes are instantiated
4. **HTTP Client**: Uses `httpx` for async HTTP communication with the API
5. **Transport Selection**: Command-line argument parsing for flexible transport configuration

### Adding New Tools

To add new tools:

1. Create a new tool class in the `tools/` directory
2. Implement the `__init__` method with MCP instance injection
3. Add a `_register_tools` method to register tool methods
4. Import and instantiate the class in `my_server.py`

Example:

```python
class NewTools:
    def __init__(self, mcp: FastMCP):
        self.mcp = mcp
        self.base_url = get_api_base_url()
        self._register_tools()

    def _register_tools(self):
        self.mcp.tool()(self.my_new_tool)

    async def my_new_tool(self, param: str) -> dict:
        """Tool description here."""
        # Implementation
        pass
```

### Error Handling

All tools include comprehensive error handling:

- **Connection Errors**: Graceful handling when the API is unavailable
- **Response Parsing**: Fallback to text if JSON parsing fails
- **Exception Handling**: Catches and reports unexpected errors
- **Structured Responses**: Consistent response format across all tools

## Dependencies

- **fastmcp**: MCP server framework (>=2.11.3)
- **httpx**: Async HTTP client (>=0.27.0)
- **python-dotenv**: Environment variable management (>=1.0.0)

## Troubleshooting

### Common Issues

**Port already in use:**
```bash
# Use a different port
uv run my_server.py --transport http --port 8002
```

**Permission denied:**
```bash
# Make sure you have execute permissions
chmod +x my_server.py
```

**Transport not supported:**
- Ensure you're using the correct transport type for your use case
- STDIO is recommended for MCP client integration
- HTTP/SSE are useful for development and testing

### Getting Help

Run the help command to see all available options:
```bash
uv run my_server.py --help
```
