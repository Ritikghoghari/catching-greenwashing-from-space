"""Overlay title/legend/source labels onto Hansen forest-loss satellite thumbnails.

Adds top and bottom bands around the original image instead of drawing over
pixels, so no forest-loss data is ever obscured by text.
"""
import os

from PIL import Image, ImageDraw, ImageFont

TOP_BAND_PX = 54
BOTTOM_BAND_PX = 46
BG = (18, 18, 18)
FG = (240, 240, 240)
MUTED = (170, 170, 170)

STATIC_LEGEND = [
    ("1a7a3c", "Forest (>30% cover, yr2000)"),
    ("d1442e", "Loss after 2020"),
]

YEARLY_LEGEND = [
    ("1a7a3c", "Standing"),
    ("fff59d", "'19"),
    ("ffd54f", "'20"),
    ("ffb300", "'21"),
    ("fb8c00", "'22"),
    ("f4511e", "'23"),
    ("e53935", "'24"),
    ("b71c1c", "'25"),
]

SOURCE_TEXT = "Source: Hansen/UMD/Google/USGS/NASA Global Forest Change v1.13"


def _font(size):
    for name in ("arial.ttf", "DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def _hex_to_rgb(h):
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def add_labels(img: Image.Image, title: str, subtitle: str, legend_items, source_text=SOURCE_TEXT) -> Image.Image:
    """Return a new RGB image with a title band on top and legend/source band on bottom."""
    img = img.convert("RGB")
    w, h = img.size
    out = Image.new("RGB", (w, h + TOP_BAND_PX + BOTTOM_BAND_PX), BG)
    out.paste(img, (0, TOP_BAND_PX))

    draw = ImageDraw.Draw(out)
    draw.text((10, 6), title, font=_font(20), fill=FG)
    draw.text((10, 30), subtitle, font=_font(13), fill=MUTED)

    legend_y = TOP_BAND_PX + h + 8
    x = 10
    swatch = 14
    font = _font(12)
    for color_hex, label in legend_items:
        draw.rectangle([x, legend_y, x + swatch, legend_y + swatch], fill=_hex_to_rgb(color_hex))
        text_w = draw.textlength(label, font=font)
        draw.text((x + swatch + 4, legend_y - 1), label, font=font, fill=FG)
        x += swatch + 4 + text_w + 14

    src_font = _font(10)
    src_w = draw.textlength(source_text, font=src_font)
    draw.text((w - src_w - 10, out.size[1] - 16), source_text, font=src_font, fill=MUTED)

    return out


def label_static(img: Image.Image, company: str, n_mills: int, loss_after_2020_ha: float) -> Image.Image:
    title = f"{company.upper()} — Forest loss vs. traceable mills"
    subtitle = f"{n_mills} mills matched · {loss_after_2020_ha:,.0f} ha lost after 2020"
    return add_labels(img, title, subtitle, STATIC_LEGEND)


def label_yearly(img: Image.Image, company: str, n_mills: int, loss_after_2020_ha: float) -> Image.Image:
    title = f"{company.upper()} — Forest loss by year (2019–2025)"
    subtitle = f"{n_mills} mills matched · {loss_after_2020_ha:,.0f} ha lost after 2020"
    return add_labels(img, title, subtitle, YEARLY_LEGEND)


if __name__ == "__main__":
    import pandas as pd

    IN_DIR = "Results/satellite_images"
    OUT_DIR = "Results/satellite_images_labeled"
    os.makedirs(OUT_DIR, exist_ok=True)

    loss = pd.read_csv("Results/master_forestloss.csv").set_index("company")

    for fname in sorted(os.listdir(IN_DIR)):
        if not fname.endswith(".png"):
            continue
        is_yearly = fname.endswith("_yearly.png")
        company = fname.replace("_forestloss_yearly.png", "").replace("_forestloss.png", "")
        if company not in loss.index:
            print(f"skip {fname}: no forest-loss row for '{company}'")
            continue
        row = loss.loc[company]
        img = Image.open(os.path.join(IN_DIR, fname))
        labeled = (label_yearly if is_yearly else label_static)(
            img, company, int(row["n_mills"]), float(row["loss_after_2020_ha"])
        )
        out_path = os.path.join(OUT_DIR, fname)
        labeled.save(out_path)
        print(f"labeled {fname} -> {out_path}")
