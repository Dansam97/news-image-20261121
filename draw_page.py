#!/usr/bin/env python3
"""Bake entry.png: one newspaper page summing up Saturday 21 November 2026.

Written for the make.fun news-image-20261121 entry. The page is drawn with
Pillow from the story data below; every figure was checked against the
day's reporting on 21 Nov 2026 and Friday's market closes are labelled
with their date. Drawing is fully deterministic: no randomness, no clock.
"""
import os
from PIL import Image, ImageDraw, ImageFont

PAGE = 1024
MARGIN = 36
INK = (20, 24, 29)
PAPER = (247, 243, 234)
ACCENT = (163, 22, 33)
SOFT = (84, 92, 102)
BAND = (24, 30, 38)
BAND_INK = (238, 240, 244)
DOWN = (255, 120, 110)
LINE = (196, 188, 172)

SERIF_BOLD_PATHS = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
]
SANS_PATHS = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
]
SANS_BOLD_PATHS = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
]


def load_font(paths, size):
    for p in paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def serif(size):
    return load_font(SERIF_BOLD_PATHS, size)


def sans(size):
    return load_font(SANS_PATHS, size)


def sans_bold(size):
    return load_font(SANS_BOLD_PATHS, size)


def wrap(draw, text, font, width):
    """Greedy word wrap returning a list of lines that fit width."""
    lines = []
    current = ""
    for word in text.split():
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=font) <= width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def text_block(draw, x, y, text, font, fill, width, leading):
    """Draw wrapped text; return the y just below the block."""
    for line in wrap(draw, text, font, width):
        draw.text((x, y), line, font=font, fill=fill)
        y += leading
    return y


def centred(draw, y, text, font, fill):
    w = draw.textlength(text, font=font)
    draw.text(((PAGE - w) / 2, y), text, font=font, fill=fill)


def rule(draw, y, weight=2, colour=INK):
    draw.line([(MARGIN, y), (PAGE - MARGIN, y)], fill=colour, width=weight)


def kicker(draw, x, y, text, colour=ACCENT):
    draw.text((x, y), text, font=sans_bold(15), fill=colour)
    return y + 22


# ---------------------------------------------------------------- stories

LEAD_HEADLINE = "RUSSIA'S BIGGEST BARRAGE OF THE YEAR — TWO MISSILES FALL IN POLAND"
LEAD_CHIPS = ["400+ DRONES", "110 MISSILES", "AT LEAST 8 DEAD IN KYIV"]
LEAD_BODY = (
    "Russia fired more than 400 drones and 110 missiles at Ukraine overnight, "
    "damaging bridges and stations in the capital. Two missiles and a suspected "
    "drone came down inside Poland: no injuries were reported, Prime Minister "
    "Tusk called it a deliberate provocation, and NATO scrambled jets. Trump "
    "called Putin a friend — and President Zelensky answered: \u201ca killer\u201d."
)

COLUMNS = [
    {
        "kicker": "THE HAGUE • JUSTICE",
        "headline": "ICJ FINDS MYANMAR COMMITTED GENOCIDE AGAINST THE ROHINGYA",
        "body": (
            "The International Court of Justice found Myanmar responsible for "
            "genocide against the Rohingya, as survivors of the 2017 exodus "
            "recounted their flight at The Hague."
        ),
    },
    {
        "kicker": "BRUSSELS • EUROPE",
        "headline": "UK AND EU SIGN THEIR BIGGEST SET OF DEALS SINCE BREXIT",
        "body": (
            "Prime Minister Burnham and EU leaders signed three agreements: food "
            "trade with border checks scrapped, linked carbon markets, and youth "
            "mobility for 100,000 young people each way. Britain rejoins Erasmus+."
        ),
    },
]

MARKET_CELLS = [
    ("S&P 500", "6,910.42", "-3.70%"),
    ("DOW JONES", "48,147.33", "-1.93%"),
    ("NASDAQ COMP.", "22,617.73", "-5.28%"),
    ("WEEK'S FALL", "S&P -8.6%", "NASDAQ-100 -10.4%"),
]
MARKET_NOTE = (
    "IN CORRECTION: S&P + DOW • ANTHROPIC $88.91, -8.5% DAY TWO • "
    "NVIDIA -14%, SEC PROBE • VIX 40"
)

BRIEFS = [
    ("ANTALYA — CLIMATE",
     "Talks run past their deadline; nearly 200 nations still split over fossil fuels."),
    ("JUNÍN, PERU — EARTHQUAKE",
     "Magnitude 6.8 quake deep in the Andes, felt in Lima; one injured in early reports."),
    ("RIYADH — MISSILES",
     "Coalition intercepts three Houthi missiles aimed at the capital, a third night running."),
    ("LONDON — MEDICINE",
     "Cancer pill daraxonrasib: tumours undetectable in 1 in 12 trial patients."),
    ("COPENHAGEN — RUSSIA PLOT",
     "Denmark expels Russia's defence attaché over an alleged rapper murder plot; Moscow denies."),
    ("GAMES — RECORD HAUL",
     "GTA VI's first-day sales reported at $3.8 billion — a new industry record."),
]

