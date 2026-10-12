#!/usr/bin/env python3
"""Audit board dimensions and build all_boards.pdf at 18 mm per square.

Run from any folder: python3 TLAC_boardgame/printables/build_all_boards.py
Uses the locally installed Inkscape and pdfunite tools. All pages are A4.
Game scripts are parsed, never executed. SVG/PDF intermediates are temporary.
"""
import ast
from collections import defaultdict
from html import escape
from pathlib import Path
import re
import subprocess
import tempfile


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
CELL = 18
BOARDS = {
    (6, 6): 'Turtle class examples',
    (8, 8): 'Sokoban',
    (10, 10): 'Minesweeper; basic lessons, problems and algorithms',
    (11, 11): 'Bomberman',
    (15, 11): 'Frogger',
    (15, 15): "Snake / Conway's Game of Life",
    (19, 14): 'Pac-Man',
}
PAGE_INDEX = {
    (6, 6): '1', (8, 8): '1', (10, 10): '2', (11, 11): '3',
    (15, 11): '4', (15, 15): '5 + 6', (19, 14): '7 + 8',
}


def audit_board_sizes():
    """Collect literal W/H settings plus standalone board input dimensions."""
    found = defaultdict(set)
    for path in ROOT.rglob('*.py'):
        if any(part.startswith('.') for part in path.relative_to(ROOT).parts):
            continue
        try:
            tree = ast.parse(path.read_text(encoding='utf-8'))
        except (SyntaxError, UnicodeDecodeError):
            # A few historical simplified examples are not executable Python.
            # They use the simulator's default board dimensions.
            continue
        assignments = defaultdict(dict)
        for node in ast.walk(tree):
            if not isinstance(node, ast.Assign):
                continue
            if not isinstance(node.value, ast.Constant) or type(node.value.value) is not int:
                continue
            for target in node.targets:
                if isinstance(target, ast.Attribute) and target.attr in ('W', 'H'):
                    assignments[ast.unparse(target.value)][target.attr] = node.value.value
        for dimensions in assignments.values():
            if set(dimensions) == {'W', 'H'}:
                found[dimensions['W'], dimensions['H']].add(str(path.relative_to(ROOT)))
    for path in ROOT.glob('*.txt'):
        rows = path.read_text(encoding='utf-8').strip().splitlines()
        if rows and all(re.fullmatch(r'(\[.\])+', row) for row in rows):
            widths = {len(row) // 3 for row in rows}
            if len(widths) != 1:
                raise ValueError(f'Unequal row lengths: {path.name}')
            found[widths.pop(), len(rows)].add(path.name)
    if set(found) != set(BOARDS):
        raise ValueError(f'Update the printable catalog. Found: {sorted(found)}; catalog: {sorted(BOARDS)}')
    return found


class Sheet:
    def __init__(self, number, landscape=False):
        self.number = number
        self.width, self.height = (297, 210) if landscape else (210, 297)
        self.parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.width}mm" height="{self.height}mm" viewBox="0 0 {self.width} {self.height}">',
            '<title>TLAC / All board sizes / Page ' + str(number) + '</title>',
            '<desc>Blank boards, 18 mm squares. Lettered columns at the top; numbered rows down the left. Print at 100% on A4.</desc>',
            '<rect width="100%" height="100%" fill="white"/>',
            '<g font-family="DejaVu Sans, sans-serif" fill="#171717">',
        ]
        self.tiles = []

    def text(self, x, y, value, size=3, anchor='start', bold=False, rotate=None):
        attrs = f'font-size="{size}" text-anchor="{anchor}"'
        if bold:
            attrs += ' font-weight="bold"'
        if rotate is not None:
            attrs += f' transform="rotate({rotate} {x} {y})"'
        self.parts.append(f'<text x="{x}" y="{y}" {attrs}>{escape(value)}</text>')

    def line(self, x1, y1, x2, y2, width=.2, color='#555'):
        self.parts.append(f'<path d="M{x1} {y1}L{x2} {y2}" fill="none" stroke="{color}" stroke-width="{width}"/>')

    def grid(self, size, x, y, first_column=0, last_column=None):
        """A full-height board or a vertical section; labels keep global values."""
        width, height = size
        end = width if last_column is None else last_column
        columns = end - first_column
        assert 0 <= first_column < end <= width <= 26
        assert x - 6 >= 4 and y - 4 >= 4
        assert x + columns * CELL <= self.width - 4
        assert y + height * CELL <= self.height - 4
        self.tiles.append((size, first_column, end))
        for col in range(columns + 1):
            xx = x + col * CELL
            outer = col in (0, columns)
            self.line(xx, y, xx, y + height * CELL, .4 if outer else .18, '#171717' if outer else '#666')
        for row in range(height + 1):
            yy = y + row * CELL
            outer = row in (0, height)
            self.line(x, yy, x + columns * CELL, yy, .4 if outer else .18, '#171717' if outer else '#666')
        for col in range(columns):
            self.text(x + (col + .5) * CELL, y - 1.5, chr(65 + first_column + col), 3.1, 'middle', True)
        for row in range(height):
            self.text(x - 2, y + (row + .5) * CELL + 1.05, str(row + 1), 3.1, 'end', True)

    def scale(self, x, y):
        self.line(x, y, x + CELL, y, .3, '#171717')
        for xx in (x, x + CELL):
            self.line(xx, y - 1.4, xx, y + 1.4, .3, '#171717')
        self.text(x + CELL / 2, y + 5, '18 mm', 2.5, 'middle')

    def footer(self):
        self.text(9, self.height - 5, 'A4 / 100% (Actual size) / 18 mm squares', 2.5)
        self.text(self.width - 9, self.height - 5, f'{self.number} / 8', 2.5, 'end')

    def svg(self):
        return '\n'.join(self.parts + ['</g></svg>'])


