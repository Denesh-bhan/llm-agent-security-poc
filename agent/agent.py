from .tools import run_tool

TOOL_NAMES = ["read_file", "draft_email", "http_get", "calculator"]

def handle_tool_request(tool_name: str, arguments: dict, hardened: bool = True,
                        user_authorized: bool = False):
    if tool_name not in TOOL_NAMES:
        return {"status": "blocked", "reason": "Tool is not registered."}
    if hardened and tool_name in {"draft_email", "http_get"} and not user_authorized:
        return {"status": "blocked", "reason": "Explicit user authorization is required."}
    return run_tool(tool_name, arguments, hardened=hardened)
