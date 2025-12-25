# PHASE_11_2_FROZEN.md

## Phase 11.2 — Exports (Download Real Assets)

**Status:** 🧊 FROZEN  
**Date:** 2025-12-25  
**Branch:** phase-10-upload-hardening  

---

## 🎯 Scope

Phase 11.2 introduces **export functionality** allowing authenticated users to **download real processed assets** using secure, time-limited URLs.

This phase completes the **end-to-end asset lifecycle**:

> Upload → Process → Preview → Export

---

## ✅ Implemented Features

### Backend

- Signed export endpoints (no direct storage access)
- Export guarded by authentication + permissions
- Export only allowed when asset status is `ready`
- Uses MinIO presigned URLs
- Audit logging for all export actions
- No database schema changes
- No breaking API changes

**Endpoints**
- `GET /models/{model_id}/exports/`
- `GET /models/{model_id}/exports/{type}`

---

### Frontend

- Export panel added to Studio UI
- “Download GLB” button:
  - Disabled when model is not selected
  - Disabled when model is not ready
  - Disabled for read-only users
- Download handled via signed URL in new browser tab
- Zero UI regressions

---

## 🔐 Security & Permissions

- Viewer or higher required
- Read-only users cannot export
- URLs are time-limited
- All downloads are auditable

---

## 🧊 Stability Guarantees

- No migrations
- No changes to asset state machine
- No changes to upload pipeline
- Additive functionality only
- Backwards compatible with Phase 11.1

---

## 🧠 Notes

This phase finalizes the **minimum viable professional studio**:
- Assets are real
- Processing is real
- Downloads are real
- Access control is enforced

System is now suitable for:
- Internal teams
- Client demos
- Early production use

---

## 🚫 Out of Scope

- Export format conversion (e.g. optimized GLB)
- Bulk exports
- Export history UI
- Public share links

---

## 🔒 Frozen

No further changes permitted to Phase 11.2 except:
- Security fixes
- Critical bug fixes

All new work must target **Phase 12+**.