def small_boards():
    page = Sheet(1)
    page.text(9, 8, '6 × 6 / Turtle class examples', 4, bold=True)
    page.grid((6, 6), 51, 16)
    page.text(9, 132, '8 × 8 / Sokoban', 4, bold=True)
    page.grid((8, 8), 33, 140)
    page.scale(174, 118)
    page.footer()
    return page


def default_board():
    page = Sheet(2)
    page.text(12, 10, '10 × 10 / General TLAC board', 4.5, bold=True)
    page.text(12, 16, 'Minesweeper, basic lessons, problems, mazes and pyramid sorting', 2.8)
    page.grid((10, 10), 18, 25)
    page.text(12, 215, 'Use A1 for the top-left square. Code (x, y) = (0, 0) is A1; (2, 3) is C4.', 2.7)
    page.text(12, 223, 'BOARD INDEX / columns × rows', 3.1, bold=True)
    page.text(198, 223, 'Pages', 3.1, 'end', True)
    for index, (size, name) in enumerate(BOARDS.items()):
        yy = 232 + index * 6.4
        page.text(12, yy, f'{size[0]} × {size[1]}', 2.8, bold=True)
        page.text(36, yy, name, 2.5)
        page.text(198, yy, PAGE_INDEX[size], 2.8, 'end')
    page.text(12, 280, 'Blank boards: place the pieces according to the game or lesson.', 2.6)
    page.scale(173, 277)
    page.footer()
    return page


def bomberman_board():
    page = Sheet(3, landscape=True)
    page.grid((11, 11), 14, 8)
    page.text(221, 25, '11 × 11', 7, bold=True)
    page.text(221, 37, 'BOMBERMAN', 4, bold=True)
    page.text(221, 52, 'A–K across', 3.2)
    page.text(221, 59, '1–11 down', 3.2)
    page.text(221, 76, 'Top-left: A1', 3)
    page.text(221, 83, 'Code position: (0, 0)', 3)
    page.text(221, 102, '18 mm squares', 3.4, bold=True)
    page.text(221, 112, 'A4 landscape', 3)
    page.text(221, 119, 'Print at 100%', 3)
    page.text(221, 126, '(Actual size)', 3)
    page.scale(221, 143)
    page.text(221, 172, 'Place walls, crates,', 3)
    page.text(221, 179, 'bombs and enemies', 3)
    page.text(221, 186, 'using the game cards.', 3)
    page.text(288, 203, '3 / 8', 2.5, 'end')
    return page


