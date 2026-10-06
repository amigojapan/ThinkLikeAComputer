#!/usr/bin/env python3
"""Rebuild the lesson: python3 build_TLAC_advanced_concepts.py.

First generate executions with bash TLAC_boardgame/makeBoards.bash --advanced.

Runs the existing htmlifyer.py on all ten original source files, embeds its
numbered/nested HTML blocks, and localizes their text (including converter
fallbacks such as while/return/inline comments). No source programs are edited.
Requires wcwidth, as htmlifyer.py does; otherwise uses the standard library.
"""
from html import escape, unescape
from pathlib import Path
import re
import subprocess
import sys
import json
from TLAC_boardgame.execution_view import board_html, BOARD_CSS, WORDS

ROOT = Path(__file__).resolve().parent
LANGS = ("en", "es", "ja")


def t(en, es, ja):
    return dict(zip(LANGS, (en, es, ja)))


# Keys are normalized text emitted by htmlifyer.py, not source instructions.
# Explicit coverage makes a newly added or changed instruction fail the build
# instead of silently displaying untranslated text in a lesson.
TEXT = {}


def line(source, en, es, ja):
    TEXT[source] = t(en, es, ja)


line('while True then', 'Repeat until an instruction stops this loop', 'Repetir hasta que una instrucción detenga este bucle', '繰り返しを止める命令が実行されるまで繰り返す')
line('while "can Turtle proceed forward?"() then', 'While the turtle can move forward 1 space, repeat', 'Mientras la tortuga pueda avanzar 1 casilla, repetir', '亀が1マス前に進める間、繰り返す')
line('while "can Turtle proceed forward?"( 2) then', 'While the turtle can move forward 2 spaces, repeat', 'Mientras la tortuga pueda avanzar 2 casillas, repetir', '亀が2マス前に進める間、繰り返す')
line('if "can Turtle proceed forward?"() then', 'If the turtle can move forward 1 space, then', 'Si la tortuga puede avanzar 1 casilla, entonces', 'もし亀が1マス前に進めるなら')
line('if "can Turtle proceed forward?"( 2) then', 'If the turtle can move forward 2 spaces, then', 'Si la tortuga puede avanzar 2 casillas, entonces', 'もし亀が2マス前に進めるなら')
line('if not "can Turtle proceed forward?"() then', 'If the turtle cannot move forward 1 space, then', 'Si la tortuga no puede avanzar 1 casilla, entonces', 'もし亀が1マス前に進めないなら')
line('if not "can Turtle proceed forward?"( 2) then', 'If the turtle cannot move forward 2 spaces, then', 'Si la tortuga no puede avanzar 2 casillas, entonces', 'もし亀が2マス前に進めないなら')
TEXT['if not "can Turtle proceed forward?"(2) then'] = TEXT['if not "can Turtle proceed forward?"( 2) then']
line('if "is Turtle laying on an egg?" then', 'If the turtle is standing on an egg, then', 'Si la tortuga está sobre un huevo, entonces', 'もし亀が卵のあるマスにいるなら')
line('if Turtle Direction = Facing Right then', 'If the turtle is facing right, then', 'Si la tortuga mira hacia la derecha, entonces', 'もし亀が右を向いているなら')
line('if Turtle Direction = Facing Up then', 'If the turtle is facing up, then', 'Si la tortuga mira hacia arriba, entonces', 'もし亀が上を向いているなら')
TEXT['if Turtle Direction=Facing Right then'] = TEXT['if Turtle Direction = Facing Right then']
TEXT['if Turtle Direction=Facing Up then'] = TEXT['if Turtle Direction = Facing Up then']
line('else:', 'Otherwise', 'En caso contrario', 'そうでなければ')
line('return', 'Return to the instruction after the call', 'Volver a la instrucción que sigue a la llamada', '呼び出し元の、呼び出した命令の次へ戻る')
for source in ('break # Break out of the loop to end the script',
               'break # Break out of the loop to safely end the script',
               'break # Breaks out of the loop to end the script',
               'break # Breaks out of the loop to safely end the script'):
    line(source, 'Leave the innermost loop', 'Salir del bucle más interno', '一番内側の繰り返しから抜ける')
line('Function call End Program', 'Function call: End Program', 'Llamar a la función: Terminar programa', '関数を呼び出す：プログラム終了')
TEXT["end() # Fixed from ''"] = TEXT['Function call End Program']
line('Function call Turn Turtle Left', 'Function call: Turn Turtle Left', 'Llamar a la función: Girar la tortuga a la izquierda', '関数を呼び出す：亀を左に90度回す')
line('Function call Turn Turtle Right', 'Function call: Turn Turtle Right', 'Llamar a la función: Girar la tortuga a la derecha', '関数を呼び出す：亀を右に90度回す')
line('Function call Turtle Move Forward', 'Function call: Move Turtle Forward 1 space', 'Llamar a la función: Avanzar la tortuga 1 casilla', '関数を呼び出す：亀を1マス前に進める')
line('Function call Turtle Move Forward parameters: 2', 'Function call: Move Turtle Forward — distance: 2', 'Llamar a la función: Avanzar la tortuga — distancia: 2', '関数を呼び出す：亀を前に進める — 距離：2')
line('Function call Turtle Move Forward parameters: H-1', 'Function call: Move Turtle Forward — distance: board height − 1', 'Llamar a la función: Avanzar la tortuga — distancia: altura del tablero − 1', '関数を呼び出す：亀を前に進める — 距離：盤面の縦のマス数 − 1')
TEXT['Function call Turtle Move Forward parameters: H - 1'] = TEXT['Function call Turtle Move Forward parameters: H-1']
line('Function call Turtle lays egg underneath itself', 'Function call: Place an egg under the turtle', 'Llamar a la función: Poner un huevo debajo de la tortuga', '関数を呼び出す：亀のいるマスに卵を置く')
line('layEgg() # Lays the final egg in the column', 'Function call: Place the last egg in this column', 'Llamar a la función: Poner el último huevo de esta columna', '関数を呼び出す：この列の最後の卵を置く')
FUNCTIONS = {
    'P': t('one step of the route', 'un paso del recorrido', '経路を1段階進む'),
    'goToBeginningOfBoard': t('go to the wall ahead', 'ir hasta la pared de enfrente', '前方の壁まで進む'),
    'fillThisRowWithEggs': t('fill this line with eggs', 'llenar esta línea de huevos', 'この1列を卵で埋める'),
    'fillThisColumnWithEggs': t('place eggs every two spaces in this column', 'poner huevos cada dos casillas en esta columna', 'この列で2マスおきに卵を置く'),
    'repeatThisUntilBoardFull': t('repeat the board pattern', 'repetir el patrón del tablero', '盤面の模様を繰り返す'),
}
for name in FUNCTIONS:
    line('Function definition ' + name, 'Function definition: ' + name, 'Definir la función: ' + name, '関数定義：' + name)
    line('Function call ' + name, 'Function call: ' + name, 'Llamar a la función: ' + name, '関数を呼び出す：' + name)
for n in range(4, 8):
    line(f'problem {n}', f'Problem {n}', f'Problema {n}', f'問題{n}')
