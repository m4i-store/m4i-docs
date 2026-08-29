# M4I Data Layer

## Goal

The M4I Data Layer is the native data architecture inside the FiveM resource `m4i_core`, which implements framework provider `m4i`.

Its purpose is to keep database I/O and repeated state work out of the gameplay hot path whenever correctness allows, while preserving strong persistence guarantees for critical state.

It is **not** a proxy layer for QBCore, Qbox, ESX, or Ox Core. Other framework providers remain responsible for their own data/cache/persistence architecture when selected through `m4i_bridge`.

## Current shipped v1 behavior

### Player state in memory

After a player is loaded, core-owned player state is held in the authoritative `m4i_core` player object.

Ordinary reads for data such as:

- identity
- accounts/balances
- job/duty
- groups
- metadata
- status

read from authoritative in-memory state instead of issuing one SQL query per getter.

```text
many logical reads
      |
      v
  m4i_bridge
      |
      v
 provider m4i
      |
      v
   m4i_core
      |
      v
 authoritative RAM state
```

## Snapshot API

The shipped Data Layer provides bounded snapshot APIs:

```lua
GetPlayerSnapshot(sourceId, fields)
GetPlayersSnapshot(fields, limit)
```

A consumer can request a bounded set of fields in one logical call instead of repeatedly resolving many fine-grained getters.

Supported snapshot fields include the normalized core state such as identity, accounts, job, groups, metadata and status, plus bounded field-specific forms such as individual account/metadata/status values.

### Revision-aware micro-cache

Equivalent snapshots may be reused inside a short configured TTL window.

The cache is revision-aware:

- player-visible state mutations advance the player view revision
- a cached snapshot must match the current character and revision
- stale revisions are not served
- snapshot variants per player are bounded
- cache entries are invalidated on relevant mutations/lifecycle changes

This reduces repeated normalization/deep-copy work for many equivalent readers without making the cache the source of truth.

## 100 x 100 logical stress model

The shipped CI workload includes:

```text
100 players
x 100 equivalent consumer rounds
= 10,000 snapshot calls
```

The test models 30,000 logical field reads and verifies the expected revision-aware coalescing behavior inside the configured micro-cache window: initial snapshot builds followed by cache hits, with a revision change invalidating only the affected player.

This is a logical/core stress harness. It is **not** a claim that 100 simultaneous real FiveM clients have been benchmarked by that unit test.

## Event and subscription bus

The Data Layer provides server-side change topics through:

```lua
SubscribeData(topic, handler)
UnsubscribeData(token)
```

and the synchronous core event:

```text
m4i_core:server:dataChanged
```

The purpose is to let scripts read initial state once and react to authoritative changes instead of polling continuously.

Examples of core topics include player lifecycle, money, job/duty, metadata and status changes.

### Bounded delivery

Subscription delivery does not create an unbounded thread per event.

The shipped implementation uses:

- bounded delivery queue
- fixed worker count
- bounded deliveries per worker tick
- cooperative yielding after each bounded batch
- explicit overflow/drop metrics
- resource-owner cleanup

This prevents a slow or recursively-emitting handler from causing unbounded coroutine growth or monopolizing the cooperative scheduler.

## Session-safe queued events

FiveM numeric source IDs can be reused.

Queued player-scoped events are therefore bound to a **per-load `sessionGeneration`**, not only to `sourceId` or `characterId`.

Before delivery, the current live player must match the captured character and load generation. Old queued work from a previous connection is rejected even when the same character reconnects on the same numeric source.

### Terminal `player.unloaded` contract

`player.unloaded` is a terminal lifecycle event and intentionally behaves differently:

- primary live `sourceId` is always `nil`
- historical numeric source remains in `meta.source`
- stable character/user identity remains in metadata/payload
- the old `sessionGeneration` is preserved

This prevents cleanup consumers from accidentally acting on a replacement player that inherited the same FiveM source ID.

The same terminal source rule applies to both queued subscriptions and the synchronous `m4i_core:server:dataChanged` path.

## Ordinary write-behind

Non-critical dirty player state such as metadata/status can be persisted through the controlled write-behind scheduler instead of creating uncontrolled repetitive database writes.

The shipped scheduler includes:

- dirty tracking
- per-character save coalescing
- bounded min-heap queue
- configured write delay
- bounded work per tick
- high-water backpressure behavior
- bounded retry/backoff
- periodic dirty scan recovery
- wrap-safe monotonic timing across `GetGameTimer()` wrap