def frogger_board():
    page = Sheet(4, landscape=True)
    page.grid((15, 11), 20, 8)
    # Side title preserves 18 mm cells without adding a third sheet dimension.
    page.text(7.5, 201, '15 × 11 / FROGGER / A4 / 100% / 18 mm squares / 4 of 8', 3.1, rotate=-90)
    page.line(9, 10, 9, 28, .3, '#171717')
    page.line(7.5, 10, 10.5, 10, .3, '#171717')
    page.line(7.5, 28, 10.5, 28, .3, '#171717')
    page.text(6, 27, '18 mm', 2.2, rotate=-90)
    return page


def joined_board(size, page_number, start, end, other_page):
    page = Sheet(page_number)
    width, height = size
    name = 'Snake / Game of Life' if size == (15, 15) else 'Pac-Man'
    side = 'LEFT' if start == 0 else 'RIGHT'
    labels = f'{chr(65 + start)}–{chr(64 + end)}'
    page.text(9, 7, f'{width} × {height} / {name} / {side} / {labels}', 3.6, bold=True)
    # Every section uses the same top edge; matching rows align after trimming.
    x = 18 if start == 0 else 22
    page.grid(size, x, 17, start, end)
    grid_right = x + (end - start) * CELL
    if height == 14:
        page.text(9, 278, f'Join with page {other_page}: trim the meeting edges to the grid border.', 2.6)
        page.text(9, 283, 'Match row numbers; tape the backs. Remove repeated row labels at the seam.', 2.55)
        page.scale(173, 276)
        page.footer()
    else:
        page.text(9, 293, f'A4 / 100% / 18 mm / Join page {other_page}: trim meeting grid edges; match rows; tape backs.', 2.3)
        page.text(201, 293, f'{page_number} / 8', 2.3, 'end')
        if start == 0:
            page.text(7, 278, 'Scale check: one square is 18 mm', 2.2, rotate=-90)
        else:
            page.text(grid_right + 8, 267, 'Trim the left margin, including the repeated row labels.', 2.5, rotate=-90)
    # A small assembly diagram fits in the unused width of right-hand sections.
    if start:
        inset = grid_right + 7
        if inset + 32 < page.width - 4:
            page.text(inset, 35, 'JOIN', 2.7, bold=True)
            for index, number in enumerate((other_page, page_number)):
                xx = inset + index * 15
                page.parts.append(f'<rect x="{xx}" y="41" width="15" height="22" fill="none" stroke="#555" stroke-width=".25"/>')
                page.text(xx + 7.5, 54, str(number), 3.5, 'middle', True)
            page.text(inset, 72, 'Left + right', 2.5)
            page.scale(inset, 84)
    return page


def build():
    inventory = audit_board_sizes()
    pages = [small_boards(), default_board(), bomberman_board(), frogger_board(),
             joined_board((15, 15), 5, 0, 10, 6),
             joined_board((15, 15), 6, 10, 15, 5),
             joined_board((19, 14), 7, 0, 10, 8),
             joined_board((19, 14), 8, 10, 19, 7)]
    # Confirm each board cell occurs exactly once in the printed sections.
    coverage = defaultdict(set)
    for page in pages:
        for size, start, end in page.tiles:
            for row in range(size[1]):
                for col in range(start, end):
                    assert (col, row) not in coverage[size], (size, col, row)
                    coverage[size].add((col, row))
    for (width, height), cells in coverage.items():
        assert len(cells) == width * height
    assert set(coverage) == set(inventory)

    with tempfile.TemporaryDirectory(prefix='tlac-boards-') as directory:
        temp = Path(directory)
        pdfs = []
        for page in pages:
            svg = temp / f'page-{page.number}.svg'
            pdf = svg.with_suffix('.pdf')
            svg.write_text(page.svg(), encoding='utf-8')
            subprocess.run(['inkscape', str(svg), '--export-type=pdf', f'--export-filename={pdf}'],
                           check=True, capture_output=True, text=True)
            pdfs.append(str(pdf))
        target = HERE / 'all_boards.pdf'
        subprocess.run(['pdfunite', *pdfs, str(target)], check=True)

    for (width, height), sources in sorted(inventory.items()):
        print(f'{width} × {height}: ' + ', '.join(sorted(sources)))
    print(f'Created {target}: 7 board sizes, 8 A4 pages, 18 mm squares, {sum(map(len, coverage.values()))} cells.')


if __name__ == '__main__':
    build()
