from app.kernel import acquire_draft_lock, release_draft_lock, handoff_draft_ownership
from app.services.presence_sessions import start_session

def test_authority_violation_audited(
    db,
    draft_snapshot,
    editor_user,
    non_owner_user,
):
    # Lock snapshot as editor_user
    acquire_draft_lock(db=db, snapshot=draft_snapshot, user=editor_user)

    # Now violate authority
    try:
        require_draft_authority(
            db=db,
            user=non_owner_user,
            snapshot=draft_snapshot,
        )
    except:
        pass

    events = get_audit_events(action="authority.violation")
    assert len(events) == 1

