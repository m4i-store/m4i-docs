# m4i_core Architecture

## Boundary

`m4i_core` is a framework provider. `m4i_bridge` selects and consumes the provider; `m4i_core` does not depend on the bridge.

This avoids a circular dependency and preserves provider neutrality for M4I scripts.

```text
M4I Script -> m4i_bridge -> selected framework provider
                              |
                              +-> m4i_core
                              +-> QBCore
                              +-> Qbox
                              +-> ESX
                              +-> Ox Core
```

## Canonical runtime model

The current native core uses:

- one canonical in-memory player object per loaded source
- one active loaded session per `characterId`
- canonical `userId` + `characterId`
- provider identity aliases in `m4i_provider_links`
- integer-cent balances in memory and persistence
- cached jobs/groups/metadata/status
- explicit dirty tracking for ordinary mutable character state

Reconnect/session handoff is guarded so overlapping or reused source IDs cannot create two active copies of the same character.

## Player lifecycle

### Load

A player load resolves or creates the canonical user and first character, loads accounts and groups, reserves the character session, builds the in-memory player object, and sends an owner-targeted snapshot to the client.

### Runtime

Ordinary player getters are served from the in-memory object after load.

There are no per-frame server loops in the core. The recurring persistence work is controlled and bounded.

### Unload

On disconnect the core:

- captures final native position before detaching the source
- detaches the old source session
- emits the unload event before a yielding persistence path can confuse a reused numeric source
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
- operation ID/idempotency validation
- optimistic concurrency detection
- balance update + audit-ledger insert in one transaction
- bounded reload/retry on optimistic conflicts

Job/group mutations are also persisted immediately.

### Cached / ordinary

Metadata and status changes update in-memory state, mark it dirty, synchronize the owning client, and are saved by the controlled persistence cycle or forced unload/save paths.

## Current database dependency

`m4i_core` currently depends on `oxmysql` as its database driver.

The architectural rule is that M4I gameplay scripts do not depend on `oxmysql` directly for core-owned player/framework state. The driver remains an internal infrastructure dependency behind `m4i_core`.

## Current alpha limitation

`0.1.0-alpha.1` automatically resolves the first non-deleted character and creates slot 1 when none exists. A complete multicharacter selection lifecycle is a later contract expansion.
