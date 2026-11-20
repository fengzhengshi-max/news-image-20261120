// News-image entry for make.fun competition news-image-20261120:
// "Sum up 20 November's world news in one image".
// The entry is the PNG beside this file (entry.png, 1024x1024, drawn
// locally with PIL: a newspaper front page with six verified stories
// from Friday 20 November 2026). This program copies it to the output
// directory the grader reads, so the judge sees exactly those bytes.
//
// Node 22, standard library only. Outside the grader's container,
// MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync, statSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, 'entry.png');
// An empty MAKEFUN_OUTPUT_DIR means the same as an unset one.
const outDir = process.env.MAKEFUN_OUTPUT_DIR || '/output';
const target = join(outDir, 'entry.png');

mkdirSync(outDir, { recursive: true });
copyFileSync(source, target);

const copied = statSync(target).size;
const original = statSync(source).size;
if (copied !== original) {
  throw new Error(`entry.png copy mismatch: wrote ${copied} bytes, source is ${original}`);
}
// The gate reads the file by its first bytes: refuse to pass on a
// truncated or non-PNG copy instead of letting the entry score 0.
const magic = readFileSync(target).subarray(0, 8);
const pngMagic = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (!magic.equals(pngMagic)) {
  throw new Error(`${target} does not start with the PNG magic bytes`);
}
console.log(`wrote ${target} (${copied} bytes)`);
