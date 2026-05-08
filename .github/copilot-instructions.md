# Copilot Instructions — windows-icons-library

## Stack
- Next.js 15 App Router, TypeScript, Node.js runtime
- Deployed on Vercel (zero-config)
- Styling: 98.css for Windows 98 aesthetics + Tailwind for layout utilities only
- Search: fuse.js (client-side, no backend)
- Image processing: sharp (Vercel Edge functions for format conversion)

## Data Shape
Each icon entry in `data/icons.json`:
```json
{
  "id": "imageres-1",
  "name": "Computer",
  "dll": "imageres.dll",
  "dllPath": "%SystemRoot%\\System32\\imageres.dll",
  "resourceId": 1,
  "file": "/icons/imageres/1.ico",
  "tags": ["computer", "hardware", "desktop", "pc", "machine"],
  "description": "Generic computer/desktop icon"
}
```

## Page Layout (single page)
1. Header: site title "Windows Icons Library" + credits link to W10-Ico-Ref
2. Search bar (fuse.js, searches name + tags + description + dll)
3. Results grouped by DLL with a sticky section header showing DLL name + path + download-whole-DLL button
4. Each icon: Win98-style card, icon preview, name, resource ID, download buttons (ICO / PNG / JPG / WEBP)

## SEO Requirements
- Static metadata in `layout.tsx`: title, description, keywords, OG tags
- Each DLL section should be an `<section>` with a descriptive `aria-label`
- JSON-LD structured data (WebSite + ItemList schema) in root layout
- All icon names and tags feed into page-level keywords meta tag
- `sitemap.xml` and `robots.txt` via Next.js App Router conventions

## Download API
`/api/download?file=imageres/1.ico&format=png`
- Reads from `public/icons/`
- Uses `sharp` to convert ICO → PNG/JPG/WEBP
- ICO format returns the file directly
- Sets `Content-Disposition: attachment` header

## DLL Sources (from W10-Ico-Ref)
31 icon sources total:
- 23 MUN files (imageres, shell32, accessibilitycpl, ddores, moricons, mmcndmgr, mmres, netcenter, netshell, networkexplorer, sensorscpl, wmploc, wpdshext, compstui, ieframe, dmdskres, dsuiext, mstscax, wiashext, comres, actioncentercpl, aclui, mstsc)
- 7 System32 DLLs (pifmgr, setupapi, autoplay, comctl32, xwizards, ncpa.cpl, url)
- 1 EXE (explorer.exe)

## Do Not
- Add a database or CMS — all data is static JSON
- Add authentication
- Add server components that fetch remote data — everything is local
- Use CSS-in-JS — use 98.css + Tailwind only
