
from pathlib import Path
from PIL import Image, ImageOps
import html

ROOT = Path(__file__).resolve().parent.parent
PHOTO = ROOT / "assets" / "profile.jpg"
OUTPUT = ROOT / "assets" / "ascii-portrait.svg"

# Characters from darkest to lightest
CHARS = "@%#*+=-:. "


def image_to_ascii(image_path, width=70):
    image = Image.open(image_path).convert("RGB")

    # Crop to a centered square
    side = min(image.width, image.height)
    left = (image.width - side) // 2
    top = (image.height - side) // 2
    image = image.crop((left, top, left + side, top + side))

    # Resize; terminal characters are taller than they are wide
    height = max(1, int(width * 0.5))
    image = image.resize((width, height))
    image = ImageOps.grayscale(image)

    lines = []
    for y in range(height):
        line = ""
        for x in range(width):
            brightness = image.getpixel((x, y))
            index = int(brightness / 256 * len(CHARS))
            index = min(index, len(CHARS) - 1)
            line += CHARS[index]
        lines.append(line)

    return lines


def render_svg(lines):
    char_width = 9
    line_height = 13
    padding = 24
    width = len(lines[0]) * char_width + padding * 2
    height = len(lines) * line_height + padding * 2

    text_lines = []
    for i, line in enumerate(lines):
        safe_line = html.escape(line)
        delay = i * 0.08
        text_lines.append(
            f'<text x="{padding}" y="{padding + (i + 1) * line_height}" '
            f'class="line" style="animation-delay:{delay:.2f}s">'
            f'{safe_line}</text>'
        )

    return f'''<svg xmlns="http://www.w3.org/2000/svg"
        width="{width}" height="{height}"
        viewBox="0 0 {width} {height}" role="img"
        aria-label="Animated ASCII portrait">
    <rect width="100%" height="100%" fill="#080b10"/>
    <style>
      .line {{
        fill: #e5e7eb;
        font-family: "Courier New", monospace;
        font-size: 10px;
        white-space: pre;
        opacity: 0;
        animation: appear 0.25s forwards;
      }}
      @keyframes appear {{
        to {{ opacity: 1; }}
      }}
      @media (prefers-reduced-motion: reduce) {{
        .line {{ animation: none; opacity: 1; }}
      }}
    </style>
    {''.join(text_lines)}
    </svg>'''


def main():
    if not PHOTO.exists():
        raise FileNotFoundError(f"Photo not found: {PHOTO}")

    lines = image_to_ascii(PHOTO)
    svg = render_svg(lines)
    OUTPUT.write_text(svg, encoding="utf-8")
    print(f"ASCII portrait created: {OUTPUT}")


if __name__ == "__main__":
    main()