line('problem 4 non-recursive solution', 'Problem 4 — without recursion', 'Problema 4 — sin recursión', '問題4 — 再帰を使わない解法')
COMMENTS = [
    ('--- Main Execution Sequence ---', 'Main instructions: start here', 'Instrucciones principales: empezar aquí', 'メインの命令：ここから開始'),
    ('Initial action before the loop starts', 'Initial action before the loop', 'Acción inicial antes del bucle', '繰り返しの前の準備'),
    ('Exit condition', 'Check when to stop', 'Comprobar cuándo parar', '止まる条件を確認'),
    ('Exit condition check', 'Check when to stop', 'Comprobar cuándo parar', '止まる条件を確認'),
    ('Turtle actions', 'Turtle actions', 'Acciones de la tortuga', '亀の動作'),
    ('Note the second parameter (2) for checking and moving', 'Use distance 2 for both the check and the movement', 'Usar la distancia 2 tanto al comprobar como al avanzar', '確認するときも進むときも距離は2'),
    ('1 Turn left and go to the beginning of the board', '1. Turn left and go to the wall', '1. Girar a la izquierda e ir hasta la pared', '1. 左に回り、壁まで進む'),
    ('2 Initial row fill (Executes before the repeating main loop)', '2. Fill the first line before the main loop', '2. Llenar la primera línea antes del bucle principal', '2. メインの繰り返しの前に最初の列を埋める'),
    ('3 Main repeating loop for the rest of the board', '3. Main loop for the rest of the board', '3. Bucle principal para el resto del tablero', '3. 盤面の残りを処理するメインの繰り返し'),
    ('Inner loop replacing fillThisRowWithEggs()', 'Inner loop: fill this line with eggs', 'Bucle interior: llenar esta línea de huevos', '内側の繰り返し：この列を卵で埋める'),
    ('Turning and proceeding logic', 'Turn and move to the next line', 'Girar y avanzar a la siguiente línea', '向きを変えて次の列へ進む'),
    ("Check if we've reached the end of the board", 'Check for the edge of the board', 'Comprobar si hemos llegado al borde del tablero', '盤面の端に着いたか確認'),
    ('1 goToBeginningOfBoard', '1. Go to the wall ahead', '1. Ir hasta la pared de enfrente', '1. 前方の壁まで進む'),
    ('2 fillThisRowWithEggs(Initial run)', '2. Fill the first line with eggs', '2. Llenar la primera línea de huevos', '2. 最初の列を卵で埋める'),
    ('3 repeatThisUntilBoardFull', '3. Repeat the board pattern', '3. Repetir el patrón del tablero', '3. 盤面の模様を繰り返す'),
    ('fillThisRowWithEggs inline', 'Fill this line with eggs here', 'Llenar esta línea de huevos aquí', 'ここでこの列を卵で埋める'),
    ('Turn logic for "^" direction', 'Turn after travelling upward', 'Girar después de avanzar hacia arriba', '上向きに進んだ後、向きを変える'),
    ('Move forward by height minus 1', 'Move forward by board height minus 1', 'Avanzar la altura del tablero menos 1', '盤面の縦のマス数から1を引いた距離だけ進む'),
    ('1 Moves turtle to the wall it\'s facing', '1. Move the turtle to the wall ahead', '1. Llevar la tortuga hasta la pared de enfrente', '1. 亀を前方の壁まで進める'),
    ('2 Lays an egg and jumps 2 spaces recursively', '2. Place an egg, move 2 spaces, and call this function again', '2. Poner un huevo, avanzar 2 casillas y volver a llamar a esta función', '2. 卵を置き、2マス進み、この関数をもう一度呼ぶ'),
    ('3 Turns the turtle jumps 2 columns and repeats', '3. Turn, move across 2 columns, and repeat', '3. Girar, avanzar 2 columnas y repetir', '3. 向きを変え、2列分進んで繰り返す'),
    ('If the turtle is at the top of the board facing UP (^)', 'When the turtle reaches the top facing up', 'Cuando la tortuga llega arriba mirando hacia arriba', '亀が上向きで盤面の上端に着いたとき'),
    ('If the turtle is at the bottom of the board facing DOWN', 'When the turtle reaches the bottom facing down', 'Cuando la tortuga llega abajo mirando hacia abajo', '亀が下向きで盤面の下端に着いたとき'),
    ('Check if we have hit the right edge of the board', 'Check whether the right edge is too close for 2 spaces', 'Comprobar si el borde derecho está demasiado cerca para avanzar 2 casillas', '右端まで2マス進めるか確認'),
    ('This neatly tucks the turtle into the final [v] corner position!', 'Adjust the final corner position if one more space is available', 'Ajustar la posición final en la esquina si queda una casilla', 'あと1マス進める場合は、最後の隅の位置へ移動'),
    ('Recursively repeat for the newly positioned column', 'Call this function again for the new column', 'Volver a llamar a esta función para la nueva columna', '新しい列でこの関数をもう一度呼ぶ'),
    ('Step A: Move to the far left wall (Column 0)', 'Step A: Go to the left wall (column 0)', 'Paso A: Ir a la pared izquierda (columna 0)', '手順A：左の壁まで進む（0列目）'),
    ('Step B: Face UP and move to the very top wall (Row 0)', 'Step B: Face up and go to the top wall (row 0)', 'Paso B: Mirar hacia arriba e ir a la pared superior (fila 0)', '手順B：上を向き、上の壁まで進む（0行目）'),
    ('Step C: Turn completely around to face DOWN and step down 1 space to Row 1', 'Step C: Turn around, face down, and move 1 space to row 1', 'Paso C: Dar media vuelta, mirar hacia abajo y avanzar 1 casilla hasta la fila 1', '手順C：反対を向いて下向きになり、1マス進む（1行目）'),
    ('Step D: Begin the iterative snaking loop!', 'Step D: Start the winding route with a loop', 'Paso D: Iniciar el recorrido de ida y vuelta con un bucle', '手順D：繰り返しを使って蛇行する経路を進む'),
    ('Step D: Begin the recursive snaking!', 'Step D: Start the winding route with recursive calls', 'Paso D: Iniciar el recorrido de ida y vuelta con llamadas recursivas', '手順D：再帰呼び出しを使って蛇行する経路を進む'),
    ('1 Inline logic replacing fillThisColumnWithEggs()', '1. Place eggs along this column', '1. Poner huevos a lo largo de esta columna', '1. この列に卵を並べる'),
    ('2 Inline logic replacing repeatThisUntilBoardFull()', '2. Move to the next column or stop', '2. Pasar a la siguiente columna o parar', '2. 次の列へ進むか、終了する'),
]
for values in COMMENTS:
    line(*values)


for name, x in [('aki', 1), ('sol', 4)]:
    display = name.title()
    line(f'Function call {name} = Turtle parameters: "{display}", {x}, 4',
         f'Create turtle {display} at X={x}, Y=4, facing up',
         f'Crear la tortuga {display} en X={x}, Y=4, mirando hacia arriba',
         f'亀{display}をX={x}、Y=4に作る（上向き）')
    line(f'Function call {name}.mark_and_move', f'Ask {display}: mark this square and move forward',
         f'Pedir a {display}: marcar esta casilla y avanzar', f'{display}に頼む：今のマスに卵を置いて前に進む')
    line(f'Function call {name}.right', f'Ask {display}: turn right',
         f'Pedir a {display}: girar a la derecha', f'{display}に頼む：右に回る')


def source_charts(source):
    result = subprocess.run(
        [sys.executable, str(ROOT / 'htmlifyer.py'), 'en', 'HTML', str(ROOT / source)],
        capture_output=True, text=True, encoding='utf-8', check=True,
    ).stdout
    match = re.search(r'<body[^>]*>(.*?)</body>', result, re.S)
    if not match:
        raise ValueError(f'Missing converter output for {source}')
    body, labels, charts = match[1], {}, {}
    number = 0
    for raw in re.findall(r'<p[^>]*>(.*?)</p>', body, re.S):
        key = ' '.join(unescape(raw).split())
        if key.isdigit():
            number = int(key)
        else:
            labels[number] = TEXT[key]
    for lang in LANGS:
        def translate(match):
            attrs, raw = match.groups()
            key = ' '.join(unescape(raw).split())
            text = key if key.isdigit() else escape(TEXT[key][lang])
            return f'<p{attrs}>{text}</p>'
        localized = re.sub(r'<p([^>]*)>(.*?)</p>', translate, body, flags=re.S)
        localized = localized.replace('<img ', '<img alt="" ')
        charts[lang] = f'<!-- htmlifyer.py en HTML {source}; localized labels -->\n' + localized
    return charts, labels


def converted_charts():
    charts = {}
    for n in range(4, 9):
        for kind, suffix in (("loop", "-non-recursive"), ("recursive", "")):
            converted, _ = source_charts(f'problem{n}-program{suffix}-simplified.py')
            for lang in LANGS:
                charts[n, kind, lang] = converted[lang]
    return charts


def execution_preview(key, lang):
    path = ROOT / 'TLAC_boardgame' / 'advanced_executions' / f'{key}.json'
    if not path.exists():
        raise FileNotFoundError('Run bash TLAC_8_basics_of_programming/TLAC_boardgame/makeBoards.bash --advanced first')
    run = json.loads(path.read_text(encoding='utf-8'))
    out = '<div class="board-pair">'
    for label, step in [('initial', run['steps'][0]), ('final', run['steps'][-1])]:
        title = WORDS[lang][label]
        out += '<figure><figcaption>' + title + '</figcaption>'
        out += board_html(step, run['width'], 'TLAC_boardgame/img', title)
        out += '<p>' + WORDS[lang]['eggs'] + ': ' + str(len(step['eggs'])) + '</p></figure>'
    out += '</div>'
    link = t('Open the full execution: every instruction and board →', 'Abrir la ejecución completa: cada instrucción y tablero →', '実行結果を開く：すべての命令と盤面 →')[lang]
    out += f'<p class="execution-link"><a href="TLAC_boardgame/advanced_executions/{key}.html?lang={lang}">{link}</a></p>'
    return out


