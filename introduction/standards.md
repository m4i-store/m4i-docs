# Standards

This hub follows these standards:

- clarity over volume
- explicit behavior over assumptions
- no undocumented integration shortcuts
- no duplicated full docs across resource repos
- implemented behavior must be separated from roadmap/planned behavior

## Required practice

- all new scripts must be documented under `scripts/`
- all core systems must be documented under `core/`
- all integration, data-access, naming, and support policies must be documented under `shared/`
- `SUMMARY.md` must be updated whenever a new docs section is added
- M4I-owned gameplay scripts must use `m4i_bridge` for framework/provider integration
- core-owned player/framework data must not be changed through direct SQL in gameplay resources

## Quality baseline

- markdown paths must be valid
- examples must reflect real supported behavior
- pages must stay readable and operationally useful
- terminology must stay consistent across sections
- provider names and resource names must be exact (`m4i_core`, `m4i_bridge`)
- performance claims require representative measurements

## Architecture baseline

The canonical separation is:

```text
M4I scripts -> m4i_bridge -> selected provider
```

`m4i_core` owns the M4I Data Layer only when it is the selected native provider. `m4i_bridge` does not become a second data source for other frameworks.

Developers must consult:

- [Universal M4I Architecture](../core/universal-architecture.md)
- [Script Development Guide](../core/m4i_bridge/script-development-guide.md)
- [M4I Data Access Policy](../shared/data-access-policy.md)

### Localization System

M4I uses a unified JSON-based localization system.

Before integrating or creating any script, developers must consult the current M4I language integration playbook when that resource uses localized content.
