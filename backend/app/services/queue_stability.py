from fastapi import HTTPException, status

MAX_QUEUE_DEPTH = 1000


def enforce_queue_backpressure(queue):
    if queue.depth >= MAX_QUEUE_DEPTH:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Queue is saturated",
        )


def enqueue_job(*, queue):
    """
    Phase S — Queue entry point (policy-level)

    No job mutation.
    No execution.
    Only backpressure enforcement.
    """
    enforce_queue_backpressure(queue)
    return True

