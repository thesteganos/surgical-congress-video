---
name: surgical-congress-video
description: >-
  Produce a blinded surgical "vídeo livre" for a medical congress from raw
  operating-room footage. Use whenever the user wants to edit, condense, caption
  or assemble surgical/laparoscopic/endoscopic video for a scientific meeting —
  SBCBM vídeo livre, tema livre em vídeo, cutting long OR recordings to a time
  limit, title/credits slides and legendas, anonymizing footage for blind review,
  exporting 720p/1080p. Also use for the companion abstract (PT/EN) grounded in
  the literature, a shot-by-shot roteiro, reading the congress edital to extract
  the rules (time limit, blind submission, format, deadline), or a submission
  checklist. Trigger on partial requests too: "corta esse vídeo de cirurgia pra 7
  minutos", "monta os slides do vídeo do congresso", "deixar o vídeo anônimo pra
  submeter", "regras do edital pro vídeo livre", "escreve o resumo do meu vídeo".
---

# Surgical congress video ("vídeo livre")

## What this skill produces

A submission-ready surgical video for a scientific congress, plus its written
companions. A complete job usually delivers:

1. The **edited video** (≤ the congress time limit), with title + credits
   slides and on-screen **legendas** describing each surgical step.
2. Two export resolutions (**720p** for easy upload, **1080p** for quality).
3. A **structured abstract** in Portuguese and English (for the site form and,
   often, an *Obesity Surgery*-style supplement).
4. A **roteiro** (shot list with timestamps) and slide texts.
5. A **submission checklist**.

The surgeon owns the medicine and the footage; your job is to turn ~30–60 min of
raw OR video into a tight, anonymous, well-captioned narrative and to remove
every technical obstacle (long encodes, huge files, identifying data).

Two steps carry most of the risk and come first: **reading the edital** (the
rules decide the runtime, the anonymity requirement, and the export formats) and
**searching the literature** (it supplies the abstract's introduction and
conclusion and the context slide). Skipping either produces work that has to be
redone.

## The hard constraints that shape everything

Two things dominate the technical approach — internalize them:

