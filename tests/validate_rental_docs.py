"""Check central rental documentation and optionally its exact review archive.

This validates documentation provenance, links and recorded contracts only.
It does not execute rental code, SQL, framework providers or the FiveM engine.
"""
from pathlib import Path
import argparse
import hashlib
import json
import re
import zipfile

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "scripts" / "m4i_rental"
PAGES = (
    "introduction", "source-status", "installation", "configuration",
    "admin-creator", "lifecycle", "payments", "integration", "exports",
    "testing", "troubleshooting", "changelog",
)


def check(condition, message):
    if not condition:
        raise AssertionError(message)


def validate(source_archive=None):
    summary = (ROOT / "SUMMARY.md").read_text(encoding="utf-8")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    texts = {}
    for page in PAGES:
        path = DOCS / f"{page}.md"
        check(path.is_file(), f"missing rental page: {page}")
        text = path.read_text(encoding="utf-8")
        check(text.startswith("# m4i_rental"), f"missing page title: {page}")
        check(len(text) > 300, f"empty or placeholder rental page: {page}")
        check(text.count("```") % 2 == 0, f"unclosed code fence: {page}")
        target = f"scripts/m4i_rental/{page}.md"
        check(summary.count(f"]({target})") == 1, f"navigation missing or duplicated: {target}")
        check("sandbox:/" not in text, f"private sandbox download in public docs: {page}")
        texts[page] = text
    check("scripts/m4i_rental/introduction.md" in readme, "README must link rental introduction")
    for page, text in texts.items():
        for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            resolved = (DOCS / target.split("#", 1)[0]).resolve()
            check(resolved.is_relative_to(ROOT.resolve()), f"link escapes repository: {page}: {target}")
            check(resolved.exists(), f"broken local link: {page}: {target}")

    snapshot = json.loads((DOCS / "source-snapshot.json").read_text(encoding="utf-8"))
    check(snapshot["schema_version"] == 1, "unsupported provenance schema")
    check(snapshot["status"] == "review-build", "update this contract explicitly when promoting a release")
    archive = snapshot["archive"]
    check(re.fullmatch(r"[0-9a-f]{64}", archive["sha256"]), "invalid archive SHA-256")
    check(archive["git_commit"] is None, "review archive must not invent a matching commit")
    check(archive["live_fivem_tested"] is False, "no live FiveM evidence recorded for this snapshot")
    check(archive["github_upload_verified"] is False, "no matching gameplay upload verified")
    check(snapshot["upstream"]["main_contains_documented_gameplay"] is False, "do not conflate main and review gameplay")
    check(archive["sha256"] in texts["source-status"], "source page must display exact archive hash")
    check("Review Build" in texts["introduction"], "review status must be prominent")
    check("not performed" in texts["testing"], "runtime gate must remain explicit")
    contract = snapshot["expected_contract"]
    for key, page in (("admin_command", "installation"), ("admin_ace", "installation"),
                      ("member_command", "exports"), ("schema_path", "installation")):
        check(contract[key] in texts[page], f"documented contract missing: {key}")
    for name in contract["server_exports"] + contract["client_exports"]:
        check(name in texts["exports"], f"missing export: {name}")
    for name in ("GetMoney", "RemoveMoney", "AddMoney", "GetCharacterId", "m4i_bridge"):
        check(name in texts["integration"], f"missing bridge boundary: {name}")
    check("ceil" in texts["payments"], "integer-ceiling price must be documented")
    check("idempotentMoney" in texts["payments"], "financial capability limits missing")
    check("debit_inflight" in texts["payments"] and "refund_inflight" in texts["payments"], "reconciliation states missing")
    order = ["ensure oxmysql", "ensure m4i_registry", "ensure m4i_core", "ensure m4i_bridge", "ensure m4i_rental"]
    positions = [texts["installation"].find(x) for x in order]
    check(all(p >= 0 for p in positions) and positions == sorted(positions), "native startup order changed")
    file_hashes = snapshot["source_files_sha256"]
    for path, digest in file_hashes.items():
        check(not Path(path).is_absolute() and ".." not in Path(path).parts, "invalid source path")
        check(re.fullmatch(r"[0-9a-f]{64}", digest), f"invalid source hash: {path}")
    assets = snapshot["retained_asset_git_blobs"]
    check(len(assets) == 6, "all six original stream assets must be represented")
    for digest in assets.values():
        check(re.fullmatch(r"[0-9a-f]{40}", digest), "invalid asset Git blob hash")

    if source_archive is not None:
        source_archive = Path(source_archive)
        check(hashlib.sha256(source_archive.read_bytes()).hexdigest() == archive["sha256"], "archive does not match documented build")
        with zipfile.ZipFile(source_archive) as bundle:
            for name, digest in file_hashes.items():
                data = bundle.read(archive["root"] + name)
                check(hashlib.sha256(data).hexdigest() == digest, f"source drift: {name}")
            for name, digest in assets.items():
                data = bundle.read(archive["root"] + "stream/" + name)
                prefix = f"blob {len(data)}\0".encode("ascii")
                check(hashlib.sha1(prefix + data).hexdigest() == digest, f"asset drift: {name}")
        print("rental review archive provenance: OK")
    print(f"rental documentation contract: OK ({len(PAGES)} pages; documentation only)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-archive", type=Path, help="optional exact private review ZIP; never uploaded by this test")
    validate(parser.parse_args().source_archive)
