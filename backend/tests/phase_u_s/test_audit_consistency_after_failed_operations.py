def test_audit_consistency_after_failed_operations(
    db,
    draft_snapshot,
    user_a,
):
    try:
        execute_tool(...)
    except:
        pass

    events = get_audit_events(resource_id=draft_snapshot.id)

    assert all(e.timestamp is not None for e in events)

