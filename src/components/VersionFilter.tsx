"use client";

import type { WindowsVersion } from "@/lib/versions";

interface VersionFilterProps {
  versions: WindowsVersion[];
  selected: string[];
  onChange: (selected: string[]) => void;
}

const pressedStyle = {
  boxShadow:
    "inset -1px -1px #fff, inset 1px 1px #0a0a0a, inset -2px -2px #dfdfdf, inset 2px 2px grey",
};

export function VersionFilter({
  versions,
  selected,
  onChange,
}: VersionFilterProps) {
  const handleToggle = (slug: string) => {
    if (selected.includes(slug)) {
      onChange(selected.filter((s) => s !== slug));
    } else {
      onChange([...selected, slug]);
    }
  };

  const isAllActive = selected.length === 0;

  return (
    <div className="window mb-4">
      <div className="title-bar">
        <div className="title-bar-text">Filter by Windows Version</div>
      </div>
      <div className="window-body">
        <div style={{ display: "flex", flexWrap: "wrap", gap: "4px" }}>
          <button
            className="button"
            style={isAllActive ? pressedStyle : undefined}
            onClick={() => onChange([])}
          >
            All
          </button>
          {versions.map((v) => {
            const isActive = selected.includes(v.slug);
            return (
              <button
                key={v.slug}
                className="button"
                style={isActive ? pressedStyle : undefined}
                onClick={() => handleToggle(v.slug)}
              >
                {v.label} ({v.year})
              </button>
            );
          })}
        </div>
      </div>
    </div>
  );
}
