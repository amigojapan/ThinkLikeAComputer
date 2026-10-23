#!/usr/bin/env python3
"""Build the maze lesson and offline replay. Run: python3 build_maze.py."""
import ast
import contextlib
from html import escape
import io
from pathlib import Path
import sys

import TLACloopyLib as loops
import TLACsimulator as TLAC
from build_pyramid_sort import LANGS, LESSON_CSS, PyramidCards, instruction_cards as convert_cards
from game_instruction_cards import Cards, words as t
from TLAC_boardgame.execution_view import board_html, render_execution

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / 'mazeTest-simplified.py'
TITLE = t('Explore a maze', 'Explora un laberinto', '迷路を探索しよう')
FUNCTIONS = {
    'notDone': t('Check whether the goal is still ahead', 'Comprobar si falta llegar a la meta', 'まだゴールに着いていないか調べる'),
    'isPathForward': t('Check the path ahead', 'Comprobar el camino al frente', '前の道を調べる'),
    'isPathLeft': t('Check the path on the left', 'Comprobar el camino a la izquierda', '左の道を調べる'),
    'turnLeft': t('Turn left', 'Girar a la izquierda', '左に回る'),
    'turnRight': t('Turn right', 'Girar a la derecha', '右に回る'),
    'moveForward': t('Move forward', 'Avanzar', '前に進む'),
    'loop_body': t('One turn of the maze loop', 'Una vuelta del bucle del laberinto', '迷路の繰り返し1回分'),
    'loop_condition': t('Check whether to stop the loop', 'Comprobar si hay que terminar el bucle', '繰り返しを終えるか調べる'),
}
PRIMITIVES = {
    'lt': FUNCTIONS['turnLeft'],
    'rt': FUNCTIONS['turnRight'],
    'fd': t('Move forward one square', 'Avanzar una casilla', '前に1マス進む'),
    'testIfICanProceed': t('the square ahead is inside the board and has no wall', 'la casilla de enfrente está dentro del tablero y no tiene muro', '前のマスが盤面内にあり、壁がない'),
    'amILayingOnTheGoalFlag': t('the turtle is on the goal flag', 'la tortuga está sobre la bandera de meta', '亀がゴールの旗の上にいる'),
}


class MazeCards(PyramidCards):
    def __init__(self, source, lang):
        Cards.__init__(self, source, 'maze', lang)
        self.source_lines = source.splitlines()
        self.tree.body = [node for node in self.tree.body if not isinstance(node, ast.Import)]
        self.instructions, self.by_source = [], {}

    def name(self, name):
        return FUNCTIONS[name][self.lang] if name in FUNCTIONS else Cards.name(self, name)

    def call(self, node, as_value=True):
        name = ast.unparse(node.func)
        if name in PRIMITIVES:
            return PRIMITIVES[name][self.lang]
        if name in FUNCTIONS:
            return self.say('Call “{name}”', 'Llamar a «{name}»', '「{name}」を呼び出す', name=self.name(name))
        if name == 'l.do_while':
            return self.say('Run one turn, then check whether to stop; repeat until the stop check says yes',
                            'Ejecutar una vuelta y comprobar si hay que parar; repetir hasta que la comprobación diga sí',
                            '1回実行してから終了するか調べる。「はい」になるまで繰り返す')
        return Cards.call(self, node, as_value)

    def statement(self, node):
        if isinstance(node, ast.Assign):
            target = ast.unparse(node.targets[0])
            if target == 'l.globals.loop_body':
                return self.card(self.say('Use “One turn of the maze loop” as the repeated action',
                                          'Usar «Una vuelta del bucle del laberinto» como acción repetida',
                                          '「迷路の繰り返し1回分」を繰り返す動作にする'), node)
            if target == 'l.globals.condition':
                return self.card(self.say('Use “Check whether to stop the loop” as the stop check',
                                          'Usar «Comprobar si hay que terminar el bucle» como comprobación de parada',
                                          '「繰り返しを終えるか調べる」を終了条件にする'), node)
        return Cards.statement(self, node)

    def block(self, label, node, body, *args):
        # Give the converter's explicit "else" line the same number as its
        # localized Otherwise card. An elif already has its own AST source line.
        if node is None:
            if self.source_lines[body[0].lineno - 1].lstrip().startswith('elif '):
                return self.body(body)
            # AST omits the else keyword and comments can precede its first
            # executable statement, so locate the keyword in the source.
            line = body[0].lineno - 1
            while self.source_lines[line - 1].strip() != 'else:':
                line -= 1
                if line < 1:
                    raise ValueError('Missing else line')
            self.by_source[line] = self.number + 1
        return super().block(label, node, body, *args)