TITLE = t('Advanced programming concepts in TLAC', 'Conceptos avanzados de programación en TLAC', 'TLACで学ぶプログラミングの発展的な概念')
SUBTITLE = t('Recursion and classes, one small step at a time.', 'Recursión y clases, paso a paso.', '再帰とクラスを、一歩ずつ学ぼう。')
NAV = [
    ('start', t('Before you begin', 'Antes de empezar', 'はじめに')),
    ('loops', t('1. First, without recursion', '1. Primero, sin recursión', '1. まずは再帰を使わずに')),
    ('recursion', t('2. Now, with recursion', '2. Ahora, con recursión', '2. 次は再帰を使って')),
    ('classes', t('3. Classes and objects', '3. Clases y objetos', '3. クラスとオブジェクト')),
    ('practice', t('4. Try it yourself', '4. Practícalo', '4. 練習してみよう')),
]
PROBLEMS = {
    4: {
        'title': t('Follow a route, one space at a time', 'Seguir un recorrido, una casilla a la vez', '1マスずつ経路を進む'),
        'loop': t('Turn left once. Each time around the loop, first look for an egg under the turtle. If there is one, end the program. Otherwise, turn right if the way ahead is blocked, place an egg, and move one space. The next loop checks the new square.', 'Gira a la izquierda una vez. En cada vuelta del bucle, primero comprueba si hay un huevo debajo de la tortuga. Si lo hay, termina el programa. Si no, gira a la derecha si no puedes avanzar, pon un huevo y avanza una casilla. La siguiente vuelta comprueba la nueva casilla.', '最初に一度だけ左に回ります。繰り返すたびに、まず亀の下に卵があるか調べます。あればプログラムを終了します。なければ、前に進めないときは右に回り、卵を置いて1マス進みます。次の繰り返しで、新しいマスを調べます。'),
        'rec': t('P contains one pass through the same actions. Its last instruction calls P again, now with the turtle on a new square. The call inside P is the recursive call. The stopping case is standing on an egg; End Program stops the entire run.', 'P contiene una vuelta de las mismas acciones. Su última instrucción vuelve a llamar a P, ahora con la tortuga en otra casilla. La llamada dentro de P es la llamada recursiva. El caso de parada es estar sobre un huevo; Terminar programa detiene toda la ejecución.', 'Pには、同じ動作の1回分が入っています。最後の命令でPをもう一度呼ぶと、亀はすでに新しいマスにいます。Pの中からPを呼ぶのが再帰呼び出しです。卵の上にいることが停止条件で、「プログラム終了」は実行全体を止めます。'),
        'focus': t('Find the egg check before the next move. Without it, returning to a visited square would not stop the route.', 'Busca la comprobación del huevo antes del siguiente movimiento. Sin ella, volver a una casilla visitada no detendría el recorrido.', '次の移動より前にある、卵の確認を探しましょう。これがないと、一度通ったマスに戻っても止まりません。'),
    },
    5: {
        'title': t('Change the step size to two', 'Cambiar el paso a dos casillas', '歩幅を2マスに変える'),
        'loop': t('This is the same loop pattern as problem 4, but both the movement check and the movement use a distance of 2. Eggs are placed only on the squares where the turtle stands, not on the skipped squares. The stop rule is still finding an egg underneath.', 'Es el mismo patrón de bucle del problema 4, pero tanto la comprobación como el movimiento usan una distancia de 2. Los huevos se ponen solo en las casillas donde está la tortuga, no en las que salta. La regla de parada sigue siendo encontrar un huevo debajo.', '問題4と同じ繰り返しですが、進めるかの確認にも移動にも距離2を使います。卵を置くのは亀が立っているマスだけで、飛び越えたマスには置きません。下に卵があれば止まるという決まりは同じです。'),
        'rec': t('P again calls itself after moving. The repeated action now advances 2 spaces, but the recursive structure has not changed. A distance check of 1 would not establish that a move of 2 stays on the board.', 'P vuelve a llamarse después de avanzar. La acción repetida ahora avanza 2 casillas, pero la estructura recursiva no cambia. Comprobar una distancia de 1 no bastaría para saber si un movimiento de 2 permanece dentro del tablero.', '移動後に、Pが再び自分自身を呼びます。進む距離は2マスになりましたが、再帰の仕組みは変わりません。1マス先だけを調べても、2マス先が盤面の中にあるとは限りません。'),
        'focus': t('Compare the two distance values. They must describe the same intended move.', 'Compara las dos distancias. Deben describir el mismo movimiento previsto.', '2か所の距離を比べましょう。どちらも、これから行う同じ移動を表す必要があります。'),
    },
    6: {
        'title': t('Fill lines, then move to the next line', 'Llenar líneas y pasar a la siguiente', '1列を埋めて、次の列へ進む'),
        'loop': t('There are several jobs: reach a wall, fill one line with eggs, then turn and move to the next line. Small inner loops move along a line; the large outer loop repeats the board pattern. Place one final egg when the end of a line is reached.', 'Hay varias tareas: llegar a una pared, llenar una línea de huevos y luego girar y pasar a la siguiente. Los bucles interiores recorren una línea; el bucle exterior repite el patrón del tablero. Al llegar al final de una línea, se pone un último huevo.', '仕事を分けて考えます。壁まで進み、1列に卵を置き、向きを変えて次の列へ進みます。内側の小さな繰り返しが1列を進み、外側の大きな繰り返しが盤面の模様を作ります。列の端に着いたら、最後の卵を1個置きます。'),
        'rec': t('Three named functions take over those jobs. goToBeginningOfBoard moves and calls itself until it reaches a wall. fillThisRowWithEggs places eggs and calls itself until the line ends, then places the last egg and returns. repeatThisUntilBoardFull calls the filling function, changes lines, and calls itself again until End Program is reached.', 'Tres funciones con nombre se encargan de esas tareas. goToBeginningOfBoard avanza y se llama hasta llegar a una pared. fillThisRowWithEggs pone huevos y se llama hasta el final de la línea; allí pone el último huevo y vuelve. repeatThisUntilBoardFull llama a la función de llenado, cambia de línea y se llama de nuevo hasta llegar a Terminar programa.', '3つの関数に仕事を任せます。goToBeginningOfBoardは壁まで進みながら自分自身を呼びます。fillThisRowWithEggsは列の端まで卵を置きながら自分自身を呼び、端で最後の卵を置いて戻ります。repeatThisUntilBoardFullは列を埋める関数を呼び、次の列へ移動して自分自身を呼びます。「プログラム終了」に達すると終わります。'),
        'focus': t('These supplied examples fill the first line before the main repetition and visit its final square again at the start of that repetition. In TLAC, placing an egg marks a square as occupied; it does not stack another egg there. The function name says “Row”, but the turtle travels vertically here, along a column.', 'Estos ejemplos llenan la primera línea antes de la repetición principal y vuelven a visitar su casilla final al iniciar esa repetición. En TLAC, poner un huevo marca una casilla como ocupada; no apila otro huevo allí. El nombre de la función dice “Row” (fila), pero aquí la tortuga recorre una columna vertical.', 'この例ではメインの繰り返しに入る前に最初の列を埋め、その繰り返しの開始時に端のマスをもう一度処理します。TLACでは卵を置くと、そのマスが「卵あり」になります。同じマスに卵が積み重なるわけではありません。関数名のRowは「行」ですが、ここでは亀が縦方向の列を進みます。'),
    },
    7: {
        'title': t('Fill on the upward pass, travel on the return', 'Llenar al subir y desplazarse al bajar', '上向きでは卵を置き、下向きでは移動する'),
        'loop': t('After the initial line is filled, the outer loop checks the direction. Facing up, it fills a line with eggs. On the downward pass, it moves board height − 1 spaces without placing eggs. It then turns toward the next column. On an empty board, that distance goes from one end of a column to the other.', 'Después de llenar la primera línea, el bucle exterior comprueba la dirección. Al mirar hacia arriba, llena una línea de huevos. Al bajar, avanza la altura del tablero − 1 sin poner huevos. Después gira hacia la siguiente columna. En un tablero vacío, esa distancia recorre una columna de un extremo al otro.', '最初の列を埋めた後、外側の繰り返しで向きを確認します。上向きなら卵を置きながら1列を進みます。下向きなら卵を置かずに「盤面の縦のマス数 − 1」だけ進み、次の列の方へ回ります。障害物のない盤面では、この距離で列の一端から反対の端まで進めます。'),
        'rec': t('The outer function still calls itself, but its direction check chooses which work to do first. The upward branch calls fillThisRowWithEggs; the other branch makes the long move. The filling helper returns at the wall, while the overall pattern ends at the right-edge check.', 'La función exterior sigue llamándose a sí misma, pero la comprobación de dirección decide qué trabajo hacer primero. La rama hacia arriba llama a fillThisRowWithEggs; la otra hace el movimiento largo. La función de llenado vuelve al llegar a la pared, mientras que el patrón completo termina al comprobar el borde derecho.', '外側の関数は引き続き自分自身を呼びますが、その前に向きで仕事を選びます。上向きならfillThisRowWithEggsを呼び、もう一方では長い距離を進みます。列を埋める関数は壁で呼び出し元へ戻り、模様全体の処理は右端の確認で終了します。'),
        'focus': t('Recursion can repeat a decision, not just a single movement. Notice which branch places eggs and which branch only moves.', 'La recursión puede repetir una decisión, además de un movimiento. Observa qué rama pone huevos y cuál solo se desplaza.', '再帰では、単なる移動だけでなく、条件による選択も繰り返せます。卵を置く分岐と、移動だけをする分岐を見分けましょう。'),
    },
    8: {
        'title': t('Leave gaps between eggs and columns', 'Dejar huecos entre huevos y columnas', '卵の間にも列の間にも空きを作る'),
        'loop': t('First go to the top-left corner, face down, and move down one square. The inner loop places eggs every 2 spaces down or up a column. The outer loop moves across 2 columns and repeats. At the right edge, it checks whether one final sideways step is possible, adjusts the position if so, and ends.', 'Primero ve a la esquina superior izquierda, mira hacia abajo y baja una casilla. El bucle interior pone huevos cada 2 casillas al subir o bajar por una columna. El bucle exterior avanza 2 columnas y repite. En el borde derecho, comprueba si cabe un último paso lateral, ajusta la posición si es posible y termina.', 'まず左上の隅へ行き、下を向いて1マス進みます。内側の繰り返しは、列を上または下へ進みながら2マスおきに卵を置きます。外側の繰り返しは横に2列分進んで同じ処理を繰り返します。右端では、最後に横へ1マス進めるか確認し、可能なら位置を調整して終了します。'),
        'rec': t('fillThisColumnWithEggs calls itself after each 2-space move. Its stopping case places the final egg and returns when another 2-space move is impossible. repeatThisUntilBoardFull handles the turns and calls itself for the next column. If moving across 2 columns is impossible, the program ends instead of making another recursive call.', 'fillThisColumnWithEggs se llama después de cada avance de 2 casillas. Su caso de parada pone el último huevo y vuelve cuando ya no se puede avanzar otras 2 casillas. repeatThisUntilBoardFull gestiona los giros y se llama para la siguiente columna. Si no se puede avanzar 2 columnas, el programa termina en lugar de hacer otra llamada recursiva.', 'fillThisColumnWithEggsは2マス進むたびに自分自身を呼びます。もう2マス進めないときは、最後の卵を置いて戻ります。repeatThisUntilBoardFullは向きを変え、次の列を処理するために自分自身を呼びます。横へ2列分進めないときは、再帰呼び出しをせずにプログラムを終了します。'),
        'focus': t('There are two different stopping questions: “Can I continue this column?” and “Can I reach another column?” Each repeated job needs its own answer.', 'Hay dos preguntas de parada distintas: «¿Puedo seguir en esta columna?» y «¿Puedo llegar a otra columna?». Cada tarea repetida necesita su propia respuesta.', '停止条件には「この列をまだ進めるか」と「次の列へ進めるか」の2種類があります。それぞれの繰り返しに、それぞれの停止条件が必要です。'),
    },
}


