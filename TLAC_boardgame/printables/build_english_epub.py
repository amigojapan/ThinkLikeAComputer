#!/usr/bin/env python3
"""Build a complete English, Japanese, or Spanish book from the tutorial pages.

Run: python3 TLAC_boardgame/printables/build_english_epub.py --language ja
Requires pandoc, beautifulsoup4 and Pillow. No network access is needed.
Rebuild the HTML tutorials first when their sources change.
"""
from functools import lru_cache
from collections import Counter
import copy
import argparse
from hashlib import sha256
from html import escape
import json
import mimetypes
from pathlib import Path
import posixpath
import re
import subprocess
import shutil
import sys
import tempfile
from urllib.parse import unquote, urlsplit
from zipfile import ZipFile, ZIP_DEFLATED
import xml.etree.ElementTree as ET

from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont

if __package__:
    from .epub_translations import translate, localize_document, EDITIONS
else:
    from epub_translations import translate, localize_document, EDITIONS

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
OUTPUT = HERE / 'ThinkLikeAComputer-English-All-Steps.epub'
LEGACY_OUTPUT = HERE / 'ThinkLikeAComputer-English.epub'
SOURCES = [
    ('basics', 'The eight basics of programming',
     ROOT / 'TLAC_8_basics_of_programming/8_basics_of_programming_TLAC.html'),
    ('advanced', 'Advanced concepts: recursion and classes', ROOT / 'TLAC_advanced_concepts.html'),
    ('games', 'Seven games in TLAC', ROOT / 'games.html'),
    ('pyramids', 'Insertion sort with pyramids', ROOT / 'algorithm-insertion-sort-pyramids.html'),
    ('maze', 'Explore a maze', ROOT / 'maze-tutorial.html'),
]
TILES = {' ': 'board_empty_slot.png', '#': 'wall.png', 'o': 'egg.png', 'G': 'goal.png',
         '^': 'turtule_up.png', 'V': 'turtule_down.png', '<': 'turtule_left.png',
         '>': 'turtule_right.png', **{str(n): f'pyramid{n}.png' for n in range(1, 6)}}
CSS = """
body { font-family: sans-serif; line-height: 1.5; color: #183342; }
h1, h2, h3 { line-height: 1.25; color: #173d5b; }
h1 { border-bottom: 3px solid #4e8794; padding-bottom: .4em; }
h2 { break-before: page; } h3, h4 { break-after: avoid; }
a { color: #125f89; } p { margin: .6em 0; }
img { max-width: 100%; height: auto; } figure { margin: 1em 0; break-inside: avoid; }
figcaption { font-weight: bold; margin-bottom: .5em; }
.board-figure { display: block; max-width: 28em; margin: .8em auto; }
.execution-preview { border: 1px solid #78929c; padding: .8em; margin: 1em 0; }
.execution-preview h4 { margin-top: 0; }
.instruction-line, .instruction-card { background: #fff5bd; color: #172d40;
  border: 1px solid #9f955b; padding: .4em; margin: .35em 0; break-inside: avoid; }
.instruction-number { font-weight: bold; color: #173d8c; padding-right: .5em; }
.instruction-block { border-left: 2px solid #8aabb7; padding-left: .6em; }
.comment { background: #e6f3df; } .function { background: #e2ecff; }
.depth1 { margin-left: .6em; } .depth2 { margin-left: 1.2em; }
.depth3 { margin-left: 1.8em; } .depth4 { margin-left: 2.4em; }
.depth5, .depth6 { margin-left: 3em; }
pre { white-space: pre-wrap; overflow-wrap: anywhere; font-size: .8em; }
code { overflow-wrap: anywhere; } table { border-collapse: collapse; max-width: 100%; }
td, th { border: 1px solid #78929c; padding: .3em; }
.step { border-top: 1px solid #9fb4bc; padding-top: .4em; }
.note { background: #e8f3f5; border-left: 3px solid #376b84; padding: .6em; }
"""


def soup(text):
    return BeautifulSoup(text, 'html.parser')


def replay_data(path):
    return json.JSONDecoder().raw_decode(path.read_text(encoding='utf-8').split('const run = ', 1)[1])[0]


