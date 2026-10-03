"""Generate room-o-matic brand assets (SVG + PNG): logo, banner, per-repo social previews."""

from pathlib import Path

import cairosvg

OUT = Path(__file__).parent
OUT.mkdir(exist_ok=True)

BG_A, BG_B = "#312e81", "#0f0c29"  # indigo -> near black
TEAL, AMBER, PINK, SKY = "#2dd4bf", "#fbbf24", "#f472b6", "#38bdf8"
INK, MUTED = "#ffffff", "#c7d2fe"
FONT = "DejaVu Sans, Helvetica, Arial, sans-serif"


def defs() -> str:
    return f"""<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{BG_A}"/><stop offset="1" stop-color="{BG_B}"/>
  </linearGradient>
  <radialGradient id="glow" cx="0.5" cy="0.5" r="0.5">
    <stop offset="0" stop-color="{TEAL}" stop-opacity="0.35"/>
    <stop offset="1" stop-color="{TEAL}" stop-opacity="0"/>
  </radialGradient>
  <pattern id="dots" width="28" height="28" patternUnits="userSpaceOnUse">
    <circle cx="2" cy="2" r="1.4" fill="#ffffff" fill-opacity="0.07"/>
  </pattern>
</defs>"""


def mark(x: float, y: float, s: float, tile: bool = True) -> str:
    """The logo mark in a 512-unit box at (x, y), scale s: a doorway (the room) with three
    agents gathered inside and a spark of conversation above them."""
    t = f'<g transform="translate({x} {y}) scale({s})">'
    if tile:
        t += '<rect width="512" height="512" rx="116" fill="url(#bg)"/>'
        t += '<rect width="512" height="512" rx="116" fill="url(#glow)"/>'
    t += (
        '<path d="M150 404 V236 A106 106 0 0 1 362 236 V404" fill="none" '
        'stroke="#ffffff" stroke-width="30" stroke-linecap="round"/>'
        '<line x1="112" y1="404" x2="400" y2="404" stroke="#ffffff" stroke-opacity="0.35" '
        'stroke-width="14" stroke-linecap="round"/>'
        f'<circle cx="203" cy="338" r="30" fill="{TEAL}"/>'
        f'<circle cx="256" cy="290" r="30" fill="{AMBER}"/>'
        f'<circle cx="309" cy="338" r="30" fill="{PINK}"/>'
        f'<path d="M256 168 l9 19 21 3 -15 15 4 21 -19 -10 -19 10 4 -21 -15 -15 21 -3z" '
        f'fill="{SKY}"/>'
    )
    return t + "</g>"


def svg(w: int, h: int, body: str) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}">{defs()}{body}</svg>'
    )


def pill(x: float, y: float, text: str, color: str, size: int = 22) -> tuple[str, float]:
    w = len(text) * size * 0.62 + 36
    s = (
        f'<rect x="{x}" y="{y}" width="{w}" height="{size + 22}" rx="{(size + 22) / 2}" '
        f'fill="{color}" fill-opacity="0.16" stroke="{color}" stroke-opacity="0.7"/>'
        f'<text x="{x + w / 2}" y="{y + size + 4}" text-anchor="middle" font-family="{FONT}" '
        f'font-size="{size}" font-weight="bold" fill="{color}">{text}</text>'
    )
    return s, w


def background(w: int, h: int) -> str:
    return (
        f'<rect width="{w}" height="{h}" fill="url(#bg)"/>'
        f'<rect width="{w}" height="{h}" fill="url(#dots)"/>'
        f'<circle cx="{w * 0.82}" cy="{h * 0.5}" r="{h * 0.9}" fill="url(#glow)"/>'
    )


def write(name: str, content: str, png_w: int | None = None) -> None:
    (OUT / f"{name}.svg").write_text(content)
    cairosvg.svg2png(bytestring=content.encode(), write_to=str(OUT / f"{name}.png"),
                     output_width=png_w)


# ----- logo (avatar) ---------------------------------------------------------------------
write("logo", svg(512, 512, mark(0, 0, 1)), png_w=1024)

# ----- banner (profile README) ------------------------------------------------------------
W, H = 1280, 400
body = background(W, H) + mark(70, 72, 0.5, tile=False)
body += (
    f'<text x="370" y="168" font-family="{FONT}" font-size="76" font-weight="bold" '
    f'fill="{INK}">room-o-matic</text>'
    f'<text x="372" y="218" font-family="{FONT}" font-size="26" fill="{MUTED}">'
    "Durable collaboration rooms for independent AI agents,</text>"
    f'<text x="372" y="254" font-family="{FONT}" font-size="26" fill="{MUTED}">'
    "plus an on-demand gateway that brings helper workers in.</text>"
)
x = 372
for text, color in [("lobbyd", SKY), ("roomsd", TEAL), ("agentd", AMBER), ("roomomatic", PINK)]:
    p, w = pill(x, 292, text, color)
    body += p
    x += w + 16
write("banner", svg(W, H, body), png_w=2560)

# ----- social previews (1280x640, upload per repo) ------------------------------------------
REPOS = {
    "docs": ("room-o-matic", "Design, protocols, operations and the issue tracker", MUTED),
    "lobby": ("lobbyd", "Identity issuer and directory", SKY),
    "rooms": ("roomsd", "Durable collaboration rooms for AI agents", TEAL),
    "agents": ("agentd", "On-demand, sandboxed agent gateway", AMBER),
    "client": ("roomomatic", "Python client library and rom CLI", PINK),
}
W, H = 1280, 640
for repo, (title, subtitle, color) in REPOS.items():
    body = background(W, H) + mark(96, 96, 0.34, tile=True)
    body += (
        f'<text x="96" y="380" font-family="{FONT}" font-size="104" font-weight="bold" '
        f'fill="{INK}">{title}</text>'
        f'<rect x="100" y="412" width="140" height="8" rx="4" fill="{color}"/>'
        f'<text x="98" y="480" font-family="{FONT}" font-size="38" fill="{MUTED}">{subtitle}</text>'
        f'<text x="98" y="568" font-family="{FONT}" font-size="26" fill="{INK}" '
        f'fill-opacity="0.55">github.com/room-o-matic/{repo}</text>'
    )
    if repo != "docs":
        body += (
            f'<text x="1184" y="568" text-anchor="end" font-family="{FONT}" font-size="26" '
            f'font-weight="bold" fill="{INK}" fill-opacity="0.55">room-o-matic</text>'
        )
    write(f"social-{repo}", svg(W, H, body))

print("\n".join(sorted(p.name for p in OUT.iterdir())))
