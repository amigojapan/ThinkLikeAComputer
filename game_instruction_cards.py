"""Translate the game ASTs into numbered, nested TLAC instruction cards.

Unsupported syntax raises an error instead of silently omitting instructions.
Python game files are parsed, never executed or changed.
"""
import ast
from html import escape
import re

LANGS = ('en', 'es', 'ja')


def words(en, es, ja):
    return dict(zip(LANGS, (en, es, ja)))


FUNCTIONS = {
    'spawn_food': words('Place new food', 'Colocar comida nueva', '新しいエサを置く'),
    'init_game': words('Prepare the snake', 'Preparar la serpiente', 'ヘビを準備する'),
    'syncEntitiesForRender': words('Prepare moving pieces for display', 'Preparar las piezas móviles para mostrar', '動くコマの表示を準備する'),
    'executePlayerInput': words('Read and apply a player command', 'Leer y aplicar una orden del jugador', 'プレイヤーの指示を読み取って実行する'),
    'updateSnakeLogic': words('Advance the snake', 'Avanzar la serpiente', 'ヘビを進める'),
    'playSnakeInteractive': words('Play Snake', 'Jugar a Snake', 'スネークを進行する'),
    'areThereCollectiblesLeft': words('Check for remaining collectibles', 'Comprobar si quedan objetos', '集める物が残っているか調べる'),
    'getValidGhostMoves': words('Find allowed ghost moves', 'Buscar movimientos permitidos del fantasma', 'ゴーストが進める移動を調べる'),
    'checkCollisions': words('Handle ghost collisions', 'Resolver colisiones con fantasmas', 'ゴーストとの衝突を処理する'),
    'runGhostPlayerTurn': words('Take the ghosts’ turn', 'Realizar el turno de los fantasmas', 'ゴーストのターンを進める'),
    'playPacManInteractive': words('Play Pac-Man', 'Jugar a Pac-Man', 'パックマンを進行する'),
    'load_level': words('Load the level', 'Cargar el nivel', 'ステージを読み込む'),
    'check_win': words('Check whether the game is won', 'Comprobar si se ha ganado', 'クリアしたか調べる'),
    'playSokoban': words('Play Sokoban', 'Jugar a Sokoban', '倉庫番を進行する'),
    'place_mines_and_calculate': words('Place mines and count neighbors', 'Colocar minas y contar vecinas', '地雷を置いて周囲の地雷を数える'),
    'print_ms_board': words('Display the Minesweeper board', 'Mostrar el tablero de Buscaminas', 'マインスイーパーの盤面を表示する'),
    'reveal_cell': words('Reveal a cell', 'Descubrir una casilla', 'マスを開く'),
    'executeMSInput': words('Read a Minesweeper command', 'Leer una orden de Buscaminas', 'マインスイーパーの指示を読み取る'),
    'play_minesweeper': words('Play Minesweeper', 'Jugar a Buscaminas', 'マインスイーパーを進行する'),
    'init_level': words('Prepare the level', 'Preparar el nivel', 'ステージを準備する'),
    'spawn_traffic': words('Place the traffic', 'Colocar el tráfico', '車を配置する'),
    'reset_player': words('Return the player to the start', 'Devolver al jugador al inicio', 'プレイヤーを開始位置に戻す'),
    'move_traffic': words('Advance the traffic', 'Avanzar el tráfico', '車を進める'),
    'check_collisions': words('Check for a traffic collision', 'Comprobar colisiones con el tráfico', '車との衝突を調べる'),
    'playFrogger': words('Play Frogger', 'Jugar a Frogger', 'フロッガーを進行する'),
    'process_explosions': words('Update bombs and explosions', 'Actualizar bombas y explosiones', '爆弾の時間と爆発を処理する'),
    'move_enemies': words('Move the enemies', 'Mover los enemigos', '敵を動かす'),
    'playBomberman': words('Play Bomberman', 'Jugar a Bomberman', 'ボンバーマンを進行する'),
    'seed_board': words('Create the starting population', 'Crear la población inicial', '最初の細胞の集団を作る'),
    'calculate_next_generation': words('Calculate the next generation', 'Calcular la siguiente generación', '次の世代を計算する'),
    'print_life_board': words('Display the Life board', 'Mostrar el tablero de la vida', 'ライフゲームの盤面を表示する'),
    'play_life': words('Run the Game of Life', 'Ejecutar el juego de la vida', 'ライフゲームを進行する'),
}

