#!/usr/bin/env python3
"""Build the trilingual basics lesson from its original examples and translations.

Run: PYTHONDONTWRITEBYTECODE=1 python3 build_TLAC_basics.py
basics_examples.json preserves the original page's 15 instruction charts (line
numbers, nesting, comments) and six board diagrams. All displayed text is
localized here; legacy example programs and execution outputs stay unchanged.
The layout and language controls are shared with the advanced lesson builder.
"""
from html import escape
import json
from pathlib import Path

from build_TLAC_advanced_concepts import CSS, JS, LANGS, TEXT as ADVANCED_TEXT, t

ROOT = Path(__file__).resolve().parent
FOLDER = ROOT / 'TLAC_8_basics_of_programming'
EXAMPLES = json.loads((FOLDER / 'basics_examples.json').read_text(encoding='utf-8'))
LABELS = dict(ADVANCED_TEXT)


def label(source, en, es, ja):
    LABELS[source] = t(en, es, ja)


label('Function call BrushMyTeeth', 'Function call: Brush my teeth', 'Llamar a la función: Cepillarme los dientes', '関数を呼び出す：歯を磨く')
label('Function call CombMyHair', 'Function call: Comb my hair', 'Llamar a la función: Peinarme', '関数を呼び出す：髪を整える')
label('Function call GoToWork', 'Function call: Go to work', 'Llamar a la función: Ir al trabajo', '関数を呼び出す：仕事に行く')
for variable, values in [('x', [3, 5]), ('X', [2]), ('turtleX', [0, 5, 8])]:
    for value in values:
        name = 'X' if variable == 'turtleX' else variable
        label(f'{variable}={value}', f'Set {name} to {value}', f'Asignar {value} a {name}', f'{name}を{value}にする')
label('x=x+1', 'Set x to its current value + 1', 'Asignar a x su valor actual + 1', '今のxの値に1を足して、xに入れる')
label('if X>3 then', 'If X is greater than 3, then', 'Si X es mayor que 3, entonces', 'もしXが3より大きいなら')
label('if X<3 then', 'If X is less than 3, then', 'Si X es menor que 3, entonces', 'もしXが3より小さいなら')
label("green lines like these are called 'comments'", 'Green cards like these are comments', 'Las tarjetas verdes como estas son comentarios', 'このような緑のカードはコメントです')
label('and do not affect the execution of the program', 'Comments do not change what the program does', 'Los comentarios no cambian lo que hace el programa', 'コメントはプログラムの動作を変えません')
label('but I want you to read them for now', 'Read them to understand the instructions', 'Léelos para entender las instrucciones', '命令を理解するために読んでみましょう')
label('since X is more than 3,', 'X is greater than 3, so', 'X es mayor que 3, por lo que', 'Xは3より大きいので、')
label('this block(the block surrounded by the', 'this group of instructions, inside the', 'este grupo de instrucciones, dentro del', '囲みの中の、この命令のまとまりは')
label('pink rectangle) of code will be executed', 'colored block, will run', 'bloque de color, se ejecutará', '実行されます')
label('since X is not less than,', 'X is not less than 3 here, so', 'Aquí X no es menor que 3, así que', 'ここではXは3より小さくないので、')
label("this block of code won't be executed", 'this block will be skipped', 'se saltará este bloque', 'このまとまりは実行しません')
label('this assignment statement teleports', 'This assignment moves', 'Esta asignación mueve', 'この代入で移動するのは、')
label('the turtle to X slot 2(two slots', 'the turtle to X=2, two squares', 'la tortuga a X=2, dos casillas', '亀の横の位置Xです。左端から2マス進んだ')
label('from the left of the board)', 'from the left edge (the third column)', 'desde el borde izquierdo (la tercera columna)', 'X=2（左から3列目）になります')
label('now after the last assignment statement', 'After changing X,', 'Después de cambiar X,', 'Xを変えたので、')
label('X is less than 3, so the following block', 'X is less than 3, so this block', 'X es menor que 3, así que este bloque', 'Xは3より小さくなり、このまとまりは')
label('of code gets executed.', 'will run', 'se ejecutará', '実行されます')
label('functions example', 'Functions example', 'Ejemplo de funciones', '関数の例')
label('the following is a function definition:', 'Define a reusable group of instructions:', 'Definir un grupo de instrucciones reutilizable:', '何度も使える命令のまとまりを定義します：')
label('Function definition Lay_Four_Eggs_In_Square_Pattern', 'Function definition: Lay four eggs in a square', 'Definir la función: Poner cuatro huevos en un cuadrado', '関数定義：4個の卵を正方形に並べる')
label('Function call Lay_Four_Eggs_In_Square_Pattern', 'Function call: Lay four eggs in a square', 'Llamar a la función: Poner cuatro huevos en un cuadrado', '関数を呼び出す：4個の卵を正方形に並べる')
label('the following two turns are', 'The next two turns', 'Los dos giros siguientes', '次の2回の回転で、')
label('to assure the turtle ends up in', 'make the turtle finish', 'hacen que la tortuga termine', '亀は最後に')
label('the up pusition', 'facing up', 'mirando hacia arriba', '上向きになります')
label('Function call print parameters: initializing board after teleport X"', 'Display: board after changing X', 'Mostrar: tablero después de cambiar X', '表示する：Xを変えた後の盤面')
label('Function call printBoard', 'Display the board', 'Mostrar el tablero', '盤面を表示する')
label('very basic program example', 'A very small program', 'Un programa muy pequeño', 'とても短いプログラム')
label('Function call Turtle Move Forward parameters: 5', 'Function call: Move forward 5 squares', 'Llamar a la función: Avanzar 5 casillas', '関数を呼び出す：5マス前に進む')
label('user input example', 'User input example', 'Ejemplo de entrada del usuario', 'ユーザーからの入力の例')
label('initialize turtle position', 'Set the starting position', 'Establecer la posición inicial', '開始位置を決める')
label('Function call teleportTurtleTo parameters: ,4,9', 'Move the turtle directly to X=4, Y=9', 'Mover la tortuga directamente a X=4, Y=9', '亀をX=4、Y=9へ直接移動する')
label('Function call orderUser parameters: ,"put turtle at top left of the board"', 'Ask the player: put the turtle in the top-left corner', 'Pedir al jugador: coloca la tortuga en la esquina superior izquierda', 'プレイヤーに頼む：亀を左上の隅に置いてください')
label('Function call simulateUserInputTeleportTurtleTo parameters: ,0,0', 'Example player response: move to X=0, Y=0', 'Respuesta de ejemplo del jugador: mover a X=0, Y=0', 'プレイヤーの操作の例：X=0、Y=0に移動する')
label('savedX=turtleX', 'Save the turtle’s X in savedX', 'Guardar la X de la tortuga en savedX', '亀のXをsavedXに保存する')
label('savedY=turtleY', 'Save the turtle’s Y in savedY', 'Guardar la Y de la tortuga en savedY', '亀のYをsavedYに保存する')
label('Function call orderUser parameters: ,"put turtle at top bottom right of the board"', 'Ask the player: put the turtle in the bottom-right corner', 'Pedir al jugador: coloca la tortuga en la esquina inferior derecha', 'プレイヤーに頼む：亀を右下の隅に置いてください')
label('Function call simulateUserInputTeleportTurtleTo parameters: ,9,9', 'Example player response: move to X=9, Y=9', 'Respuesta de ejemplo del jugador: mover a X=9, Y=9', 'プレイヤーの操作の例：X=9、Y=9に移動する')
label('Function call teleportTurtleTo parameters: , savedX, savedY', 'Move the turtle directly to savedX, savedY', 'Mover la tortuga directamente a savedX, savedY', '亀をsavedX、savedYへ直接移動する')
label('For loop counting from 5 to 9 (inclusive)', 'Count from 5 through 9, including both ends', 'Contar del 5 al 9, ambos incluidos', '5から9まで数える（5と9も含む）')
label('for i in range(5, 10) then', 'For each i in 5, 6, 7, 8, 9, repeat', 'Para cada i en 5, 6, 7, 8, 9, repetir', 'iを5、6、7、8、9にして繰り返す')
label('Function call teleportTurtleTo parameters: i, i', 'Move the turtle directly to X=i, Y=i', 'Mover la tortuga directamente a X=i, Y=i', '亀をX=i、Y=iへ直接移動する')
label('Function call promptUserToWriteDownOnPaper parameters: "counted form 5 to 9"', 'Write: “Counted from 5 to 9”', 'Escribir: «He contado del 5 al 9»', '紙に書く：「5から9まで数えました」')
label('Counting down loop from 3 to 0', 'Count down from 3 through 0', 'Cuenta atrás del 3 al 0', '3から0まで逆に数える')
label('for i in range(3, -1, -1) then', 'For each i in 3, 2, 1, 0, repeat', 'Para cada i en 3, 2, 1, 0, repetir', 'iを3、2、1、0にして繰り返す')
label('Function call Turtle Move Forward parameters: i', 'Function call: Move forward i squares', 'Llamar a la función: Avanzar i casillas', '関数を呼び出す：iマス前に進む')
label('do_while example using standard Python', 'Repeat first, then check whether to stop', 'Repetir primero y comprobar después si hay que parar', 'まず実行し、その後で止まるか調べる')
for name, value in [('n1', 1), ('n2', 3), ('step', 1)]:
    label(f'{name} = {value}', f'Set {name} to {value}', f'Asignar {value} a {name}', f'{name}を{value}にする')
