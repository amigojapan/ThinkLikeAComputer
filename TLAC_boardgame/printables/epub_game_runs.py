"""Record bounded, reproducible sample sessions of the unmodified game sources."""
import contextlib
import copy
import io
from pathlib import Path
import random
import sys

from bs4 import BeautifulSoup

from .epub_translations import translate, game_note

ROOT = Path(__file__).resolve().parents[2]
SAMPLES = {
    'snake': ('snakerulebook.py', (15, 15), ['D', 'W', 'Q']),
    'pacman': ('pacmanrulebook.py', (19, 14), ['D', 'D']),
    'sokoban': ('sokobanrulebook.py', (8, 8), ['W', 'A', 'Q']),
    'minesweeper': ('minesweeperrulebook.py', (10, 10), ['F', 'D', 'R', 'Q']),
    'frogger': ('froggerrulebook.py', (15, 11), ['W', 'W', 'Q']),
    'bomberman': ('bombermanrulebook.py', (11, 11), ['B', 'D', 'D', ' ', 'Q']),
    'life': ('conwaysgameofliferulebook.py', (15, 15), ['', 'Q']),
}


class EndSample(Exception):
    pass


def record_game(key, language="en"):
    # Import only the simulator. Game files run in an isolated namespace with
    # scripted input; no real stdin, GUI, sleeping or external writes are used.
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    import TLACsimulator as TLAC
    filename, dimensions, commands = SAMPLES[key]
    path = ROOT / filename
    page = BeautifulSoup((ROOT / 'games.html').read_text(), 'html.parser')
    section = page.find(id=key)
    title = section.h2.select_one(f'[data-lang={language}]').get_text(' ', strip=True)
    cards = section.select_one(f'.full-program[data-lang={language}]')
    by_source, labels, source_labels = {}, {}, {}
    for card in cards.select('.instruction-card[data-source-line]'):
        number = int(card.select_one('.instruction-number').get_text())
        labels[number] = ' '.join(span.get_text(' ', strip=True) for span in card.find_all('span', recursive=False)[1:])
        line = int(card['data-source-line'])
        by_source.setdefault(line, number)
        source_labels.setdefault(line, []).append(labels[number])
    board = TLAC.initGlobals()
    board.W, board.H = dimensions
    board.slots = TLAC.initSlots(board)
    board.turtle, board.ghosts = TLAC.initTurtle(), []
    steps, used = [], []
    output = io.StringIO()
    preview_start = 0
    current_frame = None
    ended = 'The sample session finished normally.'
    old_board, old_trace, old_random = TLAC.globals, sys.gettrace(), random.getstate()
    original_read = TLAC.readBoardFromFile

    def simple(value, depth=0):
        if depth > 4:
            return False
        if value is None or type(value) in (str, int, float, bool):
            return True
        if isinstance(value, (tuple, list)):
            return len(value) <= 300 and all(simple(v, depth + 1) for v in value)
        if isinstance(value, dict):
            return all(type(k) is str and simple(v, depth + 1) for k, v in value.items())
        return False

    def snapshot(label, frame=None):
        if len(steps) >= 60000:
            raise RuntimeError(f'{key}: sample exceeded 60,000 source steps')
        frame = frame or current_frame
        cells = []
        for slot in board.slots:
            if key == 'life':
                cell = 'O' if getattr(slot, 'is_alive', False) else ' '
            elif key == 'minesweeper':
                cell = ('F' if getattr(slot, 'flagged', False) else
                        '?' if not getattr(slot, 'revealed', False) else
                        '*' if getattr(slot, 'is_mine', False) else
                        str(slot.neighbor_mines) if getattr(slot, 'neighbor_mines', 0) else ' ')
            else:
                cell = '#' if slot.wall else 'G' if slot.goal else 'X' if slot.diamond else 'o' if slot.containsEgg else ' '
            cells.append(cell)

        def put(x, y, char):
            if 0 <= x < board.W and 0 <= y < board.H:
                cells[y * board.W + x] = char

        if key == 'snake':
            for x, y in getattr(board, 'snake_body', [])[1:]:
                put(x, y, 'O')
            if hasattr(board, 'food'):
                put(*board.food, '@')
        elif key == 'sokoban':
            for x, y in getattr(board, 'boxes', []):
                put(x, y, 'B')
        elif key == 'frogger':
            for car in getattr(board, 'cars', []):
                put(car['x'], car['y'], car['char'])
        elif key == 'bomberman':
            for item in getattr(board, 'enemies', []):
                put(item['x'], item['y'], item['char'])
            for item in getattr(board, 'bombs', []):
                put(item['x'], item['y'], str(max(0, item['timer'])))
        else:
            for ghost in board.ghosts:
                put(ghost.X, ghost.Y, ghost.char)
        turtles = []
        if key != 'life':
            put(board.turtle.X, board.turtle.Y, '^' if key == 'minesweeper' else board.turtle.direction)
            turtles = [{'name': 'Player', 'x': board.turtle.X, 'y': board.turtle.Y, 'direction': board.turtle.direction}]
        variables = []
        for name, value in vars(board).items():
            if name not in ('board', 'MoveNumber') and simple(value):
                variables.append({'name': name, 'scope': 'global', 'value': copy.deepcopy(value)})
        if frame and frame.f_code.co_name != '<module>':
            for name, value in frame.f_locals.items():
                if not name.startswith('__') and simple(value):
                    variables.append({'name': name, 'scope': 'local', 'value': copy.deepcopy(value)})
        depth, parent = 0, frame.f_back if frame else None
        while parent:
            depth += parent.f_code.co_filename == str(path)
            parent = parent.f_back
        steps.append({'line': by_source.get(frame.f_lineno, 0) if frame else 0,
                      'depth': depth, 'label': {language: translate(label, language)}, 'cells': ''.join(cells),
                      'eggs': [i for i, slot in enumerate(board.slots) if slot.containsEgg],
                      'turtles': turtles, 'variables': variables, 'output': {language: output.getvalue()}})

    def sample_input(prompt=''):
        nonlocal preview_start
        if not used:
            preview_start = len(steps)
            snapshot('Starting playable board: ready for the first command')
        if len(used) >= len(commands):
            sys.settrace(None)
            raise EndSample()
        command = commands[len(used)]
        used.append(command)
        print(prompt + (command if command else '[Enter]'))
        snapshot('Player input: ' + ('Enter' if command == '' else 'Space / wait' if command == ' ' else command))
        return command

    def trace(frame, event, arg):
        nonlocal current_frame
        if frame.f_code.co_filename != str(path):
            return None
        current_frame = frame
        number = by_source.get(frame.f_lineno)
        if number and event == 'line':
            snapshot('Before: ' + ' / '.join(source_labels[frame.f_lineno]), frame)
        elif number and event == 'return' and frame.f_code.co_name != '<module>':
            snapshot('Return from ' + frame.f_code.co_name, frame)
        return trace

    def read_board(state, filename):
        return original_read(state, ROOT / filename)

    try:
        TLAC.globals = board
        TLAC.readBoardFromFile = read_board
        random.seed(7)
        with contextlib.redirect_stdout(output):
            snapshot('Start: before the game setup instructions')
            sys.settrace(trace)
            try:
                exec(compile(path.read_text(), str(path), 'exec'),
                     {'__name__': '__main__', '__file__': str(path), 'input': sample_input})
            except EndSample:
                ended = 'Sample stopped at the next input prompt after the chosen commands; the game is still in progress.'
            except SystemExit as error:
                if error.code not in (None, 0):
                    raise
                ended = 'The player quit the game.'
            finally:
                sys.settrace(old_trace)
            current_frame = None
            snapshot('End of sample: ' + ended)
    finally:
        TLAC.globals = old_board
        TLAC.readBoardFromFile = original_read
        random.setstate(old_random)
        sys.settrace(old_trace)
    controls = ', '.join(translate('Enter' if c == '' else 'Space / wait' if c == ' ' else c, language) for c in used)
    legend = {
        'snake': 'O = snake body; @ = food.',
        'pacman': 'M and W = ghosts; X = diamond; eggs = pellets.',
        'sokoban': 'B = box; flag = goal.',
        'minesweeper': '? = covered cell; F = flag; * = mine; numbers = neighboring mines; turtle = cursor.',
        'frogger': 'c = car; t and T = trucks; flags = finish row.',
        'bomberman': 'M = enemy; numbers = bomb countdown; eggs = breakable crates.',
        'life': 'O = living cell; empty square = dead cell.',
    }[key]
    return {'title': {language: title + translate(' — sample game session', language)}, 'width': dimensions[0],
            'height': dimensions[1], 'has_board': True, 'show_eggs': key == 'pacman',
            'image_root': str(ROOT / 'TLAC_boardgame/img'), 'steps': steps,
            'preview_start_index': preview_start, 'game_key': key,
            'run_note': game_note(language, filename, controls, ended, legend)}
