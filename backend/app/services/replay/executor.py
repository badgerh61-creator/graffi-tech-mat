class ReplayExecutor:
    @staticmethod
    def execute(
        *,
        db,
        journal,
        dispatch,
        direction: str,
    ):
        if direction not in ("undo", "redo"):
            raise ValueError("Invalid replay direction")

        adapter = dispatch.adapter
        target = dispatch.target
        value = dispatch.value

        try:
            adapter.execute(
                db=db,
                target=target,
                value=value,
            )
            db.commit()
        except Exception as exc:
            db.rollback()
            raise RuntimeError(
                f"Replay execution failed for journal {journal.id}"
            ) from exc

