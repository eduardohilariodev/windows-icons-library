import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title:
    "Windows Icons Library — All Versions (3.1, 95, 98, XP, Vista, 7, 8, 10, 11)",
  description:
    "Search, preview, and download icons from shell32.dll, imageres.dll, and other Windows DLLs across all Windows versions from 3.1 to 11. Free ICO, PNG, JPG, WEBP downloads.",
  keywords: [
    "windows icons",
    "dll icons",
    "shell32.dll",
    "imageres.dll",
    "windows icon library",
    "system icons",
    "ico download",
    "windows 3.1 icons",
    "windows 95 icons",
    "windows 98 icons",
    "windows xp icons",
    "windows vista icons",
    "windows 7 icons",
    "windows 8 icons",
    "windows 10 icons",
    "windows 11 icons",
    "icon reference",
  ],
  openGraph: {
    title: "Windows Icons Library — All Versions",
    description:
      "Browse, search, and download icons from Windows system DLLs across all versions from 3.1 to 11. Free ICO, PNG, JPG, WEBP formats.",
    type: "website",
    locale: "en_US",
    siteName: "Windows Icons Library",
  },
  twitter: {
    card: "summary_large_image",
    title: "Windows Icons Library — All Versions",
    description:
      "Browse, search, and download icons from Windows system DLLs across all versions from 3.1 to 11.",
  },
  robots: {
    index: true,
    follow: true,
  },
};

const jsonLd = [
  {
    "@context": "https://schema.org",
    "@type": "WebSite",
    name: "Windows Icons Library",
    description:
      "Search, preview, and download icons from Windows system DLLs across all versions from 3.1 to 11.",
    url: "https://windows-icons-library.vercel.app",
    potentialAction: {
      "@type": "SearchAction",
      target: {
        "@type": "EntryPoint",
        urlTemplate:
          "https://windows-icons-library.vercel.app?q={search_term_string}",
      },
      "query-input": "required name=search_term_string",
    },
  },
  {
    "@context": "https://schema.org",
    "@type": "ItemList",
    name: "Windows Versions",
    description: "Icons available across all major Windows versions.",
    itemListElement: [
      { "@type": "ListItem", position: 1, name: "Windows 3.1" },
      { "@type": "ListItem", position: 2, name: "Windows 95" },
      { "@type": "ListItem", position: 3, name: "Windows 98" },
      { "@type": "ListItem", position: 4, name: "Windows XP" },
      { "@type": "ListItem", position: 5, name: "Windows Vista" },
      { "@type": "ListItem", position: 6, name: "Windows 7" },
      { "@type": "ListItem", position: 7, name: "Windows 8" },
      { "@type": "ListItem", position: 8, name: "Windows 10" },
      { "@type": "ListItem", position: 9, name: "Windows 11" },
    ],
  },
];

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <head>
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
        />
      </head>
      <body className="min-h-screen">
        <header className="window m-2" style={{ maxWidth: 1200, margin: "8px auto" }}>
          <div className="title-bar">
            <div className="title-bar-text">Windows Icons Library</div>
            <div className="title-bar-controls">
              <button aria-label="Minimize" />
              <button aria-label="Maximize" />
              <button aria-label="Close" />
            </div>
          </div>
          <div className="window-body flex items-center justify-between">
            <p>
              Browse, search, and download icons from all Windows versions.
            </p>
            <a
              href="https://github.com/cyqsimon/W10-Ico-Ref"
              target="_blank"
              rel="noopener noreferrer"
              className="text-xs"
              style={{ color: "#0000ff" }}
            >
              Source: W10-Ico-Ref
            </a>
          </div>
        </header>
        <main>{children}</main>
        <footer
          className="text-center py-4 text-xs"
          style={{ color: "#c0c0c0" }}
        >
          <p>
            Icons extracted from Windows system DLLs. Microsoft Windows is a
            trademark of Microsoft Corporation.
          </p>
          <p>
            <a
              href="https://github.com/eduardohilariodev/windows-icons-library"
              target="_blank"
              rel="noopener noreferrer"
              style={{ color: "#c0c0c0" }}
            >
              GitHub
            </a>
          </p>
        </footer>
      </body>
    </html>
  );
}
