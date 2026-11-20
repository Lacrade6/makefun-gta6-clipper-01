#!/usr/bin/env python3
"""Generate a 16s driving beat (140 BPM) for the gta6-clipper-01 Short.

Kick + hats + sub-bass, synthesized from scratch (no samples), written as
44.1kHz 16-bit stereo WAV. Deliberately simple and punchy: it sits under
burned-in captions, so it stays at a modest level.
"""
import math
import random
import struct
import wave

SR = 44100
DUR = 16.0
BPM = 140.0
BEAT = 60.0 / BPM  # 0.4286s
N = int(SR * DUR)
buf = [0.0] * N
random.seed(7)


def add(start_s, samples, gain=1.0):
    i0 = int(start_s * SR)
    for i, s in enumerate(samples):
        j = i0 + i
        if 0 <= j < N:
            buf[j] += s * gain


def kick():
    n = int(0.14 * SR)
    out = []
    phase = 0.0
    for i in range(n):
        t = i / SR
        freq = 45 + 115 * math.exp(-t * 30)
        phase += 2 * math.pi * freq / SR
        env = math.exp(-t * 22)
        out.append(math.sin(phase) * env)
    return out


def hat(open_hat=False):
    n = int((0.09 if open_hat else 0.04) * SR)
    out = []
    last = 0.0
    for i in range(n):
        t = i / SR
        noise = random.uniform(-1, 1)
        hp = noise - 0.92 * last  # crude highpass
        last = noise
        env = math.exp(-t * (40 if open_hat else 90))
        out.append(hp * env * 0.5)
    return out


def bass(freq, dur=0.2):
    n = int(dur * SR)
    out = []
    for i in range(n):
        t = i / SR
        env = min(1.0, t * 40) * math.exp(-t * 6)
        out.append((math.sin(2 * math.pi * freq * t) + 0.3 * math.sin(4 * math.pi * freq * t)) * env)
    return out


K = kick()
H = hat()
HO = hat(open_hat=True)

# Chord roots per bar: Am F C G (2 bars each over 16s at 140bpm = ~9.3 bars; loop the 4)
roots = [55.0, 43.65, 65.41, 49.0]
bar = BEAT * 4
n_bars = int(DUR / bar) + 1

for b in range(n_bars):
    t0 = b * bar
    root = roots[b % 4]
    for beat in range(4):
        add(t0 + beat * BEAT, K, 0.9)
        add(t0 + beat * BEAT + BEAT / 2, H, 0.5)
    # bass 8ths with a driving accent pattern
    for e in range(8):
        if e in (0, 3, 4, 6):
            add(t0 + e * BEAT / 2, bass(root), 0.55)
    if b % 2 == 1:
        add(t0 + 3.5 * BEAT, HO, 0.45)

# Riser into the end card (12.4s -> 14.2s): rising filtered noise, quiet.
riser_start = int(12.4 * SR)
riser_len = int(1.8 * SR)
last = 0.0
for i in range(riser_len):
    j = riser_start + i
    if j >= N:
        break
    frac = i / riser_len
    noise = random.uniform(-1, 1)
    lp = 0.05 + 0.85 * frac  # opens up over time
    last = last + lp * (noise - last)
    buf[j] += last * frac * 0.18

# Final hit at 14.2s (end card), then let the tail decay.
add(14.2, K, 1.0)

# Soft-clip and write stereo.
peak = max(abs(s) for s in buf) or 1.0
scale = 0.85 / peak
frames = bytearray()
for s in buf:
    v = int(max(-1.0, min(1.0, s * scale)) * 32767)
    frames += struct.pack('<hh', v, v)

with wave.open('/home/hatch/workspace/makefun/gta6-clipper-01/clipper-beat.wav', 'wb') as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(bytes(frames))
print(f"wrote clipper-beat.wav peak={peak:.2f}")
