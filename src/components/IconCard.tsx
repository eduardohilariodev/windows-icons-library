"use client";

import type { IconEntry } from "@/lib/icons";

interface IconCardProps {
  icon: IconEntry;
  onClick?: (icon: IconEntry, event: React.MouseEvent) => void;
}

export function IconCard({ icon, onClick }: IconCardProps) {
  return (
    <div
      className="icon-card"
      onClick={(e) => onClick?.(icon, e)}
      title={`${icon.name} (#${icon.resourceId})`}
    >
      {/* eslint-disable-next-line @next/next/no-img-element */}
      <img
        src={icon.file}
        alt={[icon.name, ...icon.tags].join(", ")}
        loading="lazy"
      />
      <span>{icon.name}</span>
    </div>
  );
}
