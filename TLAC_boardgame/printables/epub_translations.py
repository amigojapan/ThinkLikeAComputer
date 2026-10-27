"""Book-only prose. Lesson translations come from the existing tutorial sources.

Never translate code, recorded output, identifiers, or watched program values.
"""
import re

from bs4 import NavigableString

EDITIONS = {'en': 'English', 'ja': 'Japanese', 'es': 'Spanish'}
WORDS = {}


def add(en, es, ja):
    WORDS[en] = {'es': es, 'ja': ja}


add('Think Like A Computer', 'Piensa como una computadora', 'コンピューターのように考えよう')
add('Think Like A Computer — English edition', 'Piensa como una computadora — Edición en español', 'コンピューターのように考えよう — 日本語版')
add('Think Like A Computer — All Steps Edition', 'Piensa como una computadora — Todos los pasos', 'コンピューターのように考えよう — 全ステップ収録版')
add('English edition — every step and complete output', 'Edición en español — todos los pasos y la salida completa', '日本語版 — すべてのステップと完全な出力')
add('English edition · Every step, complete output', 'Edición en español · Todos los pasos y la salida completa', '日本語版・すべてのステップと完全な出力')
add('Table of contents', 'Índice de contenidos', '目次')
add('The eight basics of programming', 'Los ocho conceptos básicos de programación', 'プログラミングの8つの基本概念')
add('Advanced concepts: recursion and classes', 'Conceptos avanzados: recursión y clases', '応用編：再帰とクラス')
add('Seven games in TLAC', 'Siete juegos en TLAC', 'TLACの7つのゲーム')
add('Insertion sort with pyramids', 'Ordenación por inserción con pirámides', 'ピラミッドで学ぶ挿入ソート')
add('Explore a maze', 'Explora un laberinto', '迷路を探索しよう')
add('All the tutorials and games from the TLAC portal in one offline book: eight programming basics, recursion and classes, seven games, insertion sort with pyramids, and maze exploration.',
    'Todos los tutoriales y juegos del portal TLAC en un libro que se puede leer sin conexión: ocho conceptos básicos de programación, recursión y clases, siete juegos, ordenación por inserción con pirámides y exploración de laberintos.',
    'TLACポータルの教材とゲームを、オフラインで読める1冊にまとめました。プログラミングの8つの基本概念、再帰とクラス、7つのゲーム、ピラミッドを使った挿入ソート、迷路探索を収録しています。')
add('Read the explanations and numbered instruction cards, then follow the complete execution walkthroughs. Use your reader’s table of contents and the links within each lesson to navigate. Practice answers and game programs are expanded so they can be read without JavaScript.',
    'Lee las explicaciones y las tarjetas de instrucciones numeradas y después sigue los recorridos completos de ejecución. Usa el índice del lector y los enlaces de cada lección para desplazarte. Las respuestas de los ejercicios y los programas de los juegos aparecen completos y se pueden leer sin JavaScript.',
    '説明と番号付きの命令カードを読んでから、実行の全過程を追いましょう。電子書籍リーダーの目次や各教材内のリンクで移動できます。練習問題の解答とゲームのプログラムはすべて展開されており、JavaScriptなしで読めます。')
add('This edition contains static illustrations and recorded walkthroughs. Interactive debugger buttons and playable programs remain in the HTML and Python editions. The companion all_boards.pdf and all_objects.pdf files in the printables folder provide boards and pieces at their intended print size.',
    'Esta edición contiene ilustraciones estáticas y ejecuciones registradas. Los botones del depurador interactivo y los programas jugables están disponibles en las versiones HTML y Python. Los archivos all_boards.pdf y all_objects.pdf de la carpeta printables contienen tableros y piezas a su tamaño de impresión. El código fuente, los nombres de variables, los valores y la salida original de los programas se conservan tal como fueron escritos o registrados; pueden incluir texto en inglés. La licencia se reproduce en su versión original.',
    'この版には静止画と実行記録を収録しています。操作できるデバッガーや実際に遊べるプログラムはHTML版とPython版にあります。printablesフォルダーのall_boards.pdfとall_objects.pdfには、印刷用の実寸の盤面とコマが入っています。ソースコード、変数名、値、プログラムの元の出力は記述・記録されたまま掲載しているため、英語が含まれることがあります。ライセンスは原文を掲載しています。')
