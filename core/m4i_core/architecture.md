# m4i_core Architecture

## Boundary

`m4i_core` is the standalone primary framework runtime for native M4I mode and implements framework provider `m4i`.

It does not depend on `m4i_bridge`, QBCore, Qbox, ESX, or Ox Core. Core talks directly to native `m4i_registry` for canonical job/gang/group definitions so there is no Core -> Bridge -> Core dependency cycle.

Declared native runtime dependencies:

- `oxmysql`
- `m4i_registry`

Native gameplay path:

```text
M4I Script -> m4i_bridge -> provider m4i -> m4i_core
```

Native definition path:

```text
m4i_registry -> m4i_core membership validation/refresh
             -> m4i_bridge read-only gameplay definition surface
```

External framework compatibility paths remain explicit operator choices through `m4i_bridge`.

## Canonical ownership model

### Registry-owned definitions

`m4i_registry` owns definitions for jobs, gangs, generic groups and the wider shared catalog.

For group-like domains, registry owns:

- canonical key/domain
- label
- grades
- definition metadata/custom data

Jobs/gangs/groups share one registry-enforced canonical key namespace.

### Core-owned runtime state

`m4i_core` owns:

- one canonical in-memory player object per loaded source
- one active loaded session per `characterId`
- canonical `userId` + `characterId`
- provider identity aliases
- integer-cent balances
- character group memberships
- membership `group_domain`, `group_name`, `grade`, `active`, `on_duty`, metadata
- character metadata/status
- Data Layer runtime/persistence state

This split prevents definition duplication.

## Group membership persistence

Fresh Core 0.3 schema uses `m4i_group_memberships` with a domain-aware key:

```text
(character_id, group_domain, group_name)
```

Domains are normalized to:

```text
job
gang
group
```

The old `m4i_groups` definition table is not part of fresh Core definition ownership.

On an upgraded database, migration v3 may read legacy `m4i_groups` only to translate existing membership rows to their correct domain before the new runtime takes over. Active Core group code does not create/query/update legacy definitions.

The old table is deliberately not auto-dropped in this release.

## Startup ordering

Core startup is fail-closed:

1. database preflight
2. wait for required `m4i_registry` readiness
3. run Core schema migrations
4. mark Core ready
5. start Data Layer
6. publish Core ready signal
7. load already connected players

Registry must import/seed canonical group definitions before Core membership migration/player load.

## Runtime identity

`GetRuntimeInfo()` reports fields including:

```text
mode = primary
externalFrameworkRequired = false
databaseDriver = oxmysql
definitionRegistry = m4i_registry
definitionRegistryRequired = true
```

## Player lifecycle

### Load

A player load resolves/creates canonical identity, reserves the character session, loads accounts and membership rows, resolves membership definitions from registry, builds the in-memory player object, and sends an owner-targeted snapshot to the client.

Missing/invalid required definition state fails closed rather than inventing an unknown job definition inside Core.

### Runtime

Ordinary player getters are served from the in-memory player object after load.

Money, group membership, metadata/status and Data Layer behavior follow their domain-specific persistence paths.

There are no unbounded per-frame server loops in Core.

### Unload

On disconnect Core captures stable identity/session generation, detaches the old source safely, emits terminal unload semantics, drains the character session barrier, persists final state and releases the reservation.

## Live definition refresh

Registry `job`/`gang`/`group` change events are treated as hints only when the invoking resource is exactly `m4i_registry`.

Core then re-resolves authoritative registry data and refreshes a finite snapshot of affected online players. The refresh loop may cooperatively yield between players; it is not a permanent frame loop.

If a currently active job becomes invalid/disabled or its grade is removed, Core performs controlled repair/fallback according to the shipped group runtime contract rather than keeping a stale invented definition.

## Session/source safety

Core maintains per-load `sessionGeneration` and character ownership barriers.

DB-yielding paths revalidate the captured player session before mutating/syncing/emitting. This prevents a recycled FiveM numeric source from receiving stale work from a prior connection.

## Privacy model

Sensitive player state is not globally replicated through public statebags.

The owning client receives targeted snapshots/events. Balances, groups, metadata and identifiers are not exposed as global player state.

## Persistence model

### Critical money

Money mutations use:

- integer-cent arithmetic
- account-level serialization
- stable operation-ID replay/conflict validation when supplied
- optimistic concurrency detection
- balance update + audit ledger in one transaction
- bounded conflict reload/retry

### Group membership

Job/group/duty mutations use controlled immediate persistence. Definition validation comes from the registry; membership persistence stays in Core.

### Ordinary mutable state

Metadata/status use authoritative RAM state, dirty tracking and bounded Data Layer write-behind/forced lifecycle saves.

## Data Layer

The shipped native Data Layer includes bounded snapshots, subscriptions, delivery workers, write-behind, backpressure/retries, session-safe delivery and metrics. See [M4I Data Layer](data-layer.md).

## Database dependency

M4I gameplay scripts do not query Core/Registry database tables directly for framework-owned state. `oxmysql` remains infrastructure behind M4I services.

## Current alpha limitations

`0.3.0-alpha.1` still uses the current first-character/slot-1 lifecycle; complete multicharacter selection remains later work.

The latest registry-backed migration/runtime changes still require a fresh isolated real FiveM gate before production cutover claims.
