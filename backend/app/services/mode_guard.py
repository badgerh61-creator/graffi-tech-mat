from app.studio.kernel_errors import KernelRejection
from app.studio.mode_rules import MODE_ALLOWED_TOOLS

def require_mode_allows_tool(*, mode, tool):
    allowed = MODE_ALLOWED_TOOLS.get(mode, set())

    if tool not in allowed:
        raise KernelRejection(reason="mode")

