from __future__ import annotations

import argparse
from app.db.session import SessionLocal
from app.services.backup_restore import create_backup, restore_backup


def main():
    parser = argparse.ArgumentParser(prog="gtm-backup")
    sub = parser.add_subparsers(dest="cmd", required=True)

    b = sub.add_parser("backup")
    b.add_argument("--path", required=True)

    r = sub.add_parser("restore")
    r.add_argument("--path", required=True)
    r.add_argument("--allow-non-empty", action="store_true")

    args = parser.parse_args()
    db = SessionLocal()
    try:
        if args.cmd == "backup":
            meta = create_backup(db=db, path=args.path)
            print(meta)
        elif args.cmd == "restore":
            meta = restore_backup(
                db=db,
                path=args.path,
                require_empty=not args.allow_non_empty,
            )
            print(meta)
    finally:
        db.close()


if __name__ == "__main__":
    main()