def chart_css(path, slug):
    """Copy chart rules from the HTML, scoped to that page's ebook charts."""
    prefixes = ('.chart', '.htmlifyer-chart', '.instruction-chart', '.instruction-card',
                '.instruction-number', '.nested-instructions', '.instruction-block')
    result = []
    for style in soup(path.read_text(encoding='utf-8')).select('style'):
        css = re.sub(r'/\*.*?\*/', '', style.get_text(), flags=re.S)
        # Only top-level rules: skip browser media-query overrides as a unit.
        cursor = 0
        while (opening := css.find('{', cursor)) != -1:
            selector = css[cursor:opening].strip()
            depth, end = 1, opening + 1
            while depth:
                depth += (css[end] == '{') - (css[end] == '}')
                end += 1
            if not selector.startswith('@'):
                selected = [s.strip() for s in selector.split(',') if s.strip().startswith(prefixes)]
                if selected:
                    scoped = ', '.join(f'.epub-from-{slug} {s}' for s in selected)
                    result.append(scoped + ' {' + css[opening + 1:end - 1] + '}')
            cursor = end
    return '\n'.join(result)


class Book:
    def __init__(self, work, language="en"):
        self.work = work
        self.language = language
        self.output = HERE / f"ThinkLikeAComputer-{EDITIONS[language]}-All-Steps.epub"
        self.ids = {path.resolve(): slug for slug, _, path in SOURCES}
        self.ids[ROOT / 'TLACPortal.html'] = 'welcome'
        self.replays = {}
        self.appendices = {}
        self.parts = []
        self.image_count = 0
        self.step_count = 0
        self.chart_count = 0
        self.chart_styles = []
        self.replay_cache = {}
        self.full_runs = {}
        self.custom_tiles = {}

    def replay(self, path):
        path = path.resolve()
        if path not in self.replay_cache:
            self.replay_cache[path] = replay_data(path)
        return self.replay_cache[path]

    def state_figure(self, data, path, step, caption):
        image_root = (path.parent / data.get('image_root', '../img')).resolve()
        paths = [self.game_tile(data['game_key'], cell, image_root) if data.get('game_key')
                 else image_root / TILES[cell] for cell in step['cells']]
        img = self.board_image(paths, data['width'])
        text = f'<figure><figcaption>{escape(caption)}</figcaption><img class="board-figure" src="{escape(img)}" alt="{escape(caption)}"/>'
        if data.get('show_eggs', True):
            text += f'<p>Eggs on the board: {len(step.get("eggs", []))}</p>'
        return text + '</figure>'

    def game_tile(self, key, cell, image_root):
        if cell in ' #oG^V<>':
            return image_root / TILES[cell]
        cache_key = (key, cell)
        if cache_key not in self.custom_tiles:
            destination = self.work / f'game-{key}-symbol-{ord(cell)}.png'
            tile = Image.new('RGB', (40, 40), '#f5ef88')
            draw = ImageDraw.Draw(tile)
            draw.rectangle((0, 0, 39, 39), outline='#263944')
            color = {'O': '#19733a', 'B': '#874310', 'M': '#b32929', 'W': '#7f2685',
                     'X': '#006a99', '*': '#b32929', '?': '#526779', 'F': '#19733a'}.get(cell, '#173d8c')
            draw.text((20, 20), cell, font=ImageFont.truetype('DejaVuSans.ttf', 25), anchor='mm', fill=color)
            tile.save(destination)
            self.custom_tiles[cache_key] = destination
        return self.custom_tiles[cache_key]

    def output_preview(self, path, heading='Graphical execution results', anchor=''):
        data = self.replay(path)
        start, finish = data['steps'][data.get('preview_start_index', 0)], data['steps'][-1]
        identifier = f' id="{escape(anchor)}"' if anchor else ''
        parts = [f'<div class="execution-preview"{identifier}><h4>{escape(heading)}</h4>']
        if data.get('has_board', True):
            parts += [self.state_figure(data, path, start, 'Starting board'),
                      self.state_figure(data, path, finish, 'Final board — sample ended' if data.get('game_key') else 'Final board — program finished')]
        output = finish.get('output', {}).get(self.language, '')
        if output:
            parts.append('<h4>Final text output</h4><pre>' + escape(output) + '</pre>')
        parts.append('</div>')
        return ''.join(parts)

    def register_replay(self, path):
        path = path.resolve()
        if path not in self.ids:
            self.ids[path] = 'execution-' + str(len(self.replays) + 1)
        self.replays[path] = self.ids[path]
        return self.ids[path]

    @staticmethod
    @lru_cache(maxsize=None)
    def tile(path):
        with Image.open(path) as img:
            return img.convert('RGB').resize((40, 40))

    def board_image(self, paths, width):
        """Render board data as one portable, coordinate-labelled illustration."""
        key = sha256((str(width) + '\n' + '\n'.join(map(str, paths))).encode()).hexdigest()[:20]
        destination = self.work / f'board-{key}.png'
        if not destination.exists():
            assert len(paths) % width == 0
            height = len(paths) // width
            img = Image.new('RGB', (width * 40 + 28, height * 40 + 28), 'white')
            draw = ImageDraw.Draw(img)
            for column in range(width):
                draw.text((28 + column * 40 + 15, 7), chr(65 + column), fill='black')
            for row in range(height):
                draw.text((5, 28 + row * 40 + 14), str(row + 1), fill='black')
            for i, path in enumerate(paths):
                img.paste(self.tile(path), (28 + i % width * 40, 28 + i // width * 40))
            img.save(destination)
            self.image_count += 1
        return str(destination)

    def clean(self, content, path, slug):
        # Each fragment owns its ids; all book links are resolved before pandoc
        # splits the document into EPUB chapters.
        for tag in list(content.select('[lang], [data-lang], [data-language], [data-execution-language]')):
            if tag.attrs is None:
                continue
            language = tag.get('data-lang') or tag.get('data-language') or tag.get('data-execution-language') or tag.get('lang')
            if language.split('-')[0] != self.language:
                tag.decompose()
        for tag in content.select('script, style, noscript, .toolbar, button, select, input, .next-lesson'):
            tag.decompose()
        for details in content.select('details'):
            details.name = 'section'
            if details.summary:
                details.summary.name = 'h4'
        for board in content.select('.board'):
            width = int(re.search(r'--columns:\s*(\d+)', board.get('style', ''))[1])
            images = [(path.parent / unquote(img['src'])).resolve() for img in board.select('img')]
            label = board.get('aria-label', 'TLAC board')
            rendered = soup(f'<img class="board-figure" alt="{escape(label)}" src="{escape(self.board_image(images, width))}"/>').img
            board.replace_with(rendered)
        for img in content.select('img'):
            src = urlsplit(img.get('src', ''))
            if src.scheme:
                raise ValueError(f'Book image must be local: {img["src"]}')
            img['src'] = str((path.parent / unquote(src.path)).resolve())
            if not Path(img['src']).is_file():
                raise FileNotFoundError(img['src'])
            img['alt'] = img.get('alt', '')
        for tag in ([content] if content.get('id') else []) + content.select('[id]'):
            tag['id'] = slug + '-' + tag['id']
        for a in content.select('a[href]'):
            href = urlsplit(a['href'])
            if href.scheme:
                continue
            destination = (path.parent / unquote(href.path)).resolve() if href.path else path.resolve()
            if href.fragment == 'debugger' and path.name in ('maze-tutorial.html', 'algorithm-insertion-sort-pyramids.html'):
                destination = ROOT / ('maze-execution.html' if slug == 'maze' else 'algorithm-insertion-sort-pyramids-output.html')
                href = href._replace(fragment='')
                a.string = 'Read the complete execution walkthrough'
            if destination not in self.ids:
                if destination.suffix == '.html' and destination.is_file() and 'const run = ' in destination.read_text():
                    self.register_replay(destination)
                elif destination.suffix in ('.py', '.txt') and destination.is_file():
                    self.ids[destination] = 'source-' + str(len(self.appendices) + 1)
                    self.appendices[destination] = self.ids[destination]
                else:
                    raise ValueError(f'Unresolved book link: {path.name}: {a["href"]}')
            target = self.ids[destination]
            a['href'] = '#' + target + ('-' + href.fragment if href.fragment else '')
            if destination in self.replays:
                a.string = 'See every step with its graphical output'
                # Show the result in the lesson itself, not just in an
                # appendix. Advanced lessons already have board-pair previews.
                paragraph = a.parent
                previous = paragraph.find_previous_sibling()
                has_preview = previous and ('board-pair' in previous.get('class', [])
                                             or 'execution-preview' in previous.get('class', []))
                if paragraph.name == 'p' and not has_preview:
                    data = self.replay(destination)
                    heading = 'Graphical execution results' if data.get('has_board', True) else 'Execution results'
                    paragraph.insert_before(soup(self.output_preview(destination, heading)).div)
        for tag in content.find_all(True):
            for attr in list(tag.attrs):
                if attr not in ('id', 'class', 'href', 'src', 'alt', 'colspan', 'rowspan', 'style'):
                    del tag.attrs[attr]
        # These sentences describe browser-only controls; the EPUB uses links
        # to complete static logs instead. Instructional content is retained.
        for p in content.select('p'):
            text = p.get_text(' ', strip=True)
            if 'The execution links below open a step-by-step debugger.' in text:
                p.string = 'The execution links below open complete walkthroughs in this book. Read each recorded instruction, variable change, and board or text output in order.'
            elif 'After each program, compare its initial and final boards, then open the full execution link.' in text:
                p.string = 'After each program, compare its initial and final boards, then read the complete execution walkthrough. The numbered instructions match the program cards. The turtle picture hides an egg directly underneath it; the egg count still includes that egg.'
            elif 'Read the numbered TLAC cards first, then use the debugger below.' in text:
                p.string = 'Read the numbered TLAC cards first, then follow the execution walkthrough. Skip a function’s enclosed cards until it is called; after returning, continue at the call site. The right-to-left search function is defined by the original program but is not called in this run.'
            elif 'Read the numbered cards, then try Next below.' in text:
                p.string = 'Read the numbered cards, then follow the execution walkthrough. Function definitions describe reusable instructions: their bodies run only when called. The loop runs its body before checking its stop condition: no means continue, yes means stop.'
        for chart in list(content.select('.chart, .htmlifyer-chart, .instruction-chart')):
            if chart.find_parent(class_='epub-html-chart'):
                continue
            wrapper = soup(f'<div class="epub-html-chart epub-from-{slug}"></div>').div
            chart.wrap(wrapper)
        return str(content)

    def add_lessons(self):
        for slug, title, path in SOURCES:
            self.chart_styles.append(chart_css(path, slug))
            parsed = soup(path.read_text(encoding='utf-8'))
            content = parsed.select_one(f'article[lang={self.language}]') or parsed.select_one(f'section.lesson[lang={self.language}]') or parsed.select_one('main')
            if slug == 'basics':
                self.add_basic_card_walkthroughs(content)
            elif slug == 'games':
                self.add_game_walkthroughs(content)
            if content.h1:
                content.h1.decompose()
            self.parts.append(f'<h1 id="{slug}">{escape(title)}</h1>' + self.clean(content, path, slug))

    def add_game_walkthroughs(self, content):
        if str(ROOT) not in sys.path:
            sys.path.insert(0, str(ROOT))
        from TLAC_boardgame.printables.epub_game_runs import SAMPLES, record_game
        for key in SAMPLES:
            path = ROOT / 'TLAC_boardgame/game_executions' / f'{key}.html'
            data = record_game(key, self.language)
            self.register_replay(path)
            self.replay_cache[path.resolve()] = data
            section = content.find(id=key)
            section.append(soup(f'<p class="execution-link"><a href="TLAC_boardgame/game_executions/{key}.html">Every step of a sample game session</a></p>').p)
            print(f'Recorded {key}: {len(data["steps"])} sample steps.', flush=True)

    def add_basic_card_walkthroughs(self, content):
        """Walk through the six introductory card examples without HTML replays."""
        rows_by_key = json.loads((ROOT / 'TLAC_8_basics_of_programming/basics_examples.json').read_text())['charts']
        for key in ('sequence-good', 'sequence-bad', 'assignment', 'conditionals', 'sequence-functions', 'output'):
            figure = content.find(id=f'program-{key}-{self.language}')
            title = figure.figcaption.get_text(' ', strip=True)
            rows = rows_by_key[key]
            labels = {}
            for row in figure.select('.instruction-row'):
                paragraphs = row.select('p')
                if len(paragraphs) > 1:
                    labels[int(paragraphs[0].get_text())] = paragraphs[1].get_text(' ', strip=True)
            x, y = 4, 9
            values, steps = {}, []
            has_board = key in ('conditionals', 'output')
            is_routine = key.startswith('sequence-')
            if is_routine:
                values = {'teeth_brushed': False, 'hair_combed': False, 'left_for_work': False}

            def snapshot(line, label):
                cells = [' '] * 100
                cells[y * 10 + x] = '^'
                watched = dict(values)
                if has_board:
                    watched.update(X=x, Y=y)
                steps.append({'label': {self.language: label}, 'line': line, 'depth': 0,
                              'cells': ''.join(cells), 'eggs': [],
                              'turtles': [{'name': 'Turtle', 'x': x, 'y': y, 'direction': '^'}],
                              'variables': [{'name': name, 'scope': 'global', 'value': copy.deepcopy(value)}
                                            for name, value in watched.items()],
                              'output': {self.language: ''}})

            snapshot(0, 'Start: before the first instruction')
            skip_until = 0
            for row in rows:
                line = row['number']
                if line < skip_until:
                    continue
                label = labels.get(line, '')
                if not label:
                    continue
                snapshot(line, 'Before: ' + label)
                if key == 'assignment':
                    values['x'] = {1: 3, 2: 5, 3: 6}[line]
                elif key == 'conditionals':
                    if line in (4, 9, 17):
                        condition = x > 3 if line == 4 else x < 3
                        snapshot(line, 'Condition result: ' + ('true; enter the block' if condition else 'false; skip instructions 0010–0012'))
                        if not condition:
                            skip_until = 13
                        continue
                    if line in (8, 21):
                        y -= 1
                    elif line == 13:
                        x = 2
                elif key == 'output' and line == 2:
                    y -= 5
                elif is_routine:
                    if row['text'] == 'Function call BrushMyTeeth':
                        values['teeth_brushed'] = True
                    elif row['text'] == 'Function call CombMyHair':
                        values['hair_combed'] = True
                    elif row['text'] == 'Function call GoToWork':
                        values['left_for_work'] = True
                        values['hair_combed_when_leaving'] = values['hair_combed']
                snapshot(line, 'After: ' + label)
            snapshot(0, 'Finished: final state')
            path = ROOT / 'TLAC_boardgame/basics_executions' / f'{key}.html'
            self.register_replay(path)
            self.replay_cache[path.resolve()] = {
                'title': {self.language: title}, 'has_board': has_board,
                'width': 10, 'height': 10, 'image_root': '../img', 'steps': steps,
                'run_note': ('This is a card-by-card walkthrough of the lesson example. '
                             'The morning routines show the state after each conceptual action; they do not print text.'
                             if is_routine else 'This walkthrough follows the lesson cards and shows each assignment, condition check, and movement.'),
            }
            figure.insert_after(soup(f'<p class="execution-link"><a href="../TLAC_boardgame/basics_executions/{key}.html">Every step of this example</a></p>').p)

    def add_replays(self):
        for path, slug in self.replays.items():
            run_start = len(self.parts)
            data = self.replay(path)
            title = data['title'][self.language]
            steps = data['steps']
            self.parts.append(f'<section class="complete-program-output"><h2 id="{slug}">Every step: {escape(title)}</h2>'
                              f'<p>{len(steps)} recorded steps follow here, in order. Each step repeats the full current state and output, including unchanged values.</p>'
                              f'<p><a href="#{slug}-step-0">Go to the first step</a> · '
                              f'<a href="#{slug}-step-{len(steps) - 1}">Go to the last step</a></p>')
            if data.get('run_note'):
                self.parts.append('<p class="note">' + escape(data['run_note']) + '</p>')
            heading = 'Starting and final graphical results' if data.get('has_board', True) else 'Final execution results'
            self.parts.append(self.output_preview(path, heading, slug + '-results'))
            if data.get('instructions'):
                self.parts.append('<h3>Numbered instructions</h3>')
                if data.get('program_html'):
                    self.chart_styles.append(chart_css(path, slug))
                    fragment = soup('<div>' + data['program_html'][self.language] + '</div>').div
                    self.parts.append(self.clean(fragment, path, slug))
                else:
                    # This is the HTML debugger's numbered list, which has no
                    # nested block chart. Preserve its badges and indentation.
                    self.parts.append('<div class="epub-html-chart"><ol class="epub-program-list">')
                    for instruction in data['instructions']:
                        label = instruction['label'][self.language]
                        kind = ' comment' if instruction.get('comment') else ''
                        self.parts.append(f'<li class="epub-program-line{kind}" style="padding-left:{8 + instruction.get("depth", 0) * 14}px">'
                                          f'<span class="epub-program-number">{instruction["number"]:04d}</span> {escape(label)}</li>')
                    self.parts.append('</ol></div>')
            for i, step in enumerate(steps):
                if i % 100 == 0:
                    # Keep chapter files small enough for memory-limited readers.
                    self.parts.append(f'<h2 id="{slug}-steps-{i + 1}">{escape(title)}: steps {i + 1}–{min(i + 100, len(steps))}</h2>')
                self.step_count += 1
                self.parts.append(f'<div class="step" id="{slug}-step-{i}"><h4>Step {i + 1}: {escape(step["label"][self.language])}</h4>')
                self.parts.append(f'<p>Instruction {step["line"]:04d} · Function call depth: {step["depth"]}</p>')
                if data.get('has_board', True):
                    self.parts.append(self.state_figure(data, path, step, f'Board at step {i + 1}'))
                    directions = {'^': 'up', 'V': 'down', '<': 'left', '>': 'right'}
                    text = '; '.join(f'{t["name"]}: X={t["x"]}, Y={t["y"]}, facing {directions[t["direction"]]}' for t in step['turtles'])
                    self.parts.append(f'<p>{escape(text)}</p>')
                text = '\n'.join(f'{v["scope"]}: {v["name"]} = {json.dumps(v["value"], ensure_ascii=False)}' for v in step.get('variables', []))
                self.parts.append(f'<h5>Watched values at this step</h5><pre class="step-variables">{escape(text or "No watched variables.")}</pre>')
                output = step.get('output', {}).get(self.language, '')
                self.parts.append(f'<h5>Complete text output at this step</h5><pre class="step-output">{escape(output or "(No text output at this step.)")}</pre>')
                self.parts.append('</div>')
            self.parts.append('</section>')
            self.full_runs[slug] = ''.join(self.parts[run_start:])
            del self.parts[run_start:]

    def place_full_runs(self, document):
        """Place each complete run at the lesson link, with an index up front."""
        index = soup('<nav id="walkthroughs"><h2>Every program: all recorded steps</h2>'
                     '<p>Complete runs appear directly after their lesson examples. Each step shows its board, watched values, and full text output. Nothing is collapsed, and unchanged output is repeated.</p><ol></ol></nav>').nav
        for path, slug in self.replays.items():
            data = self.replay(path)
            index.ol.append(soup(f'<li><a href="#{slug}-step-0">{escape(data["title"][self.language])} — all {len(data["steps"])} steps</a></li>').li)
            link = document.select_one(f'a[href="#{slug}"]')
            if link is None:
                raise ValueError('No lesson position for full run: ' + slug)
            link.parent.insert_after(soup(self.full_runs[slug]).section)
        document.select_one('#basics').insert_before(index)

    @staticmethod
    def expose_chapter_headings(document):
        # Pandoc cannot split at headings buried inside HTML section wrappers.
        # Expose lesson and 100-step headings so readers never need to load an
        # entire game's thousands of steps as a single oversized XHTML file.
        for container in list(document.select('article, main, section')):
            if container.get('id'):
                anchor = soup(f'<div id="{escape(container["id"])}"></div>').div
                container.insert_before(anchor)
            container.unwrap()

    def validate_steps(self, path):
        """Compare every packaged step with its complete source snapshot."""
        namespace = '{http://www.w3.org/1999/xhtml}'
        packaged = {}
        with ZipFile(path) as archive:
            for name in archive.namelist():
                if name.endswith('.xhtml'):
                    for node in ET.fromstring(archive.read(name)).iter():
                        if 'step' in node.get('class', '').split():
                            assert node.get('id') not in packaged, 'Duplicate step'
                            packaged[node.get('id')] = node
        expected_count = 0
        for source, slug in self.replays.items():
            data = self.replay(source)
            for index, step in enumerate(data['steps']):
                expected_count += 1
                node = packaged[f'{slug}-step-{index}']
                outputs = [p for p in node.iter(namespace + 'pre') if 'step-output' in p.get('class', '').split()]
                variables = [p for p in node.iter(namespace + 'pre') if 'step-variables' in p.get('class', '').split()]
                assert len(outputs) == len(variables) == 1, (slug, index, 'Missing full state')
                output = step.get('output', {}).get(self.language, '') or translate('(No text output at this step.)', self.language)
                assert ''.join(outputs[0].itertext()).rstrip('\n') == output.rstrip('\n'), (slug, index, 'Partial output')
                watched = '\n'.join(f'{v["scope"]}: {v["name"]} = {json.dumps(v["value"], ensure_ascii=False)}'
                                    for v in step.get('variables', [])) or translate('No watched variables.', self.language)
                assert ''.join(variables[0].itertext()).rstrip('\n') == watched, (slug, index, 'Partial variables')
                if data.get('has_board', True):
                    assert any('board-figure' in img.get('class', '').split()
                               for img in node.iter(namespace + 'img')), (slug, index, 'Missing board')
        assert len(packaged) == expected_count, 'Missing or extra execution steps'

    def build(self):
        self.parts.append('''<h1 id="welcome">Think Like A Computer</h1>
<p>English edition · Every step, complete output</p>
<p>All the tutorials and games from the TLAC portal in one offline book: eight programming basics, recursion and classes, seven games, insertion sort with pyramids, and maze exploration.</p>
<p>Read the explanations and numbered instruction cards, then follow the complete execution walkthroughs. Use your reader’s table of contents and the links within each lesson to navigate. Practice answers and game programs are expanded so they can be read without JavaScript.</p>
<p>This edition contains static illustrations and recorded walkthroughs. Interactive debugger buttons and playable programs remain in the HTML and Python editions. The companion all_boards.pdf and all_objects.pdf files in the printables folder provide boards and pieces at their intended print size.</p>''')
        self.add_lessons()
        self.add_replays()
        if self.appendices:
            self.parts.append('<h1>Source program appendix</h1>')
            for path, slug in self.appendices.items():
                self.parts.append(f'<h2 id="{slug}">{escape(path.name)}</h2><pre>{escape(path.read_text())}</pre>')
        self.parts.append('<h1 id="license">Project license</h1><p>The repository includes the following GNU General Public License.</p><pre>'
                          + escape((ROOT / 'LICENSE').read_text()) + '</pre>')
        document = soup('<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"/><title>Think Like A Computer — English edition</title></head><body>' + ''.join(self.parts) + '</body></html>')
        self.place_full_runs(document)
        localize_document(document, self.language)
        self.expose_chapter_headings(document)
        ids = [tag['id'] for tag in document.select('[id]')]
        if len(ids) != len(set(ids)):
            raise ValueError('Duplicate book anchors: ' + str([key for key, count in Counter(ids).items() if count > 1]))
        for a in document.select('a[href^="#"]'):
            if a['href'][1:] not in ids:
                raise ValueError('Broken book anchor: ' + a['href'])
        # Pandoc normalizes inline paragraphs and drops their styles. Keep
        # anchors visible to its chapter/link resolver, then restore the exact
        # HTML charts in the generated XHTML instead of flattening the cards.
        charts = {}
        for number, chart in enumerate(document.select('.epub-html-chart'), 1):
            chart_id = f'epub-chart-{number}'
            chart['id'] = chart_id
            charts[chart_id] = str(chart)
            placeholder = soup(f'<div id="{chart_id}"></div>').div
            for tag in chart.select('[id]'):
                placeholder.append(soup(f'<div id="{escape(tag["id"])}"></div>').div)
            chart.replace_with(placeholder)
        self.chart_count = len(charts)
        (self.work / 'book.html').write_text(str(document), encoding='utf-8')
        (self.work / 'book.css').write_text(CSS + '\n'.join(self.chart_styles) + '''
.epub-html-chart { font-family: Arial, Helvetica, sans-serif; color: #102f40; }
.epub-html-chart .chart, .epub-html-chart .htmlifyer-chart { overflow: visible; }
.epub-html-chart .instruction-block { border-left: 0; padding-left: 0; }
.epub-html-chart .chart .instruction-block { border: 2px solid #e0e0e0; padding: 2px 8px; }
.epub-html-chart .instruction-number { font-weight: normal; }
.epub-html-chart p { margin-top: 0; margin-bottom: 0; }
.epub-html-chart .instruction-row, .epub-html-chart .instruction-card { break-inside: avoid; }
.epub-program-list { padding: 8px; list-style: none; background: #edf8fb; border: 1px solid #7197a5; }
.epub-program-line { padding: 8px; margin: 4px 0; border: 2px solid transparent; overflow-wrap: anywhere; }
.epub-program-line.comment { color: #24633b; background: transparent; }
.epub-program-number { background: #173d8c; color: #fff7a3; padding: 2px 5px; margin-right: 8px; }
''')
        subprocess.run(['pandoc', str(self.work / 'book.html'), '-f', 'html', '-t', 'epub3',
                        '--standalone', '--toc', '--toc-depth=2', '--split-level=2',
                        '--metadata', f'lang={self.language}', '--metadata', 'title=' + translate('Think Like A Computer — All Steps Edition', self.language),
                        '--metadata', 'subtitle=' + translate('English edition — every step and complete output', self.language),
                        '--metadata', 'toc-title=' + translate('Table of contents', self.language),
                        '--css', str(self.work / 'book.css'), '-o', str(self.output)], check=True)
        restore_html_charts(self.output, charts)
        validate(self.output, self.language)
        self.validate_steps(self.output)
        if self.language == "en":
            shutil.copyfile(self.output, LEGACY_OUTPUT)
        print(f'{self.output.name}: {len(SOURCES)} tutorial collections, {len(self.replays)} complete walkthroughs, '
              f'{self.step_count} steps, {self.image_count} board illustrations, {self.chart_count} HTML charts; '
              f'{self.output.stat().st_size / 1024 / 1024:.1f} MiB.')


def restore_html_charts(path, charts):
    """Restore styled XHTML and package its local image assets in the EPUB."""
    XHTML = 'http://www.w3.org/1999/xhtml'
    OPF = 'http://www.idpf.org/2007/opf'
    ET.register_namespace('', XHTML)
    ET.register_namespace('epub', 'http://www.idpf.org/2007/ops')
    with ZipFile(path) as original:
        entries = [(info, original.read(info.filename)) for info in original.infolist()]
    opf_name = next(info.filename for info, _ in entries if info.filename.endswith('.opf'))
    package_root = posixpath.dirname(opf_name)
    assets, restored = {}, set()
    changed = {}
    for info, data in entries:
        if not info.filename.endswith('.xhtml'):
            continue
        tree = ET.fromstring(data)
        touched = False
        for parent in list(tree.iter()):
            for index, node in enumerate(list(parent)):
                chart_id = node.get('id')
                if chart_id not in charts:
                    continue
                fragment = soup(charts[chart_id]).div
                fragment['xmlns'] = XHTML
                for img in fragment.select('img'):
                    source = Path(img['src'])
                    image_data = source.read_bytes()
                    filename = 'html-chart-' + sha256(image_data).hexdigest()[:20] + source.suffix.lower()
                    target = package_root + '/media/' + filename
                    assets[target] = image_data
                    img['src'] = posixpath.relpath(target, posixpath.dirname(info.filename))
                replacement = ET.fromstring(str(fragment))
                replacement.tail = node.tail
                parent.remove(node)
                parent.insert(index, replacement)
                restored.add(chart_id)
                touched = True
        if touched:
            changed[info.filename] = ET.tostring(tree, encoding='utf-8', xml_declaration=True)
    assert restored == set(charts), ('Missing HTML charts', set(charts) - restored)
    package = ET.fromstring(next(data for info, data in entries if info.filename == opf_name))
    manifest = package.find(f'{{{OPF}}}manifest')
    for number, target in enumerate(assets, 1):
        ET.SubElement(manifest, f'{{{OPF}}}item', {
            'id': f'html-chart-asset-{number}', 'href': posixpath.relpath(target, package_root),
            'media-type': mimetypes.guess_type(target)[0]})
    ET.register_namespace('', OPF)
    ET.register_namespace('dc', 'http://purl.org/dc/elements/1.1/')
    changed[opf_name] = ET.tostring(package, encoding='utf-8', xml_declaration=True)
    rebuilt = path.with_suffix('.tmp.epub')
    with ZipFile(rebuilt, 'w') as archive:
        for info, data in entries:
            archive.writestr(info, changed.get(info.filename, data))
        for target, data in assets.items():
            archive.writestr(target, data, compress_type=ZIP_DEFLATED)
    rebuilt.replace(path)


def validate(path, language="en"):
    """Check archive structure, edition language, XML, links and local images."""
    import posixpath
    with ZipFile(path) as archive:
        names = set(archive.namelist())
        assert archive.infolist()[0].filename == 'mimetype'
        assert archive.infolist()[0].compress_type == 0
        assert archive.read('mimetype') == b'application/epub+zip'
        documents = {name: ET.fromstring(archive.read(name)) for name in names
                     if name.endswith(('.xhtml', '.opf', '.ncx', '.xml'))}
        package = next(doc for name, doc in documents.items() if name.endswith('.opf'))
        assert package.find('{http://www.idpf.org/2007/opf}metadata/{http://purl.org/dc/elements/1.1/}language').text == language
        for name, doc in documents.items():
            if not name.endswith('.xhtml'):
                continue
            assert not doc.findall('.//{http://www.w3.org/1999/xhtml}script')
            for tag in doc.iter():
                for attr in ('src', 'href'):
                    if attr not in tag.attrib:
                        continue
                    link = urlsplit(tag.attrib[attr])
                    if link.scheme:
                        assert attr != 'src', 'Remote image in EPUB'
                        continue
                    target = posixpath.normpath(posixpath.join(posixpath.dirname(name), unquote(link.path))) if link.path else name
                    assert target in names, (name, target)
                    if link.fragment:
                        assert any(el.get('id') == unquote(link.fragment) for el in documents[target].iter()), (name, tag.attrib[attr])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--language', choices=EDITIONS, default='en')
    args = parser.parse_args()
    with tempfile.TemporaryDirectory(prefix='tlac-epub-') as directory:
        Book(Path(directory), args.language).build()