add('Source program appendix', 'Apéndice: programas fuente', '付録：プログラムのソースコード')
add('Project license', 'Licencia del proyecto', 'プロジェクトのライセンス')
add('The repository includes the following GNU General Public License.', 'El repositorio incluye la siguiente Licencia Pública General de GNU, reproducida en su idioma original.', 'このリポジトリには、以下のGNU一般公衆利用許諾書が含まれています。原文を掲載します。')
add('Every program: all recorded steps', 'Todos los programas: todos los pasos registrados', '全プログラムの実行ステップ一覧')
add('Complete runs appear directly after their lesson examples. Each step shows its board, watched values, and full text output. Nothing is collapsed, and unchanged output is repeated.',
    'Las ejecuciones completas aparecen justo después de los ejemplos de cada lección. Cada paso muestra el tablero, los valores observados y toda la salida de texto. Todo está desplegado; la salida se repite aunque no haya cambiado.',
    '各教材の例の直後に、実行の全過程を掲載しています。各ステップには盤面、確認する値、テキスト出力の全体を表示します。折りたたまれた部分はなく、変化のない出力も繰り返し掲載します。')
add('Graphical execution results', 'Resultados gráficos de la ejecución', '実行結果の図')
add('Execution results', 'Resultados de la ejecución', '実行結果')
add('Starting board', 'Tablero inicial', '開始時の盤面')
add('Final board — sample ended', 'Tablero final — fin de la sesión de ejemplo', '最後の盤面 — サンプル終了')
add('Final board — program finished', 'Tablero final — programa terminado', '最後の盤面 — プログラム終了')
add('Final text output', 'Salida de texto final', '最後のテキスト出力')
add('Starting and final graphical results', 'Resultados gráficos iniciales y finales', '開始時と終了時の実行結果の図')
add('Final execution results', 'Resultados finales de la ejecución', '最終実行結果')
add('Numbered instructions', 'Instrucciones numeradas', '番号付きの命令')
add('Watched values at this step', 'Valores observados en este paso', 'このステップで確認する値')
add('Complete text output at this step', 'Salida de texto completa en este paso', 'このステップのテキスト出力全体')
add('No watched variables.', 'No hay variables observadas.', '確認する変数はありません。')
add('(No text output at this step.)', '(No hay salida de texto en este paso.)', '（このステップにはテキスト出力がありません。）')
add('Go to the first step', 'Ir al primer paso', '最初のステップへ')
add('Go to the last step', 'Ir al último paso', '最後のステップへ')
add('Read the complete execution walkthrough', 'Leer el recorrido completo de ejecución', '実行の全過程を読む')
add('See every step with its graphical output', 'Ver cada paso con su resultado gráfico', '各ステップとその実行結果の図を見る')
add('Every step of a sample game session', 'Todos los pasos de una sesión de juego de ejemplo', 'サンプルプレイの全ステップ')
add('Every step of this example', 'Todos los pasos de este ejemplo', 'この例の全ステップ')
add('TLAC board', 'Tablero TLAC', 'TLACの盤面')
add('Turtle', 'Tortuga', '亀')
add('Player', 'Jugador', 'プレイヤー')
add('up', 'arriba', '上')
add('down', 'abajo', '下')
add('left', 'izquierda', '左')
add('right', 'derecha', '右')
add('Start: before the first instruction', 'Inicio: antes de la primera instrucción', '開始：最初の命令を実行する前')
add('Finished: final state', 'Terminado: estado final', '終了：最後の状態')
add('Condition result: true; enter the block', 'Resultado de la condición: verdadero; entrar en el bloque', '条件の結果：真。ブロックの中へ進む')
add('Condition result: false; skip instructions 0010–0012', 'Resultado de la condición: falso; saltar las instrucciones 0010–0012', '条件の結果：偽。命令0010〜0012を飛ばす')
add('This is a card-by-card walkthrough of the lesson example. The morning routines show the state after each conceptual action; they do not print text.',
    'Este recorrido sigue las tarjetas del ejemplo de la lección una a una. Las rutinas de la mañana muestran el estado después de cada acción conceptual; no imprimen texto.',
    '教材の例をカード1枚ずつ追う実行記録です。朝の日課では、それぞれの行動の後の状態を示します。テキストは出力しません。')
