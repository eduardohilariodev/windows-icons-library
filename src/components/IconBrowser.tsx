"use client";

import { useMemo, useState } from "react";
import Fuse from "fuse.js";
import type { IconEntry } from "@/lib/icons";
import { WINDOWS_VERSIONS } from "@/lib/versions";
import { SearchBar } from "./SearchBar";
import { IconGrid } from "./IconGrid";
import { VersionFilter } from "./VersionFilter";

interface IconBrowserProps {
  icons: IconEntry[];
}

export function IconBrowser({ icons }: IconBrowserProps) {
  const [query, setQuery] = useState("");
  const [selectedVersions, setSelectedVersions] = useState<string[]>([]);

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

  return (
    <>
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
      <IconGrid icons={filtered} />
    </>
  );
}
