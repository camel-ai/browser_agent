import asyncio
import inspect
from typing import Dict, Optional, Any, List

from mcp.server.fastmcp import FastMCP
from camel.toolkits.hybrid_browser_toolkit.hybrid_browser_toolkit_ts import HybridBrowserToolkit

mcp = FastMCP("Hybrid Browser Router")

_toolkit_instance: Optional[HybridBrowserToolkit] = None
_toolkit_lock = asyncio.Lock()


async def get_toolkit(**kwargs) -> HybridBrowserToolkit:
    global _toolkit_instance
    
    async with _toolkit_lock:
        if _toolkit_instance is None:
            # Load configuration from config file
            from .config import BROWSER_CONFIG
            
            # Create toolkit kwargs from config
            toolkit_kwargs = {}
            
            # Apply all config values that are not None
            for key, value in BROWSER_CONFIG.items():
                if value is not None:
                    toolkit_kwargs[key] = value
            
            # Override with any passed kwargs
            toolkit_kwargs.update(kwargs)
            _toolkit_instance = HybridBrowserToolkit(**toolkit_kwargs)
        return _toolkit_instance


async def close_toolkit():
    global _toolkit_instance
    
    async with _toolkit_lock:
        if _toolkit_instance is not None:
            await _toolkit_instance.browser_close()
            _toolkit_instance = None


@mcp.tool()
@mcp.resource("tools://all")
async def list_browser_functions():
    toolkit = await get_toolkit()
    functions = {}
    
    enabled_methods = toolkit.enabled_tools if hasattr(toolkit, 'enabled_tools') else []
    
    for method_name in enabled_methods:
        if hasattr(toolkit, method_name):
            method = getattr(toolkit, method_name)
            doc = method.__doc__ or "No description available"
            
            params = {}
            try:
                signature = inspect.signature(method)
                for param_name, param in signature.parameters.items():
                    if param_name == "self":
                        continue
                    params[param_name] = {
                        "required": param.default == param.empty,
                        "default": None if param.default == param.empty else param.default,
                        "type": str(param.annotation) if param.annotation != param.empty else "unknown"
                    }
            except Exception:
                pass
            
            functions[method_name] = {
                "description": doc.strip(),
                "parameters": params
            }
    
    return {
        "status": "success",
        "toolkit": "HybridBrowserToolkit",
        "functions": functions
    }


@mcp.tool()
async def browser_open():
    toolkit = await get_toolkit()
    return await toolkit.browser_open()


@mcp.tool()
async def browser_close():
    toolkit = await get_toolkit()
    result = await toolkit.browser_close()
    await close_toolkit()
    return result


@mcp.tool()
async def browser_visit_page(url: str):
    toolkit = await get_toolkit()
    return await toolkit.browser_visit_page(url)


@mcp.tool()
async def browser_back():
    toolkit = await get_toolkit()
    return await toolkit.browser_back()


@mcp.tool()
async def browser_forward():
    toolkit = await get_toolkit()
    return await toolkit.browser_forward()


@mcp.tool()
async def browser_get_page_snapshot():
    toolkit = await get_toolkit()
    return await toolkit.browser_get_page_snapshot()


@mcp.tool()
async def browser_get_som_screenshot(
    read_image: bool = True,
    instruction: Optional[str] = None
):
    toolkit = await get_toolkit()
    return await toolkit.browser_get_som_screenshot(
        read_image=read_image,
        instruction=instruction
    )


@mcp.tool()
async def browser_click(ref: str):
    toolkit = await get_toolkit()
    return await toolkit.browser_click(ref=ref)


@mcp.tool()
async def browser_type(
    ref: Optional[str] = None,
    text: Optional[str] = None,
    inputs: Optional[List[Dict[str, str]]] = None
):
    toolkit = await get_toolkit()
    return await toolkit.browser_type(ref=ref, text=text, inputs=inputs)


@mcp.tool()
async def browser_select(ref: str, value: str):
    toolkit = await get_toolkit()
    return await toolkit.browser_select(ref=ref, value=value)


@mcp.tool()
async def browser_scroll(direction: str, amount: int = 500):
    toolkit = await get_toolkit()
    return await toolkit.browser_scroll(direction=direction, amount=amount)


@mcp.tool()
async def browser_enter():
    toolkit = await get_toolkit()
    return await toolkit.browser_enter()


@mcp.tool()
async def browser_mouse_control(control: str, x: float, y: float):
    toolkit = await get_toolkit()
    return await toolkit.browser_mouse_control(control=control, x=x, y=y)


@mcp.tool()
async def browser_mouse_drag(from_ref: str, to_ref: str):
    toolkit = await get_toolkit()
    return await toolkit.browser_mouse_drag(from_ref=from_ref, to_ref=to_ref)


@mcp.tool()
async def browser_press_key(keys: List[str]):
    toolkit = await get_toolkit()
    return await toolkit.browser_press_key(keys=keys)


@mcp.tool()
async def browser_wait_user(timeout_sec: Optional[float] = None):
    toolkit = await get_toolkit()
    return await toolkit.browser_wait_user(timeout_sec=timeout_sec)


@mcp.tool()
async def browser_switch_tab(tab_id: str):
    toolkit = await get_toolkit()
    return await toolkit.browser_switch_tab(tab_id=tab_id)


@mcp.tool()
async def browser_close_tab(tab_id: str):
    toolkit = await get_toolkit()
    return await toolkit.browser_close_tab(tab_id=tab_id)


@mcp.tool()
async def browser_get_tab_info():
    toolkit = await get_toolkit()
    return await toolkit.browser_get_tab_info()


@mcp.tool()
async def browser_console_view():
    toolkit = await get_toolkit()
    return await toolkit.browser_console_view()


@mcp.tool()
async def browser_console_exec(code: str):
    toolkit = await get_toolkit()
    return await toolkit.browser_console_exec(code)