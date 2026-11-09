"""Render a 5-slide Instagram carousel (1080x1350) for a CertsClub exam post.

Usage: python3 render.py content.json outdir [style]
style: navy | split | card | random (default random)
"""
import json, os, random, sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1350
FD = "/usr/share/fonts/opentype/inter/"
F = lambda w, s: ImageFont.truetype(FD + f"Inter-{w}.otf", s)
URL = "www.certsclub.com"

STYLES = {
    # bg, text, muted, accent, panel
    "navy":  dict(bg="#0B1B33", fg="#FFFFFF", mu="#A9B8CF", ac="#3BA4FF", pa="#12284A"),
    "split": dict(bg="#FFFFFF", fg="#0B1B33", mu="#55647A", ac="#1F6FEB", pa="#EEF4FF"),
    "card":  dict(bg="#0E2A52", fg="#FFFFFF", mu="#B8C7DD", ac="#5CC8FF", pa="#163A6B"),
}


def wrap(d, text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines


def block(d, xy, text, font, fill, maxw, gap=1.25):
    x, y = xy
    for ln in wrap(d, text, font, maxw):
        d.text((x, y), ln, font=font, fill=fill)
        y += int(font.size * gap)
    return y


def base(s, idx, total):
    im = Image.new("RGB", (W, H), s["bg"]); d = ImageDraw.Draw(im)
    if s is STYLES["split"]:
        d.rectangle([0, 0, W, 18], fill=s["ac"])
    elif s is STYLES["card"]:
        d.rounded_rectangle([60, 60, W - 60, H - 60], 40, fill=s["pa"])
    # slide counter + progress
    d.text((W - 100, 96), f"{idx}/{total}", font=F("Medium", 30), fill=s["mu"], anchor="ra")
    seg = (W - 200) / total
    for i in range(total):
        d.rounded_rectangle([100 + i * seg + 4, H - 110, 100 + (i + 1) * seg - 4, H - 104], 3,
                            fill=s["ac"] if i < idx else s["pa"] if s is not STYLES["card"] else s["bg"])
    return im, d


def title(d, s, text, y=200):
    d.rectangle([100, y, 180, y + 10], fill=s["ac"])
    return block(d, (100, y + 50), text, F("Bold", 76), s["fg"], W - 200, 1.15) + 50


def render(c, out, style):
    s = STYLES[style]; os.makedirs(out, exist_ok=True); N = 5; paths = []
    # 1 cover
    im, d = base(s, 1, N)
    d.text((100, 300), c["vendor"].upper(), font=F("SemiBold", 34), fill=s["ac"])
    y = block(d, (100, 370), c["name"], F("Black", 104), s["fg"], W - 200, 1.08)
    d.rounded_rectangle([100, y + 40, 100 + d.textlength(c["code"], font=F("Bold", 44)) + 60, y + 130], 18, fill=s["ac"])
    d.text((130, y + 85), c["code"], font=F("Bold", 44), fill="#FFFFFF", anchor="lm")
    block(d, (100, y + 200), c["hook"], F("Regular", 42), s["mu"], W - 200)
    d.text((100, H - 200), "Swipe  →", font=F("SemiBold", 38), fill=s["fg"])
    paths.append(im)
    # 2 at a glance
    im, d = base(s, 2, N); y = title(d, s, "Exam at a glance")
    for k, v in c["facts"]:
        d.text((100, y), k.upper(), font=F("SemiBold", 28), fill=s["ac"])
        y = block(d, (100, y + 42), v, F("SemiBold", 46), s["fg"], W - 200) + 34
    paths.append(im)
    # 3 domains
    im, d = base(s, 3, N); y = title(d, s, "Exam domains")
    n = len(c["domains"])
    fs, gap = (40, 60) if n <= 6 else (34, 40) if n <= 8 else (30, 30)
    if n > 6: y -= 20
    mx = max(float(p.strip("%")) for _, p in c["domains"])
    for name, pct in c["domains"]:
        d.text((W - 100, y + 2), pct, font=F("Bold", fs), fill=s["ac"], anchor="ra")
        y2 = block(d, (100, y), name, F("SemiBold", fs), s["fg"], W - 340, 1.2)
        frac = float(pct.strip("%")) / mx
        d.rounded_rectangle([100, y2 + 4, W - 100, y2 + 14], 5, fill=s["pa"] if s is not STYLES["card"] else s["bg"])
        d.rounded_rectangle([100, y2 + 4, 100 + (W - 200) * frac, y2 + 14], 5, fill=s["ac"])
        y = y2 + gap
    paths.append(im)
    # 4 tips
    im, d = base(s, 4, N); y = title(d, s, "How to prepare")
    for i, t in enumerate(c["tips"], 1):
        d.ellipse([100, y, 160, y + 60], fill=s["ac"])
        d.text((130, y + 30), str(i), font=F("Bold", 32), fill="#FFFFFF", anchor="mm")
        y = block(d, (190, y + 6), t, F("Medium", 40), s["fg"], W - 290) + 40
    paths.append(im)
    # 5 CTA
    im, d = base(s, 5, N)
    y = block(d, (100, 360), c.get("cta", "Practice with real exam-style questions"), F("Bold", 80), s["fg"], W - 200, 1.12)
    y = block(d, (100, y + 40), f"Detailed explanations for every {c['code']} question.", F("Regular", 42), s["mu"], W - 200)
    d.rounded_rectangle([100, y + 80, W - 100, y + 200], 60, fill=s["ac"])
    d.text((W / 2, y + 140), URL, font=F("Bold", 52), fill="#FFFFFF", anchor="mm")
    paths.append(im)
    files = []
    for i, im in enumerate(paths, 1):
        p = os.path.join(out, f"slide{i}.jpg"); im.save(p, quality=93); files.append(p)
    return files


if __name__ == "__main__":
    c = json.load(open(sys.argv[1])); out = sys.argv[2]
    st = sys.argv[3] if len(sys.argv) > 3 else "random"
    if st == "random": st = random.choice(list(STYLES))
    print(st); print("\n".join(render(c, out, st)))
