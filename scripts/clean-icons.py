#!/usr/bin/env python3
"""Remove invalid ICO files from public/icons/."""

import struct
import sys
from pathlib import Path


def is_valid_ico(path: Path) -> bool:
    """Validate ICO file structure and check it contains real image data."""
    try:
        data = path.read_bytes()
    except Exception:
        return False

    # Minimum: 6-byte header + 16-byte entry = 22 bytes
    if len(data) < 22:
        return False

    reserved, ico_type, count = struct.unpack_from("<HHH", data, 0)

    # Reserved must be 0, type must be 1 (icon) or 2 (cursor)
    if reserved != 0 or ico_type not in (1, 2) or count == 0:
        return False

    dir_end = 6 + count * 16

    # Check at least one entry has real image data via directory offsets
    for i in range(min(count, 100)):
        offset = 6 + i * 16
        if offset + 16 > len(data):
            return False

        img_size = struct.unpack_from("<I", data, offset + 8)[0]
        img_offset = struct.unpack_from("<I", data, offset + 12)[0]

        if img_size > 0 and img_offset + img_size <= len(data) and img_size >= 12:
            return True

    # Fallback for old NE-format icons (wrestool): directory entries may have
    # zeroed size/offset fields, but real bitmap data exists after the directory.
    # Accept if there's meaningful data beyond the header+directory.
    if len(data) > dir_end + 12:
        return True

    return False


def main():
    icons_dir = Path(__file__).resolve().parent.parent / "public" / "icons"

    if not icons_dir.exists():
        print(f"Icons directory not found: {icons_dir}")
        sys.exit(1)

    total = 0
    removed = 0
    kept = 0
    stats: dict[str, dict[str, int]] = {}

    for ico in sorted(icons_dir.rglob("*.ico")):
        total += 1
        rel = ico.relative_to(icons_dir)
        parts = rel.parts  # e.g. ('win8', 'imageres', '123.ico')
        version = parts[0] if len(parts) >= 1 else "unknown"
        dll = parts[1] if len(parts) >= 2 else "unknown"
        key = f"{version}/{dll}"

        if key not in stats:
            stats[key] = {"kept": 0, "removed": 0}

        if is_valid_ico(ico):
            kept += 1
            stats[key]["kept"] += 1
        else:
            removed += 1
            stats[key]["removed"] += 1
            ico.unlink()

    print(f"\nResults:")
    print(f"  Total scanned: {total}")
    print(f"  Kept (valid):  {kept}")
    print(f"  Removed:       {removed}")
    print()

    # Show per-DLL stats where removals happened
    print(f"{'Source':<40} {'Kept':>6} {'Removed':>8}")
    print("─" * 56)
    for key in sorted(stats):
        s = stats[key]
        if s["removed"] > 0:
            print(f"  {key:<38} {s['kept']:>6} {s['removed']:>8}")

    print()
    print(f"Clean icon count: {kept}")


if __name__ == "__main__":
    main()