label("Python's equivalent of a do...while loop", 'The body will run at least once', 'El cuerpo se ejecutará al menos una vez', '中の命令は少なくとも1回実行する')
label('Function call promptUserToWriteDownOnPaper parameters: "value of n1 is "+str(n1)', 'Write: “The value of n1 is” followed by n1', 'Escribir: «El valor de n1 es» seguido de n1', '紙に書く：「n1の値は」に続けてn1の値を書く')
label('1. Execute the loop body', '1. Run the repeated action', '1. Ejecutar la acción repetida', '1. 繰り返す動作を実行する')
label('Function call Turtle Move Forward parameters: n1', 'Function call: Move forward n1 squares', 'Llamar a la función: Avanzar n1 casillas', '関数を呼び出す：n1マス前に進む')
label('2. Apply the step decrement', '2. Increase the counter by step', '2. Aumentar el contador en step', '2. 数える値をstepだけ増やす')
label('n1 += step', 'Add step to n1 and save the result in n1', 'Sumar step a n1 y guardar el resultado en n1', 'n1にstepを足して、n1に保存する')
label('3. Check the condition (Continue WHILE n1 > n2)', '3. Check whether n1 has passed n2', '3. Comprobar si n1 ha superado n2', '3. n1がn2を超えたか調べる')
label('If the condition is False, break out of the loop', 'If n1 is greater than n2, leave the loop', 'Si n1 es mayor que n2, salir del bucle', 'n1がn2より大きければ、繰り返しから抜ける')
label('if (n1 > n2) then', 'If n1 is greater than n2, then', 'Si n1 es mayor que n2, entonces', 'もしn1がn2より大きいなら')
label('break', 'Leave the innermost loop', 'Salir del bucle más interno', '一番内側の繰り返しから抜ける')
label('Function call promptUserToWriteDownOnPaper parameters: "n1 exceeds threshold"', 'Write: “n1 has passed the limit”', 'Escribir: «n1 ha superado el límite»', '紙に書く：「n1が上限を超えました」')
label('for i in range(1, 4) then', 'For each i in 1, 2, 3, repeat', 'Para cada i en 1, 2, 3, repetir', 'iを1、2、3にして繰り返す')
label('output = ""', 'Start with empty output text', 'Empezar con un texto de salida vacío', '出力用の文字列outputを空にする')
label('Inner loop controls the second number (1 through 3)', 'The inner loop changes the second number', 'El bucle interior cambia el segundo número', '内側の繰り返しで2つ目の数を変える')
label('for j in range(1, 4) then', 'For each j in 1, 2, 3, repeat', 'Para cada j en 1, 2, 3, repetir', 'jを1、2、3にして繰り返す')
label('Append each equation to the row with spacing', 'Add each multiplication to the output row', 'Añadir cada multiplicación a la fila de salida', '掛け算の式を出力の行に追加する')
label('output += f" {i} * {j} = {i * j}"', 'Add “i × j = their product” to output, with spaces', 'Añadir «i × j = su producto» a output, con espacios', '「i × j = 計算結果」を空白とともにoutputに追加する')
label('Print the completed row', 'Display the completed row', 'Mostrar la fila completa', 'できあがった行を表示する')
label('Function call print parameters: output', 'Display the text in output', 'Mostrar el texto de output', 'outputの文字列を表示する')
label('Print a couple of blank lines to match your requested formatting', 'Separate the rows with blank lines', 'Separar las filas con líneas en blanco', '行の間に空行を入れる')
label('Function call print parameters: "\\n"', 'Display blank lines', 'Mostrar líneas en blanco', '空行を表示する')
label('The following makes a pyramid, it is an example of how to use', 'Build a pyramid of characters using', 'Construir una pirámide de caracteres usando', '文字のピラミッドを作ります。')
label('several for loops (outer and inner) in the same program.', 'an outer loop and two inner loops', 'un bucle exterior y dos bucles interiores', '外側に1つ、内側に2つの繰り返しを使います')
label('Function definition print_many_christmas parameters: ch, times, triangle_width', 'Function definition: Make one pyramid row — inputs: ch, times, triangle_width', 'Definir la función: Hacer una fila de la pirámide — entradas: ch, times, triangle_width', '関数定義：ピラミッドの1行を作る — 引数：ch、times、triangle_width')
label('1. First inner loop: Add the spaces', '1. First inner loop: add spaces', '1. Primer bucle interior: añadir espacios', '1. 最初の内側の繰り返し：空白を追加')
label('add +1 to the range stop condition', 'Include the final count in this repetition', 'Incluir el último valor en esta repetición', '最後の数も含めて繰り返す')
label('repeat_end = triangle_width - times', 'Set repeat_end to triangle_width − times', 'Asignar triangle_width − times a repeat_end', 'repeat_endをtriangle_width − timesにする')
label('for _ in range(0, repeat_end + 1) then', 'Repeat for counts 0 through repeat_end', 'Repetir contando de 0 a repeat_end, ambos incluidos', '0からrepeat_endまで数えて繰り返す')
label('output += " "', 'Add one space to output', 'Añadir un espacio a output', 'outputに空白を1個追加する')
label('2. Second inner loop: Add the characters (stars)', '2. Second inner loop: add stars', '2. Segundo bucle interior: añadir estrellas', '2. 次の内側の繰り返し：星を追加')
label('repeat_end2 = times * 2 - 2', 'Set repeat_end2 to times × 2 − 2', 'Asignar times × 2 − 2 a repeat_end2', 'repeat_end2をtimes × 2 − 2にする')
label('for _ in range(0, repeat_end2 + 1) then', 'Repeat for counts 0 through repeat_end2', 'Repetir contando de 0 a repeat_end2, ambos incluidos', '0からrepeat_end2まで数えて繰り返す')
label('output += ch', 'Add character ch to output', 'Añadir el carácter ch a output', 'outputに文字chを追加する')
label('3. Outer loop: Run the pyramid builder for rows 1 through 5', '3. Outer loop: make rows 1 through 5', '3. Bucle exterior: crear las filas 1 a 5', '3. 外側の繰り返し：1〜5行目を作る')
label('range(1, 6) counts exactly 1, 2, 3, 4, 5', 'Use the row numbers 1, 2, 3, 4, 5', 'Usar los números de fila 1, 2, 3, 4, 5', '行の番号は1、2、3、4、5を使う')
label('for i in range(1, 6) then', 'For each i in 1, 2, 3, 4, 5, repeat', 'Para cada i en 1, 2, 3, 4, 5, repetir', 'iを1、2、3、4、5にして繰り返す')
label("Function call print_many_christmas parameters: '*', i, 5", 'Make one pyramid row — ch: *, times: i, triangle_width: 5', 'Hacer una fila de la pirámide — ch: *, times: i, triangle_width: 5', 'ピラミッドの1行を作る — ch：*、times：i、triangle_width：5')
label('Standard Python iteration (foreach)', 'Visit every item in a list', 'Recorrer todos los elementos de una lista', 'リストの要素を1つずつ取り出す')
label("my_commands_list = ['fd', 'fd', 'rt', 'fd', 'fd', 'lt', 'fd', 'fd']", 'commands: forward, forward, right, forward, forward, left, forward, forward', 'órdenes: avanzar, avanzar, derecha, avanzar, avanzar, izquierda, avanzar, avanzar', '命令リスト：前、前、右、前、前、左、前、前')
label('Loop directly through each command in the list', 'Take each command in order', 'Tomar cada orden en su orden original', '命令を順番に1つずつ取り出す')
label('for command in my_commands_list then', 'For each command in the commands list, repeat', 'Para cada orden de la lista, repetir', '命令リストの各命令について繰り返す')
label('if command = "fd" then', 'If the command is forward, then', 'Si la orden es avanzar, entonces', 'もし命令が「前」なら')
label('elif command == "rt":', 'Otherwise, if the command is right, then', 'Si no, si la orden es derecha, entonces', 'そうでなく、命令が「右」なら')
label('elif command == "lt":', 'Otherwise, if the command is left, then', 'Si no, si la orden es izquierda, entonces', 'そうでなく、命令が「左」なら')
for name in ['Turtle Move Forward', 'Turn Turtle Right', 'Turn Turtle Left']:
    LABELS['Function call ' + name + ' parameters: globals'] = LABELS['Function call ' + name]
