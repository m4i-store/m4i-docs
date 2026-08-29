# M4I Data Layer

## Goal

The M4I Data Layer is the native data architecture of `m4i_core`.

Its purpose is to keep database I/O out of the gameplay hot path whenever correctness allows, while preserving strong persistence guarantees for money and other critical state.

It is **not** a proxy layer for QBCore, Qbox, ESX, or Ox Core. Other frameworks remain responsible for their own data architecture when selected through `m4i_bridge`.

## Current v0.1 behavior

### Read path

After player load, core-owned player state is held in memory.

Ordinary getters for data such as:

- player identity
- accounts/balances
- job
- groups
- metadata
- status

read the in-memory player object instead of executing a SQL query for every request.

Example concept:

```text
100 scripts request player cash
            |
            v
       m4i_bridge
            |
            v
       m4i_core
            |
            v
     in-memory state
            |
            v
       no SQL read
```

The bridge may receive many logical calls, but those calls do not become one SQL query per getter when `m4i_core` is the provider.

### Critical write path

Money changes are not delayed merely for performance.

```text
validate -> lock -> DB transaction -> ledger -> commit -> update memory -> sync
```

The current core provides:

- integer-cent balances
- atomic balance + ledger transaction
- operation ID idempotency
- optimistic concurrency protection
- bounded retry on optimistic conflicts

### Ordinary write path

Metadata/status changes are applied to memory first, marked dirty, synchronized to the owning client, and persisted by the controlled save cycle or forced save/unload.

This reduces unnecessary repetitive writes while retaining restart/disconnect persistence behavior.

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

A script may own dedicated tables for its own domain when persistence is genuinely required. Database access should go through the approved bridge database service/exports rather than importing a database driver in gameplay business logic.

Do not store duplicate copies of core-owned balances/jobs/player identity just to avoid calling the bridge.

## Event-driven rule

Do not poll state continuously when a state-change event or subscription can drive the same behavior.

Bad pattern:

```text
every 100 ms -> GetMoney -> compare -> repeat forever
```

Preferred pattern:

```text
read initial state once
        +
react when the authoritative state changes
```

Current M4I events already cover important core transitions such as player load/unload, metadata/status changes, and other domain mutations. New subscription surfaces should be added centrally when scripts repeatedly need the same change signal.

## Target data-engine roadmap

The following items are architectural targets and must not be treated as shipped features until implemented and benchmarked:

### Snapshot APIs

Allow one call to return a bounded set of fields or a bounded player collection instead of repeated fine-grained calls.

### Request coalescing

Within a short execution window, equivalent read requests may share one resolved snapshot rather than repeating normalization/copy work.

This optimizes logical API pressure even when the source data is already in RAM.

### Smart write queues

Non-critical persistence can be grouped and scheduled rather than sent to the database as uncontrolled spikes.

### Priority classes

Conceptual target:

```text
CRITICAL
money / purchases / ownership
-> transactional commit

IMPORTANT
job / permissions / character lifecycle
-> immediate or high-priority controlled persistence

NORMAL
status / metadata / position-like state
-> dirty tracking / bounded batching where safe
```

### Backpressure

If persistence becomes slower than producers, M4I should bound concurrency and queue growth instead of allowing unlimited database work to accumulate.

Critical operations must not be hidden behind large queues of low-priority state saves.

### Batch persistence

Where semantically safe, multiple ordinary state writes can be persisted in controlled batches.

### Observability

Data-layer metrics should expose at least:

- logical reads
- database reads/writes
- transaction latency
- queued work
- retries/conflicts
- save latency
- slow operations
- cache/snapshot effectiveness

## Redis policy

Redis is not required for the current single-server architecture.

The first choice remains:

```text
FXServer memory + m4i_core + oxmysql + MariaDB/MySQL
```

Redis becomes useful only if M4I later needs shared cache/state across multiple FXServer instances, distributed locks, cross-server queues, or other genuinely distributed workloads.

## Performance claim policy

M4I may document its architecture and measured results, but it must not claim to be universally faster than QBCore/Qbox/ESX/Ox Core without representative direct benchmarks.

The goal is measurable low database pressure and predictable state behavior, not marketing claims without evidence.
