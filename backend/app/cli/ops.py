from __future__ import annotations

import argparse
import os

from app.services.backup_restore import backup_database, restore_database


def main() -> None:
    p = argparse.ArgumentParser(prog="gtm-ops")
    sub = p.add_subparsers(dest="cmd", required=True)

    b = sub.add_parser("backup")
    b.add_argument("--out", required=True, help="Output path for backup file")

    r = sub.add_parser("restore")
    r.add_argument("--src", required=True, help="Backup file path to restore from")
    r.add_argument("--confirm", required=True, help="Must be exactly YES")

    args = p.parse_args()
    db_url = os.getenv("DATABASE_URL") or "sqlite:///graffi.db"

    if args.cmd == "backup":
        res = backup_database(database_url=db_url, out_path=args.out)
        print(f"OK backup {res.backend}: {res.source} -> {res.output}")
        return

    if args.cmd == "restore":
        res = restore_database(database_url=db_url, src_path=args.src, confirm=args.confirm)
        print(f"OK restore {res.backend}: {res.source} -> {res.output}")
        return


if __name__ == "__main__":
    main()

