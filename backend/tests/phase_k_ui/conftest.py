import pytest


# ----------------------------
# Fake Geometry Engine
# ----------------------------

class FakeSurface:
    def __init__(self, hash_value):
        self.hash = hash_value


class FakeGeometryEngine:
    def __init__(self):
        self._counter = 0
        self._surface = FakeSurface(hash_value="initial")

    def generate(self, curves=None):
        # Return a snapshot, not a live reference
        return FakeSurface(hash_value=self._surface.hash)

    def apply_command(self, command):
        # Any SET_PARAM regenerates geometry deterministically
        if command["command"] == "SET_PARAM":
            self._counter += 1
            self._surface = FakeSurface(hash_value=f"surface-{self._counter}")

    def current_surface(self):
        return self._surface


# ----------------------------
# Fake UI Dispatcher
# ----------------------------

class FakeUIDispatcher:
    def __init__(self, geometry_engine):
        self._commands = []
        self._engine = geometry_engine
        self._undo_stack = []
        self._redo_stack = []

    def dispatch(self, command):
        self._commands.append(command)
        self._undo_stack.append(command)
        self._redo_stack.clear()
        self._engine.apply_command(command)

    def set_param(self, param, value):
        self.dispatch({
            "command": "SET_PARAM",
            "param": param,
            "value": value,
        })

    def segment_panel(self, surface_id, bounds):
        self.dispatch({
            "command": "SEGMENT_PANEL",
            "surface_id": surface_id,
            "bounds": bounds,
        })

    def last_command(self):
        return self._commands[-1]

    def undo(self):
        if not self._undo_stack:
            return
        cmd = self._undo_stack.pop()
        self._redo_stack.append(cmd)
        # reset geometry
        self._engine._counter -= 1
        self._engine._surface = FakeSurface(
            hash_value=f"surface-{self._engine._counter}"
        )

    def redo(self):
        if not self._redo_stack:
            return
        cmd = self._redo_stack.pop()
        self.dispatch(cmd)

    def get_symmetry_state(self):
        return True

    def get_validation_errors(self):
        return ["error"]  # read-only display

    def can_auto_fix(self):
        return False


# ----------------------------
# Pytest Fixtures
# ----------------------------

@pytest.fixture
def geometry_engine():
    return FakeGeometryEngine()


@pytest.fixture
def ui_dispatcher(geometry_engine):
    return FakeUIDispatcher(geometry_engine)


@pytest.fixture
def invalid_geometry_state():
    return {"invalid": True}


# ----------------------------
# Dummy Curve Set (Phase J/K stand-in)
# ----------------------------

@pytest.fixture
def curve_set():
    """
    Minimal stand-in for Phase J/K curve sets.
    K-UI tests only require identity, not geometry.
    """
    return ["curve-a", "curve-b"]

