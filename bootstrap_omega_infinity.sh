#!/usr/bin/env bash
set -euo pipefail
ROOT="$(pwd)"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
echo "Bootstrapping Omega-INFINITY project at: $ROOT"
echo

# 1. Create directory layout
dirs=(
  backend app backend/app backend/app/api backend/app/db backend/app/services
  frontend
  .graffi_helper_model/patches
  scripts
  agents tools ml sandbox analytics services config runtime documentation
)
for d in "${dirs[@]}"; do mkdir -p "$d"; done

# 2. Create a minimal Python backend (FastAPI + SQLite example)
cat > backend/pyproject.toml <<'PYPROJECT'
[tool.poetry]
name = "graffi-backend"
version = "0.1.0"
description = "Graffi-Tech-Mat Omega-INFINITY backend (minimal)"
authors = ["graffi"]

[tool.poetry.dependencies]
python = "^3.10"
fastapi = "^0.99.0"
uvicorn = {extras=["standard"],version="0.22.0"}
sqlalchemy = "^2.0"
alembic = "^1.11"
pydantic = "^2.3"
python-multipart = "^0.0.6"
boto3 = "^1.30.0"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
PYPROJECT

cat > backend/requirements.txt <<'REQ'
fastapi
uvicorn[standard]
sqlalchemy
alembic
pydantic
boto3
python-multipart
reqs
REQ

# Minimal FastAPI app
cat > backend/app/main.py <<'PYMAIN'
from fastapi import FastAPI, UploadFile, File
from .db import engine, Base, get_db, SessionLocal
from . import crud, schemas

app = FastAPI(title="Graffi Omega-INFINITY API (minimal)")

# create tables on startup (dev convenience)
@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"ok": True, "service": "graffi-backend"}

@app.post("/upload")
def upload(file: UploadFile = File(...)):
    content = file.file.read()
    # store logic stub
    return {"filename": file.filename, "size": len(content)}
PYMAIN

# SQLAlchemy models (small)
cat > backend/app/db.py <<'DB'
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///./graffi.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

# example model used for testing
from sqlalchemy import Column, Integer, String, Text

class Asset(Base):
    __tablename__ = "assets"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256), nullable=False)
    path = Column(String(1024))
DB

# CRUD placeholder
cat > backend/app/crud.py <<'CRUD'
from .db import SessionLocal, Asset

def create_asset(name, path):
    db = SessionLocal()
    a = Asset(name=name, path=path)
    db.add(a)
    db.commit()
    db.refresh(a)
    db.close()
    return a
CRUD

# services (S3 stub)
cat > backend/app/services/s3client.py <<'S3'
# Minimal S3 interface stub (use boto3 in production)
def upload_bytes(bucket, key, data):
    # Replace with boto3.client('s3').put_object(...)
    with open(f"/tmp/{key}", "wb") as f:
        f.write(data)
    return True
S3

# 3. Create a minimal frontend (Vite + React)
cat > frontend/package.json <<'PKG'
{
  "name": "graffi-frontend",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  },
  "devDependencies": {
    "vite": "^5.0.0"
  }
}
PKG

mkdir -p frontend/src
cat > frontend/index.html <<'HTML'
<!doctype html>
<html>
  <head>
    <meta charset="utf-8" />
    <title>Graffi Frontend (minimal)</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
HTML

cat > frontend/src/main.jsx <<'REACT'
import React from "react";
import { createRoot } from "react-dom/client";

function App(){
  return React.createElement("div", null, [
    React.createElement("h1", {key:1}, "Graffi Frontend (Omega-INFINITY minimal)"),
    React.createElement("p", {key:2}, "This is a starting skeleton.")
  ]);
}

createRoot(document.getElementById("root")).render(React.createElement(App));
REACT

