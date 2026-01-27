import pytest
from app.studio.kernel_errors import KernelRejection


def test_review_mode_blocks_transform(
    kernel,
    db,
    draft_snapshot,
    viewer_user,
):
    """
    Viewer in review mode on a draft snapshot
    must not be allowed to transform.
    """

    with pytest.raises(KernelRejection) as exc:
        kernel(
            db=db,
            snapshot=draft_snapshot,
            user=viewer_user,
            station="geometry",
            tool="transform",
            operation="translate",
            params={"x": 5},
        )

    assert exc.value.reason == "capability"


