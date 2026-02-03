def get_tool_availability(*, user):
    return {
        "tools": [
            {
                "tool_id": "translate",
                "availability": "blocked",
                "reason": {
                    "code": "MODE_MISMATCH",
                    "message": "Tool not available in current mode",
                },
            },
            {
                "tool_id": "finalize_snapshot",
                "availability": "allowed",
                "reason": None,
            },
        ]
    }