def paragraph(words, lang, css=''):
    return f'<p class="{css}">{words[lang]}</p>\n'


def numbered_steps(steps, lang):
    return '<ol class="instruction-list">' + ''.join(f'<li>{s[lang]}</li>' for s in steps) + '</ol>'


def section_heading(key, lang):
    label = next(label[lang] for name, label in NAV if name == key)
    return f'<h2 id="{key}-{lang}">{label}</h2>'


def problem(n, kind, lang, charts):
    words = PROBLEMS[n]
    label = t('Problem', 'Problema', '問題')[lang]
    variant = t('Without recursion', 'Sin recursión', '再帰を使わない')[lang] if kind == 'loop' else t('With recursion', 'Con recursión', '再帰を使う')[lang]
    other = 'recursive' if kind == 'loop' else 'loop'
    compare = t('Compare with the recursive version →', 'Comparar con la versión recursiva →', '再帰を使う版と比べる →') if kind == 'loop' else t('← Revisit the loop version', '← Volver a la versión con bucles', '← 繰り返しを使う版に戻る')
    heading = f'{label} {n} · {words["title"][lang]}'
    out = f'<section class="example" id="p{n}-{kind}-{lang}"><h3>{heading}</h3>'
    out += paragraph(words['loop' if kind == 'loop' else 'rec'], lang)
    out += f'<figure><figcaption>{variant} · {label} {n}</figcaption>'
    out += f'<div class="chart" tabindex="0" role="region" aria-label="{escape(variant + ": " + heading)}">{charts[n, kind, lang]}</div></figure>'
    if kind == 'recursive':
        out += paragraph(words['focus'], lang, 'note')
    out += execution_preview(f'problem{n}-{kind}', lang)
    out += f'<p><a href="#p{n}-{other}-{lang}">{compare[lang]}</a></p></section>'
    return out


def introduction(lang):
    out = section_heading('start', lang)
    out += paragraph(t(
        'This lesson continues <a href="TLAC_8_basics_of_programming/8_basics_of_programming_TLAC.html?lang=en">8 Basic Concepts of Programming in TLAC</a>. You only need the ideas of a variable, a condition, a function, and a loop. We will use plain-language instruction cards to learn two new ideas.',
        'Esta lección continúa <a href="TLAC_8_basics_of_programming/8_basics_of_programming_TLAC.html?lang=es">8 conceptos básicos de programación en TLAC</a>. Solo necesitas las ideas de variable, condición, función y bucle. Usaremos tarjetas de instrucciones en lenguaje sencillo para aprender dos ideas nuevas.',
        'この教材は<a href="TLAC_8_basics_of_programming/8_basics_of_programming_TLAC.html?lang=ja">TLACで学ぶプログラミングの8つの基本概念</a>の続きです。変数、条件、関数、繰り返しがわかれば始められます。わかりやすい言葉で書かれた命令カードで、2つの新しい考え方を学びましょう。'), lang)
    out += numbered_steps([
        t('<strong>Recursion:</strong> a function calls itself to continue a job.', '<strong>Recursión:</strong> una función se llama a sí misma para continuar una tarea.', '<strong>再帰：</strong>関数が自分自身を呼び出して仕事を続けます。'),
        t('<strong>Classes:</strong> describe a kind of object, with its own information and actions.', '<strong>Clases:</strong> describen un tipo de objeto, con su propia información y sus acciones.', '<strong>クラス：</strong>情報と動作をまとめて、どのようなオブジェクトを作るかを決めます。'),
    ], lang)
    out += '<aside class="note">' + paragraph(t(
        '<strong>Reading the TLAC cards.</strong> Blue numbers show instruction positions; yellow cards are instructions; green cards are comments for the reader. Enclosing blocks group instructions that belong together. Move a coin along the instructions as you read. A forward move defaults to 1 space; turns are 90°. Placing an egg marks the current square.',
        '<strong>Cómo leer las tarjetas TLAC.</strong> Los números azules indican posiciones; las tarjetas amarillas son instrucciones y las verdes son comentarios para quien lee. Los bloques agrupan instrucciones relacionadas. Mueve una moneda por las instrucciones al leer. Avanzar sin indicar distancia significa 1 casilla; los giros son de 90°. Poner un huevo marca la casilla actual.',
        '<strong>TLACカードの読み方。</strong>青い数字は命令の位置、黄色いカードは命令、緑のカードは読む人のためのコメントです。囲みは、ひとまとまりの命令を表します。コインで現在の命令を指しながら読んでみましょう。距離の指定がなければ1マス進み、回転は90度です。卵を置くと、今いるマスに印がつきます。'), lang) + '</aside>'
    out += paragraph(t(
        'Problems 4–8 below keep the original programs’ order and decisions. They are board-game examples for their intended starting positions and board layouts, not general maze solvers. An egg marks a visited square. A move of 2 uses the destination two spaces ahead; these examples assume clear paths.',
        'Los problemas 4–8 conservan el orden y las decisiones de los programas originales. Son ejemplos para sus posiciones iniciales y tableros previstos, no soluciones para cualquier laberinto. Un huevo marca una casilla visitada. Un movimiento de 2 usa la casilla de destino situada a dos pasos; estos ejemplos suponen caminos despejados.',
        '以下の問題4〜8では、元のプログラムの順番と条件分岐を保っています。それぞれの初期位置と盤面を想定した例であり、どんな迷路でも解けるわけではありません。卵は通ったマスの印です。2マス進む命令は2マス先を移動先とし、これらの例は途中に障害物がないことを想定しています。'), lang)
    out += paragraph(t(
        'After each program, compare its initial and final boards, then open the full execution link. Use Next and Previous to follow every instruction, action, and function return, or expand all steps to see every board together. The numbered instructions match the program cards. The turtle picture hides an egg directly underneath it; the egg count still includes that egg.',
        'Después de cada programa, compara sus tableros inicial y final y abre el enlace a la ejecución completa. Usa Siguiente y Anterior para seguir cada instrucción, acción y retorno de función, o despliega todos los pasos para ver todos los tableros juntos. Los números coinciden con las tarjetas del programa. La imagen de la tortuga oculta el huevo que hay justo debajo; el recuento sí lo incluye.',
        '各プログラムの後に、最初と最後の盤面があります。実行結果へのリンクを開き、「次へ」「前へ」で命令、動作、関数からの戻りを追いましょう。すべてのステップを展開して、盤面をまとめて見ることもできます。命令番号はプログラムのカードと対応しています。亀の真下の卵は絵では隠れますが、卵の数には含まれます。'), lang)
    return out


