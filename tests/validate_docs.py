from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]

required = [
    "README.md",
    "SUMMARY.md",
    "core/universal-architecture.md",
    "core/m4i_registry.md",
    "core/m4i_admin.md",
    "core/m4i_core/introduction.md",
    "core/m4i_core/architecture.md",
    "core/m4i_core/installation.md",
    "core/m4i_core/production-rollout.md",
    "core/m4i_core/changelog.md",
    "core/m4i_bridge/installation.md",
    "core/m4i_bridge/exports.md",
]

for relative in required:
    path = ROOT / relative
    assert path.is_file(), f"missing documentation file: {relative}"

summary = (ROOT / "SUMMARY.md").read_text(encoding="utf-8")
assert "core/m4i_registry.md" in summary
assert "core/m4i_admin.md" in summary

universal = (ROOT / "core/universal-architecture.md").read_text(encoding="utf-8")
registry = (ROOT / "core/m4i_registry.md").read_text(encoding="utf-8")
admin = (ROOT / "core/m4i_admin.md").read_text(encoding="utf-8")
core_intro = (ROOT / "core/m4i_core/introduction.md").read_text(encoding="utf-8")
core_arch = (ROOT / "core/m4i_core/architecture.md").read_text(encoding="utf-8")
core_install = (ROOT / "core/m4i_core/installation.md").read_text(encoding="utf-8")
rollout = (ROOT / "core/m4i_core/production-rollout.md").read_text(encoding="utf-8")
bridge_install = (ROOT / "core/m4i_bridge/installation.md").read_text(encoding="utf-8")
bridge_exports = (ROOT / "core/m4i_bridge/exports.md").read_text(encoding="utf-8")

for text, label in (
    (universal, "universal architecture"),
    (core_intro, "core introduction"),
    (core_arch, "core architecture"),
    (core_install, "core installation"),
    (rollout, "production rollout"),
    (bridge_install, "bridge installation"),
):
    assert "m4i_registry" in text, f"{label} must document registry-backed native mode"

for text, label in ((core_intro, "core introduction"), (core_arch, "core architecture")):
    assert "0.3.0-alpha.1" in text, f"{label} must track Core 0.3"

assert "0.2.0-alpha.1" in registry
assert "0.2.0-alpha.1" in admin
assert "group_namespace" in registry
assert "uq_m4i_registry_group_namespace" in registry
assert "not dropped" in registry.lower()
assert "not shipped yet" in registry.lower(), "binary asset upload must not be documented as shipped"
assert "not shipped yet" in admin.lower(), "admin asset upload must remain labeled unshipped"

expected_start_order = ["ensure oxmysql", "ensure m4i_registry", "ensure m4i_core", "ensure m4i_bridge"]
for text, label in ((universal, "universal"), (core_install, "core install"), (bridge_install, "bridge install"), (rollout, "rollout")):
    positions = [text.find(token) for token in expected_start_order]
    assert all(pos >= 0 for pos in positions), f"{label} is missing canonical startup resources"
    assert positions == sorted(positions), f"{label} has incorrect native startup order"

for stale in (
    "default framework selection remains `qbox`",
    "currently selects `qbox` as the framework provider by default",
    "The current `m4i_bridge` default framework selection remains `qbox`",
):
    for path in ROOT.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        assert stale not in text, f"stale Qbox-default statement found in {path.relative_to(ROOT)}"

for export_name in (
    "GetDefinitionRegistryState",
    "GetDefinition",
    "ResolveDefinition",
    "ResolveDefinitionKey",
    "ListDefinitions",
    "GetItemDefinition",
    "GetJobDefinition",
    "GetGangDefinition",
    "GetGroupDefinition",
    "GetVehicleDefinition",
    "GetWeaponDefinition",
    "GetLocationDefinition",
):
    assert export_name in bridge_exports, f"bridge definition export missing from docs: {export_name}"

# Lightweight relative Markdown link validation for local links. Skip anchors,
# absolute URLs, mailto links and generated GitBook schemes.
link_re = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
for path in ROOT.rglob("*.md"):
    text = path.read_text(encoding="utf-8")
    for target in link_re.findall(text):
        target = target.strip()
        if not target or target.startswith(("#", "http://", "https://", "mailto:")):
            continue
        target = target.split("#", 1)[0]
        if not target:
            continue
        resolved = (path.parent / target).resolve()
        try:
            resolved.relative_to(ROOT.resolve())
        except ValueError:
            raise AssertionError(f"link escapes docs root: {path.relative_to(ROOT)} -> {target}")
        assert resolved.exists(), f"broken local link: {path.relative_to(ROOT)} -> {target}"

print("documentation contract: OK")