# 4. Patch helper & patch storage (already created)
cat > .graffi_helper_model/README.txt <<'PATCHREADME'
Patch storage for Omega-INFINITY.
Place / keep patches in .graffi_helper_model/patches
Use scripts/patch-utilities to repair, validate, import and apply patches.
PATCHREADME

# 5. Install the key scripts into scripts/patch-utilities (repair, generate, import, validate, apply, preview, safe worktree)
mkdir -p scripts/patch-utilities

# repair_patch.sh (robust)
cat > scripts/patch-utilities/repair_patch.sh <<'REPAIR'
#!/usr/bin/env bash
set -euo pipefail
PATCH_DIR="${1:-.graffi_helper_model/patches}"
if [ ! -d "$PATCH_DIR" ]; then echo "No patch dir: $PATCH_DIR"; exit 2; fi
echo "Repairing patches in: $PATCH_DIR"
for f in "$PATCH_DIR"/*; do
  [ -f "$f" ] || continue
  echo "Repairing $(basename "$f")"
  # remove CRLF, control chars, ensure trailing newline
  perl -0777 -pe 's/\r\n?/\n/g; s/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]//g' "$f" > "$f.tmp" && mv "$f.tmp" "$f"
  # ensure last newline
  tail -c1 "$f" | od -An -t u1 | tr -d ' ' | grep -q '^10$' || echo >> "$f"
done
echo "Repair complete."
REPAIR
chmod +x scripts/patch-utilities/repair_patch.sh

# generate_patch_series.sh
cat > scripts/patch-utilities/generate_patch_series.sh <<'GEN'
#!/usr/bin/env bash
set -euo pipefail
OUT="${1:-.graffi_helper_model/patches}"
mkdir -p "$OUT"
i=1
for c in $(git rev-list --reverse HEAD); do
  parent=$(git rev-list --parents -n1 "$c" | awk '{print $2}')
  [ -z "$parent" ] && continue
  msg=$(git log -1 --pretty=format:%s "$c" | tr ' ' '-' | tr -cd '[:alnum:]-_')
  name=$(printf "%04d_%s.patch" "$i" "$msg")
  git diff "$parent" "$c" > "$OUT/$name"
  if [ ! -s "$OUT/$name" ]; then rm -f "$OUT/$name"; else echo "$name"; fi
  i=$((i+1))
done
echo "Generated patch series in $OUT"
GEN
chmod +x scripts/patch-utilities/generate_patch_series.sh

# validate_patches.sh
cat > scripts/patch-utilities/validate_patches.sh <<'VAL'
#!/usr/bin/env bash
set -euo pipefail
PATCH_DIR="${1:-.graffi_helper_model/patches}"
for p in "$PATCH_DIR"/*.patch; do
  [ -f "$p" ] || continue
  echo "Checking $(basename "$p")"
  if git apply --check "$p" 2>/tmp/patch_check.err; then
    echo " OK"
  else
    echo " FAIL"
    sed -n '1,80p' /tmp/patch_check.err
  fi
done
VAL
chmod +x scripts/patch-utilities/validate_patches.sh

# import_patches_as_commits.sh
cat > scripts/patch-utilities/import_patches_as_commits.sh <<'IMP'
#!/usr/bin/env bash
set -euo pipefail
PATCH_DIR="${1:-.graffi_helper_model/patches}"
BRANCH="patch-import/$(date +%Y%m%d_%H%M%S)"
echo "Creating branch: $BRANCH"
git checkout -b "$BRANCH"
for p in $(ls "$PATCH_DIR"/*.patch | sort); do
  [ -f "$p" ] || continue
  echo "Applying $p"
  if git apply --index "$p"; then
    git commit -m "Import patch: $(basename "$p")"
  else
    echo "Failed to apply $p — aborting import"
    git reset --hard HEAD
    git checkout -
    exit 1
  fi
done
echo "Imported patches as commits onto $BRANCH"
IMP
chmod +x scripts/patch-utilities/import_patches_as_commits.sh

# apply_patch_series.sh
cat > scripts/patch-utilities/apply_patch_series.sh <<'APPLY'
#!/usr/bin/env bash
set -euo pipefail
PATCH_DIR="${1:-.graffi_helper_model/patches}"
for p in $(ls "$PATCH_DIR"/*.patch | sort); do
  echo "Applying $p"
  if git apply "$p"; then
    git add -A
    git commit -m "Apply patch: $(basename "$p")"
  else
    echo "Failed to apply $p"; exit 1
  fi
done
APPLY
chmod +x scripts/patch-utilities/apply_patch_series.sh

# preview_autorebuild.sh (dry-run)
cat > scripts/patch-utilities/preview_autorebuild.sh <<'PREV'
#!/usr/bin/env bash
set -euo pipefail
TMP=$(mktemp -d)
echo "Generating patches to $TMP"
./scripts/patch-utilities/generate_patch_series.sh "$TMP"
for p in "$TMP"/*.patch; do
  echo "Checking $(basename "$p")"
  git apply --check "$p" || echo "Would fail: $(basename "$p")"
done
echo "Preview done. Temp: $TMP"
PREV
chmod +x scripts/patch-utilities/preview_autorebuild.sh

# safe_autorebuild_worktree.sh
cat > scripts/patch-utilities/safe_autorebuild_worktree.sh <<'SAFE'
#!/usr/bin/env bash
set -euo pipefail
TMPROOT=$(mktemp -d)
PATCH_DIR="$TMPROOT/patches"
mkdir -p "$PATCH_DIR"
./scripts/patch-utilities/generate_patch_series.sh "$PATCH_DIR"
WT="$TMPROOT/wt"
git worktree add --detach "$WT" HEAD
pushd "$WT" >/dev/null
for p in "$PATCH_DIR"/*.patch; do
  echo "Checking $(basename "$p")"
  if git apply --check "$p"; then
    git apply "$p"
  else
    echo "Patch fails: $(basename "$p")"
    popd >/dev/null
    echo "Worktree left at $WT for inspection"
    exit 2
  fi
done
echo "All patches applied in worktree (not committed). Running tests (if any)."
popd >/dev/null
SAFE
chmod +x scripts/patch-utilities/safe_autorebuild_worktree.sh

# 6. Add a README
cat > README.md <<'README'
# Graffi-Tech-Mat — Omega-INFINITY (bootstrap)
This repository is a bootstrapped Omega-INFINITY skeleton for Graffi-Tech-Mat.
Folders:
- backend: FastAPI app (minimal)
- frontend: Vite + React minimal app
- .graffi_helper_model/patches: patch storage
- scripts/patch-utilities: repair/validate/import/apply/preview scripts

Suggested workflow:
1. edit code in backend/ and frontend/
2. commit real functional changes (each logical change -> commit)
3. generate patches: ./scripts/patch-utilities/generate_patch_series.sh
4. repair, validate, import or apply with the utilities.

To run backend (dev):
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install fastapi uvicorn sqlalchemy pydantic boto3
uvicorn app.main:app --reload --port 8000

To run frontend (dev):
cd frontend
npm install
npm run dev
README

# 7. Initialize git if needed and create an initial commit
if [ ! -d .git ]; then
  git init
  git add -A
  git commit -m "Bootstrap: Omega-INFINITY skeleton (backend + frontend + patch helpers)"
  echo "Initialized git repo and made initial commit."
else
  echo "Git repo exists. Staging new files and committing them as 'bootstrap'."
  git add -A
  git commit -m "Bootstrap: Omega-INFINITY skeleton (backend + frontend + patch helpers)" || true
fi

echo
echo "Bootstrap complete."
echo " - Backend: backend/app/main.py"
echo " - Frontend: frontend/src/main.jsx"
echo " - Patch helpers: scripts/patch-utilities/"
echo
echo "Next: cd backend && python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt"
