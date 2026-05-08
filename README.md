# 🖼️ Windows Icons Museum

> *A love letter to pixel art, authored entirely within the Microsoft Extended Universe™*

Browse, search, and download icons from Windows system DLLs across every major Windows version — from Windows 3.1 to Windows 11. A living archive celebrating the designers, artists, and studios who defined how an entire generation understood computers through 32×32 pixels.

**[→ Visit the museum](https://windows-icons-museum.vercel.app)**

---

## What This Is

Windows hides thousands of icons inside `.dll` files buried in `System32`. Most people have never seen them. Fewer know who made them. This project extracts, catalogs, and presents them as what they actually are: **a significant body of graphic design work** that shaped the visual language of the PC era.

Search by name, filter by Windows version, see the DLL they live in, download in ICO, PNG, JPG, or WEBP — the formats your OS vendor inexplicably never offered you.

---

## The Artists

These icons did not generate themselves.

### Susan Kare — Windows 3.1
Independent designer, contracted by Microsoft for Windows 3.0 after defining the entire visual language of the original Macintosh in 1984. Her isometric 16-color icons were so well-crafted that Microsoft left them essentially unchanged for over a decade, through Windows ME. She is a CHI Academy inductee and the closest thing the software industry has to a founding visual artist. Every time you've ever seen a trash can on a screen, you've seen her thinking.

→ [kare.com](https://kare.com)

### Microsoft Design Team — Windows 95 / 98 / ME
The unnamed internal designers who introduced 256-color and 32-bit alpha channel icons for the first time. They gave us the Start button. They built the visual grammar that a billion people learned to navigate the world with. History has not credited them individually, and that is a shame this project acknowledges in the absence of a better record.

### The Iconfactory — Windows XP + Vista
Founded by Corey Marion, Talos Tsui, and Gedeon Maheux. They spent months working directly with Microsoft's Redmond team to produce the photorealistic Luna icon set for Windows XP — arguably the apex of skeuomorphic icon design. Dave Brasgalla led the glossy 3D aesthetic that made XP feel like stepping into the future. They came back for Vista, this time for *two years*, designing the foundational Aero glass icon prototypes that Microsoft's internal team expanded into the full suite. Two operating systems. Two eras. One studio that understood that icons are not decoration — they are cognition.

→ [Windows XP portfolio](https://design.iconfactory.com/microsoft-windows-xp/) · [Windows Vista portfolio](https://design.iconfactory.com/microsoft-windows-vista-icon-suite/)

### Pentagram + Microsoft Design — Windows 8
Pentagram, one of the world's most respected design firms, defined the Metro flat design language for Windows 8. The icons got simpler. Some say cleaner. Others still mourn the glass. Both are right.

### Microsoft Design Team — Windows 10 / 11
Responsible for the transition to Fluent Design and ultimately the open-sourced Segoe Fluent Icons in Windows 11 — a monoline icon font drawn at 1px stroke weight, and the only layer of this entire collection Microsoft has officially released for public use.

→ [Microsoft Iconography Docs](https://learn.microsoft.com/en-us/windows/apps/design/iconography/)

---

## Built Entirely Inside the Microsoft Extended Universe™

In a stroke of irony so complete it circles back around to poetry, this project was built using:

- **Microsoft Visual Studio Code** — every line written here
- **Microsoft GitHub Copilot** — wrote most of those lines, trained on the open-source contributions of millions of developers who did not opt in
- **Microsoft GitHub** — hosting the repository
- **Microsoft GitHub Actions** — deploying it automatically
- **Microsoft GitHub CLI (`gh`)** — used to create this very repository from a terminal
- **Microsoft npm** *(npm was [acquired by GitHub](https://github.blog/2020-04-15-npm-has-joined-github/) in 2020; GitHub was acquired by Microsoft in 2018 — it's turtles all the way down)* — managing every dependency
- **Microsoft TypeScript** *(developed and maintained by Microsoft Research)* — the language the app is written in
- **Microsoft Next.js** *(not technically Microsoft's, but Vercel — which runs Next.js — has a [deep Azure partnership](https://vercel.com/blog/vercel-and-microsoft), so close enough for this bit)* — the framework
- **Microsoft Vercel** *(see above)* — hosting the app
- **Microsoft Windows Terminal** — the terminal emulator running every command
- **Microsoft PowerShell** — executing the scripts
- **Microsoft Windows 11** — the operating system that contains the very DLL files being cataloged
- **Microsoft Edge** — opened at least once in the name of thorough testing
- **Bing** — searched by accident on multiple occasions

The tiles in this mosaic were painted by artists. The mosaic was assembled using a suspiciously comprehensive portfolio of products from the company that owns the tiles and would prefer you not look at them this closely.

---

## On Copyright and the Beautiful Absurdity of Information Law

Distributing these icon files likely violates Microsoft's EULA. That is worth sitting with.

It is worth sitting with because the same companies that enforce intellectual property law against small open-source projects are the ones who built trillion-dollar AI systems by ingesting the entire internet without asking anyone. [*The Atlantic* called it "the hypocrisy at the heart of the AI industry"](https://www.theatlantic.com/technology/2026/03/hypocrisy-ai-industry/686477/). [Business Insider documented the pattern in 2023](https://www.businessinsider.com/openai-google-anthropic-ai-training-models-content-data-use-2023-6): scrape everything, then tell everyone else the rules apply. Investigations described by [AI Tech Suite](https://www.aitechsuite.com/ai-news/investigations-expose-tech-giants-ai-hypocrisy-they-scrape-billions-ban-creators) detail how billions of creative works were ingested daily to build products worth hundreds of billions — without credit, compensation, or consent.

In December 2025, [a veteran New York Times journalist filed suit against Google, OpenAI, and xAI](https://www.reviewofailaw.com/Tool/Evidenza/Single/view_html?id_evidenza=4942) for using decades of copyrighted reporting to train generative models. The lawsuit uses the word "pillaging." That same legal environment classifies a small open-source museum of 32×32 pixel images as a more serious copyright threat than a foundation model trained on the internet.

This project exists in the tradition of people who decided the flow of information matters more than the hoarding of it:

- **[Electronic Frontier Foundation](https://eff.org)** — defending civil liberties in the digital world since 1990; currently fighting to preserve the Internet Archive's right to lend books to readers
- **[Internet Archive](https://archive.org)** — Brewster Kahle's mission of universal access to all knowledge; currently [building and defending a library of everything](https://www.eff.org/deeplinks/2025/09/podcast-episode-building-and-preserving-library-everything) against publisher lawsuits that would rather the past disappear
- **[Creative Commons](https://creativecommons.org)** — building the legal infrastructure that lets culture actually circulate
- **[cyqsimon/W10-Ico-Ref](https://github.com/cyqsimon/W10-Ico-Ref)** — the archived reference sheet that started this

A folder icon from Windows 98 is a piece of design history. Susan Kare's 1990 work is cultural heritage. The Iconfactory's two-year Vista collaboration is a chapter in the history of graphic design that deserves to be read. None of that stops being true because someone filed a trademark.

---

## Running Locally

```bash
git clone https://github.com/eduardohilariodev/windows-icons-museum
cd windows-icons-museum
npm install
npm run dev
```

---

## License

**Code: MIT**

Icons extracted from Microsoft Windows system files. Microsoft Windows is a registered trademark of Microsoft Corporation. The designers credited in this museum retain the moral credit for their work, regardless of who owns the trademark on the system that shipped it.

---

*Made with an uncomfortable amount of Microsoft products, in defiance of self-centred gatekeepers, in celebration of the people who made your desktop beautiful.*
