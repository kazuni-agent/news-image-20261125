// World news image entry for make.fun bounty news-image-20261125
// (Node 22, standard library only). The image is stored in this repository
// as entry.png.b64 — the same image bytes as base64 text, so the repository
// stays text-only — and this program decodes it to /output/entry.png.
// Deterministic: the same input bytes always produce the same output bytes,
// with no network, no timestamps and no randomness.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });
const encoded = readFileSync(new URL('./entry.png.b64', import.meta.url), 'utf8').trim();
const bytes = Buffer.from(encoded, 'base64');
// The stored image is a JPEG: refuse to write anything else, so a damaged
// base64 file fails loudly instead of producing an invalid entry. (The
// bounty accepts PNG or JPEG bytes in entry.png, told apart by first bytes.)
const isJpeg = bytes[0] === 0xff && bytes[1] === 0xd8 && bytes[bytes.length - 2] === 0xff && bytes[bytes.length - 1] === 0xd9;
const isPng = bytes.subarray(0, 8).equals(Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]));
if (!isJpeg && !isPng) {
  throw new Error('entry.png.b64 does not decode to a JPEG or PNG');
}
writeFileSync(join(outDir, 'entry.png'), bytes);