def instruction_cards():
    return convert_cards(SOURCE, MazeCards)


def record(instructions=None, source_map=None):
    if instructions is None:
        _, instructions, source_map = instruction_cards()
    old_board, old_loops, old_trace = TLAC.globals, loops.globals, sys.gettrace()
    board = TLAC.initGlobals()
    board.W = board.H = 10
    board.slots, board.turtle, board.ghosts = TLAC.initSlots(board), TLAC.initTurtle(), []
    steps = []
    current_line, current_frame = 0, None

    def snapshot(label, event, frame=None, action=None, result=None):
        if len(steps) >= 10000:
            raise RuntimeError('Maze did not finish within 10,000 recorded steps')
        turtle = board.turtle
        if not (0 <= turtle.X < board.W and 0 <= turtle.Y < board.H):
            raise RuntimeError('Turtle left the board')
        if board.slots[turtle.Y * board.W + turtle.X].wall:
            raise RuntimeError('Turtle entered a wall')
        cells = ['#' if cell.wall else 'G' if cell.goal else ' ' for cell in board.slots]
        cells[turtle.Y * board.W + turtle.X] = turtle.direction
        selected = frame or current_frame
        depth, parent = 0, selected.f_back if selected else None
        while parent:
            if parent.f_code.co_filename == str(SOURCE):
                depth += 1
            parent = parent.f_back
        variables = [{'name': 'at_goal', 'scope': 'global',
                      'value': board.slots[turtle.Y * board.W + turtle.X].goal}]
        if selected and 'result' in selected.f_locals:
            variables.append({'name': 'result', 'scope': 'local', 'value': selected.f_locals['result']})
        steps.append({'label': label, 'event': event, 'action': action, 'result': result,
                      'line': current_line, 'depth': depth, 'cells': ''.join(cells), 'eggs': [],
                      'turtles': [{'name': 'Turtle', 'x': turtle.X, 'y': turtle.Y, 'direction': turtle.direction}],
                      'variables': variables})

    def wrapped(name):
        def perform():
            result = getattr(TLAC, name)(board)
            answer = t('yes', 'sí', 'はい') if result else t('no', 'no', 'いいえ')
            after = t('After', 'Después', '実行後')
            label = {lang: after[lang] + ': ' + PRIMITIVES[name][lang]
                     + (' → ' + answer[lang] if isinstance(result, bool) else '') for lang in LANGS}
            snapshot(label, 'action', frame=sys._getframe(1), action=name, result=result)
            return result
        return perform

    def trace(frame, event, arg):
        nonlocal current_line, current_frame
        if frame.f_code.co_filename != str(SOURCE):
            return None
        if frame.f_lineno not in source_map:
            return trace
        current_line, current_frame = source_map[frame.f_lineno], frame
        if event == 'line':
            before = t('Before', 'Antes', '実行前')
            label = instructions[current_line - 1]['label']
            snapshot({lang: before[lang] + ': ' + label[lang] for lang in LANGS}, 'before', frame)
        elif frame.f_code.co_name != '<module>' and event in ('call', 'return'):
            prefix = t('Enter function', 'Entrar en la función', '関数に入る') if event == 'call' else t('Return from function', 'Volver de la función', '関数から戻る')
            label = FUNCTIONS[frame.f_code.co_name]
            answer = t('yes', 'sí', 'はい') if arg else t('no', 'no', 'いいえ')
            snapshot({lang: prefix[lang] + ': ' + label[lang]
                      + (' → ' + answer[lang] if event == 'return' and isinstance(arg, bool) else '')
                      for lang in LANGS}, event, frame, result=arg)
        return trace

    try:
        TLAC.globals, loops.globals = board, loops.initglobals()
        with contextlib.redirect_stdout(io.StringIO()):
            TLAC.readBoardFromFile(board, ROOT / 'complexMaze2.txt')
            TLAC.teleportTurtleTo(board, 4, 9)
            snapshot(t('Start at E10, facing up. Find the flag at I8.',
                       'Empieza en E10, mirando arriba. Busca la bandera en I8.',
                       'E10で上を向いて開始。I8の旗を目指そう。'), 'start')
            namespace = {'__name__': '__main__', '__file__': str(SOURCE),
                         **{name: wrapped(name) for name in PRIMITIVES}}
            sys.settrace(trace)
            exec(compile(SOURCE.read_text(encoding='utf-8'), str(SOURCE), 'exec'), namespace)
            sys.settrace(old_trace)
        current_frame, current_line = None, 0
        if not board.slots[board.turtle.Y * board.W + board.turtle.X].goal:
            raise RuntimeError('Maze program stopped before reaching the goal')
        snapshot(t('Finished: the turtle reached the flag at I8.',
                   'Final: la tortuga llegó a la bandera en I8.',
                   '終了：亀がI8の旗に到着した。'), 'finish')
    finally:
        sys.settrace(old_trace)
        TLAC.globals, loops.globals = old_board, old_loops
    return {'source': SOURCE.name, 'title': TITLE, 'tutorial': 'maze-tutorial.html', 'anchor': 'cards',
            'width': 10, 'height': 10, 'image_root': 'TLAC_boardgame/img', 'show_eggs': False,
            'instructions': instructions, 'steps': steps,
            'debugger_title': t('Follow the turtle through the maze', 'Sigue a la tortuga por el laberinto', '亀の迷路探索を追ってみよう'),
            'note': t('Before: the highlighted instruction is about to run. After: a move, turn, or check has finished. Checking left temporarily turns the turtle left, checks ahead, then restores its direction. Start, Previous, Next, and Finish let you inspect the full run. The flag is hidden under the turtle at the goal; at_goal becomes true. Coordinates start at (0, 0) in the top-left corner.',
                      'Antes: la instrucción resaltada está a punto de ejecutarse. Después: ha terminado un movimiento, giro o comprobación. Para mirar a la izquierda, la tortuga gira, comprueba el camino y recupera su orientación. Inicio, Anterior, Siguiente y Final permiten recorrer toda la ejecución. En la meta, la tortuga tapa la bandera y at_goal pasa a true. Las coordenadas empiezan en (0, 0) arriba a la izquierda.',
                      '「実行前」は強調された命令をこれから実行し、「実行後」は移動・回転・確認が終わったことを示します。左を調べるときは一度左に回り、前を確認してから元の向きに戻ります。「最初」「前へ」「次へ」「最後」で全過程を確認できます。ゴールでは旗が亀の下に隠れ、at_goalがtrueになります。座標は左上の(0, 0)から始まります。')}


