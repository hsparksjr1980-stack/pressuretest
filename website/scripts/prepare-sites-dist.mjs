import { cp, mkdir, rm, writeFile } from "node:fs/promises";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const root = dirname(dirname(fileURLToPath(import.meta.url)));
const outDir = join(root, "out");
const distDir = join(root, "dist");
const serverDir = join(distDir, "server");

await rm(distDir, { force: true, recursive: true });
await mkdir(serverDir, { recursive: true });
await cp(outDir, distDir, { recursive: true });

await writeFile(
  join(serverDir, "index.js"),
  `const contentTypes = {
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

async function fetchAsset(env, request, pathname) {
  const url = new URL(request.url);
  url.pathname = pathname;
  return env.ASSETS.fetch(new Request(url, request));
}

async function findAsset(env, request, pathname) {
  const variants = pathname.startsWith("/")
    ? [pathname, pathname.slice(1)]
    : [pathname, "/" + pathname];

  for (const variant of variants) {
    const response = await fetchAsset(env, request, variant);
    if (response.status !== 404) {
      return { response, pathname: variant };
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
      const match = await findAsset(env, request, pathname);
      if (match) {
        const headers = new Headers(match.response.headers);
        const type = contentTypes[extension(match.pathname)];
        if (type && !headers.has("content-type")) {
          headers.set("content-type", type);
        }
        return new Response(match.response.body, {
          status: match.response.status,
          statusText: match.response.statusText,
          headers
        });
      }
    }

    const notFound = await findAsset(env, request, "/404.html");
    if (notFound) {
      return new Response(notFound.response.body, {
        status: 404,
        headers: notFound.response.headers
      });
    }

    return new Response("Not found", { status: 404 });
  }
};
`
);
