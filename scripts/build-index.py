#!/usr/bin/env python3
"""
Build script to generate icons.json from the multi-version public/icons directory tree.

Directory structure: public/icons/{version}/{dll}/*.ico

Usage:
    python scripts/build-index.py
    python scripts/build-index.py --version win11
"""

import argparse
import json
from collections import OrderedDict
from pathlib import Path
from typing import Any, Dict, List

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False

VERSION_LABELS = OrderedDict([
    ("win31", "Windows 3.1"),
    ("win95", "Windows 95"),
    ("win98", "Windows 98"),
    ("winxp", "Windows XP"),
    ("winvista", "Windows Vista"),
    ("win7", "Windows 7"),
    ("win8", "Windows 8"),
    ("win10", "Windows 10"),
    ("win11", "Windows 11"),
])

DLL_PATHS = {
    "imageres": {"file": "imageres.dll", "path": "%SystemRoot%\\System32\\imageres.dll"},
    "shell32": {"file": "shell32.dll", "path": "%SystemRoot%\\System32\\shell32.dll"},
    "pifmgr": {"file": "pifmgr.dll", "path": "%SystemRoot%\\System32\\pifmgr.dll"},
    "explorer": {"file": "explorer.exe", "path": "%SystemRoot%\\explorer.exe"},
    "accessibilitycpl": {"file": "accessibilitycpl.dll", "path": "%SystemRoot%\\System32\\accessibilitycpl.dll"},
    "ddores": {"file": "ddores.dll", "path": "%SystemRoot%\\System32\\ddores.dll"},
    "moricons": {"file": "moricons.dll", "path": "%SystemRoot%\\System32\\moricons.dll"},
    "mmcndmgr": {"file": "mmcndmgr.dll", "path": "%SystemRoot%\\System32\\mmcndmgr.dll"},
    "mmres": {"file": "mmres.dll", "path": "%SystemRoot%\\System32\\mmres.dll"},
    "netcenter": {"file": "netcenter.dll", "path": "%SystemRoot%\\System32\\netcenter.dll"},
    "netshell": {"file": "netshell.dll", "path": "%SystemRoot%\\System32\\netshell.dll"},
    "networkexplorer": {"file": "networkexplorer.dll", "path": "%SystemRoot%\\System32\\networkexplorer.dll"},
    "pnidui": {"file": "pnidui.dll", "path": "%SystemRoot%\\System32\\pnidui.dll"},
    "sensorscpl": {"file": "sensorscpl.dll", "path": "%SystemRoot%\\System32\\sensorscpl.dll"},
    "setupapi": {"file": "setupapi.dll", "path": "%SystemRoot%\\System32\\setupapi.dll"},
    "wmploc": {"file": "wmploc.dll", "path": "%SystemRoot%\\System32\\wmploc.dll"},
    "wpdshext": {"file": "wpdshext.dll", "path": "%SystemRoot%\\System32\\wpdshext.dll"},
    "compstui": {"file": "compstui.dll", "path": "%SystemRoot%\\System32\\compstui.dll"},
    "ieframe": {"file": "ieframe.dll", "path": "%SystemRoot%\\System32\\ieframe.dll"},
    "dmdskres": {"file": "dmdskres.dll", "path": "%SystemRoot%\\System32\\dmdskres.dll"},
    "dsuiext": {"file": "dsuiext.dll", "path": "%SystemRoot%\\System32\\dsuiext.dll"},
    "mstscax": {"file": "mstscax.dll", "path": "%SystemRoot%\\System32\\mstscax.dll"},
    "wiashext": {"file": "wiashext.dll", "path": "%SystemRoot%\\System32\\wiashext.dll"},
    "comres": {"file": "comres.dll", "path": "%SystemRoot%\\System32\\comres.dll"},
    "mstsc": {"file": "mstsc.exe", "path": "%SystemRoot%\\System32\\mstsc.exe"},
    "actioncentercpl": {"file": "actioncentercpl.dll", "path": "%SystemRoot%\\System32\\actioncentercpl.dll"},
    "aclui": {"file": "aclui.dll", "path": "%SystemRoot%\\System32\\aclui.dll"},
    "autoplay": {"file": "autoplay.dll", "path": "%SystemRoot%\\System32\\autoplay.dll"},
    "comctl32": {"file": "comctl32.dll", "path": "%SystemRoot%\\System32\\comctl32.dll"},
    "xwizards": {"file": "xwizards.dll", "path": "%SystemRoot%\\System32\\xwizards.dll"},
    "ncpa": {"file": "ncpa.cpl", "path": "%SystemRoot%\\System32\\ncpa.cpl"},
    "url": {"file": "url.dll", "path": "%SystemRoot%\\System32\\url.dll"},
}

# Pre-compute version sort order for fast lookups
_VERSION_ORDER = {v: i for i, v in enumerate(VERSION_LABELS)}


