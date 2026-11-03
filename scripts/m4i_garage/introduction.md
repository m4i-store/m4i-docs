# m4i_garage

**Current verified development source:** TEST Roleplay VPS `m4i_garage v0.1.122-alpha`, inspected and source-tested on **3 November 2026**.

**Historical source snapshot:** The private `m4i-store/m4i_garage` GitHub repository had a much older `0.1.3` snapshot on 21 October 2026. Do **not** confuse that historical snapshot with the TEST VPS copy. The canonical `m4i-docs` repository documents the verified TEST version here; public documentation updates do not automatically publish or install source.

## What is m4i_garage?

A server-authoritative garage ecosystem with 3D polygon Garage Creator, land/water/air garage categories, public/private/shared storage networks, registered owned vehicles, temporary/shared access, Impound, Police Seized custody, covered vehicle preservation, native damage state persistence and LB Phone integration.

The runtime uses `m4i_bridge` for player identity, jobs, permissions, inventory, UI integration and framework/provider interactions.

## API for other scripts

The TEST source exposes **7 newly implemented Client exports and 8 new Server exports**, plus legacy read/ownership/repair exports retained for compatibility. These give developers safe garage/zone inspection, live and saved condition reads, signed vehicle lookup, access checks, server-only dealership registration and verified repair integration.

- [Client and Server Exports](exports.md) — signatures, parameters, return values, error cases, Lua integration examples
- [Integration](integration.md) — bridge boundary and secure resource-to-resource interaction
- [Five Frameworks and Bridge Providers](framework-compatibility.md)
- [Installation](installation.md) — dependencies, load order, FXServer and Asset Escrow
- [Configuration](configuration.md) — editable configuration and allowlist policy
- [Troubleshooting](troubleshooting.md) — common errors and test strategy
- [Changelog](changelog.md) — versioned source-backed changes

## Manifest and escrow

`fxmanifest.lua` is reformatted with one entry per line in all script/dependency/asset lists. `escrow_ignore` intentionally includes editable configuration, JSON, SQL install definitions, docs and the new dedicated integration API modules, **not** the core security/payment/vehicle-custody source.

## Quality and release status

The TEST VPS passed automated source-level Lua and JavaScript regression tests. Those checks exercise API contracts, schema-safe lookups and manifest packaging, but **are not a live multi-player GTA or FiveM Asset Escrow distribution test**. Full real-client verification must precede production release claims, especially for add-on vehicle deformation and detached debris.

This is a versioned development document. The installation currently running on any given server may be different until that server explicitly restarts/loads the updated resource.
