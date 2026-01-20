from datetime import datetime

class ComplianceRecord:
    def __init__(
        self,
        *,
        id,
        record_type,
        created_at,
        legal_hold=False,
    ):
        self.id = id
        self.type = record_type
        self.created_at = created_at
        self.legal_hold = legal_hold

