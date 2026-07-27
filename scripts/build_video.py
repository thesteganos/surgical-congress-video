#!/usr/bin/env python3
"""
build_video.py — assemble a congress surgical video from a segment spec.

Encodes each slide and each surgical segment to a matching intermediate clip,
then concatenates them (concat demuxer, -c copy). Runs in STAGES so no single
call exceeds the ~45 s sandbox timeout.

WHY STAGES: a long 1080p segment can take >45 s to encode, and background jobs do
NOT survive between sandbox calls. So encode a few pieces per call, re-running
until all exist (the script skips pieces already done), then concat.

SPEC (JSON):
{
  "workdir": "/tmp/build",
  "slides_dir": "/path/_SLIDES",
  "slide_durations": {"SLIDE_1_titulo":6,"SLIDE_2_caso":11,"SLIDE_3_contexto":8,
                       "SLIDE_4_takehome":10,"SLIDE_5_creditos":6},
  "intro_slides": ["SLIDE_1_titulo","SLIDE_2_caso","SLIDE_3_contexto"],
  "outro_slides": ["SLIDE_4_takehome","SLIDE_5_creditos"],
  "segments": [
    {"file":"…/VID003.mp4","start":150,"dur":25,"speed":1.4,"caption":"Inventário da cavidade"},
    {"file":"…/VID004.mp4","start":95,"dur":115,"speed":1.6,"caption":"Redução (~40 cm)"}
  ]
}

COMMANDS:
  python3 build_video.py spec.json slides            # encode all slide clips
  python3 build_video.py spec.json segments 0 3      # encode segments[0:3]
  python3 build_video.py spec.json segments 3 6      # …next batch (≈2-3 heavy/call)
  python3 build_video.py spec.json concat out.mp4    # stitch everything
  python3 build_video.py spec.json downscale out.mp4 720 small.mp4   # re-encode in thirds

Encoding: 1080p, 30 fps, libx264 ultrafast, crf 23, capped at 8 Mbit/s so peaks
don't bloat the file and each call stays under the timeout. Captions avoid ':'.
"""
import json, os, subprocess, sys

ENC = ("-c:v libx264 -preset ultrafast -crf 23 -maxrate 8M -bufsize 16M "
       "-pix_fmt yuv420p -r 30 -an -video_track_timescale 30000").split()
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

def run(args):
    subprocess.run(args, check=True)

def dur_of(path):
    out = subprocess.run(["ffprobe","-v","error","-show_entries","format=duration",
        "-of","default=nk=1:nw=1",path], capture_output=True, text=True).stdout.strip()
    return float(out) if out else 0.0

def slide_clip(spec, name, out):
    if os.path.exists(out): print("skip", os.path.basename(out)); return
    png = os.path.join(spec["slides_dir"], name + ".png")
    t = str(spec["slide_durations"][name])
    run(["ffmpeg","-y","-hide_banner","-loglevel","error","-loop","1","-t",t,"-i",png,
         "-vf","scale=1920:1080,fps=30,format=yuv420p", *ENC, out])
    print("ok", os.path.basename(out))

def seg_clip(seg, out):
    if os.path.exists(out): print("skip", os.path.basename(out)); return
    cap = seg.get("caption","").replace(":", " ").replace("'", "")
    sp = seg.get("speed", 1.0)
    vf = (f"setpts=(PTS-STARTPTS)/{sp},"
          "scale=1920:1080:force_original_aspect_ratio=decrease,"
          "pad=1920:1080:(ow-iw)/2:(oh-ih)/2:color=black,fps=30,"
          f"drawtext=fontfile={FONT}:text='{cap}':x=(w-tw)/2:y=h-118:"
          "fontsize=40:fontcolor=white:box=1:boxcolor=0x0d1b2aCC:boxborderw=22,"
          "format=yuv420p")
    run(["ffmpeg","-y","-hide_banner","-loglevel","error","-ss",str(seg["start"]),
         "-t",str(seg["dur"]),"-i",seg["file"],"-vf",vf, *ENC, out])
    print("ok", os.path.basename(out), f"({seg['dur']}s @ {sp}x)")

def piece_list(spec):
    wd = spec["workdir"]
    pieces = [os.path.join(wd, f"s_{n}.mp4") for n in spec["intro_slides"]]
    pieces += [os.path.join(wd, f"seg_{i:03d}.mp4") for i in range(len(spec["segments"]))]
    pieces += [os.path.join(wd, f"s_{n}.mp4") for n in spec["outro_slides"]]
    return pieces

def main():
    spec = json.load(open(sys.argv[1], encoding="utf-8"))
    cmd = sys.argv[2]
    wd = spec["workdir"]; os.makedirs(wd, exist_ok=True)
    if cmd == "slides":
        for n in spec["intro_slides"] + spec["outro_slides"]:
            slide_clip(spec, n, os.path.join(wd, f"s_{n}.mp4"))
    elif cmd == "segments":
        a, b = int(sys.argv[3]), int(sys.argv[4])
        for i in range(a, b):
            seg_clip(spec["segments"][i], os.path.join(wd, f"seg_{i:03d}.mp4"))
    elif cmd == "concat":
        out = sys.argv[3]
        lst = os.path.join(wd, "concat.txt")
        with open(lst, "w") as fh:
            for p in piece_list(spec): fh.write(f"file '{p}'\n")
        run(["ffmpeg","-y","-hide_banner","-loglevel","error","-f","concat","-safe","0",
             "-i",lst,"-c","copy","-movflags","+faststart",out])
        d = dur_of(out); print(f"{out}: {d:.1f}s = {int(d//60)}m{int(d%60):02d}s")
    elif cmd == "downscale":
        src, height, out = sys.argv[3], int(sys.argv[4]), sys.argv[5]
        total = dur_of(src); third = total/3 + 1
        parts = []
        enc = ("-c:v libx264 -preset ultrafast -crf 26 -maxrate 2000k -bufsize 4000k "
               "-pix_fmt yuv420p -r 30 -an -video_track_timescale 30000").split()
        for k in range(3):
            p = os.path.join(wd, f"ds_{height}_{k}.mp4"); parts.append(p)
            if os.path.exists(p): print("skip", os.path.basename(p)); continue
            args = ["ffmpeg","-y","-hide_banner","-loglevel","error","-ss",str(k*third)]
            if k < 2: args += ["-t", str(third)]
            args += ["-i",src,"-vf",f"scale=-2:{height}", *enc, p]
            run(args); print("ok", os.path.basename(p))
        lst = os.path.join(wd, f"ds_{height}.txt")
        with open(lst,"w") as fh:
            for p in parts: fh.write(f"file '{p}'\n")
        run(["ffmpeg","-y","-hide_banner","-loglevel","error","-f","concat","-safe","0",
             "-i",lst,"-c","copy","-movflags","+faststart",out])
        d = dur_of(out); print(f"{out}: {d:.1f}s ({height}p)")
    else:
        print(__doc__); sys.exit(1)

if __name__ == "__main__":
    main()
