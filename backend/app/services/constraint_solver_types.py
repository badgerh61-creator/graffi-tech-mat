class SolveResult:
    def __init__(self, success, solved_parameters=None, error_summary=None):
        self.success = success
        self.solved_parameters = solved_parameters or {}
        self.error_summary = error_summary