NAMES = {
    'W': words('board width', 'ancho del tablero', '盤面の幅'),
    'H': words('board height', 'alto del tablero', '盤面の高さ'),
    'X': words('column', 'columna', '列'), 'Y': words('row', 'fila', '行'),
    'globals': words('game state', 'estado del juego', 'ゲームの状態'),
    'slots': words('board cells', 'casillas del tablero', '盤面のマス'),
    'turtle': words('player', 'jugador', 'プレイヤー'),
    'ghosts': words('moving pieces', 'piezas móviles', '動くコマ'),
    'score': words('score', 'puntuación', '得点'),
    'playing': words('game continues', 'el juego continúa', 'ゲームを続ける'),
    'snake_body': words('snake body', 'cuerpo de la serpiente', 'ヘビの体'),
    'food': words('food position', 'posición de la comida', 'エサの位置'),
    'dx': words('horizontal change', 'cambio horizontal', '横の変化量'),
    'dy': words('vertical change', 'cambio vertical', '縦の変化量'),
    'direction': words('facing direction', 'dirección de orientación', '向き'),
    'lives': words('remaining lives', 'vidas restantes', '残りライフ'),
    'powerModeCounter': words('power counter', 'contador de poder', 'パワーのカウンター'),
    'containsEgg': words('contains an egg', 'contiene un huevo', '卵がある'),
    'diamond': words('contains a diamond', 'contiene un diamante', 'ダイヤがある'),
    'wall': words('is a wall', 'es una pared', '壁である'),
    'goal': words('is a goal', 'es una meta', 'ゴールである'),
    'char': words('display symbol', 'símbolo visible', '表示記号'),
    'boxes': words('box positions', 'posiciones de las cajas', '箱の位置のリスト'),
    'moves': words('move count', 'número de movimientos', '移動回数'),
    'cars': words('traffic', 'tráfico', '車のリスト'),
    'bombs': words('bombs', 'bombas', '爆弾のリスト'),
    'enemies': words('enemies', 'enemigos', '敵のリスト'),
    'is_alive': words('is alive', 'está viva', '生きている'),
    'next_alive': words('will be alive next generation', 'estará viva en la siguiente generación', '次の世代で生きる'),
    'is_mine': words('contains a mine', 'contiene una mina', '地雷がある'),
    'revealed': words('is revealed', 'está descubierta', '開いている'),
    'flagged': words('has a flag', 'tiene bandera', '旗がある'),
    'neighbor_mines': words('neighboring mine count', 'número de minas vecinas', '周囲の地雷数'),
    'NUM_MINES': words('number of mines', 'número de minas', '地雷の個数'),
    'fill_probability': words('starting life probability', 'probabilidad inicial de vida', '最初に生きる確率'),
    'valid_moves': words('allowed moves', 'movimientos permitidos', '進める移動のリスト'),
    'best_move': words('chosen move', 'movimiento elegido', '選んだ移動'),
    'game_state': words('game result', 'resultado del juego', 'ゲームの結果'),
    'generation': words('generation number', 'número de generación', '世代番号'),
    'alive_neighbors': words('live neighbor count', 'número de vecinas vivas', '生きた隣の細胞の数'),
    'slot': words('current cell', 'casilla actual', '現在のマス'),
    'ghost': words('current ghost', 'fantasma actual', '現在のゴースト'),
    'car': words('current vehicle', 'vehículo actual', '現在の車'),
    'move': words('player command', 'orden del jugador', 'プレイヤーの指示'),
    'valid_move': words('move is accepted', 'movimiento aceptado', '移動を受け付けた'),
    'valid_input': words('command is accepted', 'orden aceptada', '指示を受け付けた'),
    'level_1': words('level layout', 'diseño del nivel', 'ステージの配置'),
    'board_str': words('board display text', 'texto del tablero', '盤面の表示文'),
    'layout': words('layout', 'diseño', '配置'),
    'blast_zones': words('blast offsets', 'desplazamientos de la explosión', '爆風の相対位置'),
}