def recursion_intro(lang):
    out = section_heading('recursion', lang)
    out += paragraph(t(
        'A loop says “do these instructions again.” A recursive function says “do one part, then call this same function for what remains.” Every safe recursive process needs <strong>a stopping case</strong> (often called the base case) and <strong>progress toward that case</strong>. The smaller job might be a shorter distance to a wall or fewer unvisited squares.',
        'Un bucle dice «haz estas instrucciones otra vez». Una función recursiva dice «haz una parte y llama a esta misma función para lo que falta». Todo proceso recursivo que deba terminar necesita <strong>un caso de parada</strong> (o caso base) y <strong>avanzar hacia él</strong>. La tarea restante puede ser una distancia menor hasta una pared o menos casillas sin visitar.',
        '繰り返しは「この命令をもう一度行う」という方法です。再帰関数は「仕事を一部分だけ行い、残りを同じ関数に任せる」という方法です。終了する再帰処理には、<strong>止まる場合（基底ケース）</strong>と、<strong>そこへ近づく変化</strong>が必要です。残りの仕事が小さくなるとは、壁までの距離が短くなったり、まだ通っていないマスが減ったりすることです。'), lang)
    out += paragraph(t(
        '<strong>A definition does not move the turtle.</strong> It gives a group of instructions a name. In these recursive charts, begin with the main instructions after the function definitions. A call enters the named function. A call from inside that same function is recursion. Calling a different helper function is an ordinary function call.',
        '<strong>Una definición no mueve la tortuga.</strong> Da un nombre a un grupo de instrucciones. En estas tarjetas recursivas, empieza por las instrucciones principales que vienen después de las definiciones. Una llamada entra en la función indicada. Si una función se llama a sí misma, hay recursión. Llamar a otra función auxiliar es una llamada normal.',
        '<strong>関数を定義するだけでは、亀は動きません。</strong>命令のまとまりに名前をつけるだけです。この再帰の図では、関数定義の後にあるメインの命令から実行を始めます。呼び出しでその関数の中へ入り、その関数自身を中から呼ぶと再帰になります。別の補助関数を呼ぶだけなら、普通の関数呼び出しです。'), lang)
    out += '<aside class="note">' + paragraph(t(
        '<strong>Three different ways to stop:</strong> “Return” ends only the current function call and resumes after the call that started it. “Leave the innermost loop” exits only that loop. “End Program” stops everything. In the supplied programs, loop-exit or return instructions immediately after End Program are not reached.',
        '<strong>Tres formas distintas de parar:</strong> «Volver» termina solo la llamada actual y continúa después de la llamada que la inició. «Salir del bucle más interno» sale solo de ese bucle. «Terminar programa» lo detiene todo. En los programas proporcionados, las instrucciones de salir del bucle o volver que siguen inmediatamente a Terminar programa no se ejecutan.',
        '<strong>3種類の「終わる」を区別しましょう。</strong>「戻る」は今の関数呼び出しだけを終え、呼び出し元の次の命令から続けます。「一番内側の繰り返しから抜ける」は、その繰り返しだけを終えます。「プログラム終了」は全体を止めます。元のプログラムでは、その直後にある「抜ける」や「戻る」の命令には到達しません。'), lang) + '</aside>'
    out += f'<h3>{t("Follow the calls: two spaces from a wall", "Sigue las llamadas: a dos casillas de una pared", "呼び出しを追う：壁まであと2マス")[lang]}</h3>'
    out += paragraph(t(
        'Imagine goToBeginningOfBoard starting two spaces from the wall. Each call keeps a bookmark saying where to continue when its helper finishes. A new call uses the same instructions, but the turtle’s position has already changed.',
        'Imagina que goToBeginningOfBoard empieza a dos casillas de la pared. Cada llamada guarda un marcador que indica dónde continuar cuando termine la llamada que hace. La nueva llamada usa las mismas instrucciones, pero la posición de la tortuga ya ha cambiado.',
        '壁まであと2マスの位置でgoToBeginningOfBoardを呼んだとします。呼び出すたびに、終わった後に続ける位置をしおりのように覚えておきます。新しい呼び出しも同じ命令を使いますが、亀の位置はすでに変わっています。'), lang)
    out += numbered_steps([
        t('Call A: 2 spaces remain → move 1 space → call B; A waits.', 'Llamada A: faltan 2 casillas → avanzar 1 → llamar a B; A espera.', '呼び出しA：残り2マス → 1マス進む → Bを呼ぶ。Aは待つ。'),
        t('Call B: 1 space remains → move 1 space → call C; B waits.', 'Llamada B: falta 1 casilla → avanzar 1 → llamar a C; B espera.', '呼び出しB：残り1マス → 1マス進む → Cを呼ぶ。Bは待つ。'),
        t('Call C: at the wall → cannot move → return to B. This is the base case.', 'Llamada C: está en la pared → no puede avanzar → volver a B. Este es el caso base.', '呼び出しC：壁に着いた → 進めない → Bへ戻る。これが基底ケース。'),
        t('B has nothing left to do → return to A. A also finishes → return to the main instructions.', 'A B no le queda nada por hacer → vuelve a A. A también termina → vuelve a las instrucciones principales.', 'Bにはもう仕事がない → Aへ戻る。Aも終わる → メインの命令へ戻る。'),
    ], lang)
    out += paragraph(t(
        'These waiting calls form a <strong>call stack</strong>: the last call started is the first to finish. Returning does not undo a move; the turtle stays at the wall. For the board game, put each return bookmark on a small pile of paper slips, and remove the top slip when returning.',
        'Estas llamadas en espera forman una <strong>pila de llamadas</strong>: la última que empieza es la primera que termina. Volver no deshace los movimientos; la tortuga se queda en la pared. Para jugar en papel, apila papelitos con el lugar al que debes volver y retira el de arriba al regresar.',
        '待っている呼び出しは<strong>コールスタック</strong>を作ります。最後に始めた呼び出しから先に終わります。戻っても移動は取り消されず、亀は壁のところにいます。紙で遊ぶなら、戻る位置を書いた紙を積み、戻るときに一番上の紙を取りましょう。'), lang)
    out += '<details><summary>' + t('Function-name guide', 'Guía de nombres de funciones', '関数名の意味')[lang] + '</summary><dl>'
    for name, meaning in FUNCTIONS.items():
        out += f'<dt><strong>{name}</strong></dt><dd>{meaning[lang]}</dd>'
    out += '</dl></details>'
    return out


