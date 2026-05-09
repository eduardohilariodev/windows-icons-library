"use client";

import type { IconEntry } from "@/lib/icons";
import type { ReactNode } from "react";

interface DllWindowProps {
  dll: string;
  dllPath: string;
  version: string;
  icons: IconEntry[];
  children: ReactNode;
  onDownloadDll?: () => void;
}

export function DllWindow({
  dll,
  dllPath,
  icons,
  children,
  onDownloadDll,
}: DllWindowProps) {
  return (
    <section aria-label={`Icons from ${dll}`} className="dll-window">
      <div className="window">
        <div className="title-bar">
          <div className="title-bar-text">
            {dll} — {icons.length} icons
          </div>
          <div className="title-bar-controls">
            <button aria-label="Minimize" />
            <button aria-label="Maximize" />
            <button aria-label="Close" />
          </div>
        </div>
        <div className="window-body">
          <menu role="menubar" style={{ margin: 0, padding: "2px 0" }}>
            <li role="none">
              <button
                role="menuitem"
                style={{ fontSize: 11, padding: "1px 8px" }}
                onClick={onDownloadDll}
              >
                Download DLL
              </button>
            </li>
          </menu>
        </div>
        <div className="window-body">
          <span className="text-xs" style={{ color: "#808080" }}>
            {dllPath}
          </span>
        </div>
        <div className="window-body">{children}</div>
      </div>
    </section>
  );
}
