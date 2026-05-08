export interface IconEntry {
  id: string;
  name: string;
  dll: string;
  dllPath: string;
  resourceId: number;
  file: string;
  tags: string[];
  description: string;
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
