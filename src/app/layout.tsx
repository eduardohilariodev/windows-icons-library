import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Windows Icons Library — Browse & Download Windows DLL Icons",
  description:
    "Search, preview, and download icons from Windows system DLLs including shell32.dll, imageres.dll, ieframe.dll and 28 more. Free ICO, PNG, JPG, WEBP downloads.",
  keywords: [
    "windows icons",
    "dll icons",
    "shell32.dll",
    "imageres.dll",
    "windows icon library",
    "system icons",
    "ico download",
    "windows 10 icons",
    "windows 11 icons",
    "icon reference",
  ],
  openGraph: {
    title: "Windows Icons Library",
    description:
      "Browse, search, and download icons from 31 Windows system DLLs. Free ICO, PNG, JPG, WEBP formats.",
    type: "website",
    locale: "en_US",
    siteName: "Windows Icons Library",
  },
  twitter: {
    card: "summary_large_image",
    title: "Windows Icons Library",
    description:
      "Browse, search, and download icons from 31 Windows system DLLs.",
  },
  robots: {
    index: true,
    follow: true,
  },
};

const jsonLd = {
  "@context": "https://schema.org",
  "@type": "WebSite",
  name: "Windows Icons Library",
  description:
    "Search, preview, and download icons from Windows system DLLs.",
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
};

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
              Browse, search, and download icons from 31 Windows system DLLs.
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
