"use client";

import type { IconEntry } from "@/lib/icons";
import { groupByVersion } from "@/lib/icons";
import { getVersionColor, WINDOWS_VERSIONS } from "@/lib/versions";
import { DllWindow } from "./DllWindow";
import { IconCard } from "./IconCard";
import { IconContextMenu } from "./IconContextMenu";

interface IconGridProps {
  icons: IconEntry[];
  onOpenIcon?: (icon: IconEntry, event: React.MouseEvent) => void;
}

export function IconGrid({ icons, onOpenIcon }: IconGridProps) {
  const versionGroups = groupByVersion(icons);

  if (icons.length === 0) {
    return (
      <div className="window" style={{ maxWidth: 420 }}>
        <div className="title-bar">
          <div className="title-bar-text">Error</div>
        </div>
        <div className="window-body" style={{ display: "flex", gap: 16, alignItems: "flex-start", padding: 16 }}>
          <img
            src="/error.png"
            alt="Error"
            width={32}
            height={32}
            style={{ flexShrink: 0 }}
            onError={(e) => { (e.target as HTMLImageElement).style.display = "none"; }}
          />
          <p style={{ margin: 0 }}>
            No icons found. Try different search terms or adjust version filters.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div>
      {versionGroups.map((vg) => {
        const color = getVersionColor(vg.version);
        const year = WINDOWS_VERSIONS.find((v) => v.slug === vg.version)?.year;

        return (
          <section key={vg.version} style={{ marginBottom: 24 }}>
            <div className="title-bar" style={{ backgroundColor: color, color: "#fff" }}>
              <div className="title-bar-text">
                {vg.versionLabel}{year ? ` (${year})` : ""}
              </div>
            </div>
            {vg.dllGroups.map((group) => (
              <DllWindow
                key={group.dll}
                dll={group.dll}
                dllPath={group.dllPath}
                version={vg.version}
                icons={group.icons}
              >
                {group.icons.map((icon) => (
                  <IconContextMenu
                    key={icon.id}
                    icon={icon}
                    onOpen={(i) =>
                      onOpenIcon?.(i, undefined as unknown as React.MouseEvent)
                    }
                  >
                    <div>
                      <IconCard icon={icon} onClick={onOpenIcon} />
                    </div>
                  </IconContextMenu>
                ))}
              </DllWindow>
            ))}
          </section>
        );
      })}
    </div>
  );
}