label('fruits=["banana","apple","peach","pear"]', 'fruits: “banana”, “apple”, “peach”, “pear”', 'fruits: «banana», «apple», «peach», «pear»', 'fruits：「banana」、「apple」、「peach」、「pear」')
label('Function call promptUserToWriteDownOnPaper parameters: fruits[3]', 'Write the item at index 3 in fruits', 'Escribir el elemento de fruits en el índice 3', 'fruitsの添字3の要素を紙に書く')
label('Function call promptUserToWriteDownOnPaper parameters: "now re-writing all fruits:"', 'Write: “All fruits, in order:”', 'Escribir: «Todas las frutas, en orden:»', '紙に書く：「すべての果物を順番に：」')
label('Standard Python loop', 'Repeat for every fruit', 'Repetir para cada fruta', '果物を1つずつ取り出して繰り返す')
label('for fruit in fruits then', 'For each fruit in fruits, repeat', 'Para cada fruta de fruits, repetir', 'fruitsの各果物について繰り返す')
label('Function call promptUserToWriteDownOnPaper parameters: fruit', 'Write this fruit’s name', 'Escribir el nombre de esta fruta', 'この果物の名前を紙に書く')
label('Function call promptUserToWriteDownOnPaper parameters: "now re-writing all fruits in reverse:"', 'Write: “Fruits in reverse order:”', 'Escribir: «Frutas en orden inverso:»', '紙に書く：「果物を逆順に：」')
label('reverses the list', 'Reverse the order of the list', 'Invertir el orden de la lista', 'リストの順番を逆にする')
LABELS['Function call fruits.reverse'] = LABELS['reverses the list']
label('Function call promptUserToWriteDownOnPaper parameters: "now writing fruits in alphabetical order:"', 'Write: “Fruits in alphabetical order:”', 'Escribir: «Frutas en orden alfabético:»', '紙に書く：「果物をアルファベット順に：」')
label('sorts the list in alphabetical order', 'Sort the English fruit names alphabetically', 'Ordenar alfabéticamente los nombres ingleses de las frutas', '英語の果物名をアルファベット順に並べる')
LABELS['Function call fruits.sort'] = LABELS['sorts the list in alphabetical order']
label('Function call fruits.append parameters: "appricot"', 'Add “appricot” to the end of fruits', 'Añadir «appricot» al final de fruits', 'fruitsの末尾に「appricot」を追加する')
label("Inserts 'blueberry' at index 2", 'Insert “blueberry” at index 2', 'Insertar «blueberry» en el índice 2', '添字2の位置に「blueberry」を入れる')
LABELS['Function call fruits.insert parameters: 2, "blueberry"'] = LABELS["Inserts 'blueberry' at index 2"]
label('deletes the third item of the list', 'Remove the item at index 3 (the fourth item)', 'Eliminar el elemento del índice 3 (el cuarto)', '添字3の要素（4番目の要素）を取り除く')
LABELS['del fruits[3]'] = LABELS['deletes the third item of the list']
label('Function call promptUserToWriteDownOnPaper parameters: "now writing fruits in final order:"', 'Write: “The final fruit list:”', 'Escribir: «La lista final de frutas:»', '紙に書く：「最後の果物リスト：」')

TITLE = t('8 basic concepts of programming in TLAC', '8 conceptos básicos de programación en TLAC', 'TLACで学ぶプログラミングの8つの基本概念')
TOPICS = [
    t('Following instructions in order', 'Seguir instrucciones en orden', '命令を順番に実行する'),
    t('Variables', 'Variables', '変数'),
    t('Statements and assignment', 'Instrucciones y asignación', '文と代入'),
    t('Conditions and blocks', 'Condiciones y bloques', '条件分岐とブロック'),
    t('Procedures and functions', 'Procedimientos y funciones', '手続きと関数'),
    t('Input and output', 'Entrada y salida', '入力と出力'),
    t('Loops', 'Bucles', '繰り返し'),
    t('Arrays and lists', 'Arreglos y listas', '配列とリスト'),
]


def p(words, lang, css=''):
    return f'<p class="{css}">{words[lang]}</p>\n'


def heading(n, lang):
    legacy = f'<span id="{n}"></span>' if lang == 'en' else ''
    return legacy + f'<h2 id="concept-{n}-{lang}">{n}. {TOPICS[n][lang]}</h2>\n'


def h3(words, lang):
    return '<h3>' + words[lang] + '</h3>'


def chart(name, title, lang):
    out = f'<figure id="program-{name}-{lang}"><figcaption>' + title[lang] + '</figcaption><div class="chart" tabindex="0" role="region" aria-label="' + escape(title[lang]) + '">'
    depth = 0
    colors = ['#DDA0DD', '#808080', '#B0C4DE']
    for row in EXAMPLES['charts'][name]:
        # Empty numbered lines belong to the current block in the original.
        target = row['depth'] if row['text'] else depth
        while depth > target:
            out += '</div>'
            depth -= 1
        while depth < target:
            out += '<div class="instruction-block" style="background-color: ' + colors[depth % len(colors)] + '">'
            depth += 1
        out += '<div class="instruction-row"><p style="color:yellow;background-color: blue; display: inline; border: 2px solid black; padding: 2px;">' + f'{row["number"]:04d}' + '</p>'
        if row['text']:
            color = 'green' if row['comment'] else 'yellow'
            text = LABELS[row['text']][lang]
            out += f'<p style="background-color: {color}; display: inline; border: 2px solid black; padding: 2px;">{escape(text)}</p>'
        out += '</div>'
    out += '</div>' * depth
    return out + '</div></figure>\n'


def board(index, title, lang):
    cells = EXAMPLES['boards'][index]
    images = ''.join(f'<img src="../TLAC_boardgame/img/{filename}" alt="">' for filename in cells)
    return '<figure class="board-example"><figcaption>' + title[lang] + '</figcaption><div class="board" role="img" aria-label="' + escape(title[lang]) + '" style="--columns:10">' + images + '</div></figure>'


def execution(key, lang):
    path = f'../TLAC_boardgame/basics_executions/{key}.html'
    resolved = (FOLDER / path).resolve()
    if not resolved.is_file():
        raise FileNotFoundError(path)
    return '<p class="execution-link"><a href="' + path + '?lang=' + lang + '">' + t('Open the execution and its output →', 'Abrir la ejecución y su resultado →', '実行の様子と結果を開く →')[lang] + '</a></p>'


def steps(items, lang):
    return '<ol class="instruction-list">' + ''.join('<li>' + item[lang] + '</li>' for item in items) + '</ol>'


def sequence(lang):
    out = heading(0, lang)
    out += p(t(
        'A program is a set of instructions. The computer follows them in a specified order, usually from top to bottom unless a condition, loop, or function changes the flow. The order matters: the computer does not rearrange your instructions to match what you meant.',
        'Un programa es un conjunto de instrucciones. La computadora las sigue en un orden determinado, normalmente de arriba abajo, salvo que una condición, un bucle o una función cambie el recorrido. El orden importa: la computadora no reorganiza las instrucciones para hacer lo que tú querías decir.',
        'プログラムは命令の集まりです。コンピューターは決められた順番で命令を実行します。条件分岐、繰り返し、関数で流れが変わらなければ、通常は上から下へ進みます。コンピューターが意図をくんで命令を並べ直してくれるわけではないので、順番が大切です。'), lang)
    out += p(t('<strong>Playing TLAC:</strong> use a small coin to mark the current instruction. Blue numbers such as 0001 tell you where you are. Yellow cards contain instructions; green cards contain comments for the reader.', '<strong>Para jugar a TLAC:</strong> usa una moneda pequeña para señalar la instrucción actual. Los números azules, como 0001, indican dónde estás. Las tarjetas amarillas contienen instrucciones; las verdes, comentarios para quien lee.', '<strong>TLACで遊ぶヒント：</strong>小さなコインで今の命令を指しましょう。0001などの青い番号で位置がわかります。黄色いカードは命令、緑のカードは読む人のためのコメントです。'), lang, 'note')
    out += chart('sequence-good', t('A morning routine, in order', 'Una rutina de la mañana, en orden', '朝の行動を順番に'), lang)
    out += p(t('This order means brushing your teeth, combing your hair, and then going to work. Now compare it with the same actions in a different order:', 'Este orden significa cepillarte los dientes, peinarte y después ir al trabajo. Compáralo con las mismas acciones en otro orden:', 'この順番なら、歯を磨き、髪を整えてから仕事に行きます。同じ動作を別の順番にした場合と比べましょう。'), lang)
    out += chart('sequence-bad', t('The same actions, a different result', 'Las mismas acciones, otro resultado', '同じ動作でも、順番が違うと結果が変わる'), lang)
    out += p(t('Here you leave for work before combing your hair. All three instructions are still present, but the sequence changes the result. This is why checking the order is one of the first steps in finding a programming mistake.', 'Aquí sales hacia el trabajo antes de peinarte. Las tres instrucciones siguen presentes, pero la secuencia cambia el resultado. Por eso, revisar el orden es uno de los primeros pasos para encontrar un error de programación.', 'こちらでは髪を整える前に仕事へ出発してしまいます。3つの命令は同じでも、順番が変わると結果も変わります。プログラムの間違いを探すときは、まず順番を確認しましょう。'), lang)
    out += p(t('The original lesson also refers to <a href="https://www.youtube.com/watch?v=EKWGGDXe5MA">this Richard Feynman lecture</a> when discussing how literally computers follow instructions.', 'La lección original también remite a <a href="https://www.youtube.com/watch?v=EKWGGDXe5MA">esta charla de Richard Feynman</a> al hablar de cómo las computadoras siguen las instrucciones literalmente.', '元の教材では、コンピューターが命令をそのまま実行することについて、<a href="https://www.youtube.com/watch?v=EKWGGDXe5MA">リチャード・ファインマンの講義</a>も紹介しています。'), lang)
    return out


