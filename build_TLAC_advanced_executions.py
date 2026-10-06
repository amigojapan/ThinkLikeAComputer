#!/usr/bin/env python3
"""Execute the lesson sources and save complete, offline HTML board replays.

The simplified programs run unchanged with their usual TLAC instruction names
bound to TLACsimulator. Record every source instruction, primitive action/check,
and recursive call/return. The HTML embeds the trace; opening it needs no server.
Run through TLAC_boardgame/makeBoards.bash --advanced to rebuild all examples.
"""
import argparse
import contextlib
import io
import json
from pathlib import Path
import sys

import TLACsimulator as TLAC
from TLAC_turtle_class import Turtle, prepare_board
from TLAC_boardgame.execution_view import render_execution
from build_TLAC_advanced_concepts import LANGS, PROBLEMS, source_charts, t

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / 'TLAC_boardgame' / 'advanced_executions'
CLASS_TITLES = {
    'classes-turtle': t('One turtle leaves an egg trail', 'Una tortuga deja un rastro de huevos', '1匹の亀で卵の道を作る'),
    'classes-two-turtles': t('Two turtle objects share a board', 'Dos objetos tortuga comparten un tablero', '2つの亀オブジェクトで同じ盤面を使う'),
}


def specification(key):
    if key in CLASS_TITLES:
        source = 'docs_' + key.replace('-', '_') + '-simplified.py'
        return source, CLASS_TITLES[key], key
    problem, kind = key.split('-')
    number = int(problem.removeprefix('problem'))
    if number not in PROBLEMS or kind not in ('loop', 'recursive'):
        raise ValueError(key)
    suffix = '-non-recursive' if kind == 'loop' else ''
    variant = t('without recursion', 'sin recursión', '再帰なし') if kind == 'loop' else t('with recursion', 'con recursión', '再帰あり')
    title = {lang: f'{number}. {PROBLEMS[number]["title"][lang]} — {variant[lang]}' for lang in LANGS}
    return f'{problem}-program{suffix}-simplified.py', title, f'p{number}-{kind}'


