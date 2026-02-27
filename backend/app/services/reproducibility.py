# backend/app/services/reproducibility.py
from __future__ import annotations

import hashlib
import json
from typing import Any, Dict, Optional, Set

# Deterministic engines allowlist (extend later)
DETERMINISTIC_ENGINES: Set[str] = {"pseudo-v1"}


def stable_hash(obj: Any) -> str:
    """
    Stable SHA-256 hash of JSON-serializable objects.
    Deterministic because we sort keys + fixed separators.
    """
    raw = json.dumps(obj, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def compute_snapshot_hash(*, snapshot_id: int, snapshot_payload: Dict[str, Any]) -> str:
    """
    Deterministic hash of snapshot inputs that affect simulation.
    Caller supplies snapshot_payload (best-effort, schema-flexible).
    """
    return stable_hash({"snapshot_id": int(snapshot_id), "snapshot_payload": snapshot_payload})


def compute_scenario_hash(*, scenario: Dict[str, Any], engine_version: str) -> str:
    """
    Deterministic hash of scenario + engine version.
    (Template metadata can be layered in later without breaking this contract.)
    """
    return stable_hash({"engine_version": str(engine_version), "scenario": scenario or {}})


def compute_run_fingerprint(
    *,
    snapshot_hash: str,
    scenario_hash: str,
    engine_version: str,
    artifact_id: int,
) -> str:
    """
    Unique reproducibility fingerprint for a concrete run output.
    """
    return stable_hash(
        {
            "snapshot_hash": str(snapshot_hash),
            "scenario_hash": str(scenario_hash),
            "engine_version": str(engine_version),
            "artifact_id": int(artifact_id),
        }
    )


def is_verified_deterministic(
    *,
    engine_version: str,
    snapshot_hash: Optional[str],
    scenario_hash: Optional[str],
) -> bool:
    """
    Verified deterministic iff:
    - engine version is allowlisted deterministic
    - snapshot_hash + scenario_hash are present (non-empty)
    """
    if str(engine_version) not in DETERMINISTIC_ENGINES:
        return False
    if not snapshot_hash or not scenario_hash:
        return False
    return True
