#!/usr/bin/env python3
"""Execute the nine displayed basics examples and build debugger-style replays.

These executable counterparts keep the tutorial's exact instruction numbers.
They repair legacy conversion artifacts (missing receiver arguments and invalid
leading commas) without changing the displayed algorithms. Input uses the two
player responses shown in the lesson; no live user input is needed for a replay.
"""
import contextlib
import copy
import io
import json
from pathlib import Path
import sys

import TLACsimulator as TLAC
from build_TLAC_basics import EXAMPLES, LABELS, LANGS, t
from TLAC_boardgame.execution_view import render_execution

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / 'TLAC_boardgame' / 'basics_executions'

# Blank and comment lines are intentional: numbers match basics_examples.json.
SOURCES = {
    'functions': '''# functions example
# define the reusable action
def Lay_Four_Eggs_In_Square_Pattern():
    layEgg()
    fd()
    layEgg()
    rt()
    fd()
    layEgg()
    rt()
    fd()
    layEgg()
    # turn twice
    # to finish
    # facing up
    rt()
    rt()
turtle.X=0
print("board after changing X")
printBoard()
Lay_Four_Eggs_In_Square_Pattern()
turtle.X=5
print("board after changing X")
printBoard()
Lay_Four_Eggs_In_Square_Pattern()
turtle.X=8
print("board after changing X")
printBoard()
Lay_Four_Eggs_In_Square_Pattern()
''',
    'input': '''# user input example

# initial position
teleportTurtleTo(4,9)
orderUser("top-left")
simulateUserInputTeleportTurtleTo(0,0)
savedX=turtle.X
savedY=turtle.Y
orderUser("bottom-right")
simulateUserInputTeleportTurtleTo(9,9)
teleportTurtleTo(savedX,savedY)
''',
    'for': '''# count from 5 through 9
for i in range(5,10):
    teleportTurtleTo(i,i)

write("counted from 5 to 9")
''',
    'countdown': '''# count down from 3 through 0
for i in range(3,-1,-1):
    fd(i)
''',
    'do-while': '''# do first, then check
n1=1
n2=3
step=1

# run at least once
while True:
    write("value of n1 is " + str(n1))
    # repeated action
    fd(n1)

    # increment the counter
    n1 += step

    # test whether to stop
    # stop when the condition is true
    if n1 > n2:
        break
write("n1 exceeds threshold")
''',
    'nested': '''for i in range(1,4):
    output=""

    # inner loop
    for j in range(1,4):
        # add the multiplication
        output += f"    {i} * {j} = {i * j}"

    # show this row
    print(output)

    # blank lines
    print("\\n")
''',
    'pyramid': '''# build a pyramid
# use several loops

def print_many_christmas(ch,times,triangle_width):
    output=""

    # first inner loop: spaces
    # include the final count
    repeat_end=triangle_width-times
    for _ in range(0,repeat_end+1):
        output += " "

    # second inner loop: characters
    repeat_end2=times*2-2
    for _ in range(0,repeat_end2+1):
        output += ch

    print(output)

# outer loop: five rows
# use rows 1 through 5
for i in range(1,6):
    print_many_christmas('*',i,5)
''',
    'foreach': '''# visit every command
my_commands_list=['fd','fd','rt','fd','fd','lt','fd','fd']

# one command at a time
for command in my_commands_list:
    if command == 'fd':
        fd()
    elif command == 'rt':
        rt()
    elif command == 'lt':
        lt()
''',
    'lists': '''
fruits=["banana","apple","peach","pear"]
write(fruits[3])

write("all fruits")
# visit every fruit
for fruit in fruits:
    write(fruit)

write("fruits in reverse")
# reverse the list
fruits.reverse()
for fruit in fruits:
    write(fruit)

write("fruits alphabetically")
# sort the list
fruits.sort()
for fruit in fruits:
    write(fruit)

fruits.append("appricot")
# insert at index 2
fruits.insert(2,"blueberry")
# remove index 3 (fourth item)
del fruits[3]

write("final fruits")
for fruit in fruits:
    write(fruit)
''',
}
TITLES = {
    'functions': t('Three squares of eggs', 'Tres cuadrados de huevos', '卵の正方形を3つ作る'),
    'input': t('Remember a player’s position', 'Recordar la posición del jugador', 'プレイヤーが置いた位置を覚える'),
    'for': t('Count from 5 through 9', 'Contar del 5 al 9', '5から9まで数える'),
    'countdown': t('Count down from 3 through 0', 'Contar del 3 al 0', '3から0まで逆に数える'),
    'do-while': t('Repeat, then check the limit', 'Repetir y comprobar el límite', '繰り返してから上限を確認する'),
    'nested': t('Nested loops: multiplication table', 'Bucles anidados: tabla de multiplicar', '入れ子の繰り返し：掛け算の表'),
    'pyramid': t('Build a pyramid with loops', 'Construir una pirámide con bucles', '繰り返しでピラミッドを作る'),
    'foreach': t('Follow the list of turtle commands', 'Seguir la lista de órdenes', '亀の命令リストを実行する'),
    'lists': t('Read and change a fruit list', 'Leer y cambiar una lista de frutas', '果物のリストを読み、変更する'),
}
MESSAGES = {
    'board after changing X': t('Board after changing X', 'Tablero después de cambiar X', 'Xを変えた後の盤面'),
    'top-left': t('Player: put the turtle in the top-left corner.', 'Jugador: coloca la tortuga en la esquina superior izquierda.', 'プレイヤーへ：亀を左上の隅に置いてください。'),
    'bottom-right': t('Player: put the turtle in the bottom-right corner.', 'Jugador: coloca la tortuga en la esquina inferior derecha.', 'プレイヤーへ：亀を右下の隅に置いてください。'),
    'counted from 5 to 9': t('Counted from 5 to 9', 'He contado del 5 al 9', '5から9まで数えました'),
    'n1 exceeds threshold': t('n1 has passed the limit', 'n1 ha superado el límite', 'n1が上限を超えました'),
    'all fruits': t('All fruits, in order:', 'Todas las frutas, en orden:', 'すべての果物を順番に：'),
    'fruits in reverse': t('Fruits in reverse order:', 'Frutas en orden inverso:', '果物を逆順に：'),
    'fruits alphabetically': t('Fruits in alphabetical order:', 'Frutas en orden alfabético:', '果物をアルファベット順に：'),
    'final fruits': t('The final fruit list:', 'La lista final de frutas:', '最後の果物リスト：'),
}