def classes(lang):
    out = section_heading('classes', lang)
    out += paragraph(t(
        'A <strong>class</strong> describes a kind of thing: the information it keeps and the actions it can perform. Here our class describes a <strong>turtle</strong>. An <strong>object</strong> is one particular turtle made from that description, also called an instance. Aki and Sol can be two objects of the same Turtle class.',
        'Una <strong>clase</strong> describe un tipo de cosa: la información que guarda y las acciones que puede realizar. Aquí la clase describe una <strong>tortuga</strong>. Un <strong>objeto</strong> es una tortuga concreta creada a partir de esa descripción; también se llama instancia. Aki y Sol pueden ser dos objetos de la misma clase Tortuga.',
        '<strong>クラス</strong>は、ある種類のものについて「どんな情報を持つか」「何ができるか」を決める説明書です。ここでは<strong>亀</strong>のクラスを作ります。<strong>オブジェクト</strong>は、この説明書をもとに作る1匹ずつの亀で、インスタンスとも呼びます。AkiとSolは、同じ亀クラスから作った別々のオブジェクトです。'), lang)
    out += '<div class="class-card"><h3>' + t('Class: Turtle', 'Clase: Tortuga', 'クラス：亀')[lang] + '</h3>'
    out += numbered_steps([
        t('<strong>Attributes (stored information):</strong> name, horizontal position X, vertical position Y, and direction.', '<strong>Atributos (información guardada):</strong> nombre, posición horizontal X, posición vertical Y y dirección.', '<strong>属性（保存する情報）：</strong>名前、横の位置X、縦の位置Y、向き。'),
        t('<strong>Constructor (initial setup):</strong> receive a name and starting X and Y; create this turtle there, facing up.', '<strong>Constructor (preparación inicial):</strong> recibir un nombre y las coordenadas X e Y; crear esta tortuga allí, mirando hacia arriba.', '<strong>コンストラクター（最初の準備）：</strong>名前と開始位置X、Yを受け取り、そこに上向きの亀を作る。'),
        t('<strong>Method “Move forward”:</strong> move this turtle one square in its own direction.', '<strong>Método «Avanzar»:</strong> mover esta tortuga una casilla en su propia dirección.', '<strong>メソッド「前に進む」：</strong>この亀を、この亀が向いている方向に1マス進める。'),
        t('<strong>Method “Turn right”:</strong> rotate this turtle 90° clockwise; its position stays the same.', '<strong>Método «Girar a la derecha»:</strong> girar esta tortuga 90° en sentido horario; su posición no cambia.', '<strong>メソッド「右に回る」：</strong>この亀を時計回りに90度回す。位置は変えない。'),
        t('<strong>Method “Place an egg”:</strong> place an egg on this turtle’s current square.', '<strong>Método «Poner un huevo»:</strong> poner un huevo en la casilla actual de esta tortuga.', '<strong>メソッド「卵を置く」：</strong>この亀が今いるマスに卵を置く。'),
        t('<strong>Method “Mark and move”:</strong> ask this turtle to place an egg, then ask it to move forward. One method can use other methods.', '<strong>Método «Marcar y avanzar»:</strong> pedir a esta tortuga que ponga un huevo y luego que avance. Un método puede usar otros métodos.', '<strong>メソッド「卵を置いて進む」：</strong>この亀に卵を置かせてから前に進ませる。メソッドは他のメソッドを使うこともできる。'),
    ], lang) + '</div>'
    out += paragraph(t(
        'An attribute is a named piece of information belonging to an object. A method is a function provided by its class. “This turtle” means the object receiving the request: asking Aki to move changes Aki’s position. The class definition alone does not create a turtle or move it. Creating an object runs its constructor, not all of its methods.',
        'Un atributo es un dato con nombre que pertenece a un objeto. Un método es una función que proporciona su clase. «Esta tortuga» es el objeto que recibe la petición: pedir a Aki que avance cambia la posición de Aki. La definición de la clase por sí sola no crea ni mueve una tortuga. Crear un objeto ejecuta su constructor, no todos sus métodos.',
        '属性はオブジェクトが持つ名前つきの情報です。メソッドはクラスが提供する関数です。「この亀」は動作を頼まれたオブジェクトを指します。Akiに進むよう頼むと、Akiの位置が変わります。クラスを定義するだけでは亀は作られず、動きもしません。オブジェクトを作るとコンストラクターを実行しますが、すべてのメソッドを実行するわけではありません。'), lang)
    out += paragraph(t(
        'These examples use a 6 × 6 TLAC board. X increases to the right; Y increases downward. The top-left square is X=0, Y=0. The paths below stay inside the board. The full executions show every method request and the individual turtle actions it causes.',
        'Estos ejemplos usan un tablero TLAC de 6 × 6. X aumenta hacia la derecha; Y aumenta hacia abajo. La esquina superior izquierda es X=0, Y=0. Los recorridos se mantienen dentro del tablero. Las ejecuciones completas muestran cada petición a un método y las acciones de la tortuga que provoca.',
        'この例では6×6のTLAC盤面を使います。Xは右へ、Yは下へ進むほど大きくなります。左上はX=0、Y=0です。以下の経路は盤面の内側に収まります。実行結果では、メソッドへのお願いと、その中で起きる亀の動作を1つずつ確認できます。'), lang, 'note')
    out += '<section id="classes-turtle-' + lang + '"><h3>' + t('Example 1: one turtle leaves an egg trail', 'Ejemplo 1: una tortuga deja un rastro de huevos', '例1：1匹の亀で卵の道を作る')[lang] + '</h3>'
    out += paragraph(t(
        'Create Aki at X=1, Y=4, facing up. Ask Aki to mark and move twice, turn right, and mark and move once more. The two upward moves change Y from 4 to 2. The final move changes X from 1 to 2. Aki finishes at X=2, Y=2, facing right, with three eggs left behind.',
        'Crea Aki en X=1, Y=4, mirando hacia arriba. Pídele que marque y avance dos veces, gire a la derecha y marque y avance una vez más. Los dos movimientos hacia arriba cambian Y de 4 a 2. El último movimiento cambia X de 1 a 2. Aki termina en X=2, Y=2, mirando a la derecha, con tres huevos detrás.',
        'X=1、Y=4に上向きのAkiを作ります。「卵を置いて進む」を2回頼み、右に回ってから、もう一度「卵を置いて進む」を頼みます。上への2回の移動でYは4から2になり、最後の移動でXは1から2になります。AkiはX=2、Y=2で右を向き、通った場所には3個の卵が残ります。'), lang)
    chart, _ = source_charts('docs_classes_turtle-simplified.py')
    out += '<figure><figcaption>' + t('Program: Aki’s trail', 'Programa: el rastro de Aki', 'プログラム：Akiの卵の道')[lang] + '</figcaption><div class="chart" tabindex="0">' + chart[lang] + '</div></figure>'
    out += execution_preview('classes-turtle', lang) + '</section>'
    out += '<section id="classes-two-turtles-' + lang + '"><h3>' + t('Example 2: two objects, independent positions', 'Ejemplo 2: dos objetos, posiciones independientes', '例2：2つのオブジェクト、それぞれの位置')[lang] + '</h3>'
    out += paragraph(t(
        'Start a fresh board. Create Aki at X=1, Y=4 and Sol at X=4, Y=4. Both face up. Ask Aki to mark and move twice. Sol has not moved! Now ask Sol to turn right and mark and move once. Aki stays at X=1, Y=2, facing up; Sol finishes at X=5, Y=4, facing right.',
        'Empieza con un tablero nuevo. Crea Aki en X=1, Y=4 y Sol en X=4, Y=4. Ambas miran hacia arriba. Pide a Aki que marque y avance dos veces. ¡Sol no se ha movido! Ahora pide a Sol que gire a la derecha, marque y avance una vez. Aki se queda en X=1, Y=2, mirando hacia arriba; Sol termina en X=5, Y=4, mirando a la derecha.',
        '新しい盤面で始めます。X=1、Y=4にAkiを、X=4、Y=4にSolを作ります。両方とも上向きです。Akiに「卵を置いて進む」を2回頼んでも、Solは動きません。次にSolに右へ回ってから「卵を置いて進む」を1回頼みます。AkiはX=1、Y=2で上向きのまま、SolはX=5、Y=4で右向きになります。'), lang)
    chart, _ = source_charts('docs_classes_two_turtles-simplified.py')
    out += '<figure><figcaption>' + t('Program: Aki and Sol', 'Programa: Aki y Sol', 'プログラム：AkiとSol')[lang] + '</figcaption><div class="chart" tabindex="0">' + chart[lang] + '</div></figure>'
    out += execution_preview('classes-two-turtles', lang) + '</section>'
    out += paragraph(t(
        '<strong>Same class, separate state.</strong> Aki and Sol use the same methods, but each stores its own name, X, Y, and direction. They share the board, so both can see eggs placed on it. An egg belongs to a board square, not to the turtle’s personal attributes. The execution page lists both turtles’ states so you can see which one changes.',
        '<strong>Misma clase, estado separado.</strong> Aki y Sol usan los mismos métodos, pero cada una guarda su propio nombre, X, Y y dirección. Comparten el tablero y pueden ver los huevos que hay en él. Un huevo pertenece a una casilla, no a los atributos personales de una tortuga. La página de ejecución muestra los estados de ambas para ver cuál cambia.',
        '<strong>同じクラスでも、状態は別々です。</strong>AkiとSolは同じメソッドを使いますが、名前、X、Y、向きはそれぞれが持っています。盤面は共有するので、置かれた卵は両方の亀から見えます。卵はマスにあるもので、亀自身の属性ではありません。実行結果に両方の亀の状態が表示されるので、どちらが変わったか確認しましょう。'), lang, 'note')
    out += paragraph(t(
        'Calling “Mark and move” uses other methods, but it is not recursion: that method never calls itself. Classes organize information and actions. Recursion is a way for a function to repeat work. A method can be recursive, but it does not have to be.',
        '«Marcar y avanzar» usa otros métodos, pero no es recursión: ese método nunca se llama a sí mismo. Las clases organizan información y acciones. La recursión permite que una función repita trabajo. Un método puede ser recursivo, pero no tiene por qué serlo.',
        '「卵を置いて進む」は他のメソッドを使いますが、自分自身を呼ばないので再帰ではありません。クラスは情報と動作をまとめ、再帰は関数が仕事を繰り返す方法です。メソッドで再帰を使うこともできますが、必ず使う必要はありません。'), lang)
    return out


