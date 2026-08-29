# Changelog

This changelog tracks major bridge milestones.

## Universal Core Contract v4 — alpha / additive

### Added

- framework contract version `4.0.0-alpha.1`
- `GetFrameworkCapabilities`
- canonical `GetCharacterId`
- normalized money read/mutation APIs
- normalized job/duty APIs
- normalized metadata/groups APIs
- native framework provider `m4i`, implemented by resource `m4i_core`
- Qbox/QBCore/ESX/Ox Core v4 adapters
- explicit durable idempotent-money capability semantics
- server/client M4I provider recovery paths
- normalized M4I player-surface health checks

### Hardened

Review-driven hardening included fixes for:

- framework object cache invalidation after provider restarts
- M4I readiness/recovery with cached fallbacks
- client/server provider alignment
- ESX bound method invocation
- ESX money reason forwarding
- job grade validation
- metadata capability accuracy
- optional M4I status/stress handling
- exact `m4i_core` resource naming
- incomplete M4I `GetPlayer`-only provider health

### Architecture clarification

- `m4i_bridge` is the compatibility/API boundary.
- when provider `m4i` is selected, the `m4i_core` resource owns the native M4I Data Layer.
- QBCore/Qbox/ESX/Ox Core remain responsible for their own framework data architecture when selected.
- There is no M4I Data Proxy over other frameworks.

## 1.3.1 — Final Stabilization

### Added

- API stability metadata (`GetApiVersion`, `GetApiInfo`)
- explicit deprecation map for legacy surfaces
- profiling-mode summary integration in runtime metrics

### Changed

- standardized structured error flow across kernel/export registration paths
- tightened config/plugin/hook/middleware/service validation
- strengthened callback replay/double-execution protections
- improved owner-aware unregistration safety

## 1.2.0 — Phase 3 (Ecosystem Engine)

### Added

- plugin subsystem
- hook subsystem
- middleware subsystem
- DI container service resolution
- metrics/observability snapshot
- hot-reload cleanup foundation

## 1.1.0 — Phase 2 (Production Expansion)

### Added

- expanded provider coverage
- resolver fallback/health behavior
- callback improvements
- stronger security scoring/anti-injection checks
- structured logging and trace-focused diagnostics

## 1.0.0 — Phase 1 (Foundation)

### Added

- kernel lifecycle orchestration
- modular services
- adapter contract/provider selection
- callback/database/logging/security service baselines
- unified server/client export API

## Notes

- stable legacy bridge API remains available
- Universal Core Contract v4 is additive
- provider capability differences must be explicit
- framework switching remains a controlled migration/deployment operation
