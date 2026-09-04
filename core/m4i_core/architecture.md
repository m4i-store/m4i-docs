# m4i_core Architecture

## Boundary

The FiveM resource `m4i_core` is the standalone primary framework runtime for native M4I mode and implements framework provider `m4i`. `m4i_bridge` selects and consumes that provider; `m4i_core` does not depend on the bridge or on QBCore, Qbox, ESX, or Ox Core.

The declared runtime dependency is `oxmysql`, which is the database driver.

Native/default path:

```text
M4I Script -> m4i_bridge -> provider m4i -> m4i_core
```

Optional compatibility paths remain explicit operator choices:

```text
M4I Script -> m4i_bridge -> qbcore
                         -> qbox
                         -> esx
                         -> ox_core
```

The default bridge framework priority contains only `m4i`, so native M4I mode does not silently fall back to another framework core.

## Canonical runtime model

The current native core uses:

- one canonical in-memory player object per loaded source
- one active loaded session per `characterId`
- canonical `userId` + `characterId`
- provider identity aliases in `m4i_provider_links`
- integer-cent balances in memory and persistence
- cached jobs/groups/metadata/status
- explicit dirty tracking for ordinary mutable character state
- per-load session generation for queued player-scoped work
- native Data Layer snapshot/subscription/write-behind/backpressure policies

Reconnect/session handoff is guarded so overlapping or reused source IDs cannot create two active copies of the same character or receive stale queued work.

## Runtime identity

`m4i_core` exposes:

```lua
exports.m4i_core:GetRuntimeInfo()
```

The standalone-primary contract reports:

```text
mode = primary
externalFrameworkRequired = false
databaseDriver = oxmysql
```

These diagnostics describe architecture/readiness only; they do not perform provider switching or migration.

## Player lifecycle

### Load

A player load resolves or creates the canonical user and first character, loads accounts and groups, reserves the character session, builds the in-memory player object, and sends an owner-targeted snapshot to the client.

### Runtime

Ordinary player getters are served from the in-memory object after load.

There are no per-frame server loops in the core. Recurring persistence/subscription work is controlled and bounded.

### Unload

On disconnect the core:

- captures final native position before detaching the source
- captures stable identity/session generation
- detaches the old source session
- emits terminal unload with a safe primary source contract
- drains the character session barrier
- persists final state
- releases the character reservation

Deferred cleanup is bounded and identity-safe.

## Privacy model

Sensitive player state is not globally replicated through public statebags.

The owning client receives its player snapshot through targeted server-to-client events and keeps a local cache for client-side reads.

This avoids exposing balances, metadata, groups, or identifiers as globally replicated state.

## Persistence model

### Immediate / critical

Money mutations are treated as critical operations:

- account-level serialization
- integer-cent arithmetic
- stable operation-ID replay/conflict validation when supplied
- optimistic concurrency detection
- balance update + audit-ledger insert in one transaction
- bounded reload/retry on optimistic conflicts

Job/group/duty mutations use their controlled immediate persistence paths.

### Cached / ordinary

Metadata and status changes update authoritative in-memory state, mark it dirty, synchronize the owning client, and are persisted through the bounded Data Layer write-behind/forced unload-save policies.

## Database dependency

`m4i_core` depends on `oxmysql` as its database driver.

M4I gameplay scripts do not depend on `oxmysql` directly for core-owned player/framework state. The driver remains infrastructure behind `m4i_core`.

## Current alpha limitation

`0.2.0-alpha.1` still automatically resolves the first non-deleted character and creates slot 1 when none exists. A complete multicharacter selection lifecycle is a later contract expansion.