def practice(lang):
    out = section_heading('practice', lang)
    exercises = [
        (t('1. What if the move toward the wall is removed?', '1. ¿Qué pasa si se quita el movimiento hacia la pared?', '1. 壁へ近づく移動を消すとどうなる？'),
         t('If the turtle starts away from the wall, the next call sees the same position. It keeps calling without reaching the base case. A stopping condition alone is not enough: the repeated action must make progress.', 'Si la tortuga empieza lejos de la pared, la siguiente llamada ve la misma posición. Sigue llamando sin alcanzar el caso base. No basta con una condición de parada: la acción repetida debe avanzar hacia ella.', '壁から離れた位置で始めると、次の呼び出しでも位置は同じです。基底ケースに達せず、呼び出しを続けてしまいます。停止条件があるだけでは足りず、そこへ近づく動作が必要です。')),
        (t('2. Does returning from the column-filling function end the entire program?', '2. ¿Volver desde la función que llena una columna termina todo el programa?', '2. 列を埋める関数から戻ると、プログラム全体が終わる？'),
         t('No. Return resumes the caller. That caller may turn the turtle and start another column. End Program is the instruction that stops everything.', 'No. Volver reanuda la función que hizo la llamada. Esta puede girar la tortuga y empezar otra columna. Terminar programa es la instrucción que lo detiene todo.', 'いいえ。呼び出し元に戻って続けます。呼び出し元は亀の向きを変えて次の列を始めることもあります。全体を止めるのは「プログラム終了」です。')),
        (t('3. Aki and Sol face up. Ask only Sol to turn right. Does Aki turn too?', '3. Aki y Sol miran hacia arriba. Pide solo a Sol que gire a la derecha. ¿Gira también Aki?', '3. AkiもSolも上向きです。Solだけに右へ回るよう頼むと、Akiも回る？'),
         t('No. Sol faces right; Aki still faces up. Each turtle object stores its own direction attribute.', 'No. Sol mira a la derecha; Aki sigue mirando hacia arriba. Cada objeto tortuga guarda su propio atributo de dirección.', 'いいえ。Solは右向きになりますが、Akiは上向きのままです。それぞれの亀オブジェクトが自分の向きを持っているからです。')),
        (t('4. Design a “Turn around” method for the Turtle class.', '4. Diseña un método «Dar media vuelta» para la clase Tortuga.', '4. 亀クラスの「反対を向く」メソッドを考えよう。'),
         t('Ask this turtle to turn right twice. Its direction changes by 180°, while X and Y stay unchanged. Another turtle on the board should keep its own direction.', 'Pide a esta tortuga que gire a la derecha dos veces. Su dirección cambia 180°, mientras X e Y no cambian. Otra tortuga del tablero debe conservar su dirección.', 'この亀に右へ回るよう2回頼みます。向きは180度変わりますが、XとYは変わりません。盤面にいる他の亀の向きも変わりません。')),
    ]
    for question, answer in exercises:
        out += '<h3>' + question[lang] + '</h3><details><summary>' + t('Show an answer', 'Mostrar una respuesta', '答えを見る')[lang] + '</summary>' + paragraph(answer, lang) + '</details>'
    out += paragraph(t(
        '<strong>Remember:</strong> recursion needs a stopping case and progress toward it. A class describes attributes and methods; each object has its own state. You can trace both ideas with paper, coins, and a few instruction cards.',
        '<strong>Recuerda:</strong> la recursión necesita un caso de parada y avanzar hacia él. Una clase describe atributos y métodos; cada objeto tiene su propio estado. Puedes seguir ambas ideas con papel, monedas y unas tarjetas de instrucciones.',
        '<strong>覚えておこう：</strong>再帰には停止条件と、そこへ近づく変化が必要です。クラスは属性とメソッドを決め、各オブジェクトは自分の状態を持ちます。紙とコイン、そして命令カードで、どちらの仕組みもたどることができます。'), lang, 'note')
    return out


CSS = '''
* { box-sizing: border-box; }
:root { color-scheme: light; }
body { margin: 0; background: powderblue; color: #102f40; font: 17px/1.65 Arial, Helvetica, sans-serif; }
.toolbar { background: #e8f7fa; border-bottom: 2px solid #6697a6; padding: 14px max(20px, calc((100% - 1080px)/2)); }
label { font-weight: bold; }
select, button { font: inherit; border: 1px solid #315b6e; border-radius: 5px; padding: 7px 12px; background: #fff; color: #102f40; }
select { margin-left: 12px; max-width: 100%; }
button { cursor: pointer; margin: 3px 0; }
button:hover { background: #e0f0f7; }
:focus-visible { outline: 3px solid #a94700; outline-offset: 4px; }
main { max-width: 1120px; margin: auto; padding: 30px 20px 64px; }
h1 { font-size: clamp(2rem, 5vw, 3.1rem); line-height: 1.18; margin: 12px 0; max-width: 950px; }
h2 { border-bottom: 2px solid #527e8e; padding-bottom: 10px; margin: 54px 0 20px; font-size: 1.8rem; }
h3 { margin: 32px 0 12px; font-size: 1.35rem; }
h4, h5 { font-size: 1.1rem; margin: 0 0 12px; }
p { margin: 12px 0 18px; }
a { color: #064e79; text-underline-offset: 3px; }
a:hover { color: #802f00; }
.subtitle { font-size: 1.25rem; }
.eyebrow { font-weight: bold; letter-spacing: .06em; }
nav { background: #edf8fb; border: 1px solid #739dab; padding: 18px 24px; margin: 24px 0; border-radius: 8px; }
nav ol { margin: 0; padding: 0; list-style: none; }
nav li { margin: 5px 0; }
.note { background: #edf8fb; border-left: 5px solid #376b84; padding: 16px 20px; margin: 22px 0; }
.note p { margin: 0; }
.example { margin: 32px 0 48px; }
figure { margin: 22px 0; border: 1px solid #608896; border-radius: 8px; overflow: hidden; }
figcaption { padding: 10px 16px; background: #244d64; color: white; font-weight: bold; }
.chart { padding: 16px; overflow-x: auto; background: #daedf1; font-size: 15px; line-height: 2.1; }
.chart > div, .chart div { border-radius: 9px; margin: 4px 0; max-width: 100%; }
.chart p { box-decoration-break: clone; -webkit-box-decoration-break: clone; overflow-wrap: anywhere; }
.chart p[style*="background-color: green"] { background: #24633b !important; color: #fff; }
.chart p[style*="background-color: blue"] { background: #173d8c !important; color: #fff7a3 !important; font-variant-numeric: tabular-nums; }
.chart p[style*="background-color: yellow"] { background: #fff19a !important; color: #172c36; }
.chart img { width: 14px; height: 14px; vertical-align: middle; }
.instruction-list { list-style: none; padding: 0; counter-reset: steps; }
.instruction-list li { counter-increment: steps; position: relative; background: #fff3a9; padding: 12px 15px 12px 62px; border: 1px solid #aa933e; margin: 9px 0; border-radius: 5px; }
.instruction-list li::before { content: counter(steps, decimal-leading-zero); position: absolute; left: 14px; top: 12px; background: #173d8c; color: #fff7a3; border-radius: 3px; padding: 1px 7px; }
.class-card, .demo { padding: 22px; border: 1px solid #7296a3; border-radius: 8px; background: #edf8fb; margin: 20px 0; }
.execution-link { font-weight: bold; }
details { background: #eaf5f8; border: 1px solid #7197a5; padding: 12px 18px; border-radius: 6px; margin: 18px 0; }
summary { cursor: pointer; font-weight: bold; }
dd { margin-bottom: 10px; }
footer { border-top: 1px solid #608896; margin-top: 48px; padding-top: 18px; }
[hidden] { display: none !important; }
@media (max-width: 600px) {
  body { font-size: 16px; }
  main { padding: 20px 12px 40px; }
  .toolbar { padding: 12px; }
  select { margin: 8px 0 0; display: block; }
  .objects { grid-template-columns: 1fr; }
  .class-card, .demo { padding: 14px; }
  .chart { padding: 8px; font-size: 14px; }
}
@media print {
  body { background: white; font-size: 11pt; }
  main { max-width: none; padding: 0; }
  .toolbar, .demo { display: none !important; }
  h2, h3, figcaption { break-after: avoid; }
  .chart { overflow: visible; }
  .object-card, .note { break-inside: avoid; }
  * { print-color-adjust: exact; -webkit-print-color-adjust: exact; }
}
'''
CSS += BOARD_CSS