def load_overrides(overrides_file: Path) -> Dict[str, Any]:
    """Load tag/metadata overrides from tags-overrides.yaml if it exists."""
    if not overrides_file.exists():
        return {}
    if not HAS_YAML:
        print("Warning: PyYAML not installed. Skipping tags-overrides merging.")
        return {}
    with open(overrides_file, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def scan_icons(icons_dir: Path, version_filter: str | None = None) -> List[Dict[str, Any]]:
    """Scan public/icons/{version}/{dll}/*.ico and build icon entries."""
    icons: List[Dict[str, Any]] = []

    if not icons_dir.exists():
        print(f"Warning: Icons directory not found at {icons_dir}")
        return icons

    for version_dir in sorted(icons_dir.iterdir()):
        if not version_dir.is_dir():
            continue

        version = version_dir.name

        if version_filter and version != version_filter:
            continue

        version_label = VERSION_LABELS.get(version, version)

        for dll_dir in sorted(version_dir.iterdir()):
            if not dll_dir.is_dir():
                continue

            dll_name = dll_dir.name
            dll_info = DLL_PATHS.get(dll_name)
            dll_file = dll_info["file"] if dll_info else f"{dll_name}.dll"
            dll_path = dll_info["path"] if dll_info else ""

            for ico_file in sorted(dll_dir.glob("*.ico")):
                resource_id_str = ico_file.stem
                try:
                    resource_id = int(resource_id_str)
                except ValueError:
                    resource_id = resource_id_str

                icons.append({
                    "id": f"{version}-{dll_name}-{resource_id_str}",
                    "name": f"{dll_name} #{resource_id_str}",
                    "dll": dll_file,
                    "dllPath": dll_path,
                    "version": version,
                    "versionLabel": version_label,
                    "resourceId": resource_id,
                    "file": f"/icons/{version}/{dll_name}/{ico_file.name}",
                    "tags": [],
                    "description": "",
                })

    return icons


def sort_icons(icons: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Sort by version order, then dll name, then numeric resourceId."""
    return sorted(icons, key=lambda x: (
        _VERSION_ORDER.get(x["version"], len(_VERSION_ORDER)),
        x["dll"],
        x["resourceId"] if isinstance(x["resourceId"], int) else float("inf"),
    ))


def apply_overrides(icons: List[Dict[str, Any]], overrides: Dict[str, Any]) -> None:
    """Merge fields from tags-overrides.yaml into matching icons (in-place)."""
    for icon in icons:
        override = overrides.get(icon["id"])
        if not override:
            continue
        for key in ("name", "tags", "description"):
            if key in override:
                icon[key] = override[key]


def print_summary(icons: List[Dict[str, Any]]) -> None:
    """Print totals per version and per DLL within each version."""
    print(f"\n  Total icons: {len(icons)}")

    # Group by version then dll
    by_version: Dict[str, Dict[str, int]] = {}
    for icon in icons:
        v = icon["version"]
        d = icon["dll"]
        by_version.setdefault(v, {})
        by_version[v][d] = by_version[v].get(d, 0) + 1

    for version in VERSION_LABELS:
        if version not in by_version:
            continue
        dll_counts = by_version[version]
        total = sum(dll_counts.values())
        label = VERSION_LABELS[version]
        print(f"\n  {label} ({version}): {total} icons")
        for dll_name, count in sorted(dll_counts.items()):
            print(f"    {dll_name}: {count}")

    # Print any versions not in VERSION_LABELS at the end
    for version, dll_counts in sorted(by_version.items()):
        if version in VERSION_LABELS:
            continue
        total = sum(dll_counts.values())
        print(f"\n  {version}: {total} icons")
        for dll_name, count in sorted(dll_counts.items()):
            print(f"    {dll_name}: {count}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate icons.json from the multi-version public/icons directory tree"
    )
    parser.add_argument(
        "--version",
        default=None,
        help="Rebuild only this version (e.g. win11). "
             "Entries for other versions are preserved from the existing icons.json.",
    )
    args = parser.parse_args()

    project_root = Path(__file__).parent.parent
    icons_dir = project_root / "public" / "icons"
    output_dir = project_root / "data"
    output_file = output_dir / "icons.json"
    overrides_file = project_root / "data" / "tags-overrides.yaml"

    output_dir.mkdir(parents=True, exist_ok=True)

    # Scan icons (optionally filtered to one version)
    print(f"Scanning icons from {icons_dir}...")
    scanned = scan_icons(icons_dir, version_filter=args.version)

    # When rebuilding a single version, merge with existing entries for other versions
    if args.version and output_file.exists():
        with open(output_file, "r", encoding="utf-8") as f:
            existing: List[Dict[str, Any]] = json.load(f)
        kept = [e for e in existing if e.get("version") != args.version]
        scanned = kept + scanned

    # Sort
    icons = sort_icons(scanned)

    # Apply overrides
    overrides = load_overrides(overrides_file)
    if overrides:
        print(f"Applying overrides from {overrides_file}...")
        apply_overrides(icons, overrides)

    # Write
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(icons, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print(f"\n✓ Generated {output_file}")
    print("\nSummary:")
    print_summary(icons)


if __name__ == "__main__":
    main()
