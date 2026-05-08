"""Extract all icons from Windows system DLLs/EXEs into public/icons/<name>/ folders."""

import os
import re
import subprocess
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ICONS_DIR = os.path.join(BASE_DIR, "public", "icons")

# (display_name, source_path) — display_name is used for the output folder
SOURCES = []

# Group A — .mun files in SystemResources
GROUP_A = [
    "imageres.dll", "shell32.dll", "accessibilitycpl.dll", "ddores.dll",
    "moricons.dll", "mmcndmgr.dll", "mmres.dll", "netcenter.dll",
    "netshell.dll", "networkexplorer.dll", "sensorscpl.dll", "wmploc.dll",
    "wpdshext.dll", "compstui.dll", "ieframe.dll", "dmdskres.dll",
    "dsuiext.dll", "mstscax.dll", "wiashext.dll", "comres.dll",
    "actioncentercpl.dll", "aclui.dll", "mstsc.exe",
]
for name in GROUP_A:
    folder = os.path.splitext(name)[0]  # strip extension for folder name
    mun_file = name + ".mun"  # e.g. imageres.dll.mun
    src = os.path.join(r"C:\Windows\SystemResources", mun_file)
    SOURCES.append((folder, src))

# Group B — files in System32
GROUP_B = [
    "pifmgr.dll", "setupapi.dll", "autoplay.dll", "comctl32.dll",
    "xwizards.dll", "ncpa.cpl", "url.dll",
]
for name in GROUP_B:
    folder = os.path.splitext(name)[0]
    src = os.path.join(r"C:\Windows\System32", name)
    SOURCES.append((folder, src))

# Group C — standalone executables
SOURCES.append(("explorer", r"C:\Windows\explorer.exe"))


def get_icon_indices(source_path: str) -> list[int]:
    """Run icolist and parse icon indices from its output."""
    result = subprocess.run(
        ["icolist", source_path],
        capture_output=True, text=True, timeout=30,
    )
    if result.returncode != 0:
        return []

    # icolist output: "Index: 0    ID: 123(0x7b)    Offset: 0x..."
    indices = []
    for line in result.stdout.splitlines():
        m = re.match(r"^\s*Index:\s*(\d+)", line)
        if m:
            indices.append(int(m.group(1)))
    return indices


def extract_icons(name: str, source_path: str) -> None:
    """Extract all icons from a single source file."""
    out_dir = os.path.join(ICONS_DIR, name)
    os.makedirs(out_dir, exist_ok=True)

    print(f"\n{'='*60}")
    print(f"  {name}  ←  {source_path}")
    print(f"{'='*60}")

    if not os.path.isfile(source_path):
        print(f"  ⚠  Source file not found, skipping.")
        return

    indices = get_icon_indices(source_path)
    if not indices:
        print(f"  ⚠  No icons found (or icolist failed), skipping.")
        return

    print(f"  Found {len(indices)} icon(s). Extracting...")
    ok = 0
    fail = 0
    for idx in indices:
        out_file = os.path.join(out_dir, f"{idx}.ico")
        try:
            subprocess.run(
                ["icoextract", source_path, out_file, "-n", str(idx)],
                capture_output=True, text=True, timeout=15,
            )
            if os.path.isfile(out_file) and os.path.getsize(out_file) > 0:
                ok += 1
            else:
                fail += 1
        except Exception as e:
            fail += 1

    print(f"  ✔ {ok} extracted, {fail} failed")


def main():
    print(f"Output directory: {ICONS_DIR}")
    print(f"Total sources: {len(SOURCES)}")

    for name, src in SOURCES:
        try:
            extract_icons(name, src)
        except Exception as e:
            print(f"  ✖ Error processing {name}: {e}")

    print(f"\n{'='*60}")
    print("Done!")


if __name__ == "__main__":
    main()
