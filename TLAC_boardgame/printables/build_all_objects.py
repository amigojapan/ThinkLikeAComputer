#!/usr/bin/env python3
"""Build the A4 object sheet, then export it with Inkscape (no downloads).

Run: python3 TLAC_boardgame/printables/build_all_objects.py
The 18 mm tiles fit inside the cells of boardAndTurtle.pdf at 100% scale.
"""

import base64
from collections import Counter
from html import escape
from pathlib import Path
import subprocess


HERE = Path(__file__).resolve().parent
IMAGES = HERE.parent / 'img'


def text(x, y, value, size=3, **attributes):
    attrs = ' '.join(f'{key.replace("_", "-")}="{escape(str(value))}"'
                     for key, value in attributes.items())
    return f'<text x="{x}" y="{y}" font-size="{size}" {attrs}>{escape(value)}</text>'


def artwork(kind):
    """Simple vector counterparts of the board icons, on ink-saving white."""
    if kind == 'egg':
        return '<ellipse cx="9" cy="7.5" rx="4.5" ry="5.4" fill="white" stroke="#171717" stroke-width=".8"/>'
    if kind == 'wall':
        return ('<path d="M2 2H16V13H2Z" fill="#bb4545" stroke="#292929" stroke-width=".4"/>'
                '<path d="M2 5.7H16M2 9.3H16M6 2V5.7M12 5.7V9.3M7 9.3V13" fill="none" stroke="#292929" stroke-width=".4"/>')
    if kind == 'star':
        return '<path d="M9 2 11 5.7 15 6.3 12 9.2 12.7 13.3 9 11.3 5.3 13.3 6 9.2 3 6.3 7 5.7Z" fill="#e45b50" stroke="#292929" stroke-width=".4"/>'
    if kind == 'diamond':
        return '<path d="M9 1.5 15 7.5 9 13.5 3 7.5Z M9 1.5V13.5M3 7.5H15" fill="#dceefa" stroke="#292929" stroke-width=".45"/>'
    if kind == 'goal':
        flag = '<path d="M4 14V2H15V9H4" fill="white" stroke="#171717" stroke-width=".5"/>'
        for row in range(4):
            for col in range(6):
                if (row + col) % 2 == 0:
                    flag += f'<rect x="{4 + col*11/6}" y="{2 + row*7/4}" width="{11/6}" height="{7/4}" fill="#171717"/>'
        return flag
    if kind.startswith('pyramid'):
        size = int(kind[-1])
        half_width, height = 1.5 + size, 2 + size * 2
        return f'<path d="M9 {13-height} {9+half_width} 13H{9-half_width}Z" fill="#6267de" stroke="#292929" stroke-width=".35"/>'
    if kind == 'turtle':
        return '<use xlink:href="#turtle-art" x="2" y=".5" width="14" height="14"/>'
    return '<circle cx="9" cy="7.5" r="5.5" fill="white" stroke="#777" stroke-width=".3" stroke-dasharray=".8 .8"/>'


def build():
    turtle = base64.b64encode((IMAGES / 'turtule_1BW.png').read_bytes()).decode('ascii')
    out = ['<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="210mm" height="297mm" viewBox="0 0 210 297">',
           '<title>TLAC: all printable objects</title>',
           '<desc>A4 sheet of 99 square cutouts, each 18 mm: two sets of pyramids 1–5, eight goal flags, four turtles, five custom markers, 27 eggs, 27 walls, nine stars, and nine diamonds.</desc>',
           f'<defs><image id="turtle-art" width="14" height="14" xlink:href="data:image/png;base64,{turtle}"/></defs>',
           '<rect width="210" height="297" fill="white"/>',
           '<g font-family="DejaVu Sans, Noto Sans CJK JP, sans-serif" fill="#171717">',
           text(16, 14, 'TLAC / All object cutouts', 6, font_weight='bold'),
           text(16, 21, 'Todas las piezas recortables / すべての切り抜きコマ', 3.6),
           text(16, 30, '1–5 Pyramids · G Goals · Turtles · M/W/custom markers', 3),
           text(16, 35, '1–5 Pirámides · G Metas · Tortugas · M/W/marcadores libres', 3),
           text(16, 40, '1–5 ピラミッド・G ゴール・亀・M/W/自由に書けるコマ', 3),
           text(16, 45, 'o Eggs / Huevos / 卵    # Walls / Muros / 壁    * Stars / Estrellas / 星    X Diamonds / Diamantes / ダイヤ', 2.45)]

    rows = [
        [(f'pyramid{i}', str(i)) for i in range(1, 6)] + [('goal', 'G')] * 4,
        [(f'pyramid{i}', str(i)) for i in range(1, 6)] + [('goal', 'G')] * 4,
        [('turtle', label) for label in 'ABCD'] + [('marker', label) for label in ['M', 'W', '', '', '']],
        *[[('egg', 'o')] * 9 for _ in range(3)],
        *[[('wall', '#')] * 9 for _ in range(3)],
        [('star', '*')] * 9,
        [('diamond', 'X')] * 9,
    ]
    counts = Counter()
    for row, pieces in enumerate(rows):
        for col, (kind, label) in enumerate(pieces):
            counts[kind] += 1
            out.append(f'<g id="{kind}-{counts[kind]}" transform="translate({16+20*col} {49+20*row})">')
            out.append('<rect width="18" height="18" fill="white" stroke="#888" stroke-width=".2" stroke-dasharray="1 .7"/>')
            out.append(artwork(kind))
            if kind == 'marker':
                out.append(text(9, 9.6, label, 5.8, text_anchor='middle', font_weight='bold'))
            else:
                out.append(text(9, 16.6, label, 2.8, text_anchor='middle', font_weight='bold'))
            out.append('</g>')

    out += [text(16, 274, 'A4 · Print at 100%. Cut dashed squares. Rotate turtles to turn.', 3),
            text(16, 280, 'A4 · Imprime al 100%. Recorta los cuadrados. Gira las tortugas.', 3),
            text(16, 286, 'A4・倍率100%で印刷。点線で切り、亀を回して向きを変えます。', 3),
            '<path d="M176 277V280M176 278.5H194M194 277V280" fill="none" stroke="#171717" stroke-width=".25"/>',
            text(185, 284.5, '18 mm', 2.6, text_anchor='middle'),
            '</g></svg>']
    target = HERE / 'all_objects.svg'
    target.write_text('\n'.join(out) + '\n', encoding='utf-8')
    subprocess.run(['inkscape', str(target), '--export-type=pdf',
                    f'--export-filename={HERE / "all_objects.pdf"}'], check=True)
    print(f'Created all_objects.svg and all_objects.pdf: {sum(counts.values())} pieces.')


if __name__ == '__main__':
    build()
