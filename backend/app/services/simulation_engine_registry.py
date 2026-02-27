from __future__ import annotations

from typing import Dict

from app.services.engines.pseudo_engine_adapter import PseudoEngine


class SimulationEngineRegistry:
    def __init__(self) -> None:
        self._engines: Dict[str, object] = {}
        self.register(PseudoEngine())

    def register(self, engine: object) -> None:
        version = getattr(engine, "engine_version", None)
        if not version:
            raise ValueError("Engine missing engine_version")
        self._engines[str(version)] = engine

    def get(self, engine_version: str):
        engine = self._engines.get(engine_version)
        if not engine:
            raise ValueError(f"Unknown engine_version '{engine_version}'")
        return engine


engine_registry = SimulationEngineRegistry()
