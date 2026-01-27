import pytest
from app.studio.kernel_errors import KernelRejection


def test_read_only_blocks_execution(
    kernel,
    db,
    completed_snapshot,
    viewer_user,
):
    """
    Any user on a completed snapshot
    is forced into read-only mode.
    """

    with pytest.raises(KernelRejection) as exc:
        kernel(
            db=db,
            snapshot=completed_snapshot,
            user=viewer_user,
            station="geometry",
            tool="transform",
            operation="translate",
            params={"x": 5},
        )

    assert exc.value.reason == "mode"