def record(key):
    source, title, anchor = specification(key)
    _, labels = source_charts(source)
    path = str(ROOT / source)
    if key in CLASS_TITLES:
        prepare_board()
    else:
        board = TLAC.initGlobals()
        board.W = board.H = 10
        board.slots = TLAC.initSlots(board)
        board.turtle = TLAC.initTurtle()
        board.turtle.X, board.turtle.Y = 4, 9
        board.ghosts = []
        TLAC.globals = board
    steps = []
    current_line, depth, ended = 0, 0, False
    namespace = {'__name__': '__main__', 'H': TLAC.globals.H, 'W': TLAC.globals.W, 'turtledirection': '^'}

    def snapshot(label, line=None, call_depth=None):
        if len(steps) >= 20000:
            raise RuntimeError(f'{source}: execution exceeded 20,000 recorded steps')
        board = TLAC.globals
        cells = ['#' if cell.wall else 'o' if cell.containsEgg else ' ' for cell in board.slots]
        turtles = getattr(board, 'lesson_turtles', [board.turtle])
        turtle_states = []
        for turtle in turtles:
            if not (0 <= turtle.X < board.W and 0 <= turtle.Y < board.H):
                raise RuntimeError(f'{source}: turtle left the board at {turtle.X}, {turtle.Y}')
            cells[turtle.Y * board.W + turtle.X] = turtle.direction
            turtle_states.append({'name': getattr(turtle, 'name', 'Turtle'), 'x': turtle.X, 'y': turtle.Y, 'direction': turtle.direction})
        steps.append({'label': label, 'line': current_line if line is None else line,
                      'depth': depth if call_depth is None else call_depth,
                      'cells': ''.join(cells), 'turtles': turtle_states,
                      'eggs': [i for i, cell in enumerate(board.slots) if cell.containsEgg]})

    snapshot(t('Start: before the first instruction', 'Inicio: antes de la primera instrucción', '開始：最初の命令を実行する前'))
    names = ('fd', 'lt', 'rt', 'layEgg', 'testIfICanProceed', 'amILayingOnAnEgg', 'end')
    originals = {name: getattr(TLAC, name) for name in names}
    action_text = {
        'fd': t('Move forward', 'Avanzar', '前に進む'),
        'lt': t('Turn left', 'Girar a la izquierda', '左に回る'),
        'rt': t('Turn right', 'Girar a la derecha', '右に回る'),
        'layEgg': t('Place an egg', 'Poner un huevo', '卵を置く'),
        'testIfICanProceed': t('Can the turtle move forward?', '¿Puede avanzar la tortuga?', '亀は前に進める？'),
        'amILayingOnAnEgg': t('Is there an egg under the turtle?', '¿Hay un huevo debajo de la tortuga?', '亀の下に卵がある？'),
        'end': t('End Program', 'Terminar programa', 'プログラム終了'),
    }

    def wrapped(name):
        def perform(*args, **kwargs):
            nonlocal ended
            if name == 'end':
                ended = True
                snapshot(action_text[name])
                raise SystemExit(0)
            result = originals[name](*args, **kwargs)
            namespace['turtledirection'] = TLAC.globals.turtle.direction
            detail = action_text[name].copy()
            if name in ('fd', 'testIfICanProceed'):
                distance = args[1] if len(args) > 1 else kwargs.get('slots', 1)
                detail = {lang: f'{value} ({distance})' for lang, value in detail.items()}
            if isinstance(result, bool):
                answer = t('yes', 'sí', 'はい') if result else t('no', 'no', 'いいえ')
                detail = {lang: f'{value} → {answer[lang]}' for lang, value in detail.items()}
            actor = getattr(TLAC.globals.turtle, 'name', '')
            after = t('After', 'Después', '実行後')
            snapshot({lang: f'{after[lang]}: {actor + ": " if actor else ""}{detail[lang]}' for lang in LANGS})
            return result
        return perform

    def create_turtle(name, x, y):
        turtle = Turtle(name, x, y)
        after = t('Created turtle', 'Tortuga creada', '亀を作成')
        snapshot({lang: f'{after[lang]}: {name} (X={x}, Y={y})' for lang in LANGS})
        return turtle

    namespace['Turtle'] = create_turtle
    for name in names:
        setattr(TLAC, name, wrapped(name))
        def bind(name):
            return lambda *args: getattr(TLAC, name)(TLAC.globals, *args)
        namespace[name] = bind(name)

    def trace(frame, event, arg):
        nonlocal current_line, depth
        if frame.f_code.co_filename != path or ended:
            return trace
        current_line = frame.f_lineno
        parent, depth = frame.f_back, 0
        while parent:
            if parent.f_code.co_filename == path:
                depth += 1
            parent = parent.f_back
        if event == 'line':
            before = t('Before', 'Antes', '実行前')
            label = labels[current_line]
            snapshot({lang: f'{before[lang]}: {label[lang]}' for lang in LANGS})
        elif frame.f_code.co_name != '<module>' and event in ('call', 'return'):
            verb = t('Enter function', 'Entrar en la función', '関数に入る') if event == 'call' else t('Return from function', 'Volver de la función', '関数から戻る')
            snapshot({lang: f'{verb[lang]}: {frame.f_code.co_name}' for lang in LANGS})
        return trace

    previous_trace = sys.gettrace()
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            sys.settrace(trace)
            try:
                exec(compile(Path(path).read_text(encoding='utf-8'), path, 'exec'), namespace)
            except SystemExit as result:
                if result.code not in (None, 0):
                    raise
    finally:
        sys.settrace(previous_trace)
        for name, original in originals.items():
            setattr(TLAC, name, original)
    snapshot(t('Finished: final board', 'Terminado: tablero final', '終了：最後の盤面'), call_depth=0)
    return {'source': source, 'title': title, 'anchor': anchor,
            'width': TLAC.globals.W, 'height': TLAC.globals.H, 'steps': steps}


def build(key):
    data = record(key)
    OUTPUT.mkdir(exist_ok=True)
    (OUTPUT / f'{key}.json').write_text(json.dumps(data, ensure_ascii=False, separators=(',', ':')) + '\n', encoding='utf-8')
    (OUTPUT / f'{key}.html').write_text(render_execution(data), encoding='utf-8')
    log = []
    for i, step in enumerate(data['steps']):
        log.append(f'Step {i+1}: {step["label"]["en"]} (instruction {step["line"]}, depth {step["depth"]})')
        for start in range(0, len(step['cells']), data['width']):
            log.append(''.join(f'[{cell}]' for cell in step['cells'][start:start + data['width']]))
        log.append('')
    (OUTPUT / f'{key}.txt').write_text('\n'.join(log), encoding='utf-8')
    print(f'{key}: {len(data["steps"])} steps; {len(data["steps"][-1]["eggs"])} eggs')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('program', help='e.g. problem4-loop, problem4-recursive, classes-turtle')
    build(parser.parse_args().program)
