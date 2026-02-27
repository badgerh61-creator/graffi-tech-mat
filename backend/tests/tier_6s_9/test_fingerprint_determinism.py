from app.services.reproducibility import compute_run_fingerprint

def test_fingerprint_is_deterministic():
    fp1 = compute_run_fingerprint(snapshot_hash="s", scenario_hash="c", engine_version="pseudo-v1", artifact_id=10)
    fp2 = compute_run_fingerprint(snapshot_hash="s", scenario_hash="c", engine_version="pseudo-v1", artifact_id=10)
    assert fp1 == fp2
