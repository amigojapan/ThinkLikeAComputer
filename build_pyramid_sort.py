#!/usr/bin/env python3
"""Build pyramid-sort instruction cards and debugger pages from the real program.

Run: python3 build_pyramid_sort.py
The sorting source is executed unchanged; simulator calls and Python trace events
record all checks, moves, function calls, and returns, including temporary swaps.
"""
import ast
import contextlib
from html import escape
import io
from pathlib import Path
import re
import subprocess
import sys

import TLACsimulator as TLAC
from game_instruction_cards import Cards, words
from TLAC_boardgame.execution_view import render_execution

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / 'algorithm-insertion-sort-pyramids-simplified.py'
LANGS = ('en', 'es', 'ja')
t = words
TITLE = t('Insertion sort with pyramids', 'Ordenación por inserción con pirámides', 'ピラミッドの挿入ソート')
FUNCTIONS = {
    'findNextElement': t('Find the next unsorted pyramid', 'Buscar la siguiente pirámide sin ordenar', '次の未整列ピラミッドを探す'),
    'findNextBottom': t('Find the rightmost pyramid in the sorting row', 'Buscar la pirámide más a la derecha en la fila de ordenación', '整列用の行で一番右のピラミッドを探す'),
}


class PyramidCards(Cards):
    def __init__(self, source, lang):
        super().__init__(source, 'pyramids', lang)
        # Bindings/imports only adapt the simulator API. The learner starts at
        # the actual board-loading instruction, whose source line is preserved.
        start = next(i for i, node in enumerate(self.tree.body)
                     if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call)
                     and ast.unparse(node.value.func) == 'readBoardFromFile')
        self.tree.body = [node for node in self.tree.body[start:] if not isinstance(node, ast.Import)]
        self.instructions = []
        self.by_source = {}

    def name(self, name):
        return FUNCTIONS[name][self.lang] if name in FUNCTIONS else super().name(name)

    def call(self, node, as_value=True):
        name = ast.unparse(node.func)
        if name in FUNCTIONS:
            return self.say('the result of calling “{name}”', 'el resultado de llamar a «{name}»', '「{name}」を呼び出した結果', name=self.name(name)) if as_value else self.say('Call “{name}”', 'Llamar a «{name}»', '「{name}」を呼び出す', name=self.name(name))
        if name == 'readBoardFromFile':
            return self.say('Load the starting board: sizes 5, 4, 3, 1, 2 in F3–J3', 'Cargar el tablero inicial: tamaños 5, 4, 3, 1, 2 en F3–J3', '初期盤面を読み込む：F3～J3にサイズ5、4、3、1、2')
        if name == 'printBoard':
            return self.say('Display the current board', 'Mostrar el tablero actual', '現在の盤面を表示する')
        if name == 'teleportTurtleTo':
            return self.say('Place the turtle at E10 (X=4, Y=9)', 'Colocar la tortuga en E10 (X=4, Y=9)', '亀をE10（X=4、Y=9）に置く')
        if name == 'peekPyramidThere':
            return self.say('the pyramid size and coordinates at X={x}, Y={y}; use “not found” if empty', 'el tamaño y las coordenadas de la pirámide en X={x}, Y={y}; usar “not found” si está vacío', 'X={x}、Y={y}にあるピラミッドのサイズと座標。なければ「not found」', x=self.expr(node.args[0]), y=self.expr(node.args[1]))
        if name == 'simulateUserInputTeleportPyramidTo':
            return self.say('Move pyramid {size} to X={x}, Y={y}', 'Mover la pirámide {size} a X={x}, Y={y}', 'ピラミッド{size}をX={x}、Y={y}へ動かす', size=self.expr(node.args[0]), x=self.expr(node.args[1]), y=self.expr(node.args[2]))
        if name == 'range' and len(node.args) == 3:
            # These two loops use constant arithmetic bounds; do not evaluate
            # source code. Recognize the ascending/descending scan explicitly.
            if ast.unparse(node) == 'range(0, 9 + 1, 1)':
                return self.say('columns 0 through 9, from left to right', 'columnas 0 a 9, de izquierda a derecha', '左から右へ列0～9')
            if ast.unparse(node) == 'range(9, 0 - 1, -1)':
                return self.say('columns 9 through 0, from right to left', 'columnas 9 a 0, de derecha a izquierda', '右から左へ列9～0')
            raise ValueError('Unexpected pyramid scan: ' + ast.unparse(node))
        return super().call(node, as_value)

    def card(self, text, node=None, kind='action', anchor=''):
        result = super().card(text, node, kind, anchor)
        if node is not None:
            self.by_source[node.lineno] = self.number
        self.instructions.append({'number': self.number, 'text': text,
                                  'depth': node.col_offset // 4 if node else 0,
                                  'comment': kind in ('comment', 'function')})
        return result


