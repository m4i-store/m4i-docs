# Standards

This hub follows these standards:

- clarity over volume
- explicit behavior over assumptions
- no undocumented integration shortcuts
- no duplicated full docs across script repos

## Required practice

- all new scripts must be documented under `scripts/`
- all core systems must be documented under `core/`
- all integration and naming policies must be documented under `shared/`
- `SUMMARY.md` must be updated whenever a new docs section is added

## Quality baseline

- markdown paths must be valid
- examples must reflect real supported behavior
- pages must stay lightweight and readable
- terminology must stay consistent across sections

### Localization System

M4I uses a unified JSON-based localization system.

Before integrating or creating any script, developers must consult:

- `M4I_LANGUAGE_INTEGRATION_PLAYBOOK.md`
