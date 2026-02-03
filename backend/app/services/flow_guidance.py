def get_flow_guidance(*, user):
    return {
        "next_allowed_tools": ["finalize_snapshot"],
        "blocked_flows": [],
    }

