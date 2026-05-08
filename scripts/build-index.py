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
    # Legacy (Win 3.1+)
    "progman": {"file": "progman.exe", "path": "%SystemRoot%\\progman.exe", "desc": "Program Manager — general category icons"},
    "moricons": {"file": "moricons.dll", "path": "%SystemRoot%\\System32\\moricons.dll", "desc": "Icons for popular 3rd-party DOS apps"},
    # Shell (Win 95+)
    "shell32": {"file": "shell32.dll", "path": "%SystemRoot%\\System32\\shell32.dll", "desc": "Core shell icons — folders, drives, actions"},
    "explorer": {"file": "explorer.exe", "path": "%SystemRoot%\\explorer.exe", "desc": "Windows Explorer-specific icons"},
    "pifmgr": {"file": "pifmgr.dll", "path": "%SystemRoot%\\System32\\pifmgr.dll", "desc": "DOS/PIF shortcut icons"},
    "mshtml": {"file": "mshtml.dll", "path": "%SystemRoot%\\System32\\mshtml.dll", "desc": "Internet Explorer HTML rendering icons"},
    # Win XP+
    "ieframe": {"file": "ieframe.dll", "path": "%SystemRoot%\\System32\\ieframe.dll", "desc": "Internet Explorer frame & toolbar icons"},
    "xpsp2res": {"file": "xpsp2res.dll", "path": "%SystemRoot%\\System32\\xpsp2res.dll", "desc": "Security Center & SP2 feature icons"},
    "compstui": {"file": "compstui.dll", "path": "%SystemRoot%\\System32\\compstui.dll", "desc": "Printing & color composition UI icons"},
    "wmploc": {"file": "wmploc.dll", "path": "%SystemRoot%\\System32\\wmploc.dll", "desc": "Windows Media Player icons"},
    "netshell": {"file": "netshell.dll", "path": "%SystemRoot%\\System32\\netshell.dll", "desc": "Network connection & adapter icons"},
    "mmcndmgr": {"file": "mmcndmgr.dll", "path": "%SystemRoot%\\System32\\mmcndmgr.dll", "desc": "Management Console snap-in icons"},
    # Vista+
    "imageres": {"file": "imageres.dll", "path": "%SystemRoot%\\System32\\imageres.dll", "desc": "Primary icon store — devices, actions, status"},
    "ddores": {"file": "ddores.dll", "path": "%SystemRoot%\\System32\\ddores.dll", "desc": "Devices & Printers icons"},
    "setupapi": {"file": "setupapi.dll", "path": "%SystemRoot%\\System32\\setupapi.dll", "desc": "Device driver & setup icons"},
    # Win 7+
    "accessibilitycpl": {"file": "accessibilitycpl.dll", "path": "%SystemRoot%\\System32\\accessibilitycpl.dll", "desc": "Accessibility / Ease of Access icons"},
    # Win 8+
    "twinui": {"file": "twinui.dll", "path": "%SystemRoot%\\System32\\twinui.dll", "desc": "Modern UI / Metro app icons"},
    # Win 10+
    "pnidui": {"file": "pnidui.dll", "path": "%SystemRoot%\\System32\\pnidui.dll", "desc": "Network tray & status animations"},
    "vault": {"file": "Vault.dll", "path": "%SystemRoot%\\System32\\Vault.dll", "desc": "Credential Manager / vault icons"},
    "wdc": {"file": "wdc.dll", "path": "%SystemRoot%\\System32\\wdc.dll", "desc": "Windows Defender Center icons"},
    "connect": {"file": "connect.dll", "path": "%SystemRoot%\\System32\\connect.dll", "desc": "Connect (cast/project) icons"},
    "themecpl": {"file": "themecpl.dll", "path": "%SystemRoot%\\System32\\themecpl.dll", "desc": "Theme & personalization icons"},
    "user32": {"file": "user32.dll", "path": "%SystemRoot%\\System32\\user32.dll", "desc": "Core USER subsystem icons"},
    # Win 11
    "twinui.pcshell": {"file": "twinui.pcshell.dll", "path": "%SystemRoot%\\System32\\twinui.pcshell.dll", "desc": "Start menu & taskbar icons"},
    # Other Win11 DLLs
    "aclui": {"file": "aclui.dll", "path": "%SystemRoot%\\System32\\aclui.dll", "desc": "Access control list editor icons"},
    "autoplay": {"file": "autoplay.dll", "path": "%SystemRoot%\\System32\\autoplay.dll", "desc": "AutoPlay handler icons"},
    "comctl32": {"file": "comctl32.dll", "path": "%SystemRoot%\\System32\\comctl32.dll", "desc": "Common controls library icons"},
    "comres": {"file": "comres.dll", "path": "%SystemRoot%\\System32\\comres.dll", "desc": "COM+ resource icons"},
    "dmdskres": {"file": "dmdskres.dll", "path": "%SystemRoot%\\System32\\dmdskres.dll", "desc": "Disk Management snap-in icons"},
    "dsuiext": {"file": "dsuiext.dll", "path": "%SystemRoot%\\System32\\dsuiext.dll", "desc": "Active Directory UI extension icons"},
    "mmres": {"file": "mmres.dll", "path": "%SystemRoot%\\System32\\mmres.dll", "desc": "Multimedia resource icons"},
    "mstsc": {"file": "mstsc.exe", "path": "%SystemRoot%\\System32\\mstsc.exe", "desc": "Remote Desktop Connection icons"},
    "mstscax": {"file": "mstscax.dll", "path": "%SystemRoot%\\System32\\mstscax.dll", "desc": "Remote Desktop ActiveX control icons"},
    "ncpa": {"file": "ncpa.cpl", "path": "%SystemRoot%\\System32\\ncpa.cpl", "desc": "Network Connections control panel icons"},
    "netcenter": {"file": "netcenter.dll", "path": "%SystemRoot%\\System32\\netcenter.dll", "desc": "Network and Sharing Center icons"},
    "networkexplorer": {"file": "networkexplorer.dll", "path": "%SystemRoot%\\System32\\networkexplorer.dll", "desc": "Network Explorer icons"},
    "sensorscpl": {"file": "sensorscpl.dll", "path": "%SystemRoot%\\System32\\sensorscpl.dll", "desc": "Sensors control panel icons"},
    "url": {"file": "url.dll", "path": "%SystemRoot%\\System32\\url.dll", "desc": "Internet shortcut icons"},
    "wiashext": {"file": "wiashext.dll", "path": "%SystemRoot%\\System32\\wiashext.dll", "desc": "Windows Image Acquisition shell extension icons"},
    "wpdshext": {"file": "wpdshext.dll", "path": "%SystemRoot%\\System32\\wpdshext.dll", "desc": "Portable Devices shell extension icons"},
    "xwizards": {"file": "xwizards.dll", "path": "%SystemRoot%\\System32\\xwizards.dll", "desc": "Extensible Wizards framework icons"},
    "actioncentercpl": {"file": "actioncentercpl.dll", "path": "%SystemRoot%\\System32\\actioncentercpl.dll", "desc": "Action Center control panel icons"},
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
            dll_desc = dll_info.get("desc", "") if dll_info else ""

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
                    "dllDescription": dll_desc,
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
