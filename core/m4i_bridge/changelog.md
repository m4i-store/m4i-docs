# Changelog

This changelog tracks major bridge milestones in semantic version style.

## 1.3.1 - Final Stabilization

### Added

- API stability metadata (`GetApiVersion`, `GetApiInfo`)
- explicit deprecation map for legacy surfaces
- profiling-mode summary integration in runtime metrics

### Changed

- standardized structured error flow across kernel/export registration paths
- tightened validation for config, plugin/hook/middleware, and service resolution input
- strengthened callback replay/double-execution protections
- improved owner-aware unregistration safety for hooks/middleware/plugins

### Fixed

- middleware chain cancellation behavior hardening
- documentation and version consistency updates

## 1.2.0 - Phase 3 (Ecosystem Engine)

### Added

- plugin subsystem with lifecycle management
- hook subsystem with priority and cancellation semantics
- middleware subsystem with scoped chains
- DI container service resolution
- metrics/observability runtime snapshot
- hot-reload safety foundation cleanup flows

## 1.1.0 - Phase 2 (Production Expansion)

### Added

- expanded adapter/provider coverage across framework/inventory/ui/notify/progress/target/dispatch
- smart resolver fallback and health-aware behavior
- callback v2 improvements (timeouts, anti-spam, request tracking)
- stronger security scoring and anti-injection checks
- structured logging and trace-focused diagnostics

## 1.0.0 - Phase 1 (Foundation)

### Added

- kernel lifecycle orchestration
- modular service architecture
- adapter contract model and provider selection
- callback, database, logging, security service baselines
- unified export API for server/client integration

## Notes

- Public API contract: `3.0.0`
- Compatibility targets: `1.x`, `2.x`, `3.x`
- Runtime build label: `1.3.1-phase3-stable`
