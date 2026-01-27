# app/studio/__init__.py

def execute_tool(*args, **kwargs):
    # Lazy import to avoid circular dependency
    from app.studio.kernel_executor import execute_tool as _execute_tool
    return _execute_tool(*args, **kwargs)

