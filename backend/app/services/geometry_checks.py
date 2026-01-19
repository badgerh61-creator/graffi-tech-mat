def violates_min_curvature(surface):
    return getattr(surface, "violates_curvature", False)


def is_self_intersecting(surface):
    return getattr(surface, "self_intersecting", False)


def panels_overlap(panel_pair):
    return any(getattr(p, "overlaps", False) for p in panel_pair)


def panels_are_continuous(panel_pair):
    return all(getattr(p, "continuous", True) for p in panel_pair)


def adjacent_panel_pairs(panels):
    if len(panels) < 2:
        return []
    return [(panels[i], panels[i + 1]) for i in range(len(panels) - 1)]

