# Hybrid Browser MCP

A lightweight MCP server that exports [CAMEL](https://github.com/camel-ai/camel) framework's HybridBrowserToolkit as MCP-compatible tools.

## Overview

This project provides an MCP (Model Control Protocol) interface for CAMEL's HybridBrowserToolkit, enabling browser automation capabilities through a standardized protocol. It allows LLM-based applications to control web browsers, navigate pages, interact with elements, and capture screenshots.

Key features:
- Full browser automation capabilities (click, type, navigate, etc.)
- Screenshot capture with visual element identification
- Multi-tab management
- JavaScript execution in browser console
- Async operation support

## Installation

You can install the package directly from source:

```bash
git clone https://github.com/yourusername/hybrid-browser-mcp.git
cd hybrid-browser-mcp
pip install -e .
```

Or using pip:

```bash
pip install hybrid-browser-mcp
```

## Config with MCP clients

### Claude Desktop Configuration

To use this MCP server with Claude Desktop, you need to add it to your Claude Desktop configuration file.

#### Configuration File Location

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

#### Configuration Steps

1. **Open the configuration file** in your text editor:
   ```bash
   # macOS
   nano ~/Library/Application\ Support/Claude/claude_desktop_config.json
   
   # Windows (in PowerShell)
   notepad "$env:APPDATA\Claude\claude_desktop_config.json"
   
   # Linux
   nano ~/.config/Claude/claude_desktop_config.json
   ```

2. **Add the hybrid-browser configuration**:

   If the file is empty or doesn't exist, create it with:
   ```json
   {
     "mcpServers": {
       "hybrid-browser": {
         "command": "uvx",
         "args": [
           "hybrid-browser-mcp"
         ]
       }
     }
   }
   ```

   If the file already exists with other servers, add the hybrid-browser configuration:
   ```json
   {
     "mcpServers": {
       "existing-server": {
         // ... existing configuration
       },
       "hybrid-browser": {
         "command": "uvx",
         "args": [
           "hybrid-browser-mcp"
         ]
       }
     }
   }
   ```

3. **Save the file** and **completely restart Claude Desktop** (quit and reopen)

   <img width="990" height="791" alt="截屏2025-09-05 17 32 11" src="https://github.com/user-attachments/assets/aea1b8f5-59c5-4978-92ee-50f39cba653d" />
   *Example of claude_desktop_config.json with hybrid-browser-mcp configured*

4. **Verify the connection**:
   - Click the 🔌 (plug icon) in Claude's conversation interface
   - You should see "hybrid-browser" listed among available tools
   - The tools will appear with descriptions like:
     - `browser_open` - Opens a new browser session
     - `browser_visit_page` - Navigates to a URL
     - `browser_click` - Clicks on elements
     - etc.

   Then you can ask claude to use browser:
   
   <img width="601" height="533" alt="截屏2025-09-05 17 30 26" src="https://github.com/user-attachments/assets/009ad427-2f62-4e20-ad92-4884bc106fac" />
   
   *Claude Desktop showing available browser automation tools*

#### Alternative: Python Path Configuration

If you prefer using your specific Python environment:

```json
{
  "mcpServers": {
    "hybrid-browser": {
      "command": "/path/to/your/python",
      "args": [
        "-m",
        "hybrid_browser_mcp.server"
      ]
    }
  }
}
```

Replace `/path/to/your/python` with your actual Python interpreter path. You can find it with:
```bash
which python
```

#### Alternative: Local Development Configuration

If you're developing this package locally:

```json
{
  "mcpServers": {
    "hybrid-browser": {
      "command": "python",
      "args": [
        "/absolute/path/to/hybrid_browser_mcp/server.py"
      ]
    }
  }
}
```

### Browser Configuration

The browser behavior is configured through `hybrid_browser_mcp/config.py`. You can modify this file to customize the browser settings:

```python
BROWSER_CONFIG = {
    "headless": False,              # Run browser in headless mode
    "stealth": True,                # Enable stealth mode
    "viewport_limit": False,        # Include all elements in snapshots
    "cache_dir": "tmp/",           # Cache directory for screenshots
    "enabled_tools": [             # List of enabled browser tools
        "browser_open", "browser_close", "browser_visit_page",
        "browser_back", "browser_forward", "browser_get_som_screenshot",
        "browser_click", "browser_type", "browser_select",
        "browser_scroll", "browser_enter", "browser_mouse_control",
        "browser_mouse_drag", "browser_press_key", "browser_switch_tab",
        # Uncomment to enable additional tools:
        # "browser_get_page_snapshot",
        # "browser_close_tab",
        # "browser_console_view",
        # "browser_console_exec",
    ],
}
```

#### Configuration Options

| Option | Description | Default | Type |
|--------|-------------|---------|------|
| `headless` | Run browser in headless mode (no window) | `False` | `bool` |
| `stealth` | Enable stealth mode to avoid detection | `False` | `bool` |
| `viewport_limit` | Only include elements in current viewport in snapshots | `False` | `bool` |
| `cache_dir` | Directory for storing cache files | `"tmp/"` | `str` |
| `enabled_tools` | List of enabled tools | `None`* | `list` or `None` |

*When `enabled_tools` is `None`, these default tools are enabled: `browser_open`, `browser_close`, `browser_visit_page`, `browser_back`, `browser_forward`, `browser_click`, `browser_type`, `browser_switch_tab`

#### Example Configurations

**1. Headless mode for automation**:
```python
USER_BROWSER_CONFIG = {
    "headless": True,
}
```

**2. Stealth mode with visible browser**:
```python
USER_BROWSER_CONFIG = {
    "headless": False,
    "stealth": True,
}
```

**3. Limited tools for safety**:
```python
USER_BROWSER_CONFIG = {
    "enabled_tools": [
        "browser_open",
        "browser_visit_page",
        "browser_get_page_snapshot",
        "browser_close",
    ],
}
```

**4. Enable all available tools**:
```python
USER_BROWSER_CONFIG = {
    "enabled_tools": [
        "browser_open", "browser_close", "browser_visit_page",
        "browser_back", "browser_forward", "browser_get_page_snapshot",
        "browser_get_som_screenshot", "browser_click", "browser_type",
        "browser_select", "browser_scroll", "browser_enter",
        "browser_switch_tab", "browser_close_tab", "browser_get_tab_info",
        "browser_mouse_control", "browser_mouse_drag", "browser_press_key",
        "browser_wait_user", "browser_console_view", "browser_console_exec",
    ],
}
```

## Available Tools

The server exposes the following browser control tools:

### Core Navigation
- `browser_open()`: Opens a new browser session
- `browser_close()`: Closes the browser session
- `browser_visit_page(url)`: Navigates to a specific URL
- `browser_back()`: Goes back in browser history
- `browser_forward()`: Goes forward in browser history

### Page Interaction
- `browser_click(ref)`: Clicks on an element by its reference ID
- `browser_type(ref, text, inputs)`: Types text into input fields
- `browser_select(ref, value)`: Selects an option in a dropdown
- `browser_scroll(direction, amount)`: Scrolls the page
- `browser_enter()`: Presses the Enter key
- `browser_press_key(keys)`: Presses specific keyboard keys

### Page Analysis
- `browser_get_page_snapshot()`: Gets a textual snapshot of interactive elements
- `browser_get_som_screenshot(read_image, instruction)`: Captures a screenshot with element annotations
- `list_browser_functions()`: Lists all available browser functions

### Tab Management
- `browser_switch_tab(tab_id)`: Switches to a different browser tab
- `browser_close_tab(tab_id)`: Closes a specific tab
- `browser_get_tab_info()`: Gets information about all open tabs

### Advanced Features
- `browser_console_view()`: Views console logs
- `browser_console_exec(code)`: Executes JavaScript in the browser console
- `browser_mouse_control(control, x, y)`: Controls mouse actions at coordinates
- `browser_mouse_drag(from_ref, to_ref)`: Drags elements
- `browser_wait_user(timeout_sec)`: Waits for user input

### Example Usage

```python
# Open browser and navigate
await browser_open()
await browser_visit_page("https://www.google.com")

# Get page snapshot to see available elements
snapshot = await browser_get_page_snapshot()
print(snapshot)

# Interact with elements
await browser_type(ref="search-input", text="CAMEL AI framework")
await browser_enter()

# Take a screenshot
await browser_get_som_screenshot()

# Close browser
await browser_close()
```

## Architecture

The server works by:
1. Wrapping CAMEL's HybridBrowserToolkit with async support
2. Exposing toolkit methods as MCP-compatible tools
3. Managing a singleton browser instance per session
4. Handling WebSocket communication for real-time browser control

## Requirements

- Python 3.10+
- Playwright (automatically installed)
- CAMEL AI framework

## Development

To set up a development environment:

```bash
pip install -e ".[dev]"
```

Run tests:

```bash
pytest
```

## Troubleshooting

### Server Not Appearing in Claude Desktop

1. **Check if the package is installed correctly**:
   ```bash
   # Should output the path to the executable
   which hybrid-browser-mcp
   ```

2. **Test the server manually**:
   ```bash
   hybrid-browser-mcp
   # Should start without errors
   # Press Ctrl+C to stop
   ```

3. **Check Claude Desktop logs** for errors:
   ```bash
   # macOS
   tail -f ~/Library/Logs/Claude/mcp*.log
   
   # Windows
   Get-Content "$env:APPDATA\Claude\logs\mcp*.log" -Tail 20 -Wait
   ```

4. **Verify the configuration file**:
   ```bash
   # macOS
   cat ~/Library/Application\ Support/Claude/claude_desktop_config.json
   
   # Windows
   type %APPDATA%\Claude\claude_desktop_config.json
   ```

### Common Issues

#### Issue: "Command not found" error
**Solution**: Use the full Python path in your configuration:
```json
{
  "mcpServers": {
    "hybrid-browser": {
      "command": "/usr/bin/python3",  // or your Python path
      "args": ["-m", "hybrid_browser_mcp.server"]
    }
  }
}
```

#### Issue: Browser doesn't open or shows errors
**Solution**: The HybridBrowserToolkit uses a TypeScript-based browser controller that runs on Node.js. It will automatically download and manage browser binaries. If you encounter issues:
1. Ensure Node.js is installed on your system
2. The TypeScript server will start automatically when needed
3. Browser binaries will be downloaded on first use

### Debug Mode

To see detailed logs, you can run the server with debug output:
```bash
python -m hybrid_browser_mcp.server 2> debug.log
```

Then check `debug.log` for any error messages.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
