#!/usr/bin/env python3
"""
make_slides.py — render 1920x1080 congress slide PNGs with Pillow.

WHY Pillow: exact text layout, consistent theming, easy word-wrap. Slides are
later encoded to short video clips and concatenated with the surgical segments.

BLIND SUBMISSION: keep the TITLE and CREDITS slides free of author name,
institution, city, or logo. Author data goes in the submission form, not here.

USAGE:
  python3 make_slides.py <OUT_DIR> [slides.json]

If slides.json is omitted, the SLIDES dict below is used — edit it in place.
slides.json (optional) shape:
  {
    "title": "….",            "context_header": "POR QUE IMPORTA",
    "subtitle": "Relato em vídeo",
    "congress": "26º Congresso Brasileiro de Cirurgia Bariátrica e Metabólica",
    "edition": "Vídeo Livre · 2026",
    "case": ["bullet 1", "bullet 2", ...],
    "context": ["bullet 1", ...],
    "takehome": ["msg 1", "msg 2", "msg 3"]
  }
Adjust palette in THEME if desired. No author/institution fields on purpose.
"""
import json, os, sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1920, 1080
THEME = dict(BG=(13,27,42), BG2=(20,40,60), ACCENT=(42,157,140),
            ACCENT2=(233,196,106), WHITE=(240,244,248), MUTE=(168,185,200))
FDIR = "/usr/share/fonts/truetype/dejavu"
BOLD, REG, OBL = "DejaVuSans-Bold.ttf", "DejaVuSans.ttf", "DejaVuSans-Oblique.ttf"

def F(name, size): return ImageFont.truetype(os.path.join(FDIR, name), size)

def base():
    img = Image.new("RGB", (W, H), THEME["BG"]); d = ImageDraw.Draw(img)
    for y in range(H):
        t = y / H
        d.line([(0,y),(W,y)], fill=tuple(int(THEME["BG"][i]+(THEME["BG2"][i]-THEME["BG"][i])*t) for i in range(3)))
    d.rectangle([0,0,W,12], fill=THEME["ACCENT"]); d.rectangle([0,H-12,W,H], fill=THEME["ACCENT"])
    return img, d

def wrap(d, text, font, mw):
    out, cur = [], ""
    for w in text.split():
        test = (cur+" "+w).strip()
        if d.textlength(test, font=font) <= mw: cur = test
        else: out.append(cur); cur = w
    if cur: out.append(cur)
    return out

def draw_wrapped(d, text, font, x, y, mw, fill, lh):
    for ln in wrap(d, text, font, mw): d.text((x,y), ln, font=font, fill=fill); y += lh
    return y

def bullets(d, items, x, y, mw, font, fill, lh, gap):
    for it in items:
        d.ellipse([x,y+18,x+16,y+34], fill=THEME["ACCENT"])
        y = draw_wrapped(d, it, font, x+40, y, mw-40, fill, lh) + gap
    return y

def render(cfg, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    C = THEME
    # 1 — Title (BLIND)
    img, d = base()
    d.text((160,120), cfg["congress"].upper(), font=F(BOLD,30), fill=C["ACCENT2"])
    d.text((160,162), cfg["edition"], font=F(REG,28), fill=C["MUTE"])
    y = draw_wrapped(d, cfg["title"], F(BOLD,66), 160, 320, W-320, C["WHITE"], 84)
    d.rectangle([160,y+34,340,y+42], fill=C["ACCENT"])
    d.text((160,y+80), cfg.get("subtitle","Relato em vídeo"), font=F(REG,36), fill=C["ACCENT2"])
    img.save(os.path.join(out_dir,"SLIDE_1_titulo.png"))
    # 2 — Case
    img, d = base()
    d.text((160,110), "CASO CLÍNICO", font=F(BOLD,42), fill=C["ACCENT"])
    d.rectangle([160,172,280,180], fill=C["ACCENT2"])
    bullets(d, cfg.get("case",[]), 160, 260, W-320, F(REG,38), C["WHITE"], 50, 34)
    img.save(os.path.join(out_dir,"SLIDE_2_caso.png"))
    # 3 — Context
    img, d = base()
    d.text((160,110), cfg.get("context_header","POR QUE IMPORTA"), font=F(BOLD,42), fill=C["ACCENT"])
    d.rectangle([160,172,280,180], fill=C["ACCENT2"])
    bullets(d, cfg.get("context",[]), 160, 260, W-320, F(REG,38), C["WHITE"], 50, 34)
    img.save(os.path.join(out_dir,"SLIDE_3_contexto.png"))
    # 4 — Take-home
    img, d = base()
    d.text((160,110), "MENSAGENS FINAIS", font=F(BOLD,42), fill=C["ACCENT"])
    d.rectangle([160,172,280,180], fill=C["ACCENT2"])
    bullets(d, cfg.get("takehome",[]), 160, 280, W-320, F(REG,42), C["WHITE"], 56, 44)
    img.save(os.path.join(out_dir,"SLIDE_4_takehome.png"))
    # 5 — Credits (BLIND)
    img, d = base(); cy = 340
    d.text((160,cy), "Obrigado", font=F(BOLD,80), fill=C["WHITE"])
    d.rectangle([160,cy+124,340,cy+132], fill=C["ACCENT"])
    d.text((160,cy+176), cfg["congress"], font=F(BOLD,32), fill=C["ACCENT2"])
    d.text((160,cy+224), cfg["edition"], font=F(REG,28), fill=C["MUTE"])
    img.save(os.path.join(out_dir,"SLIDE_5_creditos.png"))
    print("Slides written to", out_dir)

# ---- Edit these defaults, or pass a slides.json ----
SLIDES = {
    "congress": "26º Congresso Brasileiro de Cirurgia Bariátrica e Metabólica",
    "edition":  "Vídeo Livre · 2026",
    "title":    "Título do trabalho (sem autor/instituição)",
    "subtitle": "Relato em vídeo",
    "context_header": "POR QUE IMPORTA",
    "case":     ["Idade/sexo · procedimento prévio", "Quadro clínico", "Exame de imagem"],
    "context":  ["Contexto/epidemiologia", "Mecanismo", "Relevância clínica"],
    "takehome": ["Mensagem 1", "Mensagem 2", "Mensagem 3"],
}

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "./_SLIDES"
    cfg = SLIDES
    if len(sys.argv) > 2:
        with open(sys.argv[2], encoding="utf-8") as fh: cfg = {**SLIDES, **json.load(fh)}
    render(cfg, out)
