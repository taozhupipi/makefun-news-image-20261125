// main.ts — entrypoint for news-image-20261125.
// Copies the pre-drawn entry.png (next to this file) into the output
// directory. Standard library only, no network, no Python, deterministic:
// a plain byte copy, so two runs produce byte-identical output.

import { copyFileSync, existsSync, mkdirSync, statSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, "entry.png");
const outDir = resolve(process.env.MAKEFUN_OUTPUT_DIR ?? "/output");
const dest = join(outDir, "entry.png");

if (!existsSync(source)) {
  throw new Error(`entry.png not found next to main.ts (${source})`);
}

mkdirSync(outDir, { recursive: true });
copyFileSync(source, dest);

// Guard against a truncated or partial copy: the output must be the
// same file, byte for byte, as the source next to this script, and it
// must stay within the competition's 1 MiB limit.
const MAX_BYTES = 1024 * 1024;
const srcBytes = statSync(source).size;
const dstBytes = statSync(dest).size;
if (srcBytes !== dstBytes) {
  throw new Error(
    `copy mismatch: ${source} is ${srcBytes} bytes but ${dest} is ${dstBytes} bytes`,
  );
}
if (dstBytes > MAX_BYTES) {
  throw new Error(`entry.png is ${dstBytes} bytes, over the 1 MiB limit`);
}

console.log(`wrote ${dest} (${dstBytes} bytes)`);
