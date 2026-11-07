# M4I Upload — Installation on Any Framework

> **CURRENT INSTALLATION — READ FIRST:** [Complete Upload installation — consumer UI code and permissions](complete-installation.md). This page is a companion guide; the full guide includes SQL, items, third-party script edits, provider compatibility and go-live steps. Also review [Source-audited limitations](../../shared/fivem-install-known-limitations.md).


**Resource:** `m4i_upload` · **Version:** `0.2.1-alpha` · **Updated:** 7 November 2026.

M4I Upload is a **central image asset library**, independent of QBCore/Qbox/ESX/M4I/Ox Core player frameworks. Upload a file once and resolve its image ID in any compatible item, vehicle, phone or UI script. Categories are **organisational only**, not permission barriers. Consumers should integrate **through M4I Bridge**; legacy direct Upload exports remain for compatibility.

## 1. Install

1. Back up an existing `m4i_upload/data` directory completely if upgrading. **Never overwrite `data/index.json`, `data/assets/`, `data/backups/` or `data/audit.json` with blank package data.**
2. Extract the **inner** folder to `resources/[m4i]/m4i_upload/`. Check `fxmanifest.lua`, `client/main.lua`, `server/main.lua`, and `web/index.html` exist.
3. Make sure FXServer has read/write permission to Upload's `data/` files and assets. Keep uploads on persistent disk, not an ephemeral container layer.
4. Start in `server.cfg`:

```cfg
# Your core/framework and any selected dependencies have started already.
ensure m4i_bridge       # recommended for integrations; not a manifest dependency of Upload
ensure m4i_upload
# ensure m4i_garage    # optional consumer
```

5. Only trusted admins get Upload permission (example uses ACE directly; adjust your own principals):

```cfg
add_ace group.admin m4i.upload allow
# Your existing add_principal must already assign real admins to group.admin.
# Never grant m4i.upload to group.user or builtin.everyone.
```

6. Connect as an authorized admin and type `/m4iupload` in FiveM. If your M4I Confige version has the Upload tool integration, its protected UI is another way to open it.

## 2. Choose your framework

No Upload-specific framework mode is required. You can install exactly the same `m4i_upload` folder on:

| Existing base | Upload configuration | Consumer integration |
| --- | --- | --- |
| M4I | none | Bridge `Framework='m4i'` |
| QBCore | none | Bridge `Framework='qbcore'` |
| Qbox / QBX | none | Bridge `Framework='qbox'` |
| ESX Legacy | none | Bridge `Framework='esx'` |
| Ox Core | none | Bridge `Framework='ox_core'` |

Upload stores **images**, not player ownership or money. Do not install QBCore/ESX inventory purely for Upload. Existing inventory, phone, vehicle Garage and custom NUI integrations are **consumers**, not required Upload dependencies.

## 3. Supported formats and limits

- Preserve original PNG, JPG/JPEG, WebP and GIF bytes unchanged when using **Save original**, up to **4 MiB per image**.
- Optional **Optimize image** creates a separate static WebP preview. This may change format/resolution/quality; animated sources should use original bytes to preserve motion.
- The optimizer can decode additional input formats only where FiveM's NUI decoder supports them; unsupported originals must be explicitly converted.
- Up to 700 active images, 95 MiB active catalog data and 32 MiB historical backup storage, as enforced by this build. You still need external backups.
- New image IDs must be lowercase safe identifiers. A single global ID can be reused by multiple scripts; do not re-upload the same picture for each category.

## 4. Backup/upgrade checklist

**Preserve data, audit and identifiers** during updates. Only overwrite application code and web assets; use the current catalog to verify that existing image IDs still resolve. Before replacing images or deleting IDs, export your catalog and test all consuming scripts. Do not publish private user photos, ID documents or credentials as image assets: images are readable by connected clients.

## 5. Connecting an existing script

`m4i_upload` does **not** automatically patch every vendor's HTML or inventory card. Create an adapter in that UI to ask Bridge for an image by global ID and set the resulting data URI as the `src` of an image element. Preserve local file fallback for absent/old IDs and perform async requests outside latency-sensitive render loops.

**Use the public Bridge API** described in [Image integration](integration.md). The internal/legacy Upload server exports `GetImageDataUri`, `GetImageMetadata` and `ListImages` remain but should not be the first choice for new M4I scripts.

## 6. Troubleshooting

- **Command unavailable:** exact resource folder must be `m4i_upload`, resource started, client ready; check F8.
- **Permission denied:** check ACE `m4i.upload` and the admin's effective `add_principal`.
- **Upload fails/blank image:** check original format, image dimensions/size, catalog limit, data directory write permission and any client console error.
- **Image appears only after delay:** check Bridge/Upload readiness, data URI fetch, browser cache, NUI async queue and missing image key. Avoid repeatedly fetching the same large asset every render.
- **Animation lost:** Save original for GIF/APNG/animated WebP; optimization is deliberately static.
- **Images disappear after upgrade:** restore `data/` from backup, never reset catalog IDs.
- **Consumer does not display images:** implement the consuming NUI adapter; Upload itself is only a registry.

**Release note:** A ZIP labelled Escrow is not proof of Cfx Asset Escrow encryption. See [Bridge installation](../../core/m4i_bridge/setup-selector.md) and [deployment QA](../../shared/fivem-qa-checklist.md).