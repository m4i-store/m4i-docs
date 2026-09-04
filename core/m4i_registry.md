# m4i_registry

## Purpose

`m4i_registry` is the canonical live-definition service for the M4I ecosystem. It owns definition/catalog data; it does **not** own player inventory quantities, vehicle ownership, money, or character sessions.

Current release line: `0.2.0-alpha.1`.

## Canonical domains

The shipped registry supports:

- `item`
- `job`
- `gang`
- `group`
- `vehicle`
- `weapon`
- `location`

Definitions use one canonical database source of truth and a validated RAM snapshot for hot runtime reads.

```text
Admin/import
    |
    v
m4i_registry
    |
    +--> MariaDB/MySQL = canonical persisted definitions + history
    |
    +--> RAM registry = live read path
    |
    +--> change events / generation
           |
           +--> m4i_core (job/gang/group runtime validation)
           +--> m4i_bridge (read-only gameplay definition API)
```

## Source-of-truth boundary

For native M4I:

- `m4i_registry` owns what a job/gang/group **is**: label, grades and definition metadata.
- `m4i_core` owns which memberships a character **has**: domain, name, grade, active state and duty state.
- future inventory/vehicle resources own runtime ownership/quantity while resolving definitions from this registry.

This prevents a second definition table from competing with the registry.

## Canonical group namespace

`job`, `gang`, and generic `group` share one canonical name namespace.

For example, key `police` cannot simultaneously exist as both a job and a gang.

This rule is not only a UI check. Schema version 2 adds generated column `group_namespace` and DB unique index `uq_m4i_registry_group_namespace` over `(group_namespace, entry_key)`. For job/gang/group rows, `group_namespace` resolves to `groups`; other registry domains produce `NULL` and are not part of this cross-domain identity rule.

The database constraint prevents concurrent administrator writes from racing around the rule. Startup also checks for pre-existing cross-domain collisions and fails closed instead of guessing which definition should win.

Soft-deleted entries continue to reserve their canonical identity. Reusing the same key under another group domain requires an intentional migration/rename policy rather than silently changing the meaning of existing memberships.

## Legacy Core definition migration

Before Core 0.3 begins using registry-backed group definitions, `m4i_registry` can import the historical `m4i_groups` definition table.

Migration rules:

1. registry schema is prepared first;
2. legacy `m4i_groups` definitions are read when that table exists;
3. an existing registry definition is never overwritten by the legacy importer;
4. job/gang types are mapped to their canonical domains; other valid legacy group types are preserved as generic `group` definitions through `kind`;
5. canonical `unemployed` is seeded when missing;
6. the RAM registry is published only after this bootstrap completes.

The old `m4i_groups` table is intentionally **not dropped automatically** by this release. It remains migration/rollback evidence until the isolated migration gate has been verified.

## Live updates

A successful create/update/delete/rollback:

1. validates and normalizes the definition;
2. performs the database mutation transactionally;
3. appends immutable version history;
4. updates the RAM registry;
5. advances the registry generation;
6. publishes `m4i_registry:server:changed`.

Consumers therefore do not need a Core or server restart just because a definition changed.

## Duplicate protection

The registry distinguishes:

- exact duplicate — no-op
- same key with different data — explicit conflict/update
- possible semantic duplicate — explicit review
- job/gang/group namespace conflict — rejected

Canonical hashing is deterministic and computed in-process. Registry startup validates stored payload/hash integrity and fails closed on corrupt canonical state.

## Smart Import

`m4i_registry` can preview JSON and static Lua data tables, including common QBCore-style item/job/gang/vehicle layouts and generic group data.

Pasted Lua is treated as **data syntax only**. The importer does not use `load()` or `loadstring()` and rejects dynamic expressions/trailing executable code.

Unknown provider-specific fields can be retained under canonical `custom` data when configured instead of being silently discarded.

Smart Import preview is restricted to approved writer resources; the default trusted writer is `m4i_admin`.

## Public server read surface

Direct registry exports include:

```lua
exports.m4i_registry:IsReady()
exports.m4i_registry:GetVersion()
exports.m4i_registry:GetGeneration()
exports.m4i_registry:GetDomains()
exports.m4i_registry:GetEntry(domain, key, includeDisabled)
exports.m4i_registry:ResolveKey(domain, keyOrAlias)
exports.m4i_registry:ResolveEntry(domain, keyOrAlias, includeDisabled)
exports.m4i_registry:ListEntries(domain, options)
```

M4I gameplay resources should normally use the equivalent **read-only `m4i_bridge` definition surface**, not couple directly to registry internals.

## Trusted mutation surface

Mutation exports include preview/create-update/soft-delete/rollback/history/alias/import-preview operations. They are server-resource-only and guarded by the registry writer allowlist.

The shipped trusted writer is `m4i_admin`; browser/NUI code never calls registry writes directly.

## Asset boundary

The schema includes asset metadata/reference support, but binary image upload/materialization is **not shipped yet** in `0.2.0-alpha.1`.

Current design direction is:

- DB stores asset metadata/reference, not image BLOBs;
- binary files live in a hardened asset/static storage layer;
- SHA-256 deduplicates identical files;
- inventory/provider adapters materialize or reference the correct image location without arbitrary filesystem writes.

Do not document item-image auto-placement as available until that follow-up is implemented and runtime-tested.

## Native start order

```cfg
ensure oxmysql
ensure m4i_registry
ensure m4i_core
ensure m4i_bridge
ensure m4i_admin
```

`m4i_registry` must be ready before native `m4i_core` 0.3 because Core now validates job/gang/group runtime state against the canonical registry.
