# m4i-docs

`m4i-docs` is the official centralized documentation hub for all M4I FiveM systems and scripts.

This repository is the single source of truth for:

- M4I platform/core architecture
- `m4i_core` runtime and data architecture
- `m4i_bridge` universal compatibility contracts
- M4I script documentation
- shared development, security, integration, and data-access standards
- operational rollout and support guidance

## Platform boundary

The core rule is:

```text
M4I gameplay scripts -> m4i_bridge -> selected framework provider
```

When framework provider `m4i` is selected, the FiveM resource `m4i_core` implements that provider and M4I owns the native server-authoritative data architecture.

When QBCore, Qbox, ESX, or Ox Core is selected, that framework remains responsible for its own data/cache/persistence implementation. `m4i_bridge` translates APIs; it does not create an M4I Data Proxy over another framework.

## Documentation policy

- Full documentation lives in this hub.
- Individual resource repositories should keep a short README and link to this hub.
- New script docs must be added under `scripts/<script_name>/` using `scripts/_template/` as the baseline.
- New M4I-owned gameplay scripts must follow the bridge boundary and the shared data-access policy.
- Planned architecture must be labeled as planned until it is implemented and validated.

## Structure

- `introduction/`: onboarding and documentation model
- `core/`: universal architecture, `m4i_core`, and `m4i_bridge`
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
- [m4i_core](core/m4i_core/introduction.md)
- [M4I Data Layer](core/m4i_core/data-layer.md)
- [m4i_bridge](core/m4i_bridge/introduction.md)
- [Universal Core Contract v4](core/m4i_bridge/universal-core-contract-v4.md)
- [Script Development Guide](core/m4i_bridge/script-development-guide.md)
- [Data Access Policy](shared/data-access-policy.md)
- [Integration Rules](shared/integration-rules.md)