JS = '''
(() => {
  'use strict';
  document.documentElement.classList.add('has-js');
  const selector = document.getElementById('language');
  const languages = ['en', 'es', 'ja'];
  function chooseLanguage(lang, remember = true) {
    if (!languages.includes(lang)) lang = 'en';
    for (const article of document.querySelectorAll('article[data-language]')) {
      article.hidden = article.dataset.language !== lang;
    }
    selector.value = lang;
    document.documentElement.lang = lang;
    document.title = document.querySelector(`article[lang="${lang}"] h1`).textContent;
    document.getElementById('language-label').textContent = {
      en: 'Language / Idioma / 言語', es: 'Idioma / Language / 言語', ja: '言語 / Language / Idioma'
    }[lang];
    // Preserve the current section when switching languages or following a link.
    const oldHash = location.hash;
    const newHash = oldHash.replace(/-(en|es|ja)$/, '-' + lang);
    try {
      const url = new URL(location.href);
      url.searchParams.set('lang', lang);
      url.hash = newHash;
      history.replaceState(null, '', url);
    } catch (_) { /* Some local-file viewers restrict history changes. */ }
    if (remember) {
      try { localStorage.setItem('tlac-advanced-language', lang); } catch (_) { /* Storage is optional. */ }
    }
  }
  let saved;
  try { saved = localStorage.getItem('tlac-advanced-language'); } catch (_) {}
  const query = new URLSearchParams(location.search).get('lang');
  const hashLanguage = location.hash.match(/-(en|es|ja)$/)?.[1];
  chooseLanguage(languages.includes(query) ? query : hashLanguage || saved || 'en', false);
  selector.addEventListener('change', () => chooseLanguage(selector.value));
  window.addEventListener('hashchange', () => {
    const targetLanguage = location.hash.match(/-(en|es|ja)$/)?.[1];
    if (targetLanguage && targetLanguage !== selector.value) chooseLanguage(targetLanguage);
  });
})();
'''


def build():
    charts = converted_charts()
    out = '<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="UTF-8">\n'
    out += '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
    out += '<meta name="description" content="Learn recursion and classes with beginner-friendly TLAC instruction charts in English, Spanish, and Japanese.">\n'
    out += f'<title>{TITLE["en"]}</title>\n<style>{CSS}</style>\n</head>\n<body>\n'
    out += '<!-- Generated by build_TLAC_advanced_concepts.py; edit that file and rebuild. -->\n'
    out += '<div class="toolbar"><label id="language-label" for="language">Language / Idioma / 言語</label>'
    out += '<select id="language"><option value="en" lang="en">English</option><option value="es" lang="es">Español</option><option value="ja" lang="ja">日本語</option></select></div>'
    out += '<noscript><style>article[hidden] { display: block !important; } .toolbar { display: none; }</style><p>JavaScript is off: all three languages appear below. / JavaScript está desactivado: se muestran los tres idiomas. / JavaScriptが無効のため、3言語を順に表示します。</p></noscript>\n<main>'
    for lang in LANGS:
        out += f'<article lang="{lang}" data-language="{lang}"' + (' hidden' if lang != 'en' else '') + '>'
        out += f'<header id="top-{lang}"><p class="eyebrow">TLAC · Think Like A Computer</p><h1>{TITLE[lang]}</h1>'
        out += paragraph(SUBTITLE, lang, 'subtitle') + '</header>'
        out += '<nav aria-label="' + t('Lesson contents', 'Contenido de la lección', '目次')[lang] + '"><ol>'
        for key, label in NAV:
            out += f'<li><a href="#{key}-{lang}">{label[lang]}</a></li>'
        out += '</ol></nav>'
        out += introduction(lang)
        out += section_heading('loops', lang)
        out += paragraph(t(
            'Start with repetition you already know: a loop. Read all five non-recursive examples first. For each, ask: what repeats, what changes, and what makes it stop? Then compare them with the recursive versions in the next section.',
            'Empieza con una repetición que ya conoces: un bucle. Lee primero los cinco ejemplos sin recursión. En cada uno, pregunta: ¿qué se repite, qué cambia y qué lo detiene? Después compáralos con las versiones recursivas de la siguiente sección.',
            'まずは、おなじみの繰り返しから始めましょう。先に再帰を使わない5つの例を読みます。それぞれ「何を繰り返すか」「何が変わるか」「いつ止まるか」を考えてください。その後、次の節の再帰を使う版と比べましょう。'), lang)
        for n in range(4, 9):
            out += problem(n, 'loop', lang, charts)
        out += recursion_intro(lang)
        for n in range(4, 9):
            out += problem(n, 'recursive', lang, charts)
        out += paragraph(t(
            '<strong>Which should you choose?</strong> For a simple repeated movement, a loop is often easier to follow. Recursion is useful when the remaining work naturally resembles the original job. Each unfinished call needs a return bookmark, so very deep recursion can use too much memory. These examples teach the idea; recursion does not automatically make a program faster.',
            '<strong>¿Cuál conviene elegir?</strong> Para un movimiento repetido sencillo, un bucle suele ser más fácil de seguir. La recursión es útil cuando el trabajo restante se parece de forma natural al trabajo original. Cada llamada pendiente necesita recordar dónde volver; una recursión muy profunda puede consumir demasiada memoria. Estos ejemplos enseñan la idea: la recursión no hace automáticamente más rápido un programa.',
            '<strong>どちらを使う？</strong>単純な移動の繰り返しなら、ループの方が追いやすいことが多いです。残りの仕事が元の仕事と同じ形になる場合は、再帰が役立ちます。まだ終わっていない呼び出しには戻る場所を覚えておく必要があるため、再帰が深すぎるとメモリーを使いすぎることがあります。これらは考え方を学ぶ例であり、再帰にすれば自動的に速くなるわけではありません。'), lang, 'note')
        out += classes(lang) + practice(lang)
        out += '<h2>' + t('All program executions', 'Todas las ejecuciones', 'すべてのプログラムの実行結果')[lang] + '</h2><ul>'
        keys = [f'problem{n}-{kind}' for kind in ('loop', 'recursive') for n in range(4, 9)] + ['classes-turtle', 'classes-two-turtles']
        for key in keys:
            data = json.loads((ROOT / 'TLAC_boardgame' / 'advanced_executions' / f'{key}.json').read_text(encoding='utf-8'))
            out += f'<li><a href="TLAC_boardgame/advanced_executions/{key}.html?lang={lang}">{escape(data["title"][lang])}</a></li>'
        out += '</ul>'
        out += '<footer>' + paragraph(t(
            'A companion lesson to TLAC (Think Like A Computer), created by Usmar A. Padow (amigojapan). The recursion charts use the supplied problem 4–8 programs. <a href="https://amigojapan.github.io/">amigojapan’s homepage</a>.',
            'Lección complementaria de TLAC (Think Like A Computer), creado por Usmar A. Padow (amigojapan). Las tarjetas de recursión usan los programas proporcionados de los problemas 4–8. <a href="https://amigojapan.github.io/">Página de amigojapan</a>.',
            'Usmar A. Padow（amigojapan）が制作したTLAC（Think Like A Computer）の追加教材です。再帰の図には、問題4〜8のプログラムを使用しています。<a href="https://amigojapan.github.io/">amigojapanのホームページ</a>。'), lang)
        out += f'<p><a href="#top-{lang}">' + t('Back to top', 'Volver arriba', '先頭に戻る')[lang] + '</a></p></footer></article>\n'
    out += f'</main><script>{JS}</script>\n</body>\n</html>\n'
    target = ROOT / 'TLAC_advanced_concepts.html'
    target.write_text(out, encoding='utf-8')
    print(f'Wrote {target.name}: {len(charts) + 2 * len(LANGS)} localized charts, {len(out):,} characters')


if __name__ == '__main__':
    build()
