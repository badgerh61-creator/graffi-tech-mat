from tests.helpers.audit_helpers import get_audit_events

def test_ai_interaction_audited(
    db,
    assistant_service,
    editor_user,
    snapshot,
):
    assistant_service.handle_request(
        user=editor_user,
        snapshot=snapshot,
        mode="inquiry",
        prompt="Explain symmetry error",
    )

    events = get_audit_events(action="ai.interaction")
    assert len(events) == 1
