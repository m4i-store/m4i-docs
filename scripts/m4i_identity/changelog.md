# Changelog

## 0.1.0-foundation

- Initial `m4i_identity` foundation created.
- Stage-based `playerConnecting` pipeline added.
- Identity ownership placed in `identity_service`.
- DB-only persistence layer established in `identity_store`.

## 0.2.0-production-hardening

- Structured result contracts standardized.
- Stable reason codes introduced.
- Queue checkpoint contract formalized.
- Runtime state API and read-only exports introduced.
- Reconnect throttle baseline protection added.

## 0.3.0-runtime-hardening

- Guarded deferrals lifecycle with singular completion behavior.
- Stage crash containment mapped to `INTERNAL_ERROR`.
- Watchdog timeout protection added to avoid hanging joins.
- Language card payload validation hardened.
- Throttle key-priority and memory cleanup improved.
- Operational debug snapshot export added.

## 0.3.1-docs-bridge-readonly-pass

- Official script docs integrated into `m4i-docs/scripts/m4i_identity/`.
- Export contracts documented with read-only boundaries.
- Bridge-compatible read-only consumption guidance formalized.
- Resource README aligned to centralized docs-hub workflow.

## 0.3.2-webhook-standard-adoption

- Added dedicated `webhook_service` with key/category-based routing.
- Added `Config.Webhooks` standard categories and script event keys.
- Added safe webhook fallback behavior (`key -> route -> default -> skip`).
- Added non-breaking webhook emission on important identity events:
  - identity created/updated
  - join accepted/rejected
  - language selection/fallback
  - throttle rejections
- Added webhook snapshot visibility in `GetIdentityDebugSnapshot()`.