def variables(lang):
    out = heading(1, lang)
    out += p(t('A <strong>variable</strong> is a name for a stored value. Think of a labeled box: the name tells you which box to use, and its current contents are the value. A variable can hold a number such as 5 or text such as “hello”. Text is called a <strong>string</strong>.', 'Una <strong>variable</strong> es un nombre para un valor guardado. Imagínala como una caja con etiqueta: el nombre indica qué caja usar y su contenido actual es el valor. Una variable puede guardar un número como 5 o texto como «hola». El texto se llama <strong>cadena</strong>.', '<strong>変数</strong>は、保存した値につける名前です。ラベルつきの箱を思い浮かべてください。名前で使う箱を選び、中身が現在の値になります。5のような数や「こんにちは」のような文字を保存できます。文字の並びを<strong>文字列</strong>といいます。'), lang)
    out += p(t('Names such as x or last_name are easy to use. In the examples, names do not contain spaces: last_name is one name, while “last name” is a phrase. Strings are shown in quotation marks to distinguish them from names and numbers. For example, last_name can store “Einstein”.', 'Puedes usar nombres como x o last_name. En estos ejemplos los nombres no contienen espacios: last_name es un solo nombre, mientras que «last name» es una frase. Las cadenas se muestran entre comillas para distinguirlas de nombres y números. Por ejemplo, last_name puede guardar «Einstein».', 'xやlast_nameのような名前を使います。この例では名前に空白を入れません。last_nameは1つの名前ですが、「last name」は空白を含む表現です。文字列は引用符で囲み、名前や数と区別します。たとえばlast_nameに「Einstein」を保存できます。'), lang)
    out += p(t('The kind of value matters. An identification number such as 123456789 can be written as a number, but “123-45-6789” is text because it includes separators. Choose a representation that preserves the information you need, including leading zeros when they matter.', 'El tipo de valor importa. Un identificador como 123456789 puede escribirse como número, pero «123-45-6789» es texto porque incluye separadores. Elige una representación que conserve la información necesaria, incluidos los ceros iniciales cuando sean importantes.', '値の表し方も大切です。123456789のような識別番号は数として書けますが、「123-45-6789」は区切りの記号を含む文字列です。先頭の0など、必要な情報が失われない表し方を選びます。'), lang)
    out += p(t('A variable’s value can change. Setting x to 3 and later setting x to 5 replaces the old value; x now holds 5. This operation is called <strong>assignment</strong>. It records a value at a particular point in the program, rather than declaring a mathematical equation that must always be true.', 'El valor de una variable puede cambiar. Asignar 3 a x y después asignarle 5 sustituye el valor anterior: ahora x guarda 5. Esta operación se llama <strong>asignación</strong>. Guarda un valor en un momento concreto del programa; no declara una ecuación matemática que deba ser cierta siempre.', '変数の値は変えられます。xを3にしてから5にすると、前の値が置き換わり、xは5になります。この操作が<strong>代入</strong>です。プログラムのその時点の値を保存する操作であり、いつでも成り立つ数学の等式を宣言するわけではありません。'), lang)
    out += p(t('<strong>Playing TLAC:</strong> write each variable’s name and current value on a separate sheet. Cross out the old value whenever an assignment changes it.', '<strong>Para jugar a TLAC:</strong> escribe los nombres de las variables y sus valores actuales en otra hoja. Tacha el valor anterior cuando una asignación lo cambie.', '<strong>TLACで遊ぶヒント：</strong>別の紙に変数名と現在の値を書きましょう。代入で値が変わったら、古い値を消して書き直します。'), lang, 'note')
    return out


def statements(lang):
    out = heading(2, lang)
    out += p(t('A <strong>statement</strong> is an instruction that performs a step of the program. Assignments, function calls, and conditions are examples. Follow these three assignments in order:', 'Una <strong>instrucción</strong> o sentencia realiza un paso del programa. Las asignaciones, las llamadas a funciones y las condiciones son ejemplos. Sigue estas tres asignaciones en orden:', '<strong>文</strong>は、プログラムの1つの処理を表す命令です。代入、関数呼び出し、条件分岐などがあります。次の3つの代入を順番に追いましょう。'), lang)
    out += chart('assignment', t('Change the value of x', 'Cambiar el valor de x', 'xの値を変える'), lang)
    out += steps([
        t('Line 0001 sets x to 3.', 'La línea 0001 asigna 3 a x.', '0001行目でxを3にします。'),
        t('Line 0002 replaces that value with 5.', 'La línea 0002 sustituye ese valor por 5.', '0002行目でその値を5に置き換えます。'),
        t('Line 0003 reads the current x (5), adds 1, and stores 6 back in x.', 'La línea 0003 lee el valor actual de x (5), suma 1 y guarda 6 en x.', '0003行目で現在のx（5）を読み、1を足して、6をxに保存します。'),
    ], lang)
    out += p(t('In the notation x = x + 1, first calculate the expression on the right using the old value. Then put the result in the variable on the left. That destination is sometimes called the <strong>lvalue</strong>. The final value is 6; the instruction does not mean that a number is mathematically equal to itself plus one.', 'En la notación x = x + 1, primero calcula la expresión de la derecha usando el valor anterior. Después guarda el resultado en la variable de la izquierda. Ese destino a veces se llama <strong>lvalue</strong>. El valor final es 6; la instrucción no afirma que un número sea matemáticamente igual a sí mismo más uno.', 'x = x + 1という書き方では、まず右側を古い値で計算し、結果を左側の変数へ保存します。この保存先を<strong>左辺値（lvalue）</strong>と呼ぶこともあります。最後の値は6です。ある数と、その数に1を足したものが数学的に等しいという意味ではありません。'), lang)
    return out


def conditions(lang):
    out = heading(3, lang)
    out += p(t('A <strong>condition</strong> asks a question with a true or false answer. A <strong>block</strong> is a group of instructions that belongs together. If a condition is true, follow its block; if it is false, skip that block. The colored enclosure and indentation show which instructions belong to it.', 'Una <strong>condición</strong> plantea una pregunta cuya respuesta es verdadera o falsa. Un <strong>bloque</strong> es un grupo de instrucciones que van juntas. Si la condición es verdadera, ejecuta su bloque; si es falsa, sáltalo. El recuadro de color y la sangría indican qué instrucciones pertenecen al bloque.', '<strong>条件</strong>は、正しいかどうかを調べる問いです。<strong>ブロック</strong>は、ひとまとまりの命令です。条件が成り立てば中を実行し、成り立たなければ飛ばします。色つきの囲みと字下げで、どの命令がまとまりに属するかがわかります。'), lang)
    out += board(0, t('Initial board: X=4, Y=9, facing up', 'Tablero inicial: X=4, Y=9, mirando arriba', '最初の盤面：X=4、Y=9、上向き'), lang)
    out += p(t('Coordinates start at 0. X counts columns from the left and Y counts rows from the top. X=4 is the fifth column. “Move forward” moves the turtle one square in the direction of its head unless another distance is given.', 'Las coordenadas empiezan en 0. X cuenta columnas desde la izquierda y Y cuenta filas desde arriba. X=4 es la quinta columna. «Avanzar» mueve la tortuga una casilla hacia donde mira su cabeza, salvo que se indique otra distancia.', '座標は0から数えます。Xは左からの列、Yは上からの行です。X=4は左から5列目です。「前に進む」は、距離の指定がなければ亀の頭が向いている方向に1マス進めます。'), lang)
    out += chart('conditionals', t('Choose which blocks to execute', 'Elegir qué bloques ejecutar', '実行するブロックを選ぶ'), lang)
    out += p(t('Lines 0001–0003 are comments; they explain the program without moving anything. At line 0004, X is 4, so “X is greater than 3” is true. Enter the block and execute the forward move on line 0008. X stays 4; moving up changes Y from 9 to 8.', 'Las líneas 0001–0003 son comentarios: explican el programa sin mover nada. En la línea 0004, X vale 4, así que «X es mayor que 3» es verdadero. Entra en el bloque y avanza en la línea 0008. X sigue en 4; al subir, Y cambia de 9 a 8.', '0001〜0003行目は説明のためのコメントなので、何も動かしません。0004行目ではXが4のため「Xは3より大きい」が成り立ちます。ブロックに入り、0008行目で前に進みます。上へ進むのでXは4のまま、Yが9から8になります。'), lang)
    out += board(1, t('After line 0008: X=4, Y=8', 'Después de la línea 0008: X=4, Y=8', '0008行目の後：X=4、Y=8'), lang)
    out += p(t('At line 0009, X is still 4, so “X is less than 3” is false. Skip the block, including the move on line 0012. Line 0013 then sets X to 2: move the turtle sideways to the third column without changing Y or its direction.', 'En la línea 0009, X sigue valiendo 4, así que «X es menor que 3» es falso. Salta el bloque, incluido el movimiento de la línea 0012. Después, la línea 0013 asigna 2 a X: mueve la tortuga a la tercera columna sin cambiar Y ni su dirección.', '0009行目でもXは4なので「Xは3より小さい」は成り立ちません。0012行目の移動も含め、ブロックを飛ばします。0013行目でXを2にするので、Yと向きは変えずに左から3列目へ移動します。'), lang)
    out += board(2, t('After line 0013: X=2, Y=8', 'Después de la línea 0013: X=2, Y=8', '0013行目の後：X=2、Y=8'), lang)
    out += p(t('Line 0017 asks the same question again, but now X is 2. This time “X is less than 3” is true, so execute line 0021. The turtle moves up one square to X=2, Y=7. A condition uses the values at the moment it is checked.', 'La línea 0017 hace la misma pregunta, pero ahora X vale 2. Esta vez «X es menor que 3» es verdadero, así que ejecuta la línea 0021. La tortuga sube una casilla hasta X=2, Y=7. Una condición usa los valores que existen en el momento de comprobarla.', '0017行目で同じ問いを調べ直します。今はXが2なので「Xは3より小さい」が成り立ち、0021行目を実行します。1マス上へ進み、X=2、Y=7になります。条件は、調べたその時点の値を使います。'), lang)
    out += board(3, t('Final board: X=2, Y=7', 'Tablero final: X=2, Y=7', '最後の盤面：X=2、Y=7'), lang)
    return out


