# Phase O.0 — Automation Authority & Policy Gates

## Purpose
Define and enforce who may enable automated distribution and integration behavior.

Automation amplifies power and risk.  
All automation MUST be explicitly authorized.

---

## Automation Capabilities

```json
{
  "canEnableAutomation": false,
  "canConfigureIntegrations": false,
  "canViewAutomationLogs": false
}
```

---

## Role Mapping (LOCKED)

| Role   | Enable Automation | Configure Integrations | View Logs |
| ------ | ----------------- | ---------------------- | --------- |
| Viewer | ❌                 | ❌                      | ❌         |
| Editor | ❌                 | ❌                      | ❌         |
| Owner  | ❌                 | ❌                      | ❌         |
| Admin  | ✅                 | ✅                      | ✅         |

📌 **Automation is admin-only by default.**

---

## Project Overrides

* Archived projects disable all automation
* Suspended projects disable all automation
* Automation may be disabled globally via policy

---

## Enforcement Rules

* Automation capabilities are server-derived only
* Automation cannot bypass Phase N contracts
* Automation actions must be auditable
* Manual actions must remain possible

---

## Forbidden

* Automation without explicit enablement
* Automation creating permanent access
* Automation bypassing audit
* Automation modifying export bytes

