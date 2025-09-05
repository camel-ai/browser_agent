import pytest
import asyncio
from hybrid_browser_mcp.router import list_browser_functions


class TestHybridBrowserRouter:
    @pytest.mark.asyncio
    async def test_list_browser_functions(self):
        result = await list_browser_functions()
        
        assert result["status"] == "success"
        assert result["toolkit"] == "HybridBrowserToolkit"
        assert "functions" in result
        
        functions = result["functions"]
        
        expected_functions = [
            "browser_open",
            "browser_close",
            "browser_visit_page",
            "browser_back",
            "browser_forward",
            "browser_get_page_snapshot",
            "browser_get_som_screenshot",
            "browser_click",
            "browser_type",
            "browser_select",
            "browser_scroll",
            "browser_enter",
            "browser_switch_tab",
            "browser_close_tab",
            "browser_get_tab_info",
        ]
        
        for func_name in expected_functions:
            assert func_name in functions
            assert "description" in functions[func_name]
            assert "parameters" in functions[func_name]