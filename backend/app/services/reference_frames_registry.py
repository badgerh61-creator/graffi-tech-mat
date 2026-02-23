from __future__ import annotations

from typing import Set

KNOWN_FRAMES: Set[str] = {"world_xy", "world_yz", "world_xz"}


def is_known_frame(frame_id: str) -> bool:
    return frame_id in KNOWN_FRAMES
