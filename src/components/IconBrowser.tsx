"use client";

import { useMemo, useState } from "react";
import Fuse from "fuse.js";
import type { IconEntry } from "@/lib/icons";
import { SearchBar } from "./SearchBar";
import { IconGrid } from "./IconGrid";

interface IconBrowserProps {
  icons: IconEntry[];
}

export function IconBrowser({ icons }: IconBrowserProps) {
  const [query, setQuery] = useState("");

  const fuse = useMemo(
    () =>
      new Fuse(icons, {
        keys: [
          { name: "name", weight: 2 },
          { name: "tags", weight: 1.5 },
          { name: "description", weight: 1 },
          { name: "dll", weight: 0.5 },
        ],
        threshold: 0.3,
        includeScore: true,
      }),
    [icons]
  );

  const filtered = useMemo(() => {
    if (!query.trim()) return icons;
    return fuse.search(query).map((result) => result.item);
  }, [query, fuse, icons]);

  return (
    <>
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
