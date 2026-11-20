#!/usr/bin/env python3
"""Assemble the gta6-clipper-01 Short (1080x1920, 30fps, ~16s).

Segments (beat-synced, captions burned in, loop ending):
  S1a 0.0-1.6s  HOOK A: drive capture (golden-hour skyline), punch-in zoom,
                "AI BIKIN GTA 6 SENDIRI?!"
  S1b 1.6-3.2s  HOOK B: chase capture (police chaos), "…dan DIBAYAR $500"
  S2  3.2-5.2s  chase continues — "Kota ini dibuat AI dalam 1 hari"
  S3  5.2-6.7s  drive tail slowed 2x — "Main di browser — GRATIS"
  S4  6.7-9.2s  heist still, Ken Burns — feature list
  S5  9.2-11.7s chase peak — "AI-nya dibayar USDC di make.fun"
  S6  11.7-14.2s title capture slowed — "$500 BOUNTY — agent AI bisa ikut!"
  S7  14.2-16.0s end card "make.fun", final 0.4s = S1a first frame (loop)
"""
import os
import subprocess
import sys

FF = 'ffmpeg'
FRAMES = '/home/hatch/workspace/makefun/gta6-clipper-01/frames'
STILLS = '/home/hatch/workspace/makefun/gta6-01/repo/screenshots'
COVER = '/home/hatch/workspace/makefun/gta6-01/v2-tmp/test-cover2.jpg'
OUT_DIR = '/home/hatch/workspace/makefun/gta6-clipper-01/segments'
FINAL = '/home/hatch/workspace/makefun/gta6-clipper-01/solmar-city-clipper.mp4'
FONT_BLACK = '/usr/share/fonts/truetype/noto/NotoSans-Black.ttf'
FONT_BOLD = '/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf'
FPS = 30

os.makedirs(OUT_DIR, exist_ok=True)


def run(args):
    print('+', ' '.join(args[:6]), '…')
    r = subprocess.run(args, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-3000:])
        sys.exit(1)


def esc(text):
    return text.replace('\\', '\\\\').replace(':', '\\:').replace("'", "\\'")


def hook_text(lines, y=280, size=118):
    """Big stacked hook text, white with heavy black outline."""
    parts = []
    for i, line in enumerate(lines):
        parts.append(
            f"drawtext=fontfile={FONT_BLACK}:text='{esc(line)}':fontsize={size}:"
            f"fontcolor=white:borderw=10:bordercolor=black:shadowcolor=black@0.6:shadowx=4:shadowy=4:"
            f"x=(w-text_w)/2:y={y + i * int(size * 1.18)}"
        )
    return ','.join(parts)


def caption(text, y=1420, size=56):
    """Bottom-third caption on a semi-transparent black box."""
    return (
        f"drawtext=fontfile={FONT_BOLD}:text='{esc(text)}':fontsize={size}:"
        f"fontcolor=white:box=1:boxcolor=black@0.55:boxborderw=22:"
        f"x=(w-text_w)/2:y={y}"
    )


# Center-crop a landscape frame to 9:16, upscale to 1080x1920, lift the
# dusk palette a touch (the chase scene renders dark).
CROP_SCALE = ('crop=ih*9/16:ih:(iw-ih*9/16)/2:0,scale=1080:1920:flags=lanczos,'
              'eq=brightness=0.05:gamma=1.12:saturation=1.25,unsharp=5:5:0.6:5:5:0.0')

segments = []

# --- S1a HOOK A: drive f000-f047 (48 frames = 1.6s), punch-in zoom 1.3 -> 1.0
run([FF, '-y', '-framerate', str(FPS), '-start_number', '0',
     '-i', f'{FRAMES}/drive/f%03d.jpg', '-frames:v', '48',
     '-vf', (f"{CROP_SCALE},"
             f"zoompan=z='if(lte(on,12),1.3-0.3*on/12,1)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps={FPS},"
             f"{hook_text(['AI BIKIN GTA 6', 'SENDIRI?!'])}"),
     '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-r', str(FPS), f'{OUT_DIR}/s1a.mp4'])
segments.append('s1a.mp4')

# --- S1b HOOK B: chase f008-f055 (48 frames = 1.6s)
run([FF, '-y', '-framerate', str(FPS), '-start_number', '8',
     '-i', f'{FRAMES}/chase/f%03d.jpg', '-frames:v', '48',
     '-vf', f"{CROP_SCALE},{hook_text(['…dan DIBAYAR', '$500'])}",
     '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-r', str(FPS), f'{OUT_DIR}/s1b.mp4'])
segments.append('s1b.mp4')

# --- S2: chase f056-f115 (60 frames = 2.0s)
run([FF, '-y', '-framerate', str(FPS), '-start_number', '56',
     '-i', f'{FRAMES}/chase/f%03d.jpg', '-frames:v', '60',
     '-vf', f"{CROP_SCALE},{caption('Kota ini dibuat AI dalam 1 hari')}",
     '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-r', str(FPS), f'{OUT_DIR}/s2.mp4'])
segments.append('s2.mp4')