def instruction_cards():
    converted = subprocess.run(
        [sys.executable, str(ROOT / 'htmlifyer.py'), 'en', 'HTML', str(SOURCE)],
        capture_output=True, text=True, encoding='utf-8', check=True,
    ).stdout
    body = re.search(r'<body[^>]*>(.*?)</body>', converted, re.S)
    if body is None:
        raise ValueError('htmlifyer.py did not produce a program body')
    charts, instructions, source_map = {}, [], None
    for lang in LANGS:
        renderer = PyramidCards(SOURCE.read_text(encoding='utf-8'), lang)
        # The AST supplies localized wording and trace identifiers only.
        # The actual card markup and nested blocks come from htmlifyer.py.
        renderer.render()
        if source_map is None:
            source_map = renderer.by_source
            instructions = [{key: value for key, value in item.items() if key != 'text'} | {'label': {}}
                            for item in renderer.instructions]
        assert source_map == renderer.by_source
        for destination, item in zip(instructions, renderer.instructions):
            destination['label'][lang] = item['text']
        number = None

        def localize(match):
            nonlocal number
            token = match[0]
            paragraph = re.fullmatch(r'<p([^>]*)>(.*?)</p>', token, re.S)
            if paragraph:
                attrs, raw = paragraph.groups()
                if raw.strip().isdigit():
                    number = source_map.get(int(raw.strip()))
                    return f'<p{attrs} class="instruction-number">{number:04d}</p>' if number else ''
                if number:
                    label = renderer.instructions[number - 1]['text']
                    return f'<p{attrs} data-line="{number}">{escape(label)}</p>'
                return ''
            if not number:
                return ''
            return token.replace('<img ', '<img alt="" ')

        # Remove simulator bindings, imports, comments and blank lines, while
        # preserving every converter block boundary. Number the learner's
        # executable cards consistently with the recorded execution.
        chart = re.sub(r'<p[^>]*>.*?</p>|<img\b[^>]*>|<BR>', localize, body[1], flags=re.S)
        charts[lang] = (f'<!-- Generated by htmlifyer.py; localized labels and replay card numbers. -->'
                        f'<div class="htmlifyer-chart">{chart}</div>')
    return charts, instructions, source_map


