# Changelog

This changelog tracks major bridge milestones.

## Native M4I Data Layer Contract — additive

### Added

When the selected framework provider is `m4i` and `m4i_core` exposes the shipped Data Layer contract, the bridge provides native-only capabilities for:

- `GetPlayerSnapshot`
- `GetPlayersSnapshot`
- `GetDataLayerState`
- `SubscribeData`
- `UnsubscribeData`
- dynamic capability flags for native Data Layer/snapshots/subscriptions

### Ownership and lifecycle

- bridge captures the invoking gameplay resource as subscription owner
- owner is delegated to `m4i_core` through the trusted native contract
- public unsubscribe is owner-only
- gameplay-resource stop removes its bridge-side records
- Core restart invalidates old native tokens and active gameplay-owned records are rebound after Core/provider readiness
- subscriptions owned by the old `m4i_core` runtime are removed on Core stop and are not inherited by the replacement Core process
- the authoritative `m4i_core:server:ready` signal retriggers bounded recovery even if the initial resource-start retry window expired
- overlapping lifecycle recovery signals are coalesced into bounded work
- read-only capability polling does not start or extend subscription recovery
- failed explicit Core unsubscribe preserves the bridge record/token for retry instead of orphaning a Core callback/quota slot
- finite positive-integer validation is enforced for bulk snapshot limits
- native player source IDs are validated as finite positive integers before provider forwarding

### Architecture boundary

These APIs are **not** emulated for Qbox/QBCore/ESX/Ox Core. Their native Data Layer capability flags remain unsupported/false. There is no M4I Data Proxy, cache, write-behind queue or DB interception layered over another framework.

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
- Universal Core Contract v4 and the native M4I Data Layer contract are additive
- provider capability differences must be explicit
- framework switching remains a controlled migration/deployment operation
