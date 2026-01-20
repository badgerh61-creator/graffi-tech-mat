from fastapi import APIRouter
from app.compliance.retention_engine import RetentionEngine

router = APIRouter(prefix="/compliance")

@router.get("/report")
def get_compliance_report():
    engine = RetentionEngine()
    return engine.generate_report()

