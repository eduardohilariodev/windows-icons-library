"""
Extract icons from DLL/EXE/CPL/MUN files into public/icons/{version}/{dll_name}/.

Usage:
    python scripts/extract-icons.py --version win11 --dll-dir dlls/win11/

Tries icoextract (PE format) first, then falls back to wrestool (NE format)
for legacy binaries like those from Windows 3.1/95/98.
"""

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SUPPORTED_EXTENSIONS = {".dll", ".exe", ".cpl", ".mun"}


def find_source_files(dll_dir: Path) -> list[Path]:
    """Return all extractable files in the given directory."""
    files = []
    for entry in sorted(dll_dir.iterdir()):
        if entry.is_file() and entry.suffix.lower() in SUPPORTED_EXTENSIONS:
            files.append(entry)
    return files


# ── icoextract backend ─────────────────────────────────────────────────────

def icoextract_list(source: Path) -> list[int]:
    """Run icolist and return icon indices."""
    try:
        result = subprocess.run(
            ["icolist", str(source)],
            capture_output=True, text=True, timeout=30,
        )
    except FileNotFoundError:
        return []
    if result.returncode != 0:
        return []

    indices = []
    for line in result.stdout.splitlines():
        m = re.match(r"^\s*Index:\s*(\d+)", line)
        if m:
            indices.append(int(m.group(1)))
    return indices


def icoextract_extract(source: Path, out_dir: Path, indices: list[int]) -> int:
    """Extract icons via icoextract. Returns count of successfully written files."""
    count = 0
    for idx in indices:
        out_file = out_dir / f"{idx}.ico"
        try:
            subprocess.run(
                ["icoextract", str(source), str(out_file), "-n", str(idx)],
                capture_output=True, text=True, timeout=15,
            )
            if out_file.is_file() and out_file.stat().st_size > 0:
                count += 1
            else:
                out_file.unlink(missing_ok=True)
        except Exception:
            out_file.unlink(missing_ok=True)
    return count


# ── wrestool (icoutils) backend ────────────────────────────────────────────

def wrestool_extract(source: Path, out_dir: Path) -> int:
    """Extract icons via wrestool -x -t14 (icon resources). Returns count."""
    try:
        result = subprocess.run(
            ["wrestool", "-x", "-t14", str(source)],
            capture_output=True, timeout=60,
        )
    except FileNotFoundError:
        print("    wrestool not found — install icoutils to handle NE-format DLLs")
        return 0
    if result.returncode != 0 or not result.stdout:
        return 0

    # wrestool dumps concatenated ICO data to stdout; split on ICO magic bytes.
    # Each ICO file starts with bytes 00 00 01 00.
    raw = result.stdout
    ico_magic = b"\x00\x00\x01\x00"
    parts: list[bytes] = []
    start = raw.find(ico_magic)
    while start != -1:
        next_start = raw.find(ico_magic, start + 4)
        if next_start == -1:
            parts.append(raw[start:])
        else:
            parts.append(raw[start:next_start])
        start = next_start

    count = 0
    for i, data in enumerate(parts):
        out_file = out_dir / f"{i}.ico"
        out_file.write_bytes(data)
        if out_file.stat().st_size > 0:
            count += 1
        else:
            out_file.unlink(missing_ok=True)
    return count


# ── main extraction logic ──────────────────────────────────────────────────

def extract_icons(source: Path, out_dir: Path) -> int:
    """Extract icons from a single file. Returns the number of icons extracted."""
    out_dir.mkdir(parents=True, exist_ok=True)

    # Try icoextract first (works with PE-format binaries)
    indices = icoextract_list(source)
    if indices:
        count = icoextract_extract(source, out_dir, indices)
        if count > 0:
            return count

    # Fallback to wrestool for NE-format or other legacy binaries
    return wrestool_extract(source, out_dir)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract icons from DLL/EXE/CPL/MUN files."
    )
    parser.add_argument(
        "--version", required=True,
        help="Version label for output directory (e.g. win98, win11)",
    )
    parser.add_argument(
        "--dll-dir", required=True, type=Path,
        help="Directory containing DLL/EXE/CPL/MUN files to extract from",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    version: str = args.version
    dll_dir: Path = Path(args.dll_dir).resolve()

    if not dll_dir.is_dir():
        print(f"Error: --dll-dir '{dll_dir}' is not a directory.", file=sys.stderr)
        sys.exit(1)

    icons_base = BASE_DIR / "public" / "icons" / version
    sources = find_source_files(dll_dir)

    if not sources:
        print(f"No supported files found in {dll_dir}")
        sys.exit(1)

    print(f"Version:    {version}")
    print(f"DLL dir:    {dll_dir}")
    print(f"Output dir: {icons_base}")
    print(f"Files:      {len(sources)}")

    summary: list[tuple[str, int]] = []

    for source in sources:
        dll_name = source.stem.lower()
        out_dir = icons_base / dll_name

        print(f"\n{'='*60}")
        print(f"  {dll_name}  ←  {source.name}")
        print(f"{'='*60}")

        try:
            count = extract_icons(source, out_dir)
        except Exception as e:
            print(f"  ✖ Error: {e}")
            count = 0

        if count > 0:
            print(f"  ✔ {count} icon(s) extracted")
        else:
            print(f"  ⚠ No icons extracted")

        summary.append((dll_name, count))

    # Print summary
    total = sum(c for _, c in summary)
    print(f"\n{'='*60}")
    print(f"  Summary for '{version}'")
    print(f"{'='*60}")
    for name, count in summary:
        status = f"{count:>4} icons" if count > 0 else "   –"
        print(f"  {name:<30} {status}")
    print(f"{'─'*60}")
    print(f"  {'Total':<30} {total:>4} icons")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