add('This walkthrough follows the lesson cards and shows each assignment, condition check, and movement.',
    'Este recorrido sigue las tarjetas de la lección y muestra cada asignación, comprobación de condición y movimiento.',
    '教材のカードに沿って、代入、条件の確認、移動を1つずつ示します。')
add('The sample session finished normally.', 'La sesión de ejemplo terminó normalmente.', 'サンプルプレイは正常に終了しました。')
add('Sample stopped at the next input prompt after the chosen commands; the game is still in progress.',
    'La sesión de ejemplo se detuvo en la siguiente solicitud de entrada después de los comandos elegidos; la partida sigue en curso.',
    '指定したコマンドを実行した後、次の入力待ちでサンプルを停止しました。ゲームはまだ続いています。')
add('The player quit the game.', 'El jugador salió del juego.', 'プレイヤーがゲームを終了しました。')
add('Starting playable board: ready for the first command', 'Tablero listo para jugar: esperando el primer comando', 'プレイ開始時の盤面：最初のコマンドを待っています')
add('Start: before the game setup instructions', 'Inicio: antes de las instrucciones de preparación del juego', '開始：ゲームの準備の命令を実行する前')
add('Enter', 'Intro', 'Enterキー')
add('Space / wait', 'Espacio / esperar', 'スペースキー／待機')
add(' — sample game session', ' — sesión de juego de ejemplo', ' — サンプルプレイ')
add('O = snake body; @ = food.', 'O = cuerpo de la serpiente; @ = comida.', 'O＝ヘビの体、@＝食べ物。')
add('M and W = ghosts; X = diamond; eggs = pellets.', 'M y W = fantasmas; X = diamante; huevos = puntos.', 'MとW＝おばけ、X＝ダイヤモンド、卵＝ドット。')
add('B = box; flag = goal.', 'B = caja; bandera = meta.', 'B＝箱、旗＝ゴール。')
add('? = covered cell; F = flag; * = mine; numbers = neighboring mines; turtle = cursor.', '? = casilla cubierta; F = bandera; * = mina; números = minas vecinas; tortuga = cursor.', '?＝未確認のマス、F＝旗、*＝地雷、数字＝隣接する地雷の数、亀＝カーソル。')
add('c = car; t and T = trucks; flags = finish row.', 'c = coche; t y T = camiones; banderas = fila de llegada.', 'c＝車、tとT＝トラック、旗＝ゴールの行。')
add('M = enemy; numbers = bomb countdown; eggs = breakable crates.', 'M = enemigo; números = cuenta atrás de las bombas; huevos = cajas que se pueden destruir.', 'M＝敵、数字＝爆発までのカウントダウン、卵＝壊せる箱。')
add('O = living cell; empty square = dead cell.', 'O = célula viva; casilla vacía = célula muerta.', 'O＝生きたセル、空のマス＝死んだセル。')