- **Sandbox calls time out around 45 s.** A single ffmpeg encode of a long
  1080p segment can exceed this. So: encode in **small chunks**, never rely on
  background jobs (they don't survive between calls), and prefer fast presets.
- **Copying to the user's folder is slow (~5 MB/s).** A 300–400 MB 1080p file
  won't copy in one call. Deliver a smaller re-encode, or copy the big file in
  **`dd` chunks** (see references).

Read `references/ffmpeg_and_sandbox_notes.md` before touching ffmpeg — it has the
exact commands and the non-obvious gotchas (drawtext colon escaping, keyframe
seeking, concat-copy parameter matching). It will save you a lot of retries.

## Workflow

Do these roughly in order, but adapt. Steps 1–2 come first and unblock everything
else; steps 3–5 can be drafted while the surgeon supplies the remaining case data.

### 1. Read the edital (rules) first — it dictates the whole edit

Do this before writing or cutting anything. Every downstream decision — how hard
you compress the footage, what goes on the slides, which files you export — comes
from the regulation. Getting it late means redoing work (in one real case the
blind-submission rule was discovered after delivery, forcing the title and
credits slides to be rebuilt and the video re-exported).

Extract and **write these into the master document** so they're checkable later:

| Item | Why it matters |
|---|---|
| **Time limit** (often ~7 min) | Sets how aggressively you condense / speed up |
| **Blind submission?** | If yes, *no* author, institution, city, or logo anywhere in the video — the most common disqualifier. Treat as required unless the text clearly says otherwise |
| **Format / resolution / fps** | Drives export settings |
| **Max file size**, upload vs. link | Decides whether 1080p is deliverable or 720p is the fallback |
| **Deadline** | Plan the work backwards from it |
| Abstract language(s) (PT and/or EN), word limits | Some congresses publish abstracts in an English supplement |
| Category (vídeo livre, competition track) and prizes | May carry extra rules |

**Getting the text is often the hard part.** Congress sites are frequently
JavaScript-rendered: a plain fetch returns an empty shell. Escalate in this
order — (1) plain fetch, (2) a browser tool that executes JavaScript, (3) ask the
surgeon to paste the regulation text or send a screenshot. If you can't read it,
**say so explicitly** and mark the affected fields as unconfirmed rather than
guessing; never present an assumed limit as fact.

**Deadlines move.** A date found in search results may be stale — extensions are
common and often announced only in a news post or on social media. Confirm the
current deadline with the surgeon or the organizing committee (there is usually a
scientific-committee e-mail on the site) and re-check before submitting.

### 2. Search the literature — it grounds the abstract and the context slide

A congress video is a scientific communication, not just footage. The evidence
base gives you the abstract's *Introdução* and *Conclusão*, the "why it matters"
slide, and the justification for the technique chosen — which is what
distinguishes a strong entry from a screen recording.

Search PubMed (or the literature tools available) for the specific entity and
pull out:

- **Incidence / epidemiology** — how rare is it, in what population.
- **Mechanism / pathophysiology** — including where the literature is uncertain.
- **Typical presentation and diagnostic test of choice** — lets you frame the
  case's imaging finding as classic or atypical.
- **Management options and their outcomes** — especially *recurrence rates by
  technique*, since that is what justifies the operative decision.
- **Risk factors** — often lets you point out that this patient fits (or doesn't
  fit) the classic profile, which makes the case more instructive.

Two things to get right:

- **Let the evidence match what was actually done.** Write the conclusion around
  the technique the surgeon performed, presenting alternatives as reserved for
  other scenarios. If the literature mildly favours a different approach, present
  it as individualized decision-making rather than contradicting the surgeon's
  operation in their own video.
- **Cite properly.** Keep full references with **DOIs** in the master document
  (the surgeon may need them for the abstract or discussion), and attribute the
  source database as its terms require.

### 3. Gather the case data

Collect: demographics (age, sex), index procedure + date, relevant
antropometrics (e.g. BMI before/after, %total weight loss), presentation, imaging
report, **operative findings and the technique actually performed**, and outcome
(discharge day, culture/pathology results). Pull the history verbatim from the
chart, imaging report, and operative note the surgeon provides.

Expect this to arrive **in pieces, over several messages**. Keep updating the
master document as each piece lands, and keep a visible list of what is still
missing — it lets the surgeon fill gaps without being interviewed all at once.
Derive what you can (age from date of birth, BMI and %weight loss from weights,
interval since the index operation) and state the derivation so it can be checked.

### 4. Anonymize — this is a correctness requirement, not a nicety

- **Video:** no author name, institution, city, or logo on any slide. Patient
  name/DOB/record number must not appear. **Check the raw footage corners** at
  full resolution — many OR/endoscopy towers burn patient data into the image;
  extract a full-frame still and look before assuming it's clean.
- **Filenames/folders:** the source folder is often named after the patient.
  Don't reuse the patient's name in delivered filenames; flag it to the surgeon.
- Author/institution data belongs **only in the submission form fields**, never
  baked into the video.

### 5. Write the abstract (PT + EN), roteiro, narration, slide texts

Keep a single **master markdown document** holding: case data table, abstract
(PT + EN, structured: Introdução/Objetivo/Relato/Resultado/Conclusão), a
timestamped roteiro, the on-screen legenda text per step, and the slide texts.
As the surgeon feeds details incrementally, update this doc — it's the source of
truth that keeps the video, slides, and abstract consistent.

### 6. Let the surgeon pick the key moments — use contact-sheet mosaics

You cannot meaningfully watch 45 min of video, and the surgeon shouldn't have to
re-scrub it. Generate a **thumbnail mosaic** (contact sheet) per source clip: one
frame every ~20 s with the timestamp burned in, tiled into a grid. The surgeon
then replies with the ranges to keep, per clip (e.g. "VID004 1m35s–3m30s =
redução"). This is the fastest, lowest-friction way to drive the edit.

Use `scripts/make_contact_sheets.sh` (see its header for usage). It uses fast
keyframe seeking, so even 1 GB clips process in seconds.

### 7. Build the slides

Slides are rendered as 1920×1080 PNGs with Pillow so text layout is exact and
theming is consistent. Use `scripts/make_slides.py`, which is config-driven:
edit the `SLIDES` list (or the JSON it reads) with your title/case/context/
take-home/credits text. **Keep the title and credits slides blind** (title +
"Relato em vídeo" + congress line; credits = "Obrigado" + congress line).

### 8. Encode the segments and assemble

Drive the edit from a **segment spec** (a small JSON: source file, start,
duration, speed, caption per segment). Feed it to `scripts/build_video.py`, which:

- extracts each range with fast input seeking,
- applies a mild speed-up where asked (to fit the time limit),
- scales/pads to 1080p, burns the legenda, normalizes to 30 fps,
- encodes each piece with a fast preset + capped bitrate (fits the 45 s window),
- concatenates slides + segments with the concat demuxer (`-c copy`).

**Fitting the time limit:** sum the kept ranges. If total + slides exceeds the
limit, keep the key diagnostic/decisive moments at normal speed and apply a
gentle **1.3–1.8× speed-up** to the long inventory/dissection stretches — this is
normal and expected in surgical videos. Only cut ranges if the surgeon prefers.

The script runs in **stages** so no single invocation exceeds the timeout —
follow the "run in stages" note in its header.

### 9. Export deliverables + verify

- Build the **1080p master** by concatenating the pieces (copy, instant).
- Produce a **720p** delivery by re-encoding the master in thirds, then concat.
- Deliver the **1080p** by copying it in `dd` chunks (preserves quality) or by a
  lower-bitrate re-encode if size matters.
- **Verify** by extracting frames across the whole timeline into one contact
  sheet and eyeballing it: slides present and blind, captions correct,
  transitions clean, duration under the limit.

### 10. Hand off

Deliver the two videos + the master doc, and produce a short **submission
step-by-step** (what to have ready, blind-check, portal steps, post-submission).
Remind the surgeon that author/institution go in the form, not the video, and to
confirm format/size against the regulation.

## Bundled resources

- `scripts/make_contact_sheets.sh` — thumbnail mosaics for timestamp selection.
- `scripts/make_slides.py` — 1920×1080 slide PNGs (blind title/credits).
- `scripts/build_video.py` — encode segments from a JSON spec + concat, in stages.
- `references/ffmpeg_and_sandbox_notes.md` — the exact ffmpeg commands and the
  sandbox gotchas (timeouts, big-file copy, drawtext escaping, concat matching).

Read the script headers before running — they document arguments and the staged
execution pattern that keeps each call under the timeout.
