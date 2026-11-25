// main.ts — entrypoint for news-image-20261125.
// Runs draw.py (Pillow, no network) and writes /output/entry.png.
// Output dir comes from MAKEFUN_OUTPUT_DIR, default /output.

import { execFileSync } from "node:child_process";
import { existsSync, statSync, mkdirSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const HERE = dirname(fileURLToPath(import.meta.url));
const OUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const OUT_FILE = join(OUT_DIR, "entry.png");
const MAX_BYTES = 1024 * 1024;

function draw(): void {
  mkdirSync(OUT_DIR, { recursive: true });
  execFileSync("python3", [join(HERE, "draw.py"), OUT_FILE], {
    stdio: "inherit",
    cwd: HERE,
  });
}

function verify(): void {
  if (!existsSync(OUT_FILE)) {
    throw new Error(`entry.png was not written to ${OUT_FILE}`);
  }
  const size = statSync(OUT_FILE).size;
  if (size > MAX_BYTES) {
    throw new Error(`entry.png is ${size} bytes, over the 1 MiB limit`);
  }
  console.log(`wrote ${OUT_FILE} (${size} bytes)`);
}

draw();
verify();