# These source paragraphs describe browser controls. Replace the entire paragraph
# with the same explanation adapted to an offline book, in all three languages.
OFFLINE = [
    (('The execution links below open a step-by-step debugger.', 'Los enlaces de ejecución', '実行結果へのリンクを開くと、'),
     'The execution links below open complete walkthroughs in this book. Read each recorded instruction, variable change, and board or text output in order.',
     'Los enlaces de ejecución abren recorridos completos dentro de este libro. Lee en orden cada instrucción registrada, cada cambio de variable y cada resultado en el tablero o en el texto.',
     '実行リンクから、この本に収録された実行の全過程へ移動できます。記録された命令、変数の変化、盤面やテキストの出力を順番に読んでください。'),
    (('After each program, compare its initial and final boards, then open the full execution link.', 'Después de cada programa, compara', '各プログラムの'),
     'After each program, compare its initial and final boards, then read the complete execution walkthrough. The numbered instructions match the program cards. The turtle picture hides an egg directly underneath it; the egg count still includes that egg.',
     'Después de cada programa, compara los tableros inicial y final y lee el recorrido completo de ejecución. Las instrucciones numeradas corresponden a las tarjetas del programa. La imagen de la tortuga oculta el huevo que esté justo debajo, pero el recuento de huevos lo incluye.',
     '各プログラムの最初と最後の盤面を比べてから、実行の全過程を読んでください。命令の番号はプログラムのカードに対応しています。亀の真下にある卵は絵に隠れますが、卵の数には含まれます。'),
    (('Read the numbered TLAC cards first, then use the debugger below.', 'Lee primero las tarjetas TLAC numeradas', 'まず番号付きのTLACカードを読み'),
     'Read the numbered TLAC cards first, then follow the execution walkthrough. Skip a function’s enclosed cards until it is called; after returning, continue at the call site. The right-to-left search function is defined by the original program but is not called in this run.',
     'Lee primero las tarjetas TLAC numeradas y sigue después el recorrido de ejecución. Salta las tarjetas internas de una función hasta que se llame; al volver, continúa desde la llamada. La función de búsqueda de derecha a izquierda está definida en el programa original, pero no se llama en esta ejecución.',
     'まず番号付きのTLACカードを読み、実行の全過程を追ってください。関数の中は呼び出されるまで飛ばし、戻ったら呼び出し元から続けます。右から左へ探す関数は元のプログラムで定義されていますが、この実行では呼び出されません。'),
    (('Read the numbered cards, then try Next below.', 'Lee las tarjetas numeradas y prueba Siguiente abajo.', '番号付きカードを読み、下の「次へ」を試してください。'),
     'Read the numbered cards, then follow the execution walkthrough. Function definitions describe reusable instructions: their bodies run only when called. The loop runs its body before checking its stop condition: no means continue, yes means stop.',
     'Lee las tarjetas numeradas y sigue después el recorrido de ejecución. Las definiciones de funciones describen instrucciones reutilizables: solo se ejecutan al llamarlas. El bucle ejecuta su cuerpo antes de comprobar la condición de parada: no significa continuar y sí significa terminar.',
     '番号付きカードを読んで、実行の全過程を追ってください。関数の中の命令は呼び出されたときに実行されます。この繰り返しは動作を実行してから終了条件を調べます。「いいえ」なら続け、「はい」なら終了します。'),
]
for _, en, es, ja in OFFLINE:
    add(en, es, ja)

PATTERNS = [
    (r'Eggs on the board: (\d+)', 'Huevos en el tablero: {0}', '盤面の卵の数：{0}'),
    (r'Board at step (\d+)', 'Tablero en el paso {0}', 'ステップ{0}の盤面'),
    (r'Every step: (.+)', 'Todos los pasos: {0}', '全ステップ：{0}'),
    (r'(.+): steps (\d+)–(\d+)', '{0}: pasos {1}–{2}', '{0}：ステップ{1}〜{2}'),
    (r'(.+) — all (\d+) steps', '{0} — los {1} pasos', '{0} — 全{1}ステップ'),
    (r'Step (\d+): (.+)', 'Paso {0}: {1}', 'ステップ{0}：{1}'),
    (r'Instruction (\d+) · Function call depth: (\d+)', 'Instrucción {0} · Profundidad de llamadas a funciones: {1}', '命令{0}・関数呼び出しの深さ：{1}'),
    (r'(\d+) recorded steps follow here, in order\. Each step repeats the full current state and output, including unchanged values\.',
     'A continuación aparecen {0} pasos registrados, en orden. Cada paso repite todo el estado actual y la salida, incluidos los valores que no han cambiado.',
     '以下に、記録した{0}ステップを順番に掲載します。各ステップでは、変化のない値も含めて、その時点の状態と出力をすべて繰り返し表示します。'),
    (r'Before: (.+)', 'Antes: {0}', '実行前：{0}'),
    (r'After: (.+)', 'Después: {0}', '実行後：{0}'),
    (r'Return from (.+)', 'Retorno de {0}', '{0}から戻る'),
    (r'Player input: (.+)', 'Entrada del jugador: {0}', 'プレイヤーの入力：{0}'),
    (r'End of sample: (.+)', 'Fin de la sesión de ejemplo: {0}', 'サンプル終了：{0}'),
]