def record(instructions=None, source_map=None):
    if instructions is None:
        _, instructions, source_map = instruction_cards()
    previous_board, previous_trace = TLAC.globals, sys.gettrace()
    board = TLAC.initGlobals()
    board.W = board.H = 10
    board.slots = TLAC.initSlots(board)
    board.turtle = TLAC.initTurtle()
    board.ghosts = []
    namespace = {'__name__': '__main__', '__file__': str(SOURCE)}
    steps, output = [], []
    current_line, current_frame = 0, None
    names = ('readBoardFromFile', 'teleportTurtleTo', 'printBoard',
             'peekPyramidThere', 'simulateUserInputTeleportPyramidTo')
    originals = {name: getattr(TLAC, name) for name in names}

    def snapshot(label, frame=None, line=None, event='instruction', action=None):
        if len(steps) >= 5000:
            raise RuntimeError('Pyramid sort exceeded 5,000 recorded steps')
        selected = current_frame if frame is None else frame
        depth = 0
        parent = selected.f_back if selected else None
        while parent:
            if parent.f_code.co_filename == str(SOURCE):
                depth += 1
            parent = parent.f_back
        cells = [str(cell.pyramidSize) if cell.pyramidSize else '#' if cell.wall else ' ' for cell in board.slots]
        turtle = board.turtle
        cells[turtle.Y * board.W + turtle.X] = turtle.direction
        variables = []
        for name in ('col', 'pyramidNumber', 'x', 'y', 'current', 'left_value', 'current_value'):
            if name in namespace:
                variables.append({'name': name, 'scope': 'global', 'value': namespace[name]})
        if selected and selected.f_code.co_name != '<module>':
            for name in ('x', 'value', '_x', '_y'):
                if name in selected.f_locals:
                    variables.append({'name': name, 'scope': 'local', 'value': selected.f_locals[name]})
        for name, row in (('unsorted_row', 2), ('sorted_row', 4)):
            variables.append({'name': name, 'scope': 'global',
                              'value': [cell.pyramidSize or None for cell in board.slots[row * 10:row * 10 + 10]]})
        variables.append({'name': 'temporary_A1', 'scope': 'global', 'value': board.slots[0].pyramidSize or None})
        pyramids = [{'size': cell.pyramidSize, 'x': i % 10, 'y': i // 10}
                    for i, cell in enumerate(board.slots) if cell.pyramidSize]
        steps.append({'label': label, 'line': current_line if line is None else line,
                      'depth': depth, 'cells': ''.join(cells), 'eggs': [], 'pyramids': pyramids,
                      'turtles': [{'name': 'Turtle', 'x': turtle.X, 'y': turtle.Y, 'direction': turtle.direction}],
                      'variables': variables, 'output': {lang: ''.join(output) for lang in LANGS},
                      'event': event, 'action': action})

    def program_print(*args, sep=' ', end='\n', **kwargs):
        output.append(sep.join(str(arg) for arg in args) + end)
    namespace['print'] = program_print

    def wrapped(name):
        def perform(*args, **kwargs):
            result = originals[name](*args, **kwargs)
            # Simulator internals also call printBoard. Record only direct
            # instructions in the sorting program, not duplicate rendering.
            caller = sys._getframe(1)
            if caller.f_code.co_filename != str(SOURCE):
                return result
            if name == 'simulateUserInputTeleportPyramidTo':
                _, size, x, y = args
                position = f'{chr(65 + x)}{y + 1} (X={x}, Y={y})'
                label = t(f'After: moved pyramid {size} to {position}', f'Después: pirámide {size} movida a {position}', f'実行後：ピラミッド{size}を{position}へ移動')
            elif name == 'peekPyramidThere':
                _, x, y = args
                label = t(f'After: checked X={x}, Y={y} → {result[0]}', f'Después: comprobar X={x}, Y={y} → {result[0]}', f'実行後：X={x}、Y={y}を確認 → {result[0]}')
            else:
                label = {
                    'readBoardFromFile': t('After: starting board loaded', 'Después: tablero inicial cargado', '実行後：初期盤面を読み込んだ'),
                    'teleportTurtleTo': t('After: turtle placed at E10', 'Después: tortuga colocada en E10', '実行後：亀をE10に置いた'),
                    'printBoard': t('After: board displayed', 'Después: tablero mostrado', '実行後：盤面を表示した'),
                }[name]
            snapshot(label, frame=caller, event='action', action=name)
            return result
        return perform

    def trace(frame, event, arg):
        nonlocal current_line, current_frame
        if frame.f_code.co_filename != str(SOURCE):
            return None
        if frame.f_lineno not in source_map:
            return trace
        current_line = source_map[frame.f_lineno]
        current_frame = frame
        if event == 'line':
            before = t('Before', 'Antes', '実行前')
            label = instructions[current_line - 1]['label']
            snapshot({lang: before[lang] + ': ' + label[lang] for lang in LANGS}, event='before')
        elif frame.f_code.co_name != '<module>' and event in ('call', 'return'):
            name = FUNCTIONS[frame.f_code.co_name]
            prefix = t('Enter function', 'Entrar en la función', '関数に入る') if event == 'call' else t('Return from function', 'Volver de la función', '関数から戻る')
            snapshot({lang: f'{prefix[lang]}: {name[lang]}' for lang in LANGS}, event=event)
        return trace

    try:
        TLAC.globals = board
        for name in names:
            setattr(TLAC, name, wrapped(name))
        snapshot(t('Start: before loading the board', 'Inicio: antes de cargar el tablero', '開始：盤面を読み込む前'), event='start')
        with contextlib.redirect_stdout(io.StringIO()):
            sys.settrace(trace)
            exec(compile(SOURCE.read_text(encoding='utf-8'), str(SOURCE), 'exec'), namespace)
        sys.settrace(previous_trace)
        current_frame = None
        snapshot(t('Finished: pyramids 1, 2, 3, 4, 5 in A5–E5', 'Final: pirámides 1, 2, 3, 4, 5 en A5–E5', '終了：A5～E5にピラミッド1、2、3、4、5'), event='finish')
        assert [cell.pyramidSize for cell in board.slots[40:45]] == [1, 2, 3, 4, 5]
        assert not any(cell.pyramidSize for cell in board.slots[20:30])
        assert len(steps[-1]['pyramids']) == 5 and not board.slots[0].pyramidSize
    finally:
        sys.settrace(previous_trace)
        TLAC.globals = previous_board
        for name, original in originals.items():
            setattr(TLAC, name, original)
    return {'source': SOURCE.name, 'title': TITLE, 'tutorial': 'algorithm-insertion-sort-pyramids.html',
            'anchor': 'cards', 'width': 10, 'height': 10, 'image_root': 'TLAC_boardgame/img',
            'show_eggs': False, 'instructions': instructions, 'steps': steps,
            'debugger_title': t('Step through the sorting process', 'Recorrer la ordenación paso a paso', '並べ替えを1ステップずつ確認する'),
            'note': t('Before = the highlighted card is about to run. After = a check or move has finished. Use Next and Previous to inspect every comparison and temporary move; Finish shows the sorted row. Variables and the program’s original printed messages are shown below. Empty positions appear as null. Printed A1 corresponds to X=0, Y=0; the sorting row is A5–J5 (Y=4).',
                      'Antes = la tarjeta resaltada está a punto de ejecutarse. Después = ha terminado una comprobación o movimiento. Usa Siguiente y Anterior para revisar cada comparación y movimiento temporal; Final muestra la fila ordenada. Abajo aparecen variables y los mensajes originales del programa. Las posiciones vacías se muestran como null. A1 corresponde a X=0, Y=0; la fila de ordenación es A5–J5 (Y=4).',
                      '「実行前」は強調されたカードをこれから実行すること、「実行後」は確認や移動が終わったことを示します。「次へ」「前へ」で比較や一時的な移動を確認し、「最後」で整列した行を表示します。下には変数とプログラムの元の出力を表示します。空の位置はnullです。印刷した盤面のA1はX=0、Y=0、整列用の行はA5～J5（Y=4）です。')}


LESSON_CSS = '''
.lesson { background: #edf8fb; border: 1px solid #7197a5; border-radius: 8px; padding: 20px; margin: 24px 0; }
.lesson h2 { margin-top: 0; } .lesson a { font-weight: bold; }
@media(max-width:600px) { .lesson { padding: 12px; } }
'''


def lesson(charts):
    descriptions = t(
        'Insert one pyramid at a time into the sorted row. Compare it with the pyramid to its left; if the pair is out of order, swap them using A1 as a temporary space. Continue left until the new pyramid is in order. The input is 5, 4, 3, 1, 2 and the result is 1, 2, 3, 4, 5.',
        'Inserta una pirámide a la vez en la fila ordenada. Compárala con la de su izquierda; si están desordenadas, intercámbialas usando A1 como espacio temporal. Continúa hacia la izquierda hasta que quede en orden. La entrada es 5, 4, 3, 1, 2 y el resultado es 1, 2, 3, 4, 5.',
        'ピラミッドを1つずつ整列済みの行へ挿入します。左隣と比べ、順序が逆ならA1を一時置き場にして交換します。正しい位置に来るまで左へ進めます。入力は5、4、3、1、2、結果は1、2、3、4、5です。')
    reading = t('Read the numbered TLAC cards first, then use the debugger below. Skip a function’s enclosed cards until it is called; after returning, continue at the call site. The right-to-left search function is defined by the original program but is not called in this run.',
                'Lee primero las tarjetas TLAC numeradas y después usa el depurador de abajo. Salta las tarjetas internas de una función hasta que se llame; al volver, continúa desde la llamada. La función de búsqueda de derecha a izquierda está definida en el programa original, pero no se llama en esta ejecución.',
                'まず番号付きのTLACカードを読み、その下のデバッガーを使ってください。関数の中は呼び出されるまで飛ばし、戻ったら呼び出し元から続けます。右から左へ探す関数は元のプログラムで定義されていますが、この実行では呼び出されません。')
    parts = []
    for lang in LANGS:
        parts += [f'<section class="lesson" id="cards-{lang}" data-execution-language="{lang}" lang="{lang}"{" hidden" if lang != "en" else ""}>',
                  '<h2>' + t('TLAC instruction cards', 'Tarjetas de instrucciones TLAC', 'TLAC命令カード')[lang] + '</h2>',
                  '<p>' + escape(descriptions[lang]) + '</p><p>' + escape(reading[lang]) + '</p>',
                  '<p><a href="#debugger">' + t('Jump to the step-through debugger ↓', 'Ir al depurador paso a paso ↓', 'ステップ実行のデバッガーへ ↓')[lang] + '</a></p>',
                  charts[lang], '</section>']
    return ''.join(parts)


def build():
    charts, instructions, source_map = instruction_cards()
    data = record(instructions, source_map)
    data['program_html'] = charts
    output = render_execution(data)
    (ROOT / 'algorithm-insertion-sort-pyramids-output.html').write_text(output, encoding='utf-8')
    board_output = dict(data, image_root='img', tutorial='../algorithm-insertion-sort-pyramids.html')
    board_output['program_html'] = {lang: chart.replace('TLAC_boardgame/img/', 'img/') for lang, chart in charts.items()}
    (ROOT / 'TLAC_boardgame/algorithm-insertion-sort-pyramids-output.html').write_text(render_execution(board_output), encoding='utf-8')
    combined = dict(data, lesson_html=lesson(charts), extra_css=LESSON_CSS, tutorial='TLACPortal.html', anchor='learn')
    (ROOT / 'algorithm-insertion-sort-pyramids.html').write_text(render_execution(combined), encoding='utf-8')
    print(f'Pyramid sort: {len(instructions)} TLAC cards, {len(data["steps"])} recorded steps, final row [1, 2, 3, 4, 5].')


if __name__ == '__main__':
    build()