DOCSTRINGS = {
    'Randomly distributes mines and pre-calculates neighbor numbers.': words('Place mines randomly and count neighboring mines.', 'Colocar minas al azar y contar las minas vecinas.', '地雷をランダムに配置し、周囲の地雷数を数えます。'),
    "A custom renderer that overrides TLAC's native graphics to show numbers.": words('Draw this game’s board with numbers and flags.', 'Dibujar el tablero de este juego con números y banderas.', 'このゲームの盤面を数字と旗で表示します。'),
    'Recursive flood-fill to reveal empty spaces (TLAC has a high recursion depth).': words('Reveal connected empty spaces by calling this function again.', 'Descubrir espacios vacíos conectados llamando de nuevo a esta función.', 'この関数を再び呼び出して、つながった空きマスを開きます。'),
    'Player wins when all non-mine cells are revealed.': words('The player wins when every safe cell has been revealed.', 'El jugador gana cuando se han descubierto todas las casillas seguras.', '安全なマスを全て開くとクリアです。'),
    'Processes Turtle movement and Minesweeper actions.': words('Read movement, reveal, and flag commands.', 'Leer órdenes de movimiento, apertura y banderas.', '移動・マスを開く・旗を立てる指示を読み取ります。'),
    'Randomly populates the board with initial live cells.': words('Choose the starting live cells randomly.', 'Elegir al azar las células vivas iniciales.', '最初に生きている細胞をランダムに選びます。'),
    "Applies Conway's rules to calculate the next state of the board.": words('Apply Conway’s rules to calculate the next generation.', 'Aplicar las reglas de Conway para calcular la siguiente generación.', 'コンウェイのルールで次の世代を計算します。'),
    'A custom renderer to display the cellular automaton.': words('Draw the living and dead cells.', 'Dibujar las células vivas y muertas.', '生きている細胞と死んでいる細胞を表示します。'),
}


