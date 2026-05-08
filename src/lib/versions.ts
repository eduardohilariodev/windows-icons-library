export interface WindowsVersion {
  slug: string;
  label: string;
  year: number;
  color: string;
}

export const WINDOWS_VERSIONS: WindowsVersion[] = [
  { slug: "win31", label: "Windows 3.1", year: 1992, color: "#808080" },
  { slug: "win95", label: "Windows 95", year: 1995, color: "#008080" },
  { slug: "win98", label: "Windows 98", year: 1998, color: "#000080" },
  { slug: "winxp", label: "Windows XP", year: 2001, color: "#003399" },
  { slug: "winvista", label: "Windows Vista", year: 2006, color: "#2b5797" },
  { slug: "win7", label: "Windows 7", year: 2009, color: "#1e90ff" },
  { slug: "win8", label: "Windows 8", year: 2012, color: "#00b4ff" },
  { slug: "win10", label: "Windows 10", year: 2015, color: "#0078d4" },
  { slug: "win11", label: "Windows 11", year: 2021, color: "#60cdff" },
];

export function getVersionLabel(slug: string): string {
  return WINDOWS_VERSIONS.find((v) => v.slug === slug)?.label ?? slug;
}

export function getVersionColor(slug: string): string {
  return WINDOWS_VERSIONS.find((v) => v.slug === slug)?.color ?? "#808080";
}
