"use client";

import type { IconEntry } from "@/lib/icons";
import { groupByDll } from "@/lib/icons";
import { DllSection } from "./DllSection";

interface IconGridProps {
  icons: IconEntry[];
}

export function IconGrid({ icons }: IconGridProps) {
  const groups = groupByDll(icons);

  if (icons.length === 0) {
    return (
      <div className="window">
        <div className="title-bar">
          <div className="title-bar-text">No Results</div>
        </div>
        <div className="window-body">
          <p>No icons match your search. Try different keywords.</p>
        </div>
      </div>
    );
  }

  return (
    <div>
      {groups.map((group) => (
        <DllSection key={group.dll} group={group} />
      ))}
    </div>
  );
}