class Cards:
    def __init__(self, source, game_id, lang):
        self.tree = ast.parse(source)
        self.game_id = game_id
        self.lang = lang
        self.number = 0
        self.covered = set()

    def say(self, en, es, ja, **values):
        return words(en, es, ja)[self.lang].format(**values)

    def name(self, name):
        if name in NAMES:
            return NAMES[name][self.lang]
        if name in FUNCTIONS:
            return FUNCTIONS[name][self.lang]
        return re.sub(r'([a-z])([A-Z])', r'\1 \2', name).replace('_', ' ')

    def expr(self, node):
        e, s = self.expr, self.say
        if isinstance(node, ast.Name):
            return self.name(node.id)
        if isinstance(node, ast.Constant):
            if node.value is True:
                return s('yes', 'sí', 'はい')
            if node.value is False:
                return s('no', 'no', 'いいえ')
            if node.value is None:
                return s('no value', 'sin valor', '値なし')
            if isinstance(node.value, str):
                if node.value == '':
                    return s('empty text', 'texto vacío', '空の文字列')
                return '“' + node.value.replace('\n', ' ↵ ') + '”'
            return str(node.value)
        if isinstance(node, ast.Attribute):
            if ast.unparse(node) == 'TLAC.globals':
                return self.name('globals')
            if ast.unparse(node.value) in ('globals', 'TLAC.globals'):
                return self.name(node.attr)
            return s('{field} of {owner}', '{field} de {owner}', '{owner}の「{field}」', field=self.name(node.attr), owner=e(node.value))
        if isinstance(node, (ast.Tuple, ast.List)):
            if not node.elts:
                return s('an empty list', 'una lista vacía', '空のリスト')
            items = ', '.join(e(item) for item in node.elts)
            if isinstance(node, ast.Tuple):
                return '(' + items + ')'
            return s('a list containing [{items}]', 'una lista con [{items}]', '[{items}]を並べたリスト', items=items)
        if isinstance(node, ast.Dict):
            fields = ', '.join(e(key) + ': ' + e(value) for key, value in zip(node.keys, node.values))
            return s('a record with {fields}', 'un registro con {fields}', '次の項目を持つ記録：{fields}', fields=fields)
        if isinstance(node, ast.Subscript):
            if isinstance(node.slice, ast.Slice):
                sl = node.slice
                if sl.step:
                    raise ValueError('Slice step is not supported')
                if sl.lower is None and sl.upper is None:
                    return s('a copy of {items}', 'una copia de {items}', '{items}のコピー', items=e(node.value))
                if sl.lower is None and ast.unparse(sl.upper) == '-1':
                    return s('all of {items} except the last item', 'todos los elementos de {items} salvo el último', '{items}の末尾以外の全要素', items=e(node.value))
                if ast.unparse(sl.lower) == '1' and sl.upper is None:
                    return s('all of {items} except the first item', 'todos los elementos de {items} salvo el primero', '{items}の先頭以外の全要素', items=e(node.value))
                raise ValueError(ast.dump(node))
            return s('item {index} in {items}', 'elemento {index} de {items}', '{items}の項目{index}', index=e(node.slice), items=e(node.value))
        if isinstance(node, ast.BinOp):
            symbols = {ast.Add: '+', ast.Sub: '−', ast.Mult: '×', ast.Div: '÷', ast.FloorDiv: '÷', ast.Mod: '%'}
            if isinstance(node.op, ast.Mod):
                return s('remainder of ({left} ÷ {right})', 'resto de ({left} ÷ {right})', '({left} ÷ {right})の余り', left=e(node.left), right=e(node.right))
            return f'({e(node.left)} {symbols[type(node.op)]} {e(node.right)})'
        if isinstance(node, ast.UnaryOp):
            if isinstance(node.op, ast.Not):
                return s('not ({value})', 'no ({value})', '（{value}）ではない', value=e(node.operand))
            if isinstance(node.op, ast.USub):
                return '−' + e(node.operand)
        if isinstance(node, ast.BoolOp):
            join = s(' and ', ' y ', ' かつ ') if isinstance(node.op, ast.And) else s(' or ', ' o ', ' または ')
            return join.join('(' + e(value) + ')' for value in node.values)
        if isinstance(node, ast.Compare):
            phrases = {
                ast.Eq: words('{a} equals {b}', '{a} es igual a {b}', '{a}が{b}に等しい'),
                ast.NotEq: words('{a} differs from {b}', '{a} es distinto de {b}', '{a}が{b}と異なる'),
                ast.Lt: words('{a} is less than {b}', '{a} es menor que {b}', '{a}が{b}より小さい'),
                ast.LtE: words('{a} is at most {b}', '{a} es como máximo {b}', '{a}が{b}以下'),
                ast.Gt: words('{a} is greater than {b}', '{a} es mayor que {b}', '{a}が{b}より大きい'),
                ast.GtE: words('{a} is at least {b}', '{a} es como mínimo {b}', '{a}が{b}以上'),
                ast.In: words('{a} is in {b}', '{a} está en {b}', '{a}が{b}に含まれる'),
                ast.NotIn: words('{a} is not in {b}', '{a} no está en {b}', '{a}が{b}に含まれない'),
            }
            left, comparisons = node.left, []
            for op, right in zip(node.ops, node.comparators):
                comparisons.append(phrases[type(op)][self.lang].format(a=e(left), b=e(right)))
                left = right
            return s(' and ', ' y ', ' かつ ').join(comparisons)
        if isinstance(node, ast.JoinedStr):
            return '“' + ''.join(part.value.replace('\n', ' ↵ ') if isinstance(part, ast.Constant) else '{' + e(part.value) + '}' for part in node.values) + '”'
        if isinstance(node, ast.Lambda):
            return s('for each {item}, use {value}', 'para cada {item}, usar {value}', '各{item}について{value}を使う', item=', '.join(self.name(a.arg) for a in node.args.args), value=e(node.body))
        if isinstance(node, (ast.ListComp, ast.GeneratorExp)):
            if len(node.generators) != 1:
                raise ValueError('Multiple comprehension loops')
            loop = node.generators[0]
            if loop.ifs or loop.is_async:
                raise ValueError('Unsupported comprehension condition')
            return s('the list of {value} for each {item} in {items}', 'la lista de {value} para cada {item} en {items}', '{items}の各{item}について{value}を並べたリスト', value=e(node.elt), item=e(loop.target), items=e(loop.iter))
        if isinstance(node, ast.Call):
            return self.call(node)
        raise ValueError('Unsupported expression: ' + ast.dump(node))

    def call(self, node, as_value=True):
        e, s = self.expr, self.say
        name = ast.unparse(node.func)
        args = [e(a) for a in node.args]
        if name in FUNCTIONS:
            # The shared state is implicit in the board-game instructions.
            visible = [e(a) for a in node.args if ast.unparse(a) not in ('globals', 'TLAC.globals')]
            label = FUNCTIONS[name][self.lang]
            prefix = s('the result of calling “{name}”', 'el resultado de llamar a «{name}»', '「{name}」を呼び出した結果', name=label) if as_value else s('Call “{name}”', 'Llamar a «{name}»', '「{name}」を呼び出す', name=label)
            return prefix + (s(' with {args}', ' con {args}', '（入力：{args}）', args=', '.join(visible)) if visible else '')
        if name == 'range':
            start, stop = ('0', args[0]) if len(args) == 1 else args[:2]
            return s('whole numbers from {start} up to, but not including, {stop}', 'enteros desde {start} hasta {stop}, sin incluirlo', '{start}から{stop}の直前までの整数', start=start, stop=stop)
        if name == 'len':
            return s('number of items in {items}', 'cantidad de elementos de {items}', '{items}の要素数', items=args[0])
        if name == 'enumerate':
            return s('each position and item in {items}, starting at position 0', 'cada posición y elemento de {items}, empezando en 0', '{items}の各位置と要素（位置は0から）', items=args[0])
        if name == 'abs':
            return s('absolute value of {value}', 'valor absoluto de {value}', '{value}の絶対値', value=args[0])
        if name == 'str':
            return s('{value} written as text', '{value} escrito como texto', '{value}を文字列にする', value=args[0])
        if name == 'any':
            return s('at least one result is yes in {items}', 'al menos un resultado es sí en {items}', '{items}の少なくとも1つの結果が「はい」', items=args[0])
        if name in ('max', 'min'):
            key = next(k.value for k in node.keywords if k.arg == 'key')
            return s('the item in {items} with the {which} value: {rule}', 'el elemento de {items} con el valor {which}: {rule}', '{items}のうち、次の値が{which}になる要素：{rule}', items=args[0], which=s('largest', 'máximo', '最大') if name == 'max' else s('smallest', 'mínimo', '最小'), rule=e(key))
        if name == 'random.randint':
            return s('a random whole number from {a} through {b}, inclusive', 'un entero al azar entre {a} y {b}, incluidos', '{a}から{b}までのランダムな整数（両端を含む）', a=args[0], b=args[1])
        if name == 'random.random':
            return s('a random number from 0 up to, but not including, 1', 'un número aleatorio desde 0 hasta 1, sin incluir 1', '0以上1未満のランダムな数')
        if name == 'random.choice':
            return s('a randomly chosen item from {items}', 'un elemento elegido al azar de {items}', '{items}からランダムに選んだ要素', items=args[0])
        if name == 'input':
            return s('the player’s answer after asking {prompt}', 'la respuesta del jugador tras preguntar {prompt}', '{prompt}と尋ねた後のプレイヤーの入力', prompt=args[0])
        if name == 'print':
            return s('Display {value}', 'Mostrar {value}', '{value}を表示する', value=' + '.join(args))
        if name == 'exit':
            return s('End the program', 'Terminar el programa', 'プログラムを終了する')
        if name == 'time.sleep':
            return s('Wait {time} seconds', 'Esperar {time} segundos', '{time}秒待つ', time=args[0])
        simulator = {
            'initSlots': words('Create empty board cells', 'Crear casillas vacías', '空の盤面のマスを作る'),
            'readBoardFromFile': words('Load the board from {0}', 'Cargar el tablero desde {0}', '{0}から盤面を読み込む'),
            'teleportTurtleTo': words('Place the player at column {0}, row {1}', 'Colocar al jugador en columna {0}, fila {1}', 'プレイヤーを列{0}・行{1}へ置く'),
            'setInitialTurtlePositionTo': words('Set the player’s starting position to column {0}, row {1}', 'Fijar el inicio del jugador en columna {0}, fila {1}', 'プレイヤーの開始位置を列{0}・行{1}にする'),
            'addGhost': words('Add a moving piece with symbol {0} at column {1}, row {2}', 'Añadir una pieza móvil con símbolo {0} en columna {1}, fila {2}', '記号{0}の動くコマを列{1}・行{2}に追加する'),
            'printBoard': words('Display the saved board picture', 'Mostrar la imagen guardada del tablero', '保存された盤面の表示を出す'),
            'updateBoard': words('Redraw the board from its current pieces', 'Volver a dibujar el tablero con sus piezas actuales', '現在のコマから盤面を描き直す'),
            'testIfICanProceed': words('the player can move forward {0} square(s)', 'el jugador puede avanzar {0} casilla(s)', 'プレイヤーが前に{0}マス進める'),
            'fd': words('Move the player forward {0} square(s)', 'Avanzar al jugador {0} casilla(s)', 'プレイヤーを前に{0}マス進める'),
            'amILayingOnAnEgg': words('the player stands on an egg', 'el jugador está sobre un huevo', 'プレイヤーが卵の上にいる'),
            'amILayingOnADiamond': words('the player stands on a diamond', 'el jugador está sobre un diamante', 'プレイヤーがダイヤの上にいる'),
            'eatEgg': words('Remove the egg under the player', 'Quitar el huevo bajo el jugador', 'プレイヤーの下の卵を取り除く'),
            'eatDiamond': words('Remove the diamond under the player', 'Quitar el diamante bajo el jugador', 'プレイヤーの下のダイヤを取り除く'),
        }
        if isinstance(node.func, ast.Attribute):
            method = node.func.attr
            if name.startswith('TLAC.') and method in simulator:
                return simulator[method][self.lang].format(*args[1:])
            owner = e(node.func.value)
            if method == 'strip':
                return s('{value}, with surrounding spaces removed', '{value}, sin espacios al principio ni al final', '{value}の前後の空白を取り除く', value=owner)
            if method == 'upper':
                return s('{value}, converted to uppercase', '{value}, convertido a mayúsculas', '{value}を大文字にする', value=owner)
            if method == 'append':
                return s('Add {value} to the end of {items}', 'Añadir {value} al final de {items}', '{items}の末尾に{value}を追加する', value=args[0], items=owner)
            if method == 'insert':
                return s('Insert {value} at position {index} in {items}', 'Insertar {value} en la posición {index} de {items}', '{items}の位置{index}に{value}を挿入する', value=args[1], index=args[0], items=owner)
            if method == 'pop':
                return s('Remove the last item from {items}', 'Quitar el último elemento de {items}', '{items}の末尾の要素を取り除く', items=owner)
            if method == 'remove':
                return s('Remove {value} from {items}', 'Quitar {value} de {items}', '{items}から{value}を取り除く', value=args[0], items=owner)
            if method == 'index':
                return s('the position of {value} in {items}', 'la posición de {value} en {items}', '{items}の中での{value}の位置', value=args[0], items=owner)
        raise ValueError('Unsupported call: ' + ast.dump(node))

    def card(self, text, node=None, kind='action', anchor=''):
        self.number += 1
        if node is not None:
            self.covered.add(id(node))
        attr = f' id="{escape(anchor)}"' if anchor else ''
        line = f' data-source-line="{node.lineno}"' if node is not None else ''
        return f'<div class="instruction-card {kind}"{attr}{line}><span class="instruction-number">{self.number:04}</span><span>{escape(text)}</span></div>'

    def body(self, nodes):
        return ''.join(self.statement(node) for node in nodes)

    def block(self, label, node, body, kind='control', anchor=''):
        return '<div class="instruction-block">' + self.card(label, node, kind, anchor) + '<div class="nested-instructions">' + self.body(body) + '</div></div>'

    def statement(self, node):
        e, s, c = self.expr, self.say, self.card
        if isinstance(node, ast.Import):
            libraries = {'TLACsimulator': s('the TLAC board simulator', 'el simulador de tablero TLAC', 'TLACの盤面シミュレーター'), 'random': s('random choices', 'elecciones al azar', 'ランダムな選択'), 'time': s('timed pauses', 'pausas temporizadas', '時間を指定した待機')}
            return c(s('Prepare {tools}', 'Preparar {tools}', '{tools}を準備する', tools=', '.join(libraries[a.name] for a in node.names)), node, 'comment')
        if isinstance(node, ast.FunctionDef):
            defaults = [None] * (len(node.args.args) - len(node.args.defaults)) + list(node.args.defaults)
            params = []
            for param, default in zip(node.args.args, defaults):
                if param.arg == 'globals':
                    continue
                label = self.name(param.arg)
                if default is not None:
                    label += s(' (default: {value})', ' (por defecto: {value})', '（省略時：{value}）', value=e(default))
                params.append(label)
            label = s('Define function: {name}', 'Definir función: {name}', '関数を定義する：{name}', name=self.name(node.name))
            if params:
                label += s(' · Inputs: {params}', ' · Entradas: {params}', ' · 入力：{params}', params=', '.join(params))
            label += s(' · Run these cards only when called.', ' · Ejecutar estas tarjetas solo al llamar a la función.', ' · 呼び出されたときにだけ中のカードを実行します。')
            return self.block(label, node, node.body, 'function', self.game_id + '-function-' + node.name + '-' + self.lang)
        if isinstance(node, ast.Assign):
            return c(s('Set {target} to {value}', 'Poner {target} en {value}', '{target}を{value}にする', target=', '.join(e(target) for target in node.targets), value=e(node.value)), node)
        if isinstance(node, ast.AugAssign):
            return c(s('Update {target}: {value}', 'Actualizar {target}: {value}', '{target}を更新する：{value}', target=e(node.target), value=e(ast.BinOp(left=node.target, op=node.op, right=node.value))), node)
        if isinstance(node, ast.Expr):
            if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
                return c(DOCSTRINGS[node.value.value][self.lang], node, 'comment')
            # min(...) in Pac-Man is evaluated but its result is not assigned.
            if isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Name) and node.value.func.id in ('min', 'max'):
                return c(s('Calculate {value}; leave the stored values unchanged', 'Calcular {value}; dejar los valores guardados sin cambios', '{value}を計算する。保存済みの値は変更しない', value=e(node.value)), node)
            return c(self.call(node.value, as_value=False) if isinstance(node.value, ast.Call) else e(node.value), node)
        if isinstance(node, ast.If):
            direct_run = isinstance(node.test, ast.Compare) and ast.unparse(node.test) == "__name__ == '__main__'"
            label = s('When this game program is started directly', 'Cuando se inicia este programa directamente', 'このゲームのプログラムを直接起動したとき') if direct_run else s('If {test}, then', 'Si {test}, entonces', 'もし{test}なら', test=e(node.test))
            result = self.block(label, node, node.body)
            if node.orelse:
                result += self.block(s('Otherwise', 'En caso contrario', 'そうでなければ'), None, node.orelse)
            return result
        if isinstance(node, ast.For):
            if node.orelse:
                raise ValueError('For-else not supported')
            return self.block(s('For each {item} in {items}, repeat', 'Para cada {item} en {items}, repetir', '{items}の各{item}について繰り返す', item=e(node.target), items=e(node.iter)), node, node.body)
        if isinstance(node, ast.While):
            if node.orelse:
                raise ValueError('While-else not supported')
            label = s('Repeat until an instruction leaves this loop', 'Repetir hasta que una instrucción salga de este bucle', '中の命令で抜けるまで繰り返す') if isinstance(node.test, ast.Constant) and node.test.value is True else s('While {test}, repeat', 'Mientras {test}, repetir', '{test}の間、繰り返す', test=e(node.test))
            return self.block(label, node, node.body)
        if isinstance(node, ast.Return):
            return c(s('Return to the caller', 'Volver a quien llamó a la función', '呼び出し元に戻る') + (s(' with result: {result}', ' con el resultado: {result}', '（結果：{result}）', result=e(node.value)) if node.value else ''), node)
        if isinstance(node, ast.Break):
            return c(s('Leave the innermost loop', 'Salir del bucle más interno', '一番内側の繰り返しを抜ける'), node)
        if isinstance(node, ast.Continue):
            return c(s('Skip to the next turn of the innermost loop', 'Pasar a la siguiente vuelta del bucle más interno', '一番内側の繰り返しの次の回へ進む'), node)
        if isinstance(node, ast.Try):
            if node.orelse or node.finalbody:
                raise ValueError('Unsupported try variant')
            result = self.block(s('Run these instructions; allow the player to interrupt', 'Ejecutar estas instrucciones; permitir que el jugador interrumpa', '次の命令を実行する。プレイヤーによる中断を受け付ける'), node, node.body)
            for handler in node.handlers:
                if ast.unparse(handler.type) != 'KeyboardInterrupt':
                    raise ValueError('Unsupported handler')
                result += self.block(s('If the player presses Ctrl+C', 'Si el jugador pulsa Ctrl+C', 'プレイヤーがCtrl+Cを押したら'), None, handler.body)
            return result
        raise ValueError('Unsupported statement: ' + ast.dump(node))

    def render(self):
        chart = self.body(self.tree.body)
        expected = {id(n) for n in ast.walk(self.tree) if isinstance(n, ast.stmt)}
        if self.covered != expected:
            raise ValueError('Not all source statements were rendered')
        return chart, self.number


def game_cards(source, game_id, lang):
    return Cards(source, game_id, lang).render()
