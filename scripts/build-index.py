#!/usr/bin/env python3
"""
Build script to generate icons.json from the public/icons directory tree.

This script scans the public/icons/ directory for icon files (subdirectories are DLL sources),
generates metadata for each icon, and outputs to data/icons.json.

Usage:
    python scripts/build-index.py              # Generate icons.json
    python scripts/build-index.py --tags       # Merge tags from tags.yaml if it exists
"""

import argparse
import json
import os
from pathlib import Path
from typing import Dict, List, Any

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False

# DLL path mapping
DLL_PATHS = {
    "imageres": {"file": "imageres.dll", "path": "%SystemRoot%\\System32\\imageres.dll", "description": "Miscellaneous icons (folders, devices, actions)"},
    "shell32": {"file": "shell32.dll", "path": "%SystemRoot%\\System32\\shell32.dll", "description": "Shell/explorer icons"},
    "pifmgr": {"file": "pifmgr.dll", "path": "%SystemRoot%\\System32\\pifmgr.dll", "description": "Legacy Win95/98 icons"},
    "explorer": {"file": "explorer.exe", "path": "%SystemRoot%\\explorer.exe", "description": "Explorer icons"},
    "accessibilitycpl": {"file": "accessibilitycpl.dll", "path": "%SystemRoot%\\System32\\accessibilitycpl.dll", "description": "Accessibility icons"},
    "ddores": {"file": "ddores.dll", "path": "%SystemRoot%\\System32\\ddores.dll", "description": "Hardware devices and resources"},
    "moricons": {"file": "moricons.dll", "path": "%SystemRoot%\\System32\\moricons.dll", "description": "Legacy pre-2000 icons"},
    "mmcndmgr": {"file": "mmcndmgr.dll", "path": "%SystemRoot%\\System32\\mmcndmgr.dll", "description": "Computer management icons"},
    "mmres": {"file": "mmres.dll", "path": "%SystemRoot%\\System32\\mmres.dll", "description": "Audio hardware icons"},
    "netcenter": {"file": "netcenter.dll", "path": "%SystemRoot%\\System32\\netcenter.dll", "description": "Networking icons"},
    "netshell": {"file": "netshell.dll", "path": "%SystemRoot%\\System32\\netshell.dll", "description": "Networking, Bluetooth, wireless icons"},
    "networkexplorer": {"file": "networkexplorer.dll", "path": "%SystemRoot%\\System32\\networkexplorer.dll", "description": "Network peripheral icons"},
    "pnidui": {"file": "pnidui.dll", "path": "%SystemRoot%\\System32\\pnidui.dll", "description": "Network status icons"},
    "sensorscpl": {"file": "sensorscpl.dll", "path": "%SystemRoot%\\System32\\sensorscpl.dll", "description": "Sensor icons"},
    "setupapi": {"file": "setupapi.dll", "path": "%SystemRoot%\\System32\\setupapi.dll", "description": "Hardware setup wizard icons"},
    "wmploc": {"file": "wmploc.dll", "path": "%SystemRoot%\\System32\\wmploc.dll", "description": "Multimedia icons"},
    "wpdshext": {"file": "wpdshext.dll", "path": "%SystemRoot%\\System32\\wpdshext.dll", "description": "Portable device icons"},
    "compstui": {"file": "compstui.dll", "path": "%SystemRoot%\\System32\\compstui.dll", "description": "Printing icons (legacy)"},
    "ieframe": {"file": "ieframe.dll", "path": "%SystemRoot%\\System32\\ieframe.dll", "description": "Internet Explorer icons"},
    "dmdskres": {"file": "dmdskres.dll", "path": "%SystemRoot%\\System32\\dmdskres.dll", "description": "Disk management icons"},
    "dsuiext": {"file": "dsuiext.dll", "path": "%SystemRoot%\\System32\\dsuiext.dll", "description": "Network locations/services icons"},
    "mstscax": {"file": "mstscax.dll", "path": "%SystemRoot%\\System32\\mstscax.dll", "description": "Remote desktop icons"},
    "wiashext": {"file": "wiashext.dll", "path": "%SystemRoot%\\System32\\wiashext.dll", "description": "Imaging hardware icons"},
    "comres": {"file": "comres.dll", "path": "%SystemRoot%\\System32\\comres.dll", "description": "General status icons"},
    "mstsc": {"file": "mstsc.exe", "path": "%SystemRoot%\\System32\\mstsc.exe", "description": "System monitoring/config icons"},
    "actioncentercpl": {"file": "actioncentercpl.dll", "path": "%SystemRoot%\\System32\\actioncentercpl.dll", "description": "Action center icons"},
    "aclui": {"file": "aclui.dll", "path": "%SystemRoot%\\System32\\aclui.dll", "description": "Permission check/cross icons"},
    "autoplay": {"file": "autoplay.dll", "path": "%SystemRoot%\\System32\\autoplay.dll", "description": "Autoplay icon"},
    "comctl32": {"file": "comctl32.dll", "path": "%SystemRoot%\\System32\\comctl32.dll", "description": "Legacy info/warning/error icons"},
    "xwizards": {"file": "xwizards.dll", "path": "%SystemRoot%\\System32\\xwizards.dll", "description": "Software install icon"},
    "ncpa": {"file": "ncpa.cpl", "path": "%SystemRoot%\\System32\\ncpa.cpl", "description": "Network folder icon"},
    "url": {"file": "url.dll", "path": "%SystemRoot%\\System32\\url.dll", "description": "Network related icons"},
}


