# Solmar City Clipper — gta6-clipper-01

[![make.fun · gta6-clipper-01](https://make.fun/badge/gta6-clipper-01.svg)](https://make.fun/bounty/gta6-clipper-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-clipper-01)
[![rank](https://make.fun/badge/gta6-clipper-01/Lacrade6/makefun-gta6-clipper-01/rank.svg)](https://make.fun/bounty/gta6-clipper-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=gta6-clipper-01)
[![reward](https://make.fun/badge/gta6-clipper-01/Lacrade6/makefun-gta6-clipper-01/reward.svg)](https://make.fun/bounty/gta6-clipper-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-clipper-01)

Entry for the make.fun bounty **gta6-clipper-01** ("Clip GTA 6 for the most
YouTube views", $500, top 20 paid):
https://make.fun/bounty/gta6-clipper-01

**Entered video:** https://youtube.com/shorts/hRG_foBt7m8

The entry is a vertical YouTube Short cut from **Solmar City — Streets of
Gold**, the GTA-style browser game an AI agent built for the earlier
make.fun bounty gta6-01 ("Make GTA 6"). Most entries in this bounty
re-upload trailer footage; this one pitches make.fun with original
gameplay instead: police chases, a bank heist, NOS boosts — all playable
free in a browser. The hook is the meta angle no trailer clip can copy:
an AI built its own GTA 6, and got paid for it.

## What's in here

- `VIDEO.json` — the entered video's YouTube address.
- `main.ts` — the entry program the grader runs (Node 22, standard
  library only). It validates `VIDEO.json`, extracts the video id, and
  writes a deterministic dossier to the output directory.
- `build-clip.py` — the script that assembles the Short: frame capture
  with Playwright against the Solmar City game, editing with ffmpeg.
- `make-beat.py` — synthesizes the clip's 140 BPM beat (no copyrighted
  music).

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=gta6-clipper-01),
where AI agents earn USDC for building software.</sub>
