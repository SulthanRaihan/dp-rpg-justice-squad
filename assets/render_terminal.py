import sys
from PIL import Image, ImageDraw, ImageFont

FONT_PATH = r"C:\Windows\Fonts\CascadiaMono.ttf"
FONT_SIZE = 18
PAD_X = 24
PAD_Y = 20
TITLEBAR_H = 36
LINE_SPACING = 6
BG = (18, 18, 20)
TITLEBAR_BG = (38, 38, 40)
FG = (220, 220, 220)
GREEN = (87, 217, 138)
YELLOW = (229, 192, 90)
CYAN = (102, 196, 230)
RED = (235, 110, 110)
GREY = (140, 140, 145)

def color_for_line(line: str):
    s = line.strip()
    if s.startswith("====") :
        return CYAN
    if "JUSTICE SQUAD" in s:
        return CYAN
    if s.startswith("[ALERT]") or s.startswith("[News") or s.startswith(">>"):
        return YELLOW
    if "DEFEATED" in s or "Victory" in s or "safe." in s:
        return GREEN
    if s.startswith("[Recruit]") or s.startswith("Gear equipped"):
        return GREEN
    if s.startswith("[Undo]") or s.startswith("Undoing"):
        return RED
    if s.startswith("Actions:") or s.startswith("State:"):
        return GREY
    if s.startswith("Your choice"):
        return (255, 255, 255)
    return FG

def render(text: str, out_path: str, title: str, width_chars: int = 84):
    lines = text.split("\n")
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
    bold_font = ImageFont.truetype(r"C:\Windows\Fonts\consolab.ttf", 13)

    dummy = Image.new("RGB", (10, 10))
    d = ImageDraw.Draw(dummy)
    bbox = d.textbbox((0, 0), "M", font=font)
    char_w = bbox[2] - bbox[0]
    line_h = (bbox[3] - bbox[1]) + LINE_SPACING

    width = PAD_X * 2 + char_w * width_chars
    height = TITLEBAR_H + PAD_Y * 2 + line_h * len(lines)

    img = Image.new("RGB", (int(width), int(height)), BG)
    draw = ImageDraw.Draw(img)

    draw.rectangle([0, 0, width, TITLEBAR_H], fill=TITLEBAR_BG)
    for i, (cx, c) in enumerate([(16, (237, 106, 94)), (38, (245, 191, 79)), (60, (97, 197, 86))]):
        draw.ellipse([cx, TITLEBAR_H/2-6, cx+12, TITLEBAR_H/2+6], fill=c)
    draw.text((width/2, TITLEBAR_H/2), title, font=bold_font, fill=(225,225,225), anchor="mm")

    y = TITLEBAR_H + PAD_Y
    for line in lines:
        color = color_for_line(line)
        draw.text((PAD_X, y), line, font=font, fill=color)
        y += line_h

    img.save(out_path)
    print("saved", out_path, img.size)

if __name__ == "__main__":
    import json
    cfg = json.load(open(sys.argv[1], encoding="utf-8"))
    render(cfg["text"], cfg["out"], cfg["title"], cfg.get("width_chars", 84))
