# m4i_identity Introduction

`m4i_identity` is the identity ownership resource for M4I servers.

It controls pre-join identity validation, queue-aware checkpoints, language selection, and runtime identity state for connected players.

## Why It Exists

M4I needs one authoritative place for identity decisions so every script follows the same access and trust model.

`m4i_identity` provides that authority by centralizing:

- identifier validation
- allowlist/auto-create identity policy
- language policy
- reconnect throttling
- runtime identity state

## Ownership Boundaries

`m4i_identity` owns:

- identity resolution and persistence decisions
- create/update identity writes
- pre-join connection acceptance/rejection logic

Other scripts must not:

- insert/update identity rows directly
- bypass identity checks with custom SQL
- re-implement identity creation logic

## Relationship to m4i_bridge

`m4i_bridge` is an integration layer, not the identity owner.

Bridge compatibility for identity is read-only:

- `m4i_bridge` may consume `m4i_identity` read exports
- `m4i_bridge` must not query identity DB tables directly
- `m4i_bridge` must not create/update/delete identity records

This keeps ownership explicit and prevents cross-resource logic drift.
