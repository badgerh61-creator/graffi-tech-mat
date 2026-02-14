"""
Legacy guard shim.

Authority is fully enforced inside:
    app.studio.kernel_executor

This file exists ONLY for backward compatibility.
"""

def enforce_tool_authority(*args, **kwargs):
    # No-op.
    # Real authority enforcement is inside studio kernel.
    return

