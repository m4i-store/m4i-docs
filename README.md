# m4i-docs

`m4i-docs` is the official centralized documentation hub for all M4I systems and scripts.

This repository is the single source of truth for:

- M4I core platform documentation
- M4I script documentation
- M4I integration standards
- operational and support guidance

## Why this hub exists

M4I documentation is no longer maintained as many full standalone doc sets across individual script resources.

Instead:

- full docs live in this hub
- script/resource repos keep a short README and link back here
- standards are shared and enforced from one place

This keeps docs consistent, reduces drift, and scales cleanly as new scripts are added.

## GitBook and Git Sync

This project is GitBook-ready:

- root `README.md` is the docs landing page
- root `SUMMARY.md` defines navigation
- root `.gitbook.yaml` defines structure mapping

Recommended workflow:

1. Connect this repository to GitBook via Git Sync.
2. Treat pull requests in this repo as the docs change control path.
3. Update script docs here first, then link from script repos.

## Repository structure

- `introduction/`: onboarding and documentation model
- `core/`: core M4I systems (starting with `m4i_bridge`)
- `scripts/`: script docs and reusable script template
- `shared/`: cross-project standards and policies

## Maintainer note

When adding a new M4I script:

1. create `scripts/<script_name>/`
2. copy from `scripts/_template/`
3. add navigation entries in `SUMMARY.md`
4. update script repo README to link to this hub
