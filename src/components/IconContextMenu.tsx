"use client";

import type { ReactNode } from "react";
import * as ContextMenu from "@radix-ui/react-context-menu";
import type { IconEntry } from "@/lib/icons";

interface IconContextMenuProps {
  icon: IconEntry;
  onOpen: (icon: IconEntry) => void;
  children: ReactNode;
}

const FORMATS = ["ico", "png", "jpg", "webp"] as const;

function downloadUrl(icon: IconEntry, format: string) {
  return `/api/download?file=${encodeURIComponent(icon.file.replace(/^\/icons\//, ""))}&format=${format}`;
}

function triggerDownload(icon: IconEntry, format: string) {
  const a = document.createElement("a");
  a.href = downloadUrl(icon, format);
  a.download = `${icon.id}.${format}`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
}

export function IconContextMenu({
  icon,
  onOpen,
  children,
}: IconContextMenuProps) {
  return (
    <ContextMenu.Root>
      <ContextMenu.Trigger asChild>{children}</ContextMenu.Trigger>
      <ContextMenu.Portal>
        <ContextMenu.Content>
          <ContextMenu.Item onSelect={() => onOpen(icon)}>
            Open
          </ContextMenu.Item>
          <ContextMenu.Separator />
          {FORMATS.map((fmt) => (
            <ContextMenu.Item
              key={fmt}
              onSelect={() => triggerDownload(icon, fmt)}
            >
              Download {fmt.toUpperCase()}
            </ContextMenu.Item>
          ))}
          <ContextMenu.Separator />
          <ContextMenu.Item
            onSelect={() => navigator.clipboard.writeText(icon.name)}
          >
            Copy name
          </ContextMenu.Item>
          <ContextMenu.Item
            onSelect={() =>
              navigator.clipboard.writeText(icon.resourceId.toString())
            }
          >
            Copy resource ID
          </ContextMenu.Item>
        </ContextMenu.Content>
      </ContextMenu.Portal>
    </ContextMenu.Root>
  );
}