Queue overflow never acknowledges or clears unsaved dirty state. Dirty state remains recoverable by the bounded scan/forced persistence paths.

## Critical write path

Critical money state is intentionally **not** moved behind the ordinary write-behind queue.

```text
validate
  -> player/account lock
  -> atomic DB transaction
  -> ledger
  -> commit
  -> update authoritative RAM
  -> sync/event
```

Current money guarantees include:

- integer-cent balances
- atomic balance + ledger transaction
- operation-ID idempotency
- optimistic concurrency protection
- bounded conflict retry
- conflicting operation-ID reuse rejection

Reads can remain memory-backed while critical money writes stay durable and transactional.

## Important state

Important state such as job/duty remains on its immediate controlled persistence path rather than being hidden behind the ordinary write queue.

DB-yielding paths revalidate the captured player session before mutating/syncing/emitting so source reuse cannot apply an old operation to a replacement session.

## Backpressure and boundedness

The Data Layer is designed so producers cannot grow background work without limits.

Bounded structures include:

- snapshot variants per player
- bulk snapshot player count
- subscription handlers globally and per owner
- queued event deliveries
- delivery worker concurrency/work per tick
- write-behind queue depth
- retries
- metrics timer samples

The objective is predictable degradation under pressure rather than uncontrolled queue/coroutine/memory growth.

## Observability

Data Layer metrics expose operational signals including:

- logical reads
- snapshot requests/hits/misses/invalidations
- snapshot latency/slow snapshots
- event emission/delivery/overflow/stale-session rejection
- active subscriptions
- write queue depth/capacity/pressure
- coalesced/scheduled/processed/retried/failed saves
- save and queue latency
- critical vs normal write counters
- database operation metrics from the core DB layer

Metrics use bounded sampling for latency percentiles.

## Bridge ownership delegation

M4I gameplay scripts should subscribe through `m4i_bridge`, not call `m4i_core` directly.

For native subscriptions, `m4i_bridge` captures the original gameplay resource and delegates that owner to `m4i_core`.

Core accepts an owner override **only** from the resource named exactly `m4i_bridge`.

This preserves:

- per-resource subscription caps
- owner-only unsubscribe semantics
- gameplay-resource stop cleanup
- bridge-stop/crash cleanup of delegated callback references
- bounded delegation bookkeeping

Non-bridge resources cannot spoof another owner through the Core export.

## Mandatory data rules for M4I scripts

### Core-owned data

M4I gameplay scripts must never write directly to `m4i_core` tables for:

- users/characters
- money/accounts/ledger
- jobs/groups/memberships
- provider identity links
- core metadata/status

Use `m4i_bridge` contracts instead.

### Script-owned data

A script may own dedicated tables for its own domain when persistence is genuinely required.

Database access should use the approved bridge database service/exports rather than importing a database driver throughout gameplay business logic.

Do not store duplicate copies of core-owned balance/job/player identity merely to avoid calling the bridge.

## Event-driven rule

Avoid continuous polling when a subscription/change event provides the same semantics.

Bad:

```text
every 100 ms -> GetMoney -> compare -> repeat
```

Preferred:

```text
read initial snapshot once
        +
subscribe to authoritative changes
```

## Provider boundary / no Data Proxy

The native Data Layer exists only when provider `m4i` is implemented by `m4i_core`.

With another selected framework:

```text
M4I script -> m4i_bridge -> QBCore/Qbox/ESX/Ox Core
```

that framework owns its own state/cache/database behavior.

`m4i_bridge` does **not** place M4I snapshot caching, batching, write-behind or database interception over non-M4I frameworks.

## Redis policy

Redis is not required for the current single-FXServer architecture.

Current preferred foundation:

```text
FXServer RAM + m4i_core + oxmysql + MariaDB/MySQL
```

Redis should be introduced only for a real distributed requirement such as shared state across multiple FXServer instances, distributed locks, cross-server queues or shared cache.

## Performance claim policy

M4I can document measured behavior and its architecture, but must not claim universal performance superiority over QBCore/Qbox/ESX/Ox Core without representative direct benchmarks.

The shipped 100 x 100 harness proves bounded logical/core behavior; real-client/VPS soak and cross-framework comparisons are separate benchmark gates.
