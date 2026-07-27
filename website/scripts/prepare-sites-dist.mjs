import { cp, mkdir, readdir, readFile, rm, stat, writeFile } from "node:fs/promises";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const root = dirname(dirname(fileURLToPath(import.meta.url)));
const outDir = join(root, "out");
const distDir = join(root, "dist");
const serverDir = join(distDir, "server");

await rm(distDir, { force: true, recursive: true });
await mkdir(serverDir, { recursive: true });
await cp(outDir, distDir, { recursive: true });

async function collectAssets(dir, prefix = "") {
  const entries = await readdir(dir);
  const assets = [];

  for (const entry of entries) {
    if (entry === "server") {
      continue;
    }

    const absolute = join(dir, entry);
    const relative = `${prefix}/${entry}`;
    const details = await stat(absolute);

    if (details.isDirectory()) {
      assets.push(...await collectAssets(absolute, relative));
    } else if (details.isFile()) {
      const bytes = await readFile(absolute);
      assets.push([relative, bytes.toString("base64")]);
    }
  }

  return assets;
}

const embeddedAssets = await collectAssets(distDir);

await writeFile(
  join(serverDir, "index.js"),
  `const embeddedAssets = new Map(${JSON.stringify(embeddedAssets)});

const contentTypes = {
  ".css": "text/css; charset=utf-8",
  ".gif": "image/gif",
  ".html": "text/html; charset=utf-8",
  ".ico": "image/x-icon",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".js": "text/javascript; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".png": "image/png",
  ".svg": "image/svg+xml",
  ".txt": "text/plain; charset=utf-8",
  ".webp": "image/webp"
};

function extension(pathname) {
  const match = pathname.match(/\\.[a-z0-9]+$/i);
  return match ? match[0].toLowerCase() : "";
}

function decodeBase64(value) {
  const binary = atob(value);
  const bytes = new Uint8Array(binary.length);

  for (let index = 0; index < binary.length; index += 1) {
    bytes[index] = binary.charCodeAt(index);
  }

  return bytes;
}

function findAsset(pathname) {
  const variants = pathname.startsWith("/")
    ? [pathname, pathname.slice(1)]
    : [pathname, "/" + pathname];

  for (const variant of variants) {
    const normalized = variant.startsWith("/") ? variant : "/" + variant;
    const body = embeddedAssets.get(normalized);

    if (body) {
      return { body, pathname: normalized };
    }
  }

  return null;
}

export default {
  async fetch(request, env) {
    if (request.method !== "GET" && request.method !== "HEAD") {
      return new Response("Method not allowed", { status: 405 });
    }

    const url = new URL(request.url);
    const cleanPath = url.pathname.replace(/\\/+$|^$/g, "") || "/";
    const candidates = cleanPath.includes(".")
      ? [cleanPath]
      : [
          cleanPath === "/" ? "/index.html" : cleanPath + ".html",
          cleanPath === "/" ? "/index.html" : cleanPath + "/index.html"
    ];

    for (const pathname of candidates) {
      const match = findAsset(pathname);
      if (match) {
        const headers = new Headers();
        const type = contentTypes[extension(match.pathname)];
        if (type) {
          headers.set("content-type", type);
        }
        return new Response(request.method === "HEAD" ? null : decodeBase64(match.body), {
          status: 200,
          headers
        });
      }
    }

    const notFound = findAsset("/404.html");
    if (notFound) {
      const headers = new Headers({ "content-type": "text/html; charset=utf-8" });
      return new Response(request.method === "HEAD" ? null : decodeBase64(notFound.body), {
        status: 404,
        headers
      });
    }

    return new Response("Not found", { status: 404 });
  }
};
`
);