FOOTER = (
    "ALSO TODAY — SPAIN VOTES 29 NOV • GEN Z PROTESTS IN 25 EUROPEAN COUNTRIES • "
    "CONGRESS SWEEPS RAJASTHAN POLLS, 33 OF 37"
)


# ------------------------------------------------------------------- page

def draw_masthead(draw):
    centred(draw, 20, "O N E   I M A G E   •   O N E   D A Y", sans_bold(14), SOFT)
    centred(draw, 40, "THE WORLD LEDGER", serif(54), INK)
    draw.rectangle([MARGIN, 108, PAGE - MARGIN, 140], fill=BAND)
    draw.text((MARGIN + 14, 114), "SATURDAY 21 NOVEMBER 2026",
              font=sans_bold(19), fill=BAND_INK)
    right = "THE DAY'S NEWS, SUMMED UP"
    w = draw.textlength(right, font=sans_bold(15))
    draw.text((PAGE - MARGIN - 14 - w, 116), right, font=sans_bold(15), fill=BAND_INK)
    return 154


def draw_lead(draw, y):
    y = kicker(draw, MARGIN, y, "KYIV • WARSAW — WAR IN EUROPE")
    head_font = serif(48)
    for line in wrap(draw, LEAD_HEADLINE, head_font, PAGE - 2 * MARGIN):
        draw.text((MARGIN, y), line, font=head_font, fill=INK)
        y += 54
    y += 6
    chip_font = sans_bold(19)
    x = MARGIN
    for chip in LEAD_CHIPS:
        w = draw.textlength(chip, font=chip_font) + 28
        draw.rectangle([x, y, x + w, y + 38], outline=ACCENT, width=2)
        draw.text((x + 14, y + 8), chip, font=chip_font, fill=ACCENT)
        x += w + 14
    y += 50
    y = text_block(draw, MARGIN, y, LEAD_BODY, sans(19), INK,
                   PAGE - 2 * MARGIN, 25)
    return y + 8


def draw_columns(draw, y):
    col_w = (PAGE - 2 * MARGIN - 24) // 2
    xs = [MARGIN, MARGIN + col_w + 24]
    bottom = y
    for x, story in zip(xs, COLUMNS):
        cy = kicker(draw, x, y, story["kicker"])
        head_font = serif(27)
        for line in wrap(draw, story["headline"], head_font, col_w):
            draw.text((x, cy), line, font=head_font, fill=INK)
            cy += 32
        cy += 4
        cy = text_block(draw, x, cy, story["body"], sans(16), INK, col_w, 21)
        bottom = max(bottom, cy)
    mid = MARGIN + col_w + 12
    draw.line([(mid, y + 2), (mid, bottom)], fill=LINE, width=1)
    return bottom + 12


def draw_markets(draw, y):
    draw.rectangle([MARGIN, y, PAGE - MARGIN, y + 92], fill=BAND)
    draw.text((MARGIN + 14, y + 9),
              "FRIDAY'S ROUT — WALL STREET CLOSES, FRI 20 NOV",
              font=sans_bold(16), fill=BAND_INK)
    cell_w = (PAGE - 2 * MARGIN - 28) // 4
    for i, (name, value, change) in enumerate(MARKET_CELLS):
        x = MARGIN + 14 + i * cell_w
        draw.text((x, y + 33), name, font=sans_bold(14), fill=(170, 180, 192))
        draw.text((x, y + 50), value, font=serif(22), fill=BAND_INK)
        draw.text((x, y + 74), change, font=sans_bold(14), fill=DOWN)
    note_y = y + 100
    centred(draw, note_y, MARKET_NOTE, sans_bold(12), SOFT)
    return note_y + 18


def draw_briefs(draw, y):
    col_w = (PAGE - 2 * MARGIN - 2 * 22) // 3
    for row in range(2):
        row_bottom = y
        for col in range(3):
            head, body = BRIEFS[row * 3 + col]
            x = MARGIN + col * (col_w + 22)
            by = text_block(draw, x, y, head, sans_bold(13), ACCENT, col_w, 15)
            by = text_block(draw, x, by + 2, body, sans(13), INK, col_w, 16)
            row_bottom = max(row_bottom, by)
        y = row_bottom + 10
    return y


def build_page():
    img = Image.new("RGB", (PAGE, PAGE), PAPER)
    draw = ImageDraw.Draw(img)
    y = draw_masthead(draw)
    y = draw_lead(draw, y)
    rule(draw, y)
    y = draw_columns(draw, y + 12)
    y = draw_markets(draw, y + 2)
    rule(draw, y + 2)
    y = draw_briefs(draw, y + 10)
    rule(draw, PAGE - 36)
    centred(draw, PAGE - 27, FOOTER, sans_bold(11), SOFT)
    return img


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    build_page().save(out, format="PNG")
    print("baked", out)
