# ffmpeg + sandbox notes

Hard-won details for editing surgical video inside a time-limited sandbox. Skim
this before running ffmpeg — most of these caused real retries.

## Table of contents
- Sandbox timeouts (the 45 s rule)
- Copying large files to the user's folder
- Fast thumbnail extraction
- Speed-up (setpts)
- Captions with drawtext (colon trap)
- Concatenation (concat demuxer -c copy)
- Presets, bitrate, and file size
- Verification

## Sandbox timeouts (the 45 s rule)
Each shell call is killed around 45 s, and **background jobs (`nohup … &`) do NOT
survive between calls** — the child is reaped when the call returns. So:
- Encode in small batches (≈2–3 heavy 1080p segments, or ≤~130 s of source input,
  per call). Measure once with `time` and calibrate.
- Make encode steps **idempotent** (skip outputs that already exist) so you can
  re-run the same command until everything is built. `build_video.py` does this.
- Decoding is cheap; **encoding** is the cost. A weird `r_frame_rate` like 125/1
  is usually a metadata quirk — decoding is still fast; don't panic.

## Copying large files to the user's folder
The mounted user folder writes at only ~5 MB/s, so a 300–400 MB file won't copy
in one call. Two options:
- **Deliver a smaller re-encode** (e.g. 720p ~90 MB copies in ~20 s).
- **Copy the big file in `dd` chunks** (preserves quality, byte-identical):
  ```bash
  SZ=$(stat -c%s BIG.mp4)   # e.g. 380 MB
  dd if=BIG.mp4 of=DEST.mp4 bs=1M count=175            conv=notrunc   # call 1
  dd if=BIG.mp4 of=DEST.mp4 bs=1M skip=175 seek=175 count=120 conv=notrunc  # call 2
  dd if=BIG.mp4 of=DEST.mp4 bs=1M skip=295 seek=295          conv=notrunc  # call 3 (rest)
  cmp BIG.mp4 DEST.mp4 && echo OK   # verify identical
  ```
  Keep each chunk under ~190 MB so it finishes inside one call.
- Deleting a user file may fail with "Operation not permitted" — request delete
  permission via the delete-enable tool rather than reporting it as impossible.

## Fast thumbnail extraction
Seek with `-ss` **before** `-i` (input/keyframe seek) — near-instant even on 1 GB
files. `-vf fps=1/20` decodes the whole file instead; avoid it for sampling.
```bash
ffmpeg -ss $T -i clip.mp4 -frames:v 1 -vf scale=384:-1 thumb.jpg
```

## Speed-up (setpts)
Drop presentation timestamps proportionally; reset to zero at the cut:
```
setpts=(PTS-STARTPTS)/1.6     # 1.6× faster
```
Keep decisive/diagnostic moments at 1.0×; speed the long inventory/dissection
stretches 1.3–1.8× to fit the time limit. This is normal in surgical videos.

## Captions with drawtext (colon trap)
The `:` character separates options inside a filtergraph, so a caption or
timestamp containing `:` is **silently truncated**. Use a colon-free label
(`2m20s`, not `2:20`) or escape it. Also strip `'` from captions. Lower-third
box:
```
drawtext=fontfile=$FONT:text='Redução (~40 cm)':x=(w-tw)/2:y=h-118:\
fontsize=40:fontcolor=white:box=1:boxcolor=0x0d1b2aCC:boxborderw=22
```

## Concatenation (concat demuxer -c copy)
`-c copy` is instant but requires every piece to share codec parameters
(resolution, pixel format, profile/level, timebase). So encode **all** pieces —
slides and segments — with the **same** settings (same scale, `-pix_fmt
yuv420p`, `-r 30`, `-video_track_timescale 30000`). If you regenerate one slide,
re-encode it with those same params before re-concatenating. Mismatched params
produce a glitchy or broken join.
```bash
printf "file '/tmp/a.mp4'\nfile '/tmp/b.mp4'\n" > list.txt
ffmpeg -f concat -safe 0 -i list.txt -c copy -movflags +faststart out.mp4
```

## Presets, bitrate, and file size
- `ultrafast` is the fast path that fits the timeout, but it's inefficient →
  cap size with `-maxrate 8M -bufsize 16M` (VBV-capped CRF).
- `veryfast`/`faster` look better per byte but often blow the 45 s budget on
  long 1080p segments — reserve them for short clips, or split the input.
- Deliver 1080p (quality) and a downscaled 720p (upload/backup). Confirm the
  congress's max file size; if the 1080p exceeds it, the 720p is the fallback.

## Verification
Before handing off, extract frames across the whole timeline into one contact
sheet and look:
```bash
i=0; for t in 3 12 21 34 75 120 175 235 300 340 380 398; do
  ffmpeg -ss $t -i FINAL.mp4 -frames:v 1 -vf scale=440:-1 chk/$(printf %02d $i).jpg; i=$((i+1)); done
ffmpeg -framerate 1 -i chk/%02d.jpg -frames:v 1 -vf tile=4x3:padding=5:color=white chk_sheet.png
```
Check: slides present and **blind** (no author/institution), captions correct,
transitions clean, total duration under the limit.
