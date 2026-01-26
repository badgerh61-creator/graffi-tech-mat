import pytest
from fastapi import HTTPException

from app.services.queue_stability import enqueue_job

def test_queue_backpressure_rejects_jobs(
    saturated_queue,
):
    with pytest.raises(HTTPException) as exc:
        enqueue_job(queue=saturated_queue)

    assert exc.value.status_code == 503

