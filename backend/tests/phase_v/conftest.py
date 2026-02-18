import pytest

from app.models.assistant_proposal import AssistantProposal


@pytest.fixture
def project_id():
    return 1


@pytest.fixture
def assistant_proposal_factory(db):
    """
    Local factory because the repo doesn't provide `assistant_proposal_factory`
    as a built-in fixture.
    """
    def _make(
        *,
        snapshot_id: int,
        station: str,
        tool: str,
        payload: dict,
        created_by_user_id: int,
    ):
        p = AssistantProposal(
            snapshot_id=int(snapshot_id),
            station=str(station),
            tool=str(tool),
            payload=payload or {},
            created_by_user_id=int(created_by_user_id),
        )
        db.add(p)
        db.commit()
        db.refresh(p)
        return p

    return _make

