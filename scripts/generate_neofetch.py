from pathlib import Path
from datetime import datetime
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "assets" / "neofetch.svg"

PROFILE = {
    "NAME": "SARTHAK S",
    "GITHUB": "Sarthak-S-2005",
    "ROLE": "Aspiring Software Developer",
    "LOCATION": "India",
    "LANGUAGES": "Python | Java | SQL",
    "INTERESTS": "Machine Learning | Generative AI",
    "EDITOR": "VS Code",
    "STATUS": "Learning and building projects",
}


def render_svg():
    rows = []

    for index, (label, value) in enumerate(PROFILE.items()):
        y = 230 + index * 37
        rows.append(
            f'<text x="425" y="{y}" class="label">'
            f'{escape(label)}</text>'
            f'<text x="575" y="{y}" class="value">'
            f'{escape(value)}</text>'
        )

    details = "\n".join(rows)
    year = datetime.now().year

    return f"""<svg xmlns="http://www.w3.org/2000/svg"
    width="1000" height="600" viewBox="0 0 1000 600">

    <defs>
      <linearGradient id="accent" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0%" stop-color="#58a6ff"/>
        <stop offset="100%" stop-color="#bc8cff"/>
      </linearGradient>
      <linearGradient id="panel" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0%" stop-color="#161b22"/>
        <stop offset="100%" stop-color="#0d1117"/>
      </linearGradient>
    </defs>

    <rect width="1000" height="600" rx="22" fill="url(#panel)"/>
    <rect x="1" y="1" width="998" height="598" rx="21"
          fill="none" stroke="#30363d" stroke-width="2"/>

    <path d="M1 65 H999" stroke="#30363d" stroke-width="2"/>

    <circle cx="32" cy="33" r="7" fill="#ff5f56"/>
    <circle cx="56" cy="33" r="7" fill="#ffbd2e"/>
    <circle cx="80" cy="33" r="7" fill="#27c93f"/>

    <text x="500" y="39" text-anchor="middle"
          fill="#c9d1d9" font-family="Consolas, monospace"
          font-size="17">sarthak@github: ~</text>

    <rect x="30" y="95" width="335" height="450" rx="14"
          fill="#0d1117" stroke="#30363d"/>

    <text x="55" y="132" fill="#58a6ff"
          font-family="Consolas, monospace"
          font-size="17" font-weight="bold">$ whoami</text>

    <text x="55" y="165" fill="#3fb950"
          font-family="Consolas, monospace"
          font-size="19">Sarthak-S-2005</text>

    <path d="M55 187 H335" stroke="#30363d"/>

    <text x="55" y="225" fill="#bc8cff"
          font-family="Consolas, monospace"
          font-size="15">PROFILE</text>

    <text x="55" y="265" fill="#c9d1d9"
          font-family="Consolas, monospace"
          font-size="14">Building projects,</text>
    <text x="55" y="290" fill="#c9d1d9"
          font-family="Consolas, monospace"
          font-size="14">learning new skills,</text>
    <text x="55" y="315" fill="#c9d1d9"
          font-family="Consolas, monospace"
          font-size="14">exploring AI.</text>

    <rect x="55" y="350" width="255" height="4" rx="2"
          fill="url(#accent)"/>

    <text x="55" y="390" fill="#8b949e"
          font-family="Consolas, monospace"
          font-size="13">CURRENT FOCUS</text>
    <text x="55" y="420" fill="#58a6ff"
          font-family="Consolas, monospace"
          font-size="15">Software + AI</text>

    <text x="55" y="495" fill="#3fb950"
          font-family="Consolas, monospace"
          font-size="13">Status: Learning</text>

    <text x="425" y="130" fill="#58a6ff"
          font-family="Consolas, monospace"
          font-size="21" font-weight="bold">
      $ neofetch --profile
    </text>

    <text x="425" y="166" fill="#8b949e"
          font-family="Consolas, monospace"
          font-size="14">Developer information</text>

    <path d="M425 190 H950" stroke="#30363d"/>

    <style>
      .label {{
        fill: #79c0ff;
        font-family: Consolas, monospace;
        font-size: 14px;
        font-weight: bold;
      }}
      .value {{
        fill: #f0f6fc;
        font-family: Consolas, monospace;
        font-size: 14px;
      }}
    </style>

    {details}

    <path d="M425 505 H950" stroke="#30363d"/>

    <text x="425" y="540" fill="#3fb950"
          font-family="Consolas, monospace"
          font-size="14">$ echo "Keep building."</text>

    <rect x="425" y="555" width="9" height="16"
          fill="#58a6ff">
      <animate attributeName="opacity"
               values="1;0;1" dur="1.2s"
               repeatCount="indefinite"/>
    </rect>

    <text x="950" y="580" text-anchor="end"
          fill="#8b949e" font-family="Consolas, monospace"
          font-size="12">Generated with Python | {year}</text>
    </svg>"""


def main():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    svg_content = render_svg()
    OUTPUT.write_text(svg_content, encoding="utf-8")
    print(f"Developer card created successfully: {OUTPUT}")


if __name__ == "__main__":
    main()