def stretched_frames(src_dir, start, count, out_frames, dst_dir):
    """Copy `count` frames starting at `start` into dst_dir as out_frames
    sequential files (nearest-neighbour stretch) so a plain 30fps encode
    plays them slowed down. (setpts/fps stretching proved unreliable with
    the image2 demuxer on this ffmpeg build.)"""
    import shutil
    os.makedirs(dst_dir, exist_ok=True)
    for j in range(out_frames):
        src_idx = start + min(count - 1, int(j * count / out_frames))
        shutil.copy(f'{src_dir}/f{src_idx:03d}.jpg', f'{dst_dir}/f{j:03d}.jpg')
    return dst_dir


# --- S3: drive f048-f069 (22 frames) stretched to 44 frames (~1.47s)
s3dir = stretched_frames(f'{FRAMES}/drive', 48, 22, 44, f'{OUT_DIR}/s3frames')
run([FF, '-y', '-framerate', str(FPS), '-start_number', '0',
     '-i', f'{s3dir}/f%03d.jpg', '-frames:v', '44',
     '-vf', f"{CROP_SCALE},{caption('Main di browser — GRATIS!', size=54)}",
     '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-r', str(FPS), f'{OUT_DIR}/s3.mp4'])
segments.append('s3.mp4')

# --- S4: heist still, Ken Burns zoom-in (2.5s)
run([FF, '-y', '-loop', '1', '-i', f'{STILLS}/2-heist.jpg', '-t', '2.5',
     '-vf', (f"{CROP_SCALE},"
             f"zoompan=z='1+0.15*on/75':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=75:s=1080x1920:fps={FPS},"
             f"{caption('Heist bank • kejar-kejaran polisi • NOS')}"),
     '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-r', str(FPS), f'{OUT_DIR}/s4.mp4'])
segments.append('s4.mp4')

# --- S5: chase f116-f190 (75 frames = 2.5s)
run([FF, '-y', '-framerate', str(FPS), '-start_number', '116',
     '-i', f'{FRAMES}/chase/f%03d.jpg', '-frames:v', '75',
     '-vf', f"{CROP_SCALE},{caption('AI-nya dibayar USDC di make.fun')}",
     '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-r', str(FPS), f'{OUT_DIR}/s5.mp4'])
segments.append('s5.mp4')

# --- S6: title capture f000-f039 (40 frames) stretched to 75 frames (2.5s)
s6dir = stretched_frames(f'{FRAMES}/title', 0, 40, 75, f'{OUT_DIR}/s6frames')
run([FF, '-y', '-framerate', str(FPS), '-start_number', '0',
     '-i', f'{s6dir}/f%03d.jpg', '-frames:v', '75',
     '-vf', f"{CROP_SCALE},{caption('$500 BOUNTY — agent AI bisa ikut!')}",
     '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-r', str(FPS), f'{OUT_DIR}/s6.mp4'])
segments.append('s6.mp4')

# --- S7: end card on cover still, darkened, 1.4s + 0.4s loop frame (= S1a frame 0)
endcard = (
    f"{CROP_SCALE},eq=brightness=-0.25:saturation=1.1,"
    f"drawtext=fontfile={FONT_BLACK}:text='make.fun':fontsize=170:fontcolor=white:"
    f"borderw=12:bordercolor=black:x=(w-text_w)/2:y=760,"
    f"drawtext=fontfile={FONT_BOLD}:text='earn money with AI agents':fontsize=58:fontcolor=white:"
    f"box=1:boxcolor=black@0.55:boxborderw=20:x=(w-text_w)/2:y=990"
)
run([FF, '-y', '-loop', '1', '-i', COVER, '-t', '1.4',
     '-vf', endcard, '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-r', str(FPS), f'{OUT_DIR}/s7a.mp4'])
run([FF, '-y', '-loop', '1', '-i', f'{FRAMES}/drive/f000.jpg', '-t', '0.4',
     '-vf', f"{CROP_SCALE},{hook_text(['AI BIKIN GTA 6', 'SENDIRI?!'])}",
     '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-r', str(FPS), f'{OUT_DIR}/s7b.mp4'])
with open(f'{OUT_DIR}/s7list.txt', 'w') as f:
    f.write("file 's7a.mp4'\nfile 's7b.mp4'\n")
run([FF, '-y', '-f', 'concat', '-safe', '0', '-i', f'{OUT_DIR}/s7list.txt',
     '-c', 'copy', f'{OUT_DIR}/s7.mp4'])
segments.append('s7.mp4')

# --- Concat all + mux beat
with open(f'{OUT_DIR}/all.txt', 'w') as f:
    for s in segments:
        f.write(f"file '{s}'\n")
run([FF, '-y', '-f', 'concat', '-safe', '0', '-i', f'{OUT_DIR}/all.txt',
     '-i', '/home/hatch/workspace/makefun/gta6-clipper-01/clipper-beat.wav',
     '-c:v', 'copy', '-c:a', 'aac', '-b:a', '160k', '-shortest',
     '-movflags', '+faststart', FINAL])
print('FINAL:', FINAL)
