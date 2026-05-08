import { IconBrowser } from "@/components/IconBrowser";
import type { IconEntry } from "@/lib/icons";
import fs from "fs";
import path from "path";

function loadIcons(): IconEntry[] {
  const filePath = path.join(process.cwd(), "data", "icons.json");
  if (!fs.existsSync(filePath)) {
    return [];
  }
  const raw = fs.readFileSync(filePath, "utf-8");
  return JSON.parse(raw) as IconEntry[];
}

export default function Home() {
  const icons = loadIcons();

  return <IconBrowser icons={icons} />;
}