def record(key):
    source = SOURCES[key]
    rows = EXAMPLES['charts'][key]
    if len(source.splitlines()) != len(rows):
        raise ValueError(f'{key}: source line numbers do not match the tutorial')
    labels = {row['number']: LABELS[row['text']] for row in rows if row['text']}
    filename = f'<TLAC basics: {key}>'
    board = TLAC.initGlobals()
    board.W = board.H = 10
    board.slots = TLAC.initSlots(board)
    board.turtle = TLAC.initTurtle()
    board.turtle.X, board.turtle.Y = 4, 9
    board.ghosts = []
    TLAC.globals = board
    has_board = key not in ('nested', 'pyramid', 'lists')
    namespace = {'__name__': '__main__', 'turtle': board.turtle}
    output = {lang: '' for lang in LANGS}
    steps = []
    current_frame = None

    def simple(value):
        return (value is None or type(value) in (str, bool, int, float)
                or isinstance(value, (list, tuple)) and all(simple(item) for item in value))

    def snapshot(label, frame=None):
        frame = frame or current_frame
        variables = []
        scopes = [('global', namespace)]
        if frame and frame.f_code.co_name != '<module>':
            scopes.append(('local', frame.f_locals))
        for scope, values in scopes:
            for name, value in values.items():
                if not name.startswith('__') and simple(value):
                    variables.append({'scope': scope, 'name': name, 'value': copy.deepcopy(value)})
        depth, parent = 0, frame.f_back if frame else None
        while parent:
            if parent.f_code.co_filename == filename:
                depth += 1
            parent = parent.f_back
        x, y = board.turtle.X, board.turtle.Y
        if not (0 <= x < board.W and 0 <= y < board.H):
            raise RuntimeError(f'{key}: turtle left the board: {x}, {y}')
        cells = ['o' if cell.containsEgg else ' ' for cell in board.slots]
        cells[y * board.W + x] = board.turtle.direction
        if len(steps) > 10000:
            raise RuntimeError(f'{key}: too many execution steps')
        steps.append({'label': label, 'line': frame.f_lineno if frame else 0,
                      'depth': depth, 'cells': ''.join(cells),
                      'turtles': [{'name': 'Turtle', 'x': x, 'y': y, 'direction': board.turtle.direction}],
                      'eggs': [i for i, cell in enumerate(board.slots) if cell.containsEgg],
                      'variables': variables, 'output': output.copy()})

    def after():
        prefix = t('After', 'Después', '実行後')
        instruction = labels[current_frame.f_lineno]
        snapshot({lang: f'{prefix[lang]}: {instruction[lang]}' for lang in LANGS})

    def movement(name):
        def run(*args):
            getattr(TLAC, name)(board, *args)
            after()
        return run

    def localized(text):
        if text.startswith('value of n1 is '):
            number = text.removeprefix('value of n1 is ')
            return t('The value of n1 is ' + number, 'El valor de n1 es ' + number, 'n1の値は ' + number)
        return MESSAGES.get(text, t(text, text, text))

    def display(*values, sep=' ', end='\n'):
        message = localized(sep.join(str(value) for value in values))
        for lang in LANGS:
            output[lang] += message[lang] + end
        after()

    def display_board():
        # Snapshot from live cells/coordinates, not the simulator's cached text.
        after()

    namespace.update({name: movement(name) for name in ['fd', 'rt', 'lt', 'layEgg', 'teleportTurtleTo', 'simulateUserInputTeleportTurtleTo']})
    namespace.update({'print': display, 'write': display, 'orderUser': display, 'printBoard': display_board})

    def trace(frame, event, arg):
        nonlocal current_frame
        if frame.f_code.co_filename != filename:
            return trace
        current_frame = frame
        if event == 'line':
            prefix = t('Before', 'Antes', '実行前')
            instruction = labels[frame.f_lineno]
            snapshot({lang: f'{prefix[lang]}: {instruction[lang]}' for lang in LANGS}, frame)
        elif frame.f_code.co_name != '<module>' and event in ('call', 'return'):
            prefix = t('Enter', 'Entrar', '呼び出し') if event == 'call' else t('Return', 'Volver', '戻る')
            name = labels[frame.f_code.co_firstlineno]
            snapshot({lang: f'{prefix[lang]}: {name[lang]}' for lang in LANGS}, frame)
        return trace

    snapshot(t('Start: before the first instruction', 'Inicio: antes de la primera instrucción', '開始：最初の命令を実行する前'))
    previous_trace = sys.gettrace()
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            sys.settrace(trace)
            exec(compile(source, filename, 'exec'), namespace)
    finally:
        sys.settrace(previous_trace)
    snapshot(t('Finished: final state and output', 'Terminado: estado y salida finales', '終了：最後の状態と出力'))
    return {
        'source': filename, 'title': TITLES[key], 'anchor': 'program-' + key,
        'tutorial': '../../TLAC_8_basics_of_programming/8_basics_of_programming_TLAC.html',
        'has_board': has_board, 'width': board.W, 'height': board.H, 'steps': steps,
        'instructions': [{**{field: row[field] for field in ('number', 'depth', 'comment')},
                          'label': labels.get(row['number'], t('', '', ''))} for row in rows],
        'note': t('Use Next and Previous to follow the recorded execution. “Before” shows the state just before the highlighted instruction; “After” shows the result of an action or output. Watch variables and output change as you step. Input examples replay the player responses shown in the lesson.',
                  'Usa Siguiente y Anterior para seguir la ejecución grabada. «Antes» muestra el estado justo antes de la instrucción resaltada; «Después» muestra el resultado de una acción o salida. Observa cómo cambian las variables y la salida. Los ejemplos de entrada reproducen las respuestas del jugador de la lección.',
                  '「次へ」「前へ」で記録した実行を追えます。「実行前」は強調した命令の直前、「実行後」は動作や出力の結果です。変数や出力が変わる様子を確認しましょう。入力の例は教材にあるプレイヤーの操作を再現します。'),
        'all_label': t('Show every step, state, and output', 'Mostrar cada paso, estado y salida', 'すべてのステップ、状態、出力を表示'),
    }


def build():
    OUTPUT.mkdir(exist_ok=True)
    for key in SOURCES:
        data = record(key)
        (OUTPUT / f'{key}.json').write_text(json.dumps(data, ensure_ascii=False, separators=(',', ':')) + '\n', encoding='utf-8')
        (OUTPUT / f'{key}.html').write_text(render_execution(data), encoding='utf-8')
        print(f'{key}: {len(data["steps"])} debugger steps')


if __name__ == '__main__':
    build()
