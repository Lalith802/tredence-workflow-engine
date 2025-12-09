from typing import Callable, Dict, Any

ToolFunc = Callable[[Dict[str, Any], Dict[str, Any]], Dict[str, Any]]
TOOL_REGISTRY: Dict[str, ToolFunc] = {}


def register_tool(name: str):
    def decorator(func: ToolFunc) -> ToolFunc:
        TOOL_REGISTRY[name] = func
        return func
    return decorator


def get_tool(name: str) -> ToolFunc:
    if name not in TOOL_REGISTRY:
        raise KeyError(
            f"Tool '{name}' not found in registry. Current: {list(TOOL_REGISTRY.keys())}"
        )
    return TOOL_REGISTRY[name]