def functions(lang):
    out = heading(4, lang)
    out += p(t('A <strong>function definition</strong> gives a name to a reusable group of instructions. A <strong>function call</strong> asks the program to perform that group. Defining a function does not run its body. We already used calls in the morning routine:', 'Una <strong>definición de función</strong> da un nombre a un grupo reutilizable de instrucciones. Una <strong>llamada a función</strong> pide al programa que realice ese grupo. Definir una función no ejecuta su cuerpo. Ya usamos llamadas en la rutina de la mañana:', '関数の<strong>定義</strong>は、何度も使える命令のまとまりに名前をつけます。関数の<strong>呼び出し</strong>は、そのまとまりを実行するよう頼みます。定義するだけでは中の命令は実行しません。朝の行動の例でも、関数を呼び出していました。'), lang)
    out += chart('sequence-functions', t('Calling named actions', 'Llamar a acciones con nombre', '名前をつけた動作を呼び出す'), lang)
    out += p(t('Now define a new turtle action: lay four eggs in a square. “Place an egg” marks the square under the turtle. “Turn right” rotates it 90° clockwise without moving to another square. These are built-in TLAC actions; the square-making function below is a new action defined by the programmer.', 'Ahora define una acción nueva para la tortuga: poner cuatro huevos en un cuadrado. «Poner un huevo» marca la casilla bajo la tortuga. «Girar a la derecha» la rota 90° en sentido horario sin cambiar de casilla. Son acciones incluidas en TLAC; la función que forma el cuadrado es una acción nueva definida por quien programa.', '次は、4個の卵を正方形に並べる動作を定義します。「卵を置く」は亀のいるマスに印をつけます。「右に回る」は位置を変えず、時計回りに90度回転します。これらはTLACに用意されている動作です。正方形を作る関数は、プログラムを書く人が新しく定義する動作です。'), lang)
    out += chart('functions', t('Define one egg pattern; use it three times', 'Definir un patrón de huevos y usarlo tres veces', '卵の模様を1回定義し、3回使う'), lang)
    out += p(t('Lines 0003–0017 define the function. Start the main instructions at line 0018: set X to 0, show the board, and call the new function on line 0021. Follow its body, then continue after the call. Next set X to 5 and call it again at line 0025. Finally set X to 8 and call it at line 0029.', 'Las líneas 0003–0017 definen la función. Empieza las instrucciones principales en la línea 0018: asigna 0 a X, muestra el tablero y llama a la función en la línea 0021. Sigue su cuerpo y continúa después de la llamada. Luego asigna 5 a X y llámala en la línea 0025. Por último, asigna 8 a X y llámala en la línea 0029.', '0003〜0017行目で関数を定義しています。メインの命令は0018行目からです。Xを0にして盤面を表示し、0021行目で関数を呼びます。関数の中を実行したら、呼び出した命令の次へ戻ります。次はXを5にして0025行目で呼び、最後にXを8にして0029行目で呼びます。'), lang)
    out += p(t('Each call lays four eggs in a 2 × 2 square and finishes facing up. The three calls make three squares: twelve marked cells altogether. Instead of copying the same instructions three times, we write the pattern once and reuse it. That makes the program shorter and easier to read or change.', 'Cada llamada pone cuatro huevos formando un cuadrado de 2 × 2 y termina mirando hacia arriba. Las tres llamadas forman tres cuadrados: doce casillas marcadas en total. En vez de copiar las mismas instrucciones tres veces, escribimos el patrón una vez y lo reutilizamos. Así el programa es más corto y más fácil de leer o modificar.', '1回呼ぶたびに2×2の正方形に卵を4個置き、上向きで終わります。3回の呼び出しで3つの正方形、合計12マスに卵が置かれます。同じ命令を3回書き写す代わりに、1回定義して使い回すので、短く、読みやすく、変更しやすくなります。'), lang)
    out += execution('functions', lang)
    out += h3(t('Parameters: give a function the details it needs', 'Parámetros: dar a una función los datos que necesita', '引数：関数に必要な情報を渡す'), lang)
    out += p(t('A function name follows the same naming idea as a variable name. Some functions also accept <strong>parameters</strong>: values used for that call. “Move forward 5 squares” gives the movement function a distance of 5. A different call can give it another distance without redefining the movement instructions.', 'El nombre de una función sigue la misma idea que el de una variable. Algunas funciones también aceptan <strong>parámetros</strong>: valores que se usan en esa llamada. «Avanzar 5 casillas» da a la función de movimiento una distancia de 5. Otra llamada puede darle otra distancia sin volver a definir las instrucciones.', '関数には変数と同じように名前をつけます。関数に渡す値を<strong>引数</strong>といいます。「5マス前に進む」では、移動する関数に距離5を渡します。別の呼び出しで別の距離を渡しても、移動の手順を定義し直す必要はありません。'), lang)
    out += p(t('The display instructions in this example label and show the board after changing X. They help you see what happened; they do not lay eggs or turn the turtle. Changing X moves the turtle directly, whereas the forward instruction moves it in the direction of its head.', 'Las instrucciones de mostrar de este ejemplo ponen un título y muestran el tablero después de cambiar X. Ayudan a ver lo ocurrido; no ponen huevos ni giran la tortuga. Cambiar X mueve la tortuga directamente, mientras que avanzar la mueve hacia donde mira su cabeza.', 'この例の表示命令は、Xを変えた後に見出しと盤面を表示して、何が起きたかを見やすくします。卵を置いたり、亀を回したりはしません。Xの変更は横の位置を直接変え、「前に進む」は頭の向きに移動します。'), lang)
    out += p(t('<strong>Returning from a function:</strong> when the function finishes, continue at the instruction after the call. A return instruction can finish the function early and can also send back a result. This example reaches the end of its body without an explicit return. A function used mainly for an action, rather than a returned value, is sometimes called a procedure.', '<strong>Volver de una función:</strong> cuando termina, continúa en la instrucción que sigue a la llamada. Una instrucción de retorno puede terminar la función antes y también devolver un resultado. Este ejemplo llega al final de su cuerpo sin un retorno explícito. Una función usada principalmente para realizar una acción, en lugar de devolver un valor, a veces se llama procedimiento.', '<strong>関数から戻る：</strong>関数が終わると、呼び出した命令の次へ進みます。「戻る」という命令で途中で終えることも、結果の値を返すこともできます。この例は明示的な戻る命令を使わず、中の命令の最後まで実行して戻ります。値を返すよりも動作を行うための関数を、手続きと呼ぶこともあります。'), lang, 'note')
    return out


def input_output(lang):
    out = heading(5, lang)
    out += h3(t('Output: show what happened', 'Salida: mostrar lo que ocurrió', '出力：結果を見せる'), lang)
    out += p(t('<strong>Output</strong> is information or a visible result produced by a program. In TLAC, it may be a changed board or something written on paper. Here is a very small program:', '<strong>Salida</strong> es la información o el resultado visible que produce un programa. En TLAC puede ser un tablero que cambia o algo escrito en papel. Este es un programa muy pequeño:', '<strong>出力</strong>は、プログラムが作る情報や、見える結果です。TLACでは盤面の変化や紙に書いた内容が出力になります。次はとても短いプログラムです。'), lang)
    out += chart('output', t('Move forward five squares', 'Avanzar cinco casillas', '5マス前に進む'), lang)
    out += '<div class="board-pair">' + board(4, t('Before: X=4, Y=9', 'Antes: X=4, Y=9', '実行前：X=4、Y=9'), lang) + board(5, t('After: X=4, Y=4', 'Después: X=4, Y=4', '実行後：X=4、Y=4'), lang) + '</div>'
    out += p(t('The turtle starts facing up. A distance of 5 moves it from Y=9 to Y=4 while X stays 4. The changed board is the output. A printed message can also report the movement and its move number.', 'La tortuga empieza mirando hacia arriba. Una distancia de 5 la lleva de Y=9 a Y=4, mientras X sigue en 4. El tablero cambiado es la salida. Un mensaje escrito también puede informar del movimiento y su número.', '亀は上向きです。5マス進むとYが9から4になり、Xは4のままです。この盤面の変化が出力です。移動した内容や移動番号を文字で表示することもできます。'), lang)
    out += h3(t('Input: receive information from a player', 'Entrada: recibir información de un jugador', '入力：プレイヤーから情報を受け取る'), lang)
    out += p(t('<strong>Input</strong> is information received by the program. In TLAC, a player can provide input by moving a piece when asked. The program can read the resulting position and remember it.', '<strong>Entrada</strong> es información que recibe el programa. En TLAC, un jugador puede proporcionar entrada moviendo una pieza cuando se le pide. El programa puede leer la posición resultante y recordarla.', '<strong>入力</strong>は、プログラムが受け取る情報です。TLACでは、プレイヤーが頼まれたとおりに駒を動かすことで入力できます。プログラムはその位置を読み、覚えておくことができます。'), lang)
    out += chart('input', t('Remember a player’s chosen position', 'Recordar la posición elegida por un jugador', 'プレイヤーが置いた位置を覚える'), lang)
    out += steps([
        t('Line 0004 sets the usual starting position to X=4, Y=9. Blank line 0002 does nothing.', 'La línea 0004 establece la posición inicial habitual X=4, Y=9. La línea vacía 0002 no hace nada.', '0004行目でいつもの開始位置X=4、Y=9にします。空白の0002行目では何もしません。'),
        t('Line 0005 asks the player to move to the top-left corner. Line 0006 records an example response: X=0, Y=0.', 'La línea 0005 pide al jugador que vaya a la esquina superior izquierda. La línea 0006 registra una respuesta de ejemplo: X=0, Y=0.', '0005行目で左上の隅に置くよう頼みます。0006行目は、その操作の例としてX=0、Y=0へ移動します。'),
        t('Lines 0007 and 0008 save the current X and Y in savedX and savedY. These are copies of the values at this moment.', 'Las líneas 0007 y 0008 guardan X e Y en savedX y savedY. Son copias de los valores de ese momento.', '0007、0008行目で現在のXとYをsavedXとsavedYに保存します。その時点の値をコピーします。'),
        t('Lines 0009 and 0010 ask for and demonstrate a move to the bottom-right corner, X=9, Y=9.', 'Las líneas 0009 y 0010 piden y muestran un movimiento a la esquina inferior derecha, X=9, Y=9.', '0009、0010行目で右下の隅X=9、Y=9への移動を頼み、操作の例を示します。'),
        t('Line 0011 returns the turtle to savedX, savedY. In this example it returns to X=0, Y=0.', 'La línea 0011 devuelve la tortuga a savedX, savedY. En este ejemplo vuelve a X=0, Y=0.', '0011行目でsavedX、savedYの位置へ戻します。この例ではX=0、Y=0に戻ります。'),
    ], lang)
    out += p(t('The example-response instructions let the saved execution demonstrate the player’s actions. When playing on paper, the person performs those actions. A player may choose another position or make a mistake: the program remembers the position it actually reads, not the position you hoped they would choose. This makes input useful for games where one person acts as the computer and another controls the pieces.', 'Las instrucciones de respuesta de ejemplo permiten mostrar las acciones del jugador en la ejecución guardada. Al jugar en papel, la persona realiza esas acciones. Un jugador puede elegir otra posición o equivocarse: el programa recuerda la posición que realmente lee, no la que esperabas que eligiera. Esto permite juegos donde una persona hace de computadora y otra controla las piezas.', '操作例の命令は、保存された実行結果でプレイヤーの動きを示すためのものです。紙で遊ぶときは、人が操作します。別の場所を選んだり間違えたりした場合、保存するのは期待した位置ではなく、実際に読み取った位置です。1人がコンピューター役、もう1人が駒を操作するゲームなどに使えます。'), lang)
    out += execution('input', lang)
    return out


