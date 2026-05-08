import { WINDOWS_VERSIONS } from "./versions";

export interface IconEntry {
  id: string;
  name: string;
  dll: string;
  dllPath: string;
  dllDescription: string;
  resourceId: number;
  file: string;
  tags: string[];
  description: string;
  version: string;
  versionLabel: string;
}

export interface DllGroup {
  dll: string;
  dllPath: string;
  description: string;
  icons: IconEntry[];
}

export function groupByDll(icons: IconEntry[]): DllGroup[] {
  const groups = new Map<string, DllGroup>();

  for (const icon of icons) {
    if (!groups.has(icon.dll)) {
      groups.set(icon.dll, {
        dll: icon.dll,
        dllPath: icon.dllPath,
        description: "",
        icons: [],
      });
    }
    groups.get(icon.dll)!.icons.push(icon);
  }

  return Array.from(groups.values()).sort((a, b) =>
    a.dll.localeCompare(b.dll)
  );
}

export interface VersionGroup {
  version: string;
  versionLabel: string;
  dllGroups: DllGroup[];
}

export function groupByVersion(icons: IconEntry[]): VersionGroup[] {
  const versionOrder = WINDOWS_VERSIONS.map((v) => v.slug);
  const groups = new Map<string, IconEntry[]>();

  for (const icon of icons) {
    if (!groups.has(icon.version)) {
      groups.set(icon.version, []);
    }
    groups.get(icon.version)!.push(icon);
  }

  const sortedKeys = Array.from(groups.keys()).sort((a, b) => {
    const ai = versionOrder.indexOf(a);
    const bi = versionOrder.indexOf(b);
    return (ai === -1 ? Infinity : ai) - (bi === -1 ? Infinity : bi);
  });

  return sortedKeys.map((version) => {
    const versionIcons = groups.get(version)!;
    const versionLabel =
      versionIcons[0]?.versionLabel ?? version;
    return {
      version,
      versionLabel,
      dllGroups: groupByDll(versionIcons),
    };
  });
}