def translate(text, language):
    if language == 'en':
        return text
    if text in WORDS:
        return WORDS[text][language]
    stripped = text.strip()
    if stripped in WORDS:
        return text[:len(text) - len(text.lstrip())] + WORDS[stripped][language] + text[len(text.rstrip()):]
    for pattern, es, ja in PATTERNS:
        match = re.fullmatch(pattern, stripped, re.S)
        if match:
            return (es if language == 'es' else ja).format(*(translate(group, language) for group in match.groups()))
    if re.fullmatch(r'.+: X=-?\d+, Y=-?\d+, facing (up|down|left|right)(; .+)*', stripped):
        def turtle(match):
            name, x, y, direction = match.groups()
            name, direction = translate(name, language), translate(direction, language)
            return (f'{name}: X={x}, Y={y}, mirando {direction}' if language == 'es'
                    else f'{name}：X={x}、Y={y}、向き：{direction}')
        return re.sub(r'([^;]+): X=(-?\d+), Y=(-?\d+), facing (up|down|left|right)', turtle, stripped)
    return text


def game_note(language, filename, controls, ended, legend):
    ended, legend = translate(ended, language), translate(legend, language)
    if language == 'es':
        return (f'Esta es una sesión de ejemplo reproducible del programa original {filename}; no representa todas las partidas posibles. '
                f'Entradas del jugador: {controls}. Semilla aleatoria: 7. Se registran todos los pasos ejecutados, incluidos los bucles de preparación. '
                f'{ended} {legend} La salida de texto original también se repite en cada paso. '
                'Las tarjetas que corresponden a una misma línea del código Python se muestran juntas en la etiqueta del paso.')
    if language == 'ja':
        return (f'これは変更を加えていない{filename}の、再現可能なサンプルプレイ1回分です。すべての遊び方を示すものではありません。'
                f'プレイヤーの入力：{controls}。乱数シード：7。準備の繰り返しを含め、実行したすべての命令ステップを記録しています。'
                f'{ended} {legend} 各ステップでは元のテキスト出力も繰り返し表示します。'
                'Pythonソースの同じ行に対応するカードは、ステップの説明にまとめて表示します。')
    return (f'This is one reproducible sample of the unmodified {filename} program, not every possible playthrough. '
            f'Player inputs: {controls}. Random seed: 7. All executed instruction steps, including setup loops, are recorded. '
            f'{ended} {legend} The original text output is also repeated at every step. '
            'Cards written on the same Python source line are shown together in the step label.')


def localize_document(document, language):
    document.html['lang'] = language
    if language == 'en':
        return
    for paragraph in document.select('p'):
        text = paragraph.get_text(' ', strip=True)
        for starts, en, es, ja in OFFLINE:
            if any(text.startswith(start) for start in starts):
                paragraph.string = es if language == 'es' else ja
                break
    for node in list(document.find_all(string=True)):
        # Source appendices, license, original output and variable values are
        # documentary data. Only the explicit empty-state messages are localized.
        pre = node.find_parent('pre')
        if pre or node.find_parent(['code', 'script', 'style']):
            if pre and node.strip() in ('No watched variables.', '(No text output at this step.)'):
                node.replace_with(NavigableString(translate(str(node), language)))
            continue
        translated = translate(str(node), language)
        if translated != str(node):
            node.replace_with(NavigableString(translated))
    for tag in document.select('[alt], [title]'):
        for attr in ('alt', 'title'):
            if attr in tag.attrs:
                tag[attr] = translate(tag[attr], language)