def loops(lang):
    out = heading(6, lang)
    out += p(t('A <strong>loop</strong> repeats a block of instructions. Instead of writing similar commands many times, describe which values to use or when to stop. Always ask: what repeats, what changes, and when does the repetition finish?', 'Un <strong>bucle</strong> repite un bloque de instrucciones. En lugar de escribir órdenes parecidas muchas veces, indica qué valores usar o cuándo parar. Pregúntate siempre: ¿qué se repite, qué cambia y cuándo termina?', '<strong>繰り返し（ループ）</strong>は、命令のまとまりを何度も実行します。似た命令を何回も書く代わりに、使う値や終了条件を指定します。「何を繰り返すか」「何が変わるか」「いつ終わるか」を考えましょう。'), lang)
    out += h3(t('Count upward with a for loop', 'Contar hacia arriba con un bucle', '数を増やしながら繰り返す'), lang)
    out += chart('for', t('Use each number from 5 through 9', 'Usar cada número del 5 al 9', '5から9までの数を順番に使う'), lang)
    out += p(t('At line 0002, i takes the values 5, 6, 7, 8, and 9. For each value, line 0003 uses i for both coordinates. The turtle visits (5,5), (6,6), (7,7), (8,8), and (9,9), making a diagonal path. Both 5 and 9 are included; 10 is not. The message on line 0005 is outside the loop, so it is written once after the loop finishes.', 'En la línea 0002, i toma los valores 5, 6, 7, 8 y 9. Para cada valor, la línea 0003 usa i en ambas coordenadas. La tortuga visita (5,5), (6,6), (7,7), (8,8) y (9,9), formando una diagonal. Se incluyen 5 y 9; no se incluye 10. El mensaje de la línea 0005 está fuera del bucle y se escribe una sola vez al terminar.', '0002行目でiは5、6、7、8、9になります。各値について0003行目で両方の座標にiを使うので、亀は(5,5)、(6,6)、(7,7)、(8,8)、(9,9)を訪れ、斜めの経路になります。5と9は含み、10は含みません。0005行目のメッセージはループの外なので、終わった後に1回だけ書きます。'), lang)
    out += execution('for', lang)
    out += h3(t('Count downward', 'Contar hacia atrás', '数を減らしながら繰り返す'), lang)
    out += p(t('A countdown is useful for a rocket launch or any job whose remaining count gets smaller. Here the count controls how far the turtle moves each time.', 'Una cuenta atrás sirve para un lanzamiento de cohete o cualquier tarea cuya cantidad pendiente disminuye. Aquí la cuenta controla cuánto avanza la tortuga cada vez.', 'カウントダウンは、ロケットの発射など、残りの数が減っていく場面に使えます。ここでは数を使って、その回に亀が進む距離を決めます。'), lang)
    out += chart('countdown', t('Move 3, then 2, then 1, then 0 squares', 'Avanzar 3, luego 2, luego 1 y luego 0 casillas', '3、2、1、0マスと順番に進む'), lang)
    out += p(t('The counter starts at 3 and decreases by 1 each time, including the final value 0. The movements are 3 + 2 + 1 + 0 = 6 squares altogether. Moving zero squares leaves the turtle in place. From X=4, Y=9 facing up, it ends at X=4, Y=3.', 'El contador empieza en 3 y disminuye en 1 cada vez, incluido el valor final 0. Los movimientos suman 3 + 2 + 1 + 0 = 6 casillas. Avanzar cero casillas deja a la tortuga en su sitio. Desde X=4, Y=9 mirando arriba, termina en X=4, Y=3.', '3から始めて1ずつ減らし、最後の0も使います。進む距離の合計は3 + 2 + 1 + 0 = 6マスです。0マス進んでも位置は変わりません。X=4、Y=9で上向きに始めると、X=4、Y=3で終わります。'), lang)
    out += execution('countdown', lang)
    out += h3(t('Do first, check afterward: a do-while pattern', 'Hacer primero y comprobar después: patrón do-while', '先に実行してから調べる：do-whileの考え方'), lang)
    out += p(t('Sometimes the body must run at least once before checking whether to continue. This example repeats, increases a counter, and leaves the loop when the counter passes a limit. It has the behavior of a do-while loop: perform the body first, then decide whether to repeat.', 'A veces el cuerpo debe ejecutarse al menos una vez antes de decidir si continuar. Este ejemplo repite, aumenta un contador y sale cuando este supera un límite. Tiene el comportamiento de un bucle do-while: primero ejecutar el cuerpo y después decidir si repetir.', '続けるか調べる前に、少なくとも1回は実行したい場合があります。この例は動作を繰り返し、数を増やして、上限を超えたら抜けます。先に中の命令を実行してから継続を判断する、do-while型の繰り返しです。'), lang)
    out += chart('do-while', t('Stop after the counter passes its limit', 'Parar cuando el contador supere su límite', '数が上限を超えたら止まる'), lang)
    out += p(t('The starting values are n1=1, n2=3, and step=1. Each pass writes n1, moves forward n1 squares, and adds step to n1. The movement distances are therefore 1, 2, and 3. After the third pass n1 becomes 4, so “n1 is greater than n2” is true and the loop exits. The final message is outside the loop.', 'Los valores iniciales son n1=1, n2=3 y step=1. Cada vuelta escribe n1, avanza n1 casillas y suma step a n1. Por tanto, las distancias son 1, 2 y 3. Tras la tercera vuelta n1 vale 4, así que «n1 es mayor que n2» es verdadero y se sale del bucle. El mensaje final está fuera del bucle.', '初期値はn1=1、n2=3、step=1です。毎回n1を書き、n1マス進んでからn1にstepを足します。進む距離は1、2、3です。3回目の後にn1が4になり「n1はn2より大きい」が成り立つので、抜けます。最後のメッセージはループの外にあります。'), lang)
    out += p(t('Notice that the counter increases here. The condition is a stopping test: leave when n1 is greater than n2, otherwise repeat. Without a change that eventually makes the stopping test true, the loop could continue forever.', 'Observa que aquí el contador aumenta. La condición comprueba cuándo parar: salir si n1 es mayor que n2; en caso contrario, repetir. Sin un cambio que finalmente cumpla la condición de parada, el bucle podría seguir para siempre.', 'ここでは数を増やしています。条件は「いつ止めるか」を調べており、n1がn2より大きければ抜け、それ以外は続けます。停止条件に近づく変化がなければ、いつまでも繰り返すことがあります。'), lang, 'note')
    out += execution('do-while', lang)
    out += h3(t('Nested loops: multiplication tables', 'Bucles anidados: tablas de multiplicar', '入れ子の繰り返し：掛け算の表'), lang)
    out += p(t('A loop can contain another loop. The <strong>outer loop</strong> chooses a row; the <strong>inner loop</strong> works through every item in that row. Here i and j each take the values 1, 2, and 3.', 'Un bucle puede contener otro. El <strong>bucle exterior</strong> elige una fila y el <strong>bucle interior</strong> recorre todos los elementos de esa fila. Aquí i y j toman los valores 1, 2 y 3.', '繰り返しの中に別の繰り返しを入れられます。<strong>外側のループ</strong>が行を選び、<strong>内側のループ</strong>がその行の各要素を処理します。ここではiとjの両方が1、2、3になります。'), lang)
    out += chart('nested', t('Make a 3 × 3 multiplication table', 'Crear una tabla de multiplicar de 3 × 3', '3×3の掛け算の表を作る'), lang)
    out += p(t('For i=1, the inner loop runs with j=1, j=2, and j=3 before i changes. Then the same three j values are used for i=2 and again for i=3. There are 3 × 3 = 9 multiplications. Start a fresh output string for each row, append the three equations, and display the completed row.', 'Para i=1, el bucle interior pasa por j=1, j=2 y j=3 antes de que i cambie. Luego se usan los mismos tres valores de j para i=2 y otra vez para i=3. Hay 3 × 3 = 9 multiplicaciones. Empieza cada fila con un texto vacío, añade sus tres ecuaciones y muestra la fila completa.', 'i=1の間に、内側でj=1、2、3をすべて処理してからiを変えます。i=2、i=3でも同じ3つのjを使い、合計3×3=9回の掛け算になります。各行で出力文字列を空にし、3つの式を追加してから完成した行を表示します。'), lang)
    out += '<pre class="text-output">1 × 1 = 1    1 × 2 = 2    1 × 3 = 3\n2 × 1 = 2    2 × 2 = 4    2 × 3 = 6\n3 × 1 = 3    3 × 2 = 6    3 × 3 = 9</pre>'
    out += execution('nested', lang)
    out += h3(t('Several loops: build a pyramid', 'Varios bucles: construir una pirámide', '複数の繰り返し：ピラミッドを作る'), lang)
    out += chart('pyramid', t('Build each row from spaces and stars', 'Construir cada fila con espacios y estrellas', '空白と星で各行を作る'), lang)
    out += p(t('The outer loop calls the row-making function five times. It passes the star character as ch, the row number as times, and 5 as triangle_width. Inside the function, the first inner loop adds spaces, and the second adds stars. These two inner loops happen one after the other. The completed row is then displayed.', 'El bucle exterior llama cinco veces a la función que crea una fila. Le pasa el carácter estrella como ch, el número de fila como times y 5 como triangle_width. Dentro, el primer bucle añade espacios y el segundo estrellas. Los dos bucles interiores se ejecutan uno después del otro. Después se muestra la fila completa.', '外側のループが、1行を作る関数を5回呼びます。chに星の文字、timesに行番号、triangle_widthに5を渡します。関数の中では、最初のループで空白を追加し、次のループで星を追加します。この2つは順番に実行され、最後に完成した行を表示します。'), lang)
    out += '<div class="table-scroll"><table><thead><tr>' + ''.join('<th scope="col">'+x[lang]+'</th>' for x in [t('Row','Fila','行'),t('Spaces','Espacios','空白'),t('Stars','Estrellas','星')]) + '</tr></thead><tbody>'
    for row in range(1, 6):
        out += f'<tr><th scope="row">{row}</th><td>{6-row}</td><td>{2*row-1}</td></tr>'
    out += '</tbody></table></div><pre class="text-output">     *\n    ***\n   *****\n  *******\n *********</pre>'
    out += p(t('In the board game, displaying text means writing the characters on paper, keeping the spaces so that the shape lines up. This program combines functions, parameters, counting, and multiple loops.', 'En el juego de mesa, mostrar texto significa escribir los caracteres en papel, conservando los espacios para alinear la figura. Este programa combina funciones, parámetros, cuentas y varios bucles.', 'ボードゲームでは、文字を表示する代わりに紙へ書きます。空白もそのまま書くと、形がそろいます。この例は、関数、引数、数える処理、複数の繰り返しを組み合わせています。'), lang)
    out += execution('pyramid', lang)
    return out


