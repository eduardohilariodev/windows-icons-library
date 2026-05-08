"use client";

import type { IconEntry } from "@/lib/icons";

interface IconCardProps {
  icon: IconEntry;
}

const FORMATS = ["ico", "png", "jpg", "webp"] as const;

export function IconCard({ icon }: IconCardProps) {
  const downloadUrl = (format: string) =>
    `/api/download?file=${encodeURIComponent(icon.file.replace(/^\/icons\//, ""))}&format=${format}`;

  return (
    <div className="window inline-block" style={{ width: 180 }}>
      <div className="title-bar">
        <div className="title-bar-text" title={icon.name}>
          {icon.name}
        </div>
      </div>
      <div className="window-body flex flex-col items-center gap-2">
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img
          src={icon.file}
          alt={[icon.name, ...icon.tags].join(", ")}
          width={48}
          height={48}
          loading="lazy"
          style={{ imageRendering: "pixelated" }}
        />
        <span className="text-xs text-center" style={{ color: "#808080" }}>
          #{icon.resourceId}
        </span>
        <div className="flex flex-wrap gap-1 justify-center">
          {FORMATS.map((fmt) => (
            <a
              key={fmt}
              href={downloadUrl(fmt)}
              download={`${icon.id}.${fmt}`}
              className="no-underline"
            >
              <button className="text-xs" style={{ minWidth: 36, padding: "1px 4px" }}>
                {fmt.toUpperCase()}
              </button>
            </a>
          ))}
        </div>
      </div>
    </div>
  );
}
