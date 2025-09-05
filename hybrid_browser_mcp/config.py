"""Configuration for hybrid browser MCP server."""

# Browser configuration
BROWSER_CONFIG = {
    "headless": False,
    "stealth": True,
    "viewport_limit": False,
    "cache_dir": "tmp/",
    "enabled_tools": [
        "browser_open",
        "browser_close",
        "browser_visit_page",
        "browser_back",
        "browser_forward",
        "browser_get_som_screenshot",
        "browser_click",
        "browser_type",
        "browser_select",
        "browser_scroll",
        "browser_enter",
        "browser_mouse_control",
        "browser_mouse_drag",
        "browser_press_key",
        "browser_switch_tab",
        # "browser_get_page_snapshot",
        # "browser_close_tab",
        # "browser_console_view",
        # "browser_console_exec",


    ],
}

