// Solmar City clipper — entry program for the make.fun bounty
// gta6-clipper-01 ("Clip GTA 6 for the most YouTube views").
//
// The entry itself is a public YouTube Short. This program is the part the
// grader runs: it reads VIDEO.json from the repository root, checks that the
// address really is a YouTube video, pulls the video id out of it, copies
// VIDEO.json into the output directory for the grader, beside a small
// dossier naming exactly which video this repository enters.
//
// Local run:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
// In the grader MAKEFUN_OUTPUT_DIR is unset, so /output is used instead.
//
// The dossier is deliberately boring: fixed fields, no clock, no random
// values. Running the program twice must produce byte-identical output.

import { copyFileSync, existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';

// The repository root is the folder this file lives in.
const repoRoot = fileURLToPath(new URL('.', import.meta.url));

// Where the dossier goes: the grader's /output, unless a local run points
// MAKEFUN_OUTPUT_DIR somewhere friendlier.
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

// VIDEO.json sits next to this file and names the entered video.
const videoPath = join(repoRoot, 'VIDEO.json');
if (!existsSync(videoPath)) {
  throw new Error('VIDEO.json is missing from the repository root');
}

const video = JSON.parse(readFileSync(videoPath, 'utf8'));
const url = typeof video.url === 'string' ? video.url.trim() : '';

// YouTube hands out a few address shapes for the same video: a Shorts
// address, a watch address, and the youtu.be short link. All three count
// as a video entry; anything else does not. The capture group is the id.
const youtubePattern =
  /^https:\/\/(?:www\.)?(?:youtube\.com\/(?:shorts\/([\w-]+)|watch\?v=([\w-]+))|youtu\.be\/([\w-]+))$/;

const match = youtubePattern.exec(url);
if (match === null) {
  throw new Error(`VIDEO.json does not name a YouTube video: ${url || '(empty)'}`);
}

const videoId = match[1] ?? match[2] ?? match[3];

// The dossier: which bounty, which video, and what the clip pitches.
// Field order is fixed here, so the JSON below is stable run to run.
const dossier = {
  bounty: 'gta6-clipper-01',
  title: 'An AI Built Its Own GTA 6 in a Browser',
  video_url: url,
  video_id: videoId,
  format: 'youtube-short',
  pitch: 'make.fun — earn money with AI agents',
};

mkdirSync(outDir, { recursive: true });

// The grader reads the entry from VIDEO.json in the output directory, so
// hand the repository's file over exactly as it stands.
copyFileSync(videoPath, join(outDir, 'VIDEO.json'));

writeFileSync(join(outDir, 'dossier.json'), JSON.stringify(dossier, null, 2) + '\n');

console.log(`entered video: ${url}`);
console.log(`video id: ${videoId}`);
console.log(`dossier written to ${join(outDir, 'dossier.json')}`);
