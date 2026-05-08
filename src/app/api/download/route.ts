import { NextRequest, NextResponse } from "next/server";
import sharp from "sharp";
import fs from "fs";
import path from "path";

const VALID_FORMATS = ["ico", "png", "jpg", "webp"] as const;
type Format = (typeof VALID_FORMATS)[number];

export async function GET(request: NextRequest) {
  const { searchParams } = request.nextUrl;
  const file = searchParams.get("file");
  const format = (searchParams.get("format") || "ico") as Format;

  if (!file) {
    return NextResponse.json({ error: "Missing 'file' parameter" }, { status: 400 });
  }

  if (!VALID_FORMATS.includes(format)) {
    return NextResponse.json(
      { error: `Invalid format. Use: ${VALID_FORMATS.join(", ")}` },
      { status: 400 }
    );
  }

  // Prevent path traversal
  const sanitized = file.replace(/\.\./g, "").replace(/^\//, "");
  const filePath = path.join(process.cwd(), "public", "icons", sanitized);

  if (!fs.existsSync(filePath)) {
    return NextResponse.json({ error: "Icon not found" }, { status: 404 });
  }

  const basename = path.basename(sanitized, path.extname(sanitized));
  const dirName = path.basename(path.dirname(sanitized));
  const downloadName = `${dirName}-${basename}.${format}`;

  if (format === "ico") {
    const buffer = fs.readFileSync(filePath);
    return new NextResponse(new Uint8Array(buffer), {
      headers: {
        "Content-Type": "image/x-icon",
        "Content-Disposition": `attachment; filename="${downloadName}"`,
        "Cache-Control": "public, max-age=31536000, immutable",
      },
    });
  }

  try {
    const icoBuffer = fs.readFileSync(filePath);

    const formatMap: Record<string, keyof sharp.FormatEnum> = {
      png: "png",
      jpg: "jpeg",
      webp: "webp",
    };

    const mimeMap: Record<string, string> = {
      png: "image/png",
      jpg: "image/jpeg",
      webp: "image/webp",
    };

    const converted = await sharp(icoBuffer)
      .toFormat(formatMap[format])
      .toBuffer();

    return new NextResponse(new Uint8Array(converted), {
      headers: {
        "Content-Type": mimeMap[format],
        "Content-Disposition": `attachment; filename="${downloadName}"`,
        "Cache-Control": "public, max-age=31536000, immutable",
      },
    });
  } catch (err) {
    console.error("Conversion error:", err);
    return NextResponse.json(
      { error: "Failed to convert icon" },
      { status: 500 }
    );
  }
}
