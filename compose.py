from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
ASSETS = ROOT.parent.parent / "assets" / "gta6-meme-x-01"
SCALE = 2
SIZE = 1080 * SCALE

BACKGROUND = ASSETS / "vice-city-bg.jpg"
MARK = ASSETS / "mark-1024.png"
ANTONIO = "/usr/share/fonts/truetype/sand-box/google/Antonio/Antonio-VariableFont_wght.ttf"
OSWALD = "/usr/share/fonts/truetype/sand-box/google/Oswald/Oswald-VariableFont_wght.ttf"


def fitted_font(draw, text, font_path, max_width, max_height, start_size):
    for size in range(start_size, 0, -1):
        font = ImageFont.truetype(font_path, size=size)
        bounds = draw.textbbox((0, 0), text, font=font, stroke_width=max(1, size // 18))
        if bounds[2] - bounds[0] <= max_width and bounds[3] - bounds[1] <= max_height:
            return font
    raise ValueError(f"Text does not fit: {text}")


def draw_centered_label(draw, text, y, height, font_path, start_size):
    margin = 52 * SCALE
    stroke = max(2, start_size // 18)
    font = fitted_font(draw, text, font_path, SIZE - 2 * margin, height, start_size)
    bounds = draw.textbbox((0, 0), text, font=font, stroke_width=max(1, font.size // 18))
    x = (SIZE - (bounds[2] - bounds[0])) // 2 - bounds[0]
    top = y - bounds[1]
    draw.text(
        (x, top),
        text,
        font=font,
        fill="#FFF8E8",
        stroke_width=max(2, font.size // 18),
        stroke_fill="#090710",
    )


background = Image.open(BACKGROUND).convert("RGB")
background = background.resize((SIZE, SIZE), Image.Resampling.LANCZOS)
canvas = background.convert("RGBA")

# A subtle dark wash keeps the top caption legible without obscuring the sunset.
shade = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
shade_draw = ImageDraw.Draw(shade)
shade_draw.rectangle((0, 0, SIZE, 390 * SCALE), fill=(3, 5, 15, 75))
canvas = Image.alpha_composite(canvas, shade)

# The official mark sits over the cash in the convertible's empty driver's seat.
mark = Image.open(MARK).convert("RGBA")
mark_size = 450 * SCALE
mark = mark.resize((mark_size, mark_size), Image.Resampling.LANCZOS)
canvas.alpha_composite(mark, (402 * SCALE, 394 * SCALE))

# Keep the make.fun wordmark separate from the badge on a dark road plaque.
plaque = Image.new("RGBA", (210 * SCALE, 100 * SCALE), (8, 8, 18, 220))
plaque_draw = ImageDraw.Draw(plaque)
plaque_draw.rounded_rectangle(
    (0, 0, plaque.width - 1, plaque.height - 1),
    radius=18 * SCALE,
    fill=(8, 8, 18, 220),
    outline=(255, 255, 255, 90),
    width=2 * SCALE,
)
plaque_x, plaque_y = 28 * SCALE, 835 * SCALE
canvas.alpha_composite(plaque, (plaque_x, plaque_y))

draw = ImageDraw.Draw(canvas)
wordmark = "make.fun"
wordmark_font = fitted_font(draw, wordmark, OSWALD, 190 * SCALE, 70 * SCALE, 104 * SCALE)
wordmark_bounds = draw.textbbox((0, 0), wordmark, font=wordmark_font, stroke_width=5 * SCALE)
wordmark_x = plaque_x + (plaque.width - (wordmark_bounds[2] - wordmark_bounds[0])) // 2 - wordmark_bounds[0]
wordmark_y = plaque_y + (plaque.height - (wordmark_bounds[3] - wordmark_bounds[1])) // 2 - wordmark_bounds[1]
draw.text(
    (wordmark_x, wordmark_y),
    wordmark,
    font=wordmark_font,
    fill="#FFF8E8",
    stroke_width=5 * SCALE,
    stroke_fill="#090710",
)

draw_centered_label(
    draw,
    "CALLED IN SICK FOR GTA 6",
    20 * SCALE,
    118 * SCALE,
    ANTONIO,
    112 * SCALE,
)
draw_centered_label(
    draw,
    "MY AI AGENT CASHED A MAKE.FUN BOUNTY",
    982 * SCALE,
    76 * SCALE,
    OSWALD,
    116 * SCALE,
)

final = canvas.convert("RGB").resize((1080, 1080), Image.Resampling.LANCZOS)
final.save(ROOT / "meme.png", format="PNG", optimize=True)
final.thumbnail((768, 480), Image.Resampling.LANCZOS)
final.save("/tmp/meme-judge-preview.jpg", format="JPEG", quality=90, optimize=True)
