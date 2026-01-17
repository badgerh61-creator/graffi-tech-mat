# Phase N.1 — Distribution Request Contracts

## Purpose
Define and validate distribution requests for exported artifacts.

---

## Endpoint

POST /distributions/requests

---

## Request Shape

```json
{
  "export_id": "uuid",
  "target": "direct_download | signed_url | external_system",
  "options": {}
}

