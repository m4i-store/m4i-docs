# m4i_core Configuration

## Configuration file

Current runtime defaults live in:

```text
config/default.lua
```

## Database

```lua
database = {
    autoMigrate = true
}
```

- `autoMigrate = true`: run M4I schema migrations during core boot.
- disable it only when migrations are managed by a controlled external deployment process.

Never disable migrations simply to hide a migration failure. Diagnose the database error first.

## Persistence

```lua
persistence = {
    saveIntervalMs = 30000,
    metadataMaxBytes = 65536
}
```

- `saveIntervalMs`: controlled periodic save interval for dirty ordinary player state.
- `metadataMaxBytes`: maximum serialized metadata size accepted by the core.

Money and group/job correctness do not rely on waiting for this periodic save interval.

## Identity

```lua
identity = {
    preferredIdentifiers = { "license", "license2", "fivem", "discord" },
    defaultCharacterSlot = 1,
    handoffTimeoutMs = 5000,
    loadRetryAttempts = 3,
    loadRetryBackoffMs = 500
}
```

- `preferredIdentifiers`: ordered source identifiers used to resolve the canonical M4I user.
- `defaultCharacterSlot`: current alpha first-character slot.
- `handoffTimeoutMs`: bounded wait for overlapping character session handoff.
- `loadRetryAttempts` / `loadRetryBackoffMs`: bounded reconnect/load retry behavior.

## Accounts

```lua
accounts = {
    allowDynamic = false,
    allowNegative = false,
    maxTransaction = 100000000.00,
    defaults = {
        cash = 500.00,
        bank = 5000.00,
        crypto = 0.00
    }
}
```

Balances are stored internally as integer cents.

- `allowDynamic`: whether arbitrary account names may be created.
- `allowNegative`: whether balances may go below zero.
- `maxTransaction`: maximum accepted money mutation amount.
- `defaults`: account balances created for a new character.

Changing these values is an economy decision and should be version-controlled and tested.

## Groups / jobs

```lua
groups = {
    defaultJob = "unemployed",
    defaultJobLabel = "Unemployed",
    defaultJobGrade = 0,
    allowImplicitJobs = false
}
```

`allowImplicitJobs = false` is the safe default: job/grade mutations should reference defined group/job data rather than silently inventing authorization state.

## Status

```lua
status = {
    defaults = {
        hunger = 100,
        thirst = 100,
        stress = 0
    },
    min = 0,
    max = 100
}
```

Status values are bounded to the configured range.

## Security

```lua
security = {
    adminAces = { "m4i.admin", "command" },
    adminGroups = {
        admin = true,
        superadmin = true,
        god = true
    }
}
```

Admin checks can be satisfied through configured ACE permissions or loaded M4I groups.

Do not use client-supplied admin claims as authority.

## Production configuration rules

- keep config changes in source control
- back up the database before changing identity/schema behavior
- do not change the active framework provider with players connected
- do not change account semantics without a migration plan
- validate configuration in a staging profile before production