def lists(lang):
    out = heading(7, lang)
    out += p(t('A <strong>list</strong> stores several values in order. Each value is an <strong>item</strong> or element. An <strong>index</strong> tells you an item’s position. In these examples, counting begins at 0: the first item has index 0, the second has index 1, and so on. Arrays are another way to organize indexed values; here we use lists.', 'Una <strong>lista</strong> guarda varios valores en orden. Cada valor es un <strong>elemento</strong>. Un <strong>índice</strong> indica su posición. En estos ejemplos se empieza a contar en 0: el primer elemento tiene índice 0, el segundo índice 1, y así sucesivamente. Los arreglos son otra forma de organizar valores con índices; aquí usaremos listas.', '<strong>リスト</strong>は複数の値を順番に保存します。1つずつの値を<strong>要素</strong>といい、<strong>添字（インデックス）</strong>で位置を表します。この例では0から数えるので、最初の要素は添字0、2番目は添字1です。配列も添字で値を扱う方法ですが、ここではリストを使います。'), lang)
    out += h3(t('For each item: follow a list of turtle commands', 'Para cada elemento: seguir una lista de órdenes', '各要素について：亀の命令リストを使う'), lang)
    out += p(t('A <strong>for-each loop</strong> visits each item of a list in order. The list below describes a turtle route. Take one command, decide what it means, perform the action, and then take the next command. The list itself becomes data that describes a small program.', 'Un <strong>bucle para cada elemento</strong> recorre la lista en orden. La siguiente lista describe una ruta de la tortuga. Toma una orden, decide qué significa, realiza la acción y pasa a la siguiente. La lista se convierte en datos que describen un pequeño programa.', '<strong>各要素についての繰り返し</strong>は、リストの要素を順番に取り出します。次のリストは亀の経路を表します。命令を1つ取り出し、意味を判断して実行し、次の命令へ進みます。リストというデータで、小さなプログラムを表しているのです。'), lang)
    out += chart('foreach', t('Execute eight turtle commands in order', 'Ejecutar ocho órdenes de la tortuga en orden', '亀の8つの命令を順番に実行する'), lang)
    out += p(t('The list on line 0002 has eight commands: forward, forward, right, forward, forward, left, forward, forward. The loop begins on line 0005. The conditions choose the matching turtle action for the current command. From X=4, Y=9 facing up, two forward moves reach (4,7); turning right and moving twice reaches (6,7); turning left and moving twice reaches (6,5), facing up.', 'La lista de la línea 0002 tiene ocho órdenes: avanzar, avanzar, derecha, avanzar, avanzar, izquierda, avanzar, avanzar. El bucle empieza en la línea 0005. Las condiciones eligen la acción correspondiente a la orden actual. Desde X=4, Y=9 mirando arriba, dos avances llegan a (4,7); girar a la derecha y avanzar dos veces lleva a (6,7); girar a la izquierda y avanzar dos veces lleva a (6,5), mirando arriba.', '0002行目のリストには「前、前、右、前、前、左、前、前」の8命令があります。0005行目で繰り返しが始まり、条件分岐で現在の命令に合う動作を選びます。X=4、Y=9で上向きに始めると、2回進んで(4,7)、右に回って2回進むと(6,7)、左に回って2回進むと(6,5)で上向きになります。'), lang)
    out += execution('foreach', lang)
    out += h3(t('Read and change a list', 'Leer y modificar una lista', 'リストを読み、変更する'), lang)
    out += p(t('Now use a list of fruit names. We keep the stored words in English so that the alphabetical order and the saved output agree in all three versions of this lesson. The initial list contains banana, apple, peach, and pear.', 'Ahora usaremos una lista de frutas. Conservamos los valores guardados en inglés para que el orden alfabético y el resultado guardado coincidan en las tres versiones de la lección. La lista inicial contiene banana (banana), apple (manzana), peach (melocotón) y pear (pera).', '次は果物名のリストです。3言語の教材でアルファベット順と保存された出力をそろえるため、データの単語は英語のままにします。最初のリストはbanana（バナナ）、apple（リンゴ）、peach（モモ）、pear（ナシ）です。'), lang)
    out += '<div class="table-scroll"><table><thead><tr><th scope="col">' + t('Index','Índice','添字')[lang] + '</th><th scope="col">' + t('Stored value','Valor guardado','保存した値')[lang] + '</th></tr></thead><tbody>'
    for index, value in enumerate(['banana', 'apple', 'peach', 'pear']):
        out += f'<tr><th scope="row">{index}</th><td>{value}</td></tr>'
    out += '</tbody></table></div>'
    out += p(t('The notation fruits[0] means the item at index 0: banana in the initial list. fruits[3] means the fourth item: pear. An index identifies a position, so the word at that position may change when the list is rearranged.', 'La notación fruits[0] significa el elemento del índice 0: banana en la lista inicial. fruits[3] es el cuarto elemento: pear. Un índice identifica una posición, así que la palabra que ocupa esa posición puede cambiar al reorganizar la lista.', 'fruits[0]は添字0の要素、最初のリストではbananaを指します。fruits[3]は4番目のpearです。添字は位置を表すので、並べ替えるとその位置にある単語も変わることがあります。'), lang)
    out += chart('lists', t('Reverse, sort, add, insert, and remove items', 'Invertir, ordenar, añadir, insertar y eliminar elementos', '逆順、並べ替え、追加、挿入、削除'), lang)
    out += steps([
        t('Create the list on line 0002. Line 0003 writes the item at index 3: pear. The next loop writes every item in its current order.', 'Crear la lista en la línea 0002. La línea 0003 escribe el elemento del índice 3: pear. El siguiente bucle escribe todos los elementos en su orden actual.', '0002行目でリストを作ります。0003行目で添字3のpearを書き、その後の繰り返しで現在の順番ですべての要素を書きます。'),
        t('Reverse it on line 0012: pear, peach, apple, banana. Reversing changes the order, not the words.', 'Invertirla en la línea 0012: pear, peach, apple, banana. Se cambia el orden, no las palabras.', '0012行目で逆順にして、pear、peach、apple、bananaにします。単語そのものは変えず、順番を変えます。'),
        t('Sort it on line 0018: apple, banana, peach, pear. Sorting arranges the English names alphabetically.', 'Ordenarla en la línea 0018: apple, banana, peach, pear. La ordenación coloca los nombres ingleses alfabéticamente.', '0018行目で英語名をアルファベット順に並べ、apple、banana、peach、pearにします。'),
        t('Append “appricot” on line 0022. Appending adds an item at the end. This is the spelling stored in the original example; the usual spelling is “apricot”.', 'Añadir «appricot» al final en la línea 0022. Añadir al final conserva los elementos anteriores. Esa es la escritura del ejemplo original; la palabra habitual es «apricot» (albaricoque).', '0022行目で末尾に「appricot」を追加します。元の例ではこのつづりで保存されていますが、通常のつづりは「apricot」（アンズ）です。'),
        t('Insert “blueberry” at index 2 on line 0024. It becomes the third item; the later items shift one position to the right.', 'Insertar «blueberry» (arándano) en el índice 2 en la línea 0024. Pasa a ser el tercer elemento; los posteriores se desplazan una posición a la derecha.', '0024行目で添字2に「blueberry」（ブルーベリー）を挿入します。3番目の要素となり、それ以降の要素は1つずつ後ろへずれます。'),
        t('Remove index 3 on line 0026. Index 3 is the fourth item, now peach. The final list is apple, banana, blueberry, pear, appricot.', 'Eliminar el índice 3 en la línea 0026. Es el cuarto elemento, que ahora es peach. La lista final es apple, banana, blueberry, pear, appricot.', '0026行目で添字3を削除します。添字3は4番目の要素で、今はpeachです。最後のリストはapple、banana、blueberry、pear、appricotになります。'),
    ], lang)
    out += execution('lists', lang)
    out += p(t('<strong>Remember:</strong> list positions start at 0. Reading an item does not remove it. Reversing and sorting change the order; appending, inserting, and removing change the contents or length. After a change, use the list’s new order when interpreting an index.', '<strong>Recuerda:</strong> las posiciones empiezan en 0. Leer un elemento no lo elimina. Invertir y ordenar cambian el orden; añadir, insertar y eliminar cambian el contenido o la longitud. Después de un cambio, usa el nuevo orden al interpretar un índice.', '<strong>覚えておこう：</strong>リストの位置は0から数えます。読むだけでは要素は消えません。逆順や並べ替えは順番を変え、追加、挿入、削除は中身や長さを変えます。変更した後は、新しい並びで添字を考えましょう。'), lang, 'note')
    return out


