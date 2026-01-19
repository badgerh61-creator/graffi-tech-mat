from app.db.session import SessionLocal
from app.worker.automation_worker import run_worker_once

def main():
    db = SessionLocal()
    try:
        run_worker_once(db=db)
    finally:
        db.close()