def load_tags(tags_file: Path) -> Dict[str, Any]:
    """Load tags from tags.yaml if it exists."""
    if not tags_file.exists():
        return {}
    
    if not HAS_YAML:
        print("Warning: PyYAML not installed. Skipping tags merging.")
        return {}
    
    with open(tags_file, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f) or {}


def scan_icons(icons_dir: Path) -> List[Dict[str, Any]]:
    """Scan the icons directory and generate icon metadata."""
    icons = []
    
    if not icons_dir.exists():
        print(f"Warning: Icons directory not found at {icons_dir}")
        return icons
    
    # Iterate through subdirectories (each is a DLL source)
    for dll_dir in sorted(icons_dir.iterdir()):
        if not dll_dir.is_dir():
            continue
        
        dll_name = dll_dir.name
        
        # Skip if DLL not in mapping
        if dll_name not in DLL_PATHS:
            continue
        
        dll_info = DLL_PATHS[dll_name]
        
        # Find all .ico files in this directory
        ico_files = sorted(dll_dir.glob('*.ico'))
        
        for ico_file in ico_files:
            # Resource ID is filename without extension
            resource_id_str = ico_file.stem
            
            # Try to convert to integer for sorting
            try:
                resource_id = int(resource_id_str)
            except ValueError:
                resource_id = resource_id_str
            
            icon_entry = {
                "id": f"{dll_name}-{resource_id_str}",
                "name": f"{dll_name} #{resource_id_str}",
                "dll": dll_info["file"],
                "dllPath": dll_info["path"],
                "resourceId": resource_id,
                "file": f"/icons/{dll_name}/{ico_file.name}",
                "tags": [],
                "description": ""
            }
            
            icons.append(icon_entry)
    
    return icons


def sort_icons(icons: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Sort icons by dll name, then by resourceId (numeric)."""
    return sorted(icons, key=lambda x: (x["dll"], 
                                         x["resourceId"] if isinstance(x["resourceId"], int) else float('inf')))


def merge_tags(icons: List[Dict[str, Any]], tags: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Merge tags from tags.yaml into icons."""
    for icon in icons:
        icon_id = icon["id"]
        if icon_id in tags:
            tag_data = tags[icon_id]
            if "name" in tag_data:
                icon["name"] = tag_data["name"]
            if "tags" in tag_data:
                icon["tags"] = tag_data["tags"]
            if "description" in tag_data:
                icon["description"] = tag_data["description"]
    
    return icons


def main():
    parser = argparse.ArgumentParser(
        description="Generate icons.json from public/icons directory tree"
    )
    parser.add_argument(
        "--tags",
        action="store_true",
        help="Merge tags from tags.yaml if it exists"
    )
    
    args = parser.parse_args()
    
    # Determine paths relative to project root
    project_root = Path(__file__).parent.parent
    icons_dir = project_root / "public" / "icons"
    output_dir = project_root / "data"
    output_file = output_dir / "icons.json"
    tags_file = project_root / "tags.yaml"
    
    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Scan icons
    print(f"Scanning icons from {icons_dir}...")
    icons = scan_icons(icons_dir)
    
    # Sort icons
    icons = sort_icons(icons)
    
    # Merge tags if requested
    if args.tags:
        print(f"Loading tags from {tags_file}...")
        tags = load_tags(tags_file)
        icons = merge_tags(icons, tags)
    
    # Write to JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(icons, f, indent=2, ensure_ascii=False)
    
    # Print summary
    print(f"\n✓ Generated {output_file}")
    print(f"\nSummary:")
    print(f"  Total icons: {len(icons)}")
    
    # Count icons per DLL
    dll_counts = {}
    for icon in icons:
        dll = icon["dll"]
        dll_counts[dll] = dll_counts.get(dll, 0) + 1
    
    for dll, count in sorted(dll_counts.items()):
        print(f"  {dll}: {count} icons")


if __name__ == "__main__":
    main()