EXTRA_CSS = '''
.chart .instruction-row { border-radius: 0; margin: 0; padding: 8px 0; }
.chart .instruction-row p + p { margin-left: 3px; }
.chart .instruction-block { border: 2px solid #e0e0e0; padding: 2px 8px; }
.board-example .board { margin: 16px; max-width: calc(100% - 32px); }
.board-pair .board-example .board { margin: 0; max-width: 100%; }
.text-output { background: #edf8fb; border: 1px solid #7197a5; border-radius: 8px; padding: 18px; overflow-x: auto; font-size: .95rem; }
.table-scroll { overflow-x: auto; }
table { border-collapse: collapse; background: #edf8fb; margin: 20px 0; min-width: 260px; }
th, td { padding: 10px 18px; text-align: left; border: 1px solid #7197a5; }
th { background: #d8ecf3; }
.next-lesson { display: block; padding: 20px; background: #edf8fb; border: 1px solid #7197a5; border-radius: 8px; font-weight: bold; }
@media print { .text-output { white-space: pre-wrap; } }
'''


def build():
    # Validate every original line has a translation before replacing the page.
    for rows in EXAMPLES['charts'].values():
        for row in rows:
            if row['text']:
                assert set(LABELS[row['text']]) == set(LANGS), row['text']
    script = JS.replace('tlac-advanced-language', 'tlac-basics-language')
    script = script.replace('const oldHash = location.hash;', "const oldHash = /^#[0-7]$/.test(location.hash) ? '#concept-' + location.hash.slice(1) + '-' + lang : location.hash;")
    script = script.replace("const targetLanguage = location.hash.match", "if (/^#[0-7]$/.test(location.hash)) { chooseLanguage(selector.value); document.querySelector(location.hash)?.scrollIntoView(); return; }\n    const targetLanguage = location.hash.match")
    out = '<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="UTF-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n'
    out += '<meta name="description" content="Learn eight basic programming concepts with TLAC instruction cards and boards in English, Spanish, and Japanese.">\n'
    out += f'<title>{TITLE["en"]}</title>\n<style>{CSS}{EXTRA_CSS}</style>\n</head><body>\n'
    out += '<!-- Generated by build_TLAC_basics.py using basics_examples.json. -->\n'
    out += '<div class="toolbar"><label id="language-label" for="language">Language / Idioma / 言語</label><select id="language"><option value="en" lang="en">English</option><option value="es" lang="es">Español</option><option value="ja" lang="ja">日本語</option></select></div>'
    out += '<noscript><style>article[hidden] { display: block !important; } .toolbar { display: none; }</style><p>JavaScript is off: all three languages appear below. / JavaScript está desactivado: se muestran los tres idiomas. / JavaScriptが無効のため、3言語を順に表示します。</p></noscript><main>\n'
    for lang in LANGS:
        hidden = ' hidden' if lang != 'en' else ''
        out += f'<article lang="{lang}" data-language="{lang}"{hidden}><header id="top-{lang}"><p class="eyebrow">TLAC · Think Like A Computer</p><h1>{TITLE[lang]}</h1>'
        out += p(t('Learn to program, one instruction at a time.', 'Aprende a programar, una instrucción a la vez.', '命令を1つずつ追いながら、プログラミングを学ぼう。'), lang, 'subtitle')
        out += p(t('By Usmar A. Padow (amigojapan) · <a href="https://amigojapan.github.io/">Author’s homepage</a>', 'Por Usmar A. Padow (amigojapan) · <a href="https://amigojapan.github.io/">Página del autor</a>', '著者：Usmar A. Padow（amigojapan） · <a href="https://amigojapan.github.io/">著者のホームページ</a>'), lang) + '</header>'
        out += p(t('This lesson is for complete beginners. You can follow the instructions with the turtle board game, a coin, and paper. No programming experience is needed. Start with the order of instructions, then add one new idea at a time.', 'Esta lección es para principiantes sin experiencia. Puedes seguir las instrucciones con el tablero de la tortuga, una moneda y papel. No necesitas saber programar. Empieza por el orden de las instrucciones y añade una idea nueva cada vez.', '初めてプログラミングを学ぶ人のための教材です。亀のボードゲームとコイン、紙を使って命令を追えます。プログラミングの経験は必要ありません。命令の順番から始め、考え方を1つずつ増やしていきましょう。'), lang)
        out += '<nav aria-label="' + t('Lesson contents', 'Contenido de la lección', '目次')[lang] + '"><ol>'
        for n, topic in enumerate(TOPICS):
            out += f'<li><a href="#concept-{n}-{lang}">{n}. {topic[lang]}</a></li>'
        out += '</ol></nav>'
        out += p(t('The execution links below open a step-by-step debugger. Use Next and Previous to watch the current instruction, variables, and board or text output. The execution page keeps your selected language.', 'Los enlaces de ejecución abren un depurador paso a paso. Usa Siguiente y Anterior para observar la instrucción actual, las variables y el tablero o la salida de texto. La página de ejecución mantiene el idioma seleccionado.', '実行結果へのリンクを開くと、1ステップずつ確認できるデバッガーが表示されます。「次へ」「前へ」で現在の命令、変数、盤面や文字の出力を追えます。選んだ言語で実行結果も表示されます。'), lang, 'note')
        for render in [sequence, variables, statements, conditions, functions, input_output, loops, lists]:
            out += render(lang)
        out += p(t('You have now met the eight foundations: order, variables, statements, conditions, functions, input/output, loops, and lists. Try tracing an example yourself before looking at its output. When these ideas feel familiar, continue with recursion and turtle classes.', 'Ya has conocido los ocho fundamentos: orden, variables, instrucciones, condiciones, funciones, entrada/salida, bucles y listas. Intenta seguir un ejemplo antes de mirar su resultado. Cuando te resulten familiares, continúa con la recursión y las clases de tortugas.', '順番、変数、文、条件分岐、関数、入出力、繰り返し、リストという8つの基本を学びました。出力を見る前に、自分で例を追ってみましょう。慣れてきたら、再帰と亀のクラスへ進めます。'), lang)
        out += '<footer>' + p(t('Originally written in 2017 for Python 2 and C, updated for Python 3 in 2022, and adapted to TLAC in 2025. This edition presents the same eight topics and examples in English, Spanish, and Japanese.', 'Escrito originalmente en 2017 para Python 2 y C, actualizado para Python 3 en 2022 y adaptado a TLAC en 2025. Esta edición presenta los mismos ocho temas y ejemplos en inglés, español y japonés.', '2017年にPython 2とCの教材として書かれ、2022年にPython 3向けに更新、2025年にTLAC向けに改訂されました。この版では、同じ8つのテーマと例を英語、スペイン語、日本語で学べます。'), lang)
        out += f'<p><a href="#top-{lang}">' + t('Back to top', 'Volver arriba', '先頭に戻る')[lang] + '</a></p></footer>'
        out += f'<a class="next-lesson" href="../TLAC_advanced_concepts.html?lang={lang}">' + t('Next: Advanced concepts — recursion and classes →', 'Siguiente: Conceptos avanzados — recursión y clases →', '次へ：応用編 — 再帰とクラス →')[lang] + '</a></article>\n'
    out += '</main><script>' + script + '</script></body></html>\n'
    target = FOLDER / '8_basics_of_programming_TLAC.html'
    target.write_text(out, encoding='utf-8')
    print(f'Wrote {target.name}: 3 languages, 8 topics, 45 charts, 18 boards')


if __name__ == '__main__':
    build()
