"use client";

import { useEffect, useCallback } from "react";
import Draggable from "react-draggable";
import type { IconEntry } from "@/lib/icons";

interface IconDetailWindowProps {
  icon: IconEntry | null;
  onClose: () => void;
  initialPosition?: { x: number; y: number };
}

const FORMATS = ["ico", "png", "jpg", "webp"] as const;

function downloadUrl(icon: IconEntry, format: string) {
  return `/api/download?file=${encodeURIComponent(icon.file.replace(/^\/icons\//, ""))}&format=${format}`;
}

export function IconDetailWindow({
  icon,
  onClose,
  initialPosition,
}: IconDetailWindowProps) {
  const handleKeyDown = useCallback(
    (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
    },
    [onClose]
  );

  useEffect(() => {
    if (!icon) return;
    document.addEventListener("keydown", handleKeyDown);
    return () => document.removeEventListener("keydown", handleKeyDown);
  }, [icon, handleKeyDown]);

  if (!icon) return null;

  const defaultPos = initialPosition ?? {
    x: Math.round(window.innerWidth / 2 - 140),
    y: Math.round(window.innerHeight / 2 - 200),
  };

  return (
    <Draggable handle=".title-bar" defaultPosition={defaultPos}>
      <div className="icon-detail-window window">
        <div className="title-bar">
          <div className="title-bar-text">{icon.name}</div>
          <div className="title-bar-controls">
            <button aria-label="Close" onClick={onClose} />
          </div>
        </div>
        <div className="window-body">
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img
            src={icon.file}
            alt={icon.name}
            width={64}
            height={64}
            style={{ imageRendering: "pixelated" }}
          />
          <div className="field-row-stacked" style={{ width: "100%" }}>
            <p style={{ margin: "2px 0" }}>
              <strong>Name:</strong> {icon.name}
            </p>
            <p style={{ margin: "2px 0" }}>
              <strong>DLL:</strong> {icon.dll}
            </p>
            <p style={{ margin: "2px 0" }}>
              <strong>Resource ID:</strong> #{icon.resourceId}
            </p>
            <p style={{ margin: "2px 0" }}>
              <strong>Version:</strong> {icon.versionLabel}
            </p>
          </div>
          <div className="download-buttons">
            {FORMATS.map((fmt) => (
              <a
                key={fmt}
                href={downloadUrl(icon, fmt)}
                download={`${icon.id}.${fmt}`}
                className="no-underline"
              >
                <button
                  style={{ fontSize: 11, minWidth: 42, padding: "2px 6px" }}
                >
                  {fmt.toUpperCase()}
                </button>
              </a>
            ))}
          </div>
        </div>
      </div>
    </Draggable>
  );
}
