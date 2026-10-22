# m4i_upload — M4I image library

The correct resource name is **m4i_upload**. Repository: https://github.com/m4i-store/m4i_upload (private).

## Live release (October 22, 2026)

m4i_upload 0.1.0-alpha (main df0d61d) is running on the Roleplay VPS alongside Confige and Inventory. The new gallery can be opened with /m4iupload by the authorized master admin, or as a protected native tool through M4I Confige.

The image catalog initially includes 26 copied PNG images from existing M4I Inventory and HUD sources, without removing originals. Two HUD screenshots were skipped because they exceeded the 200 KiB limit. The UI offers category filtering, search, upload, replacement and deletion. Categories include items, vehicles, characters, jobs, logos, UI and other.

Each new upload is compressed to WebP (maximum 768 px) in the client browser, then validated server-side with filename, image type, size, roles, revision, backup and audit checks. Backend resource limits are 700 images, 95 MiB active data, and 32 MiB cumulative backups. Only the trusted master has private m4i.upload ACE. Image content itself is public; do not store secrets or private identities.

Runtime media index, uploaded data, backup images and audit journal reside in the m4i_upload/data folder, excluded from the GitHub source. Server exports GetImageDataUri, GetImageMetadata and ListImages and a client async GetImageDataUri callback let other M4I scripts consume new images without a restart. Old script UIs are not automatically rewired: each needs a consumer adapter.

## Verification

Unit mock: permission denials, safe image upload, read, source magic checks, revision conflicts, replacement/backup and delete passed. Chromium NUI mock: gallery, category filters, preview, PNG-to-WebP conversion and upload request passed.

The first service restart logged missing file warnings because the new directory permissions were too restrictive. The service account m4i_core_test was granted appropriate source read and image data write permissions. A no-player restart then successfully started m4i_upload with 26 catalog entries. Confige health PASS and all 40 server resources loaded.

Real in-game CEF uploads and every legacy script's image adapter remain to be acceptance-tested.
