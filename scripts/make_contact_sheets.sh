#!/bin/bash
# make_contact_sheets.sh — thumbnail mosaic (contact sheet) per video clip.
#
# WHY: The surgeon marks the key moments by looking at a grid of timestamped
# thumbnails instead of re-scrubbing 30–60 min of footage. One frame every
# INTERVAL seconds, timestamp burned in, tiled COLS wide.
#
# USAGE:
#   bash make_contact_sheets.sh <SRC_DIR> <OUT_DIR> [INTERVAL_SEC] [COLS]
# EXAMPLE:
#   bash make_contact_sheets.sh "/path/CIRURGIA X" "/path/CIRURGIA X/_MOSAICOS" 20 5
#
# NOTES:
#  - Uses fast INPUT seeking (-ss before -i) so even 1 GB clips are quick.
#  - Label format is "MmSSs" (e.g. 2m20s). Do NOT use "mm:ss": the ':' is a
#    special char in ffmpeg filtergraphs and silently truncates the label.
#  - Processes every *.mp4/*.mov/*.mkv in SRC_DIR. View the sheets, then ask
#    the surgeon for keep-ranges per clip.

set -e
SRC="${1:?SRC_DIR required}"
OUT="${2:?OUT_DIR required}"
INT="${3:-20}"
COLS="${4:-5}"
FONT="$(fc-match -f '%{file}' 'DejaVu Sans:bold' 2>/dev/null || echo /usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf)"
mkdir -p "$OUT"

shopt -s nullglob nocaseglob
for f in "$SRC"/*.mp4 "$SRC"/*.mov "$SRC"/*.mkv "$SRC"/*.avi; do
  tag="$(basename "${f%.*}")"
  dur="$(ffprobe -v error -show_entries format=duration -of default=nk=1:nw=1 "$f" | cut -d. -f1)"
  [ -z "$dur" ] && continue
  d="$OUT/.thumbs_$tag"; rm -rf "$d"; mkdir -p "$d"; i=0
  for ((t=0; t<dur; t+=INT)); do
    lbl="$(printf '%dm%02ds' $((t/60)) $((t%60)))"
    n="$(printf '%03d' $i)"
    ffmpeg -y -hide_banner -loglevel error -ss "$t" -i "$f" -frames:v 1 \
      -vf "scale=384:-1,drawtext=fontfile=$FONT:text='$lbl':x=6:y=6:fontsize=24:fontcolor=yellow:box=1:boxcolor=black@0.7:boxborderw=5" \
      "$d/$n.jpg" 2>/dev/null
    i=$((i+1))
  done
  rows=$(( (i + COLS - 1) / COLS ))
  ffmpeg -y -hide_banner -loglevel error -framerate 1 -i "$d/%03d.jpg" -frames:v 1 \
    -vf "tile=${COLS}x${rows}:padding=4:color=white" "$OUT/SHEET_$tag.png" 2>/dev/null
  rm -rf "$d"
  echo "SHEET_$tag.png  ($i thumbs, ${dur}s)"
done
echo "Done. Sheets in: $OUT"
