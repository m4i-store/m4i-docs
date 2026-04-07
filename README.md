# m4i-docs

`m4i-docs` is the official centralized documentation hub for all M4I systems and scripts.

This repository is the single source of truth for:

- M4I core systems documentation
- M4I script documentation
- shared standards and integration rules
- operational and support guidance

## Documentation policy

- Full documentation lives in this hub.
- Individual script/resource repositories should keep a short README and link to this hub.
- New script docs must be added under `scripts/<script_name>/` using `scripts/_template/` as the baseline.

## Structure

- `introduction/`: onboarding and documentation model
- `core/`: core M4I systems (for example `m4i_bridge`)
- `scripts/`: script documentation and reusable template
- `shared/`: standards, conventions, and support policy

## GitBook / Git Sync

This repository is GitBook-ready:

- root README: `README.md`
- navigation: `SUMMARY.md`
- GitBook config: `.gitbook.yaml`

## Quick links

- [Welcome](introduction/welcome.md)
- [m4i_bridge docs](core/m4i_bridge/introduction.md)
- [Script template](scripts/_template/introduction.md)
- [Integration rules](shared/integration-rules.md)
