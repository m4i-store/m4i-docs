# m4i-docs

`m4i-docs` is the official centralized documentation hub for all M4I FiveM systems and scripts.

This repository is the single source of truth for:

- M4I platform/core architecture
- `m4i_registry` canonical live definitions
- `m4i_core` runtime and Data Layer architecture
- `m4i_bridge` universal compatibility/read contracts
- `m4i_admin` in-game registry management
- M4I script documentation
- shared development, security, integration, and data-access standards
- operational rollout and support guidance

## Platform boundary

M4I gameplay code follows:

```text
M4I gameplay scripts -> m4i_bridge -> selected framework provider
```

Native M4I mode adds a canonical definition layer:

```text
m4i_admin -> m4i_registry -> canonical definitions
                |                 |
                |                 +--> m4i_bridge read-only definition API
                +--------------------> m4i_core job/gang/group validation

M4I gameplay scripts -> m4i_bridge -> provider m4i -> m4i_core
```

`m4i_registry` owns definition/catalog data. `m4i_core` owns native player/runtime state such as character sessions, accounts, memberships, grades and duty. These responsibilities must not become competing sources of truth.

When QBCore, Qbox, ESX, or Ox Core is explicitly selected as the framework provider, that framework remains responsible for its own player cache/persistence implementation. `m4i_bridge` translates APIs; it does not create an M4I Data Proxy above another framework.

## Native startup order

Current native M4I startup is:

```cfg
ensure oxmysql
ensure m4i_registry
ensure m4i_core
ensure m4i_bridge
ensure m4i_admin
```

The bridge default framework provider is `m4i` and its default framework priority is M4I-only. External framework adapters remain explicit compatibility choices.

## Documentation policy

- Full documentation lives in this hub.
- Individual resource repositories should keep a short README and link to this hub.
- New script docs must be added under `scripts/<script_name>/` using `scripts/_template/` as the baseline.
- New M4I-owned gameplay scripts must follow the bridge boundary and shared data-access policy.
- Planned architecture must be labeled as planned until it is implemented and validated.
- Do not describe binary asset upload/materialization as shipped until the hardened asset phase is merged and runtime-tested.

## Structure

- `introduction/`: onboarding and documentation model
- `core/`: universal architecture, registry, Core, Bridge and administration
- `scripts/`: script documentation and reusable template
- `shared/`: standards, conventions, integration/data policies, and support rules

## GitBook / Git Sync

This repository is the Git source for the M4I GitBook site.

- root README: `README.md`
- navigation: `SUMMARY.md`
- GitBook config: `.gitbook.yaml`

Changes merged to the Git-synced branch are intended to become the canonical documentation source for the GitBook site.

## Quick links

- [Welcome](introduction/welcome.md)
- [Platform Overview](introduction/overview.md)
- [Universal M4I Architecture](core/universal-architecture.md)
- [m4i_registry](core/m4i_registry.md)
- [m4i_core](core/m4i_core/introduction.md)
- [M4I Data Layer](core/m4i_core/data-layer.md)
- [m4i_bridge](core/m4i_bridge/introduction.md)
- [Bridge Exports](core/m4i_bridge/exports.md)
- [m4i_admin](core/m4i_admin.md)
- [Universal Core Contract v4](core/m4i_bridge/universal-core-contract-v4.md)
- [Script Development Guide](core/m4i_bridge/script-development-guide.md)
- [Data Access Policy](shared/data-access-policy.md)
- [Integration Rules](shared/integration-rules.md)
