def advance_flow_state(snapshot, executed_tool):
    """
    Advance flow only after successful execution.
    """
    snapshot.last_flow_state = executed_tool

