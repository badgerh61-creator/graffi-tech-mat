from app.services.replay.journal_resolver import JournalResolver
from app.services.replay.dispatcher import AdapterDispatcher
from app.services.replay.executor import ReplayExecutor
from app.services.replay.safety import SafetyGate


class ReplayController:
    @staticmethod
    def replay(*, db, model_id: int, cursor_id: int, direction: str):
        """
        Orchestrates undo / redo.
        No logic yet.
        """
        raise NotImplementedError

