import pytest
from types import SimpleNamespace

from app.observability.metrics import MetricsCollector
from app.observability import metrics as global_metrics
from app.observability.tracing import start_span

# Real services (Phase O–P boundary)
from app.services.automation_job_executor import execute_job
from app.services.signed_url_service import create_signed_url
from app.services.geometry_validator import validate_geometry


# ============================================================
# Global observability fixtures (Phase P canonical)
# ============================================================

@pytest.fixture
def metrics_collector(monkeypatch):
    """
    Replaces the global metrics sink with a test collector.
    """
    collector = MetricsCollector()

    monkeypatch.setattr(
        global_metrics,
        "metrics",
        collector,
        raising=False,
    )

    return collector


@pytest.fixture
def trace_context():
    """
    Minimal trace context adapter for Phase P.
    """
    class TraceContext:
        def start_span(self, name):
            return start_span(name)

    return TraceContext()


# ============================================================
# Phase P — Automation job adapter
# ============================================================

@pytest.fixture
def automation_job(export_job):
    """
    Canonical Phase-P automation job input.
    """
    export_job.job_type = "export"
    export_job.policy = {}
    export_job.payload = {}
    export_job.status = "pending"
    export_job.attempt = 0
    export_job.max_attempts = 1
    return export_job


# ============================================================
# Phase P — Distribution adapter
# ============================================================

@pytest.fixture
def distribution_request(signed_url_distribution_request):
    """
    Canonical Phase-P distribution request input.
    """
    return signed_url_distribution_request


# ============================================================
# Phase P — Geometry observability (CORRECT MODEL)
# ============================================================

@pytest.fixture
def geometry_engine():
    """
    Phase P does NOT observe geometry objects.

    This fixture exists ONLY to satisfy test signatures.
    Geometry is validator-owned and ephemeral.
    """
    return None


@pytest.fixture
def invalid_geometry_state():
    """
    Invalid geometry is represented by invalid inputs
    passed directly to validate_geometry().
    """
    return SimpleNamespace(
        surfaces=[],  # deliberately invalid
        panels=[],
    )


# ============================================================
# Phase P — GLOBAL SYMBOL INJECTION (REQUIRED)
# ============================================================

@pytest.fixture(autouse=True)
def inject_phase_p_symbols(request):
    """
    Inject Phase-P services into test module globals.

    Phase-P tests intentionally call these without importing.
    """
    request.module.execute_job = execute_job
    request.module.create_signed_url = create_signed_url
    request.module.validate_geometry = validate_geometry

