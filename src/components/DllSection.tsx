"use client";

import type { DllGroup } from "@/lib/icons";
import { IconCard } from "./IconCard";

interface DllSectionProps {
  group: DllGroup;
}

export function DllSection({ group }: DllSectionProps) {
  return (
    <section aria-label={`Icons from ${group.dll}`}>
      <div
        className="window mb-2 sticky top-0 z-10"
        style={{ background: "#c0c0c0" }}
      >
        <div className="title-bar">
          <div className="title-bar-text">
            {group.dll} — {group.icons.length} icons
          </div>
        </div>
        <div className="window-body flex items-center justify-between py-1">
          <span className="text-xs" style={{ color: "#808080" }}>
            {group.dllPath}
          </span>
        </div>
      </div>
      <div className="flex flex-wrap gap-2 mb-6">
        {group.icons.map((icon) => (
          <IconCard key={icon.id} icon={icon} />
        ))}
      </div>
    </section>
  );
}
