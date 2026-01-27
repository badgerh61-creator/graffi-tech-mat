# backend/app/studio/kernel_errors.py

class KernelRejection(Exception):
    """
    Authoritative studio kernel rejection.
    Reason MUST be one of:
    - station
    - tool
    - flow
    - mode
    - capability
    """
    def __init__(self, *, reason: str):
        self.reason = reason
        super().__init__(reason)

