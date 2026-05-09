"use client";

import { useMemo, useState } from "react";
import Fuse from "fuse.js";
import type { IconEntry } from "@/lib/icons";
import { WINDOWS_VERSIONS } from "@/lib/versions";
import { SearchBar } from "./SearchBar";
import { IconGrid } from "./IconGrid";
import { VersionFilter } from "./VersionFilter";
import { IconDetailWindow } from "./IconDetailWindow";

interface IconBrowserProps {
  icons: IconEntry[];
}

export function IconBrowser({ icons }: IconBrowserProps) {
  const [query, setQuery] = useState("");
  const [selectedVersions, setSelectedVersions] = useState<string[]>([]);
  const [openIcon, setOpenIcon] = useState<IconEntry | null>(null);
  const [clickPosition, setClickPosition] = useState<{ x: number; y: number }>({
    x: 0,
    y: 0,
  });

  const availableVersions = useMemo(() => {
    const slugs = new Set(icons.map((i) => i.version));
    return WINDOWS_VERSIONS.filter((v) => slugs.has(v.slug));
  }, [icons]);

  const fuse = useMemo(
    () =>
      new Fuse(icons, {
        keys: [
          { name: "name", weight: 2 },
          { name: "tags", weight: 1.5 },
          { name: "description", weight: 1 },
          { name: "dll", weight: 0.5 },
          { name: "version", weight: 0.3 },
          { name: "versionLabel", weight: 0.3 },
        ],
        threshold: 0.3,
        includeScore: true,
      }),
    [icons]
  );

  const filtered = useMemo(() => {
    let result = icons;

    if (query.trim()) {
      result = fuse.search(query).map((r) => r.item);
    }

    if (selectedVersions.length > 0) {
      result = result.filter((icon) =>
        selectedVersions.includes(icon.version)
      );
    }

    return result;
  }, [query, fuse, icons, selectedVersions]);

  const handleOpen = (icon: IconEntry, event?: React.MouseEvent) => {
    setOpenIcon(icon);
    if (event) {
      setClickPosition({ x: event.clientX - 140, y: event.clientY - 100 });
    } else {
      setClickPosition({
        x: Math.round(window.innerWidth / 2 - 140),
        y: Math.round(window.innerHeight / 2 - 200),
      });
    }
  };

  return (
    <div id="desktop">
      <VersionFilter
        versions={availableVersions}
        selected={selectedVersions}
        onChange={setSelectedVersions}
      />
      <SearchBar
        query={query}
        onQueryChange={setQuery}
        resultCount={filtered.length}
        totalCount={icons.length}
      />
      <IconGrid icons={filtered} onOpenIcon={handleOpen} />
      <IconDetailWindow
        icon={openIcon}
        onClose={() => setOpenIcon(null)}
        initialPosition={clickPosition}
      />
    </div>
  );
}