def lesson(charts, data):
    intro = t('Guide the turtle from E10 (X=4, Y=9), facing up, to the goal flag at I8 (X=8, Y=7). Walls block movement; the edge of the board also counts as blocked. This is the complexMaze2 board used by the original maze example.',
              'Guía a la tortuga desde E10 (X=4, Y=9), mirando arriba, hasta la bandera en I8 (X=8, Y=7). Los muros y los bordes del tablero impiden avanzar. Este es el tablero complexMaze2 del ejemplo original.',
              '上を向いたE10（X=4、Y=9）の亀を、I8（X=8、Y=7）のゴールの旗まで導きましょう。壁と盤面の端は通れません。元の迷路の例で使われているcomplexMaze2の盤面です。')
    rules = [
        t('If the path on the left is open, turn left.', 'Si el camino a la izquierda está libre, gira a la izquierda.', '左に道があれば、左に回る。'),
        t('Otherwise, if the path ahead is blocked, turn right.', 'Si no, y el camino al frente está bloqueado, gira a la derecha.', 'そうでなければ、前が通れないときに右に回る。'),
        t('After choosing a direction, move one square only if the path ahead is open.', 'Después de elegir la dirección, avanza una casilla solo si el camino al frente está libre.', '向きを決めたら、前に道がある場合だけ1マス進む。'),
        t('Check for the goal after each turn of the loop. Stop at the flag; otherwise repeat.', 'Comprueba la meta después de cada vuelta del bucle. Detente en la bandera; si no, repite.', '繰り返し1回の最後にゴールを確認する。旗に着いたら終了し、まだなら繰り返す。'),
    ]
    explanation = t('At a dead end, one right turn may still leave a wall ahead. The turtle stays put and tries again on the next loop. This left-hand rule can take detours: it does not search for the shortest route, and it is not guaranteed to solve every possible maze.',
                    'En un callejón sin salida, un giro a la derecha puede dejar otro muro enfrente. La tortuga espera y vuelve a intentarlo en la siguiente vuelta. La regla de la mano izquierda puede dar rodeos: no busca la ruta más corta ni garantiza resolver cualquier laberinto.',
                    '行き止まりでは、右に1回回っても前が壁の場合があります。その場で次の繰り返しに進み、もう一度調べます。この左手法は遠回りすることがあり、最短経路を探す方法ではありません。すべての迷路でゴールに着けるとは限りません。')
    reading = t('Read the numbered cards, then try Next below. Function definitions describe reusable instructions: their bodies run only when called. The loop runs its body before checking its stop condition: no means continue, yes means stop.',
                'Lee las tarjetas numeradas y prueba Siguiente abajo. Las definiciones de funciones describen instrucciones reutilizables: solo se ejecutan al llamarlas. El bucle ejecuta su cuerpo antes de comprobar la condición de parada: no significa continuar y sí significa terminar.',
                '番号付きカードを読み、下の「次へ」を試してください。関数の中の命令は呼び出されたときに実行されます。この繰り返しは動作を実行してから終了条件を調べます。「いいえ」なら続け、「はい」なら終了します。')
    parts = []
    for lang in LANGS:
        initial = t('Starting maze · E10 → I8', 'Laberinto inicial · E10 → I8', '最初の迷路・E10 → I8')[lang]
        final = t('Goal reached · I8', 'Meta alcanzada · I8', 'ゴールに到着・I8')[lang]
        parts.append(f'<section class="lesson" id="cards-{lang}" data-execution-language="{lang}" lang="{lang}"{" hidden" if lang != "en" else ""}>'
                     f'<h2>{t("The maze challenge", "El reto del laberinto", "迷路に挑戦")[lang]}</h2><p>{escape(intro[lang])}</p>'
                     '<div class="board-pair">'
                     f'<figure><figcaption>{initial}</figcaption>{board_html(data["steps"][0], 10, data["image_root"], initial)}</figure>'
                     f'<figure><figcaption>{final}</figcaption>{board_html(data["steps"][-1], 10, data["image_root"], final)}</figure></div>'
                     f'<h3>{t("Follow the left-hand rule", "Sigue la regla de la mano izquierda", "左手法で進む")[lang]}</h3>'
                     '<ol>' + ''.join(f'<li>{escape(rule[lang])}</li>' for rule in rules) + '</ol>'
                     f'<p>{escape(explanation[lang])}</p>'
                     f'<p><a href="#debugger">{t("Try the step-through debugger ↓", "Prueba el depurador paso a paso ↓", "ステップ実行を試す ↓")[lang]}</a></p>'
                     f'<h2>{t("TLAC instruction cards", "Tarjetas de instrucciones TLAC", "TLAC命令カード")[lang]}</h2>'
                     f'<p>{escape(reading[lang])}</p>{charts[lang]}'
                     f'<p><a href="{SOURCE.name}">{t("Simplified Python source", "Código Python simplificado", "簡略版Pythonのソース")[lang]}</a></p></section>')
    return ''.join(parts)


def build():
    charts, instructions, source_map = instruction_cards()
    data = record(instructions, source_map)
    data['program_html'] = charts
    (ROOT / 'maze-execution.html').write_text(render_execution(data), encoding='utf-8')
    combined = dict(data, lesson_html=lesson(charts, data), extra_css=LESSON_CSS,
                    tutorial='TLACPortal.html', anchor='learn')
    (ROOT / 'maze-tutorial.html').write_text(render_execution(combined), encoding='utf-8')
    print(f'Maze: {len(instructions)} cards, {len(data["steps"])} recorded steps; goal reached at I8.')


if __name__ == '__main__':
    build()
