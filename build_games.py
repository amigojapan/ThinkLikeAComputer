#!/usr/bin/env python3
"""Build the offline game-program collection: python3 build_games.py.

Reads the game sources as text; never imports or executes the interactive games.
The generated document contains the full programs as plain-language TLAC cards.
"""
import ast
from html import escape
from pathlib import Path
from game_instruction_cards import FUNCTIONS, game_cards

ROOT = Path(__file__).resolve().parent
LANGS = ('en', 'es', 'ja')


def t(en, es, ja):
    return dict(zip(LANGS, (en, es, ja)))


GAMES = [
    dict(id='snake', title=t('Snake', 'Snake', 'スネーク'), file='snakerulebook.py', board='15 × 15', assets=['snakefield.txt'],
         description=t('Grow a snake by collecting food. Keep its head away from walls and its own body.', 'Haz crecer una serpiente recogiendo comida. Evita las paredes y su propio cuerpo.', 'エサを食べてヘビを伸ばします。壁や自分の体に頭がぶつからないように進みます。'),
         controls=t('W / A / S / D: choose direction · Q: quit. Press Enter after each command.', 'W / A / S / D: dirección · Q: salir. Pulsa Enter después de cada orden.', 'W / A / S / D：方向を選ぶ · Q：終了。入力後にEnterを押します。'),
         concepts=t('Lists · coordinates · collision checks', 'Listas · coordenadas · colisiones', 'リスト · 座標 · 衝突判定'),
         steps=[
             t('Load the board, create a four-segment snake, set the score to zero, and place food outside its body.', 'Cargar el tablero, crear una serpiente de cuatro segmentos, poner la puntuación a cero y colocar comida fuera del cuerpo.', '盤面を読み込み、長さ4のヘビを作り、得点を0にして、体と重ならない場所にエサを置きます。'),
             t('Draw the snake and food, then read a direction. Prevent a direct reversal into the body.', 'Dibujar la serpiente y la comida; leer una dirección. Impedir que gire directamente hacia su cuerpo.', 'ヘビとエサを表示して方向を入力します。体に向かって180度反転することはできません。'),
             t('Calculate the next head position. End the game if it hits a wall or the checked body segments.', 'Calcular la siguiente posición de la cabeza. Terminar si choca con una pared o con los segmentos comprobados.', '頭の次の位置を計算します。壁や判定対象の体にぶつかったら終了します。'),
             t('Insert the new head at the front of the list. If it eats food, add 10 points and place new food; otherwise remove the tail.', 'Insertar la cabeza al inicio de la lista. Si come, sumar 10 puntos y colocar comida nueva; si no, quitar la cola.', 'リストの先頭に新しい頭を追加します。エサを食べたら10点を加えて新しいエサを置き、食べなければ末尾を取り除きます。'),
             t('Repeat until a collision or Q ends the game, then print the final score.', 'Repetir hasta una colisión o hasta pulsar Q; mostrar la puntuación final.', '衝突するかQを入力するまで繰り返し、最後に得点を表示します。'),
         ]),
    dict(id='pacman', title=t('Pac-Man', 'Pac-Man', 'パックマン'), file='pacmanrulebook.py', board='19 × 14', assets=['pacman-board1.txt'],
         description=t('Collect eggs and diamonds while sharing a maze with two ghosts. Diamonds give temporary power.', 'Recoge huevos y diamantes en un laberinto con dos fantasmas. Los diamantes dan poder temporal.', '2匹のゴーストがいる迷路で卵とダイヤを集めます。ダイヤを取ると一時的にパワーアップします。'),
         controls=t('W / A / S / D, then Enter: move. Ctrl+C: stop the program.', 'W / A / S / D y Enter: moverse. Ctrl+C: detener el programa.', 'W / A / S / Dを入力してEnter：移動。Ctrl+C：プログラムを停止。'),
         concepts=t('Game state · timers · lists · conditions', 'Estado del juego · temporizadores · listas · condiciones', 'ゲームの状態 · タイマー · リスト · 条件分岐'),
         steps=[
             t('Load the maze, place the player and two ghosts, and start with three lives and zero points.', 'Cargar el laberinto, colocar al jugador y dos fantasmas; empezar con tres vidas y cero puntos.', '迷路を読み込み、プレイヤーと2匹のゴーストを配置し、残り3ライフ・0点で始めます。'),
             t('While collectibles remain and lives are above zero, read a move until the player can enter the chosen square.', 'Mientras queden objetos y vidas, leer un movimiento hasta que el jugador pueda entrar en la casilla elegida.', '集める物とライフが残っている間、進める方向が入力されるまで移動指示を受け付けます。'),
             t('Check for a ghost collision. Without power, lose a life and return to the start; with power, earn 200 points and reset that ghost.', 'Comprobar colisiones con fantasmas. Sin poder, perder una vida y volver al inicio; con poder, ganar 200 puntos y reiniciar ese fantasma.', 'ゴーストとの衝突を確認します。通常時はライフを1つ失って開始位置へ戻り、パワー中は200点を得てそのゴーストを戻します。'),
             t('Collect an egg for 10 points or a diamond for 50 points. A diamond sets the power counter to 10.', 'Recoger un huevo por 10 puntos o un diamante por 50. Un diamante pone el contador de poder en 10.', '卵を取ると10点、ダイヤを取ると50点です。ダイヤはパワーのカウンターを10にします。'),
             t('Decrease the power counter and move the ghosts. Powered ghosts choose a move away from the player; otherwise this source chooses random valid moves. Check collisions again.', 'Reducir el contador y mover los fantasmas. Con poder activo se alejan del jugador; en otro caso, este código elige movimientos válidos al azar. Comprobar colisiones de nuevo.', 'パワーのカウンターを減らしてゴーストを動かします。パワー中はプレイヤーから離れる移動を選び、通常時はこのソースでは進める方向をランダムに選びます。もう一度衝突を確認します。'),
             t('Repeat until all collectibles are gone or no lives remain, then print the final score.', 'Repetir hasta recoger todos los objetos o perder todas las vidas; mostrar la puntuación final.', '全て集めるかライフがなくなるまで繰り返し、得点を表示します。'),
         ]),
    dict(id='sokoban', title=t('Sokoban', 'Sokoban', '倉庫番'), file='sokobanrulebook.py', board='8 × 8', assets=[],
         description=t('Push every box onto a goal. A box can move only if the square behind it is clear.', 'Empuja cada caja hasta una meta. Solo se puede mover si la casilla detrás está libre.', '全ての箱をゴールへ押します。箱の奥のマスが空いているときだけ押せます。'),
         controls=t('W / A / S / D: move or push · Q: quit. Press Enter after each command.', 'W / A / S / D: moverse o empujar · Q: salir. Pulsa Enter tras cada orden.', 'W / A / S / D：移動・箱を押す · Q：終了。入力後にEnterを押します。'),
         concepts=t('Lists · level layouts · conditions', 'Listas · diseño de niveles · condiciones', 'リスト · ステージの配置 · 条件分岐'),
         steps=[
             t('Read the level stored in the program. Place walls, goals, boxes, and the player.', 'Leer el nivel guardado en el programa. Colocar paredes, metas, cajas y jugador.', 'プログラム内のステージを読み、壁・ゴール・箱・プレイヤーを配置します。'),
             t('Draw the board and check whether every box is on a goal. If so, show the move count and finish.', 'Dibujar el tablero y comprobar si cada caja está en una meta. Si es así, mostrar los movimientos y terminar.', '盤面を表示し、全ての箱がゴール上にあるか確認します。揃ったら移動回数を表示して終了します。'),
             t('Read a direction. Reject movement into a wall.', 'Leer una dirección. Rechazar movimientos hacia una pared.', '方向を入力します。壁に向かう移動はできません。'),
             t('If there is a box ahead, check the square beyond it. Push only when neither a wall nor another box blocks that square.', 'Si hay una caja delante, comprobar la casilla siguiente. Empujar solo si no hay una pared ni otra caja.', '前に箱がある場合は、さらに奥のマスを確認します。壁も別の箱もない場合だけ押します。'),
             t('Move the player, add one to the move count, and repeat.', 'Mover al jugador, sumar un movimiento y repetir.', 'プレイヤーを移動し、移動回数を1増やして繰り返します。'),
         ]),
    dict(id='minesweeper', title=t('Minesweeper', 'Buscaminas', 'マインスイーパー'), file='minesweeperrulebook.py', board='10 × 10', assets=[],
         description=t('Reveal every safe cell on a board with 12 hidden mines. Numbers count mines in the eight neighboring cells.', 'Descubre todas las casillas seguras en un tablero con 12 minas ocultas. Los números cuentan las minas en las ocho casillas vecinas.', '12個の地雷を避けて安全なマスを全て開きます。数字は周囲8マスの地雷の数です。'),
         controls=t('W / A / S / D: cursor · R: reveal · F: toggle flag · Q: quit. Confirm with Enter.', 'W / A / S / D: cursor · R: descubrir · F: poner o quitar bandera · Q: salir. Confirmar con Enter.', 'W / A / S / D：カーソル · R：開く · F：旗を切り替える · Q：終了。Enterで確定します。'),
         concepts=t('Recursion · neighbor counting · cell state', 'Recursión · vecinos · estado de las casillas', '再帰 · 周囲の数え上げ · マスの状態'),
         steps=[
             t('Place 12 mines at distinct random positions and count adjacent mines for every safe cell.', 'Colocar 12 minas en posiciones aleatorias distintas y contar las minas vecinas de cada casilla segura.', '異なるランダムな位置に地雷を12個置き、安全な各マスの周囲の地雷数を数えます。'),
             t('Draw covered cells, flags, revealed numbers, and the cursor. Read one command.', 'Dibujar casillas cubiertas, banderas, números descubiertos y cursor. Leer una orden.', '未開封のマス、旗、開いた数字、カーソルを表示して指示を入力します。'),
             t('Move the cursor, toggle a flag on a covered cell, or reveal an unflagged cell.', 'Mover el cursor, alternar una bandera en una casilla cubierta o descubrir una casilla sin bandera.', 'カーソルを動かす、未開封のマスの旗を切り替える、または旗のないマスを開きます。'),
             t('When a revealed cell has no neighboring mines, recursively reveal its neighbors. Already revealed or flagged cells stop that recursive branch.', 'Si una casilla descubierta no tiene minas vecinas, descubrir sus vecinas mediante recursión. Las casillas ya descubiertas o con bandera detienen esa rama.', '周囲に地雷がなければ再帰で隣のマスも開きます。既に開いたマスや旗のあるマスでは、その再帰を止めます。'),
             t('Lose if a mine is revealed. Win when every non-mine cell is revealed; flags alone do not win the game.', 'Perder al descubrir una mina. Ganar al descubrir todas las casillas sin minas; las banderas por sí solas no bastan.', '地雷を開くと負けです。地雷以外を全て開くと勝ちです。旗を立てるだけではクリアになりません。'),
         ]),
    dict(id='frogger', title=t('Frogger', 'Frogger', 'フロッガー'), file='froggerrulebook.py', board='15 × 11', assets=[],
         description=t('Cross moving traffic and reach the top row. You start with three lives.', 'Cruza el tráfico y llega a la fila superior. Empiezas con tres vidas.', '動く車を避けて最上段を目指します。最初のライフは3つです。'),
         controls=t('W / A / S / D: move · Enter alone: wait · Q: quit. Confirm commands with Enter.', 'W / A / S / D: moverse · Enter solo: esperar · Q: salir. Confirmar con Enter.', 'W / A / S / D：移動 · Enterのみ：待つ · Q：終了。指示はEnterで確定します。'),
         concepts=t('Lists of dictionaries · wrapping · collision checks', 'Listas de diccionarios · bordes cíclicos · colisiones', '辞書のリスト · 端での折り返し · 衝突判定'),
         steps=[
             t('Mark the top row as the goal, place traffic in its lanes, and start the player at the bottom.', 'Marcar la fila superior como meta, colocar el tráfico en sus carriles y al jugador abajo.', '最上段をゴールにし、車を各車線に配置して、プレイヤーを下端に置きます。'),
             t('Draw the traffic and lives, then move the player or wait.', 'Dibujar el tráfico y las vidas; mover al jugador o esperar.', '車と残りライフを表示し、プレイヤーを動かすか待機します。'),
             t('Check collisions. On a hit, remove one life, reset the player, and begin the next turn.', 'Comprobar colisiones. Si hay un choque, quitar una vida, reiniciar al jugador y comenzar el siguiente turno.', '衝突を確認します。当たったらライフを1つ減らし、開始位置に戻して次のターンへ進みます。'),
             t('Advance each vehicle by its speed and wrap it around the board edge. Check collisions again, including a fast truck passing over the player.', 'Avanzar cada vehículo según su velocidad y hacerlo reaparecer por el otro borde. Comprobar colisiones, incluidos camiones rápidos que pasan sobre el jugador.', '車を速度に応じて進め、端を越えた車は反対側へ回します。速いトラックがプレイヤーを飛び越える場合も含めて、再び衝突を確認します。'),
             t('Win upon reaching the top row after the collision checks. Otherwise repeat while lives remain.', 'Ganar al llegar arriba tras comprobar las colisiones. Si no, repetir mientras queden vidas.', '衝突判定後に最上段にいれば勝ちです。それ以外はライフが残っている間繰り返します。'),
         ]),
    dict(id='bomberman', title=t('Bomberman', 'Bomberman', 'ボンバーマン'), file='bombermanrulebook.py', board='11 × 11', assets=[],
         description=t('Place timed bombs to destroy crates and three roaming enemies. Stay clear of the cross-shaped blast.', 'Coloca bombas con temporizador para destruir cajas y tres enemigos. Evita la explosión en forma de cruz.', '時限爆弾で木箱と動く3体の敵を倒します。十字型の爆風を避けましょう。'),
         controls=t('W / A / S / D: move · B: bomb · Enter alone: wait · Q: quit. Confirm with Enter.', 'W / A / S / D: moverse · B: bomba · Enter solo: esperar · Q: salir. Confirmar con Enter.', 'W / A / S / D：移動 · B：爆弾 · Enterのみ：待つ · Q：終了。Enterで確定します。'),
         concepts=t('Timers · dictionaries · list updates', 'Temporizadores · diccionarios · cambios en listas', 'タイマー · 辞書 · リストの更新'),
         steps=[
             t('Build border walls and pillars, scatter crates, and place the player and three enemies.', 'Crear paredes y pilares, distribuir cajas y colocar al jugador y tres enemigos.', '外壁と柱を作り、木箱を散らして、プレイヤーと3体の敵を配置します。'),
             t('Draw the arena. If no enemies remain, announce a win; otherwise read a move, bomb, or wait command.', 'Dibujar la arena. Si no quedan enemigos, anunciar la victoria; si no, leer una orden de movimiento, bomba o espera.', '盤面を表示します。敵がいなければ勝ちです。そうでなければ移動・爆弾・待機を入力します。'),
             t('Reject movement into walls, crates, or bombs. A new bomb starts at 4 and immediately ticks down to 3 on this turn.', 'Impedir movimientos hacia paredes, cajas o bombas. Una bomba nueva empieza en 4 y baja inmediatamente a 3 en este turno.', '壁・木箱・爆弾のある場所には進めません。新しい爆弾は4から始まり、そのターンですぐに3になります。'),
             t('Decrease bomb timers. At zero, affect the bomb cell and its four direct neighbors, skipping walls. Remove hit crates and enemies; a blast hitting the player ends play.', 'Reducir temporizadores. Al llegar a cero, afectar la casilla de la bomba y sus cuatro vecinas directas, excepto paredes. Quitar cajas y enemigos alcanzados; si alcanza al jugador, terminar.', 'タイマーを減らし、0になったら中心と上下左右1マスに爆風を発生させます。壁は除きます。当たった木箱や敵を取り除き、プレイヤーに当たれば終了します。'),
             t('Move enemies into randomly chosen clear neighboring squares. End on a player collision; otherwise repeat.', 'Mover enemigos a casillas vecinas libres elegidas al azar. Terminar si chocan con el jugador; si no, repetir.', '敵をランダムに選んだ隣の空きマスへ動かします。プレイヤーにぶつかったら終了し、それ以外は繰り返します。'),
         ]),
    dict(id='life', title=t('Conway’s Game of Life', 'Juego de la vida de Conway', 'コンウェイのライフゲーム'), file='conwaysgameofliferulebook.py', board='15 × 15', assets=[],
         description=t('Watch a population of cells evolve. Each generation follows the same four rules, with no player movement.', 'Observa cómo evoluciona una población de células. Cada generación sigue las mismas cuatro reglas, sin mover un jugador.', '細胞の集団が変化する様子を観察します。プレイヤーを動かさず、毎世代同じ4つのルールを適用します。'),
         controls=t('Enter: next generation · A then Enter: auto-play · Ctrl+C: stop auto-play · Q then Enter: quit.', 'Enter: siguiente generación · A y Enter: automático · Ctrl+C: detener automático · Q y Enter: salir.', 'Enter：次の世代 · AとEnter：自動再生 · Ctrl+C：自動再生を停止 · QとEnter：終了。'),
         concepts=t('Nested loops · neighbor counting · simultaneous updates', 'Bucles anidados · vecinos · actualización simultánea', '入れ子の繰り返し · 周囲の数え上げ · 同時更新'),
         steps=[
             t('Seed the board randomly: each cell has a 25% chance of starting alive. Display generation zero.', 'Inicializar al azar: cada célula tiene un 25 % de probabilidad de estar viva. Mostrar la generación cero.', '各細胞が25%の確率で生きた状態になるよう初期化し、第0世代を表示します。'),
             t('For every cell, count live neighbors among the eight surrounding positions that lie inside the board.', 'Para cada célula, contar vecinas vivas entre las ocho posiciones circundantes dentro del tablero.', '各細胞について、盤面内にある周囲8マスの生きた細胞を数えます。'),
             t('A live cell dies with fewer than two neighbors or more than three. It survives with two or three.', 'Una célula viva muere con menos de dos vecinas o más de tres. Sobrevive con dos o tres.', '生きた細胞は隣が2個未満または3個より多いと死に、2個か3個なら生き残ります。'),
             t('A dead cell becomes alive with exactly three live neighbors. Otherwise it stays dead.', 'Una célula muerta nace con exactamente tres vecinas vivas. En otro caso sigue muerta.', '死んだ細胞は隣の生きた細胞がちょうど3個なら誕生し、それ以外は死んだままです。'),
             t('Store all next states before replacing the current generation. Increment the generation number and display the board.', 'Guardar todos los estados siguientes antes de sustituir la generación actual. Incrementar el número de generación y mostrar el tablero.', '全ての次の状態を計算してから現在の世代を置き換えます。世代番号を増やして盤面を表示します。'),
             t('Continue one generation per Enter, or automatically every 0.3 seconds until auto-play is interrupted.', 'Continuar una generación por Enter, o automáticamente cada 0,3 segundos hasta interrumpir la reproducción.', 'Enterごとに1世代進めるか、自動再生を止めるまで0.3秒ごとに進めます。'),
         ]),
]


def localized(words):
    return ''.join(f'<span data-lang="{lang}" lang="{lang}"{ " hidden" if lang != "en" else ""}>{escape(words[lang])}</span>' for lang in LANGS)


def heading(level, words):
    return f'<h{level}>{localized(words)}</h{level}>'


CSS = """
* { box-sizing: border-box; }
:root { color-scheme: light; }
body { margin: 0; background: powderblue; color: #102f40; font: 17px/1.65 Arial, Helvetica, sans-serif; }
.toolbar { background: #e8f7fa; border-bottom: 2px solid #6697a6; padding: 14px max(20px, calc((100% - 1080px)/2)); display: flex; align-items: center; gap: 12px; flex-wrap: wrap; }
label, summary { font-weight: bold; }
select { font: inherit; padding: 7px 12px; border: 1px solid #315b6e; border-radius: 5px; background: white; color: #102f40; max-width: 100%; }
:focus-visible { outline: 3px solid #a94700; outline-offset: 4px; }
main { max-width: 1120px; margin: auto; padding: 30px 20px 64px; }
h1 { font-size: clamp(2rem, 5vw, 3.1rem); line-height: 1.18; margin: 12px 0; }
h2 { border-bottom: 2px solid #527e8e; padding-bottom: 10px; margin: 48px 0 20px; font-size: 1.8rem; line-height: 1.35; }
h3 { font-size: 1.2rem; margin: 24px 0 12px; }
p { margin: 12px 0 18px; }
a { color: #064e79; text-underline-offset: 3px; }
a:hover { color: #802f00; }
.eyebrow { font-weight: bold; letter-spacing: .06em; }
.subtitle { font-size: 1.2rem; max-width: 850px; }
.tag { color: #376176; font-weight: bold; font-size: .9rem; }
.note { border-left: 5px solid #376b84; background: #edf8fb; padding: 16px 20px; margin: 22px 0; }
.note p { margin: 0; }
nav { margin: 28px 0; }
.cards { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 14px; list-style: none; padding: 0; }
.cards a { display: block; height: 100%; background: #edf8fb; border: 1px solid #739dab; border-radius: 8px; padding: 16px 20px; text-decoration: none; }
.cards a:hover { background: #fff3a9; }
.cards strong { font-size: 1.15rem; }
.cards small { display: block; color: #376176; margin-top: 4px; }
.cards li:last-child { grid-column: 1 / -1; }
.facts { display: grid; grid-template-columns: 1fr 1fr; gap: 18px; background: #edf8fb; border: 1px solid #739dab; border-radius: 8px; padding: 18px 22px; }
.facts p { margin: 5px 0; }
.instruction-list { list-style: none; padding: 0; counter-reset: steps; }
.instruction-list li { counter-increment: steps; position: relative; background: #fff3a9; padding: 12px 15px 12px 62px; border: 1px solid #aa933e; margin: 9px 0; border-radius: 5px; }
.instruction-list li::before { content: counter(steps, decimal-leading-zero); position: absolute; left: 14px; top: 12px; background: #173d8c; color: #fff7a3; border-radius: 3px; padding: 1px 7px; }
details { background: #eaf5f8; border: 1px solid #7197a5; border-radius: 8px; margin: 20px 0; padding: 14px 18px; min-width: 0; }
summary { cursor: pointer; overflow-wrap: anywhere; }
.instruction-chart { margin-top: 20px; }
.instruction-card { display: grid; grid-template-columns: auto minmax(0, 1fr); align-items: start; gap: 12px; padding: 10px 12px; background: #fff19a; border: 1px solid #aa933e; border-radius: 6px; margin: 8px 0; overflow-wrap: anywhere; scroll-margin-top: 20px; }
.instruction-number { background: #173d8c; color: #fff7a3; border-radius: 3px; padding: 0 6px; font-size: .85em; font-variant-numeric: tabular-nums; }
.instruction-card.comment, .instruction-card.function { background: #24633b; color: white; border-color: #174f2b; }
.instruction-card.control { background: #ffdf76; border-color: #a47e24; }
.nested-instructions { border-left: 2px solid #7296a3; margin-left: 18px; padding-left: 14px; }
.function-links { margin: 16px 0; padding: 12px 18px; border: 1px solid #739dab; border-radius: 6px; }
.function-links ul { margin: 0; padding-left: 20px; }
.board-text { background: #edf8fb; border: 1px solid #739dab; padding: 14px; overflow-x: auto; font: 14px/1.5 monospace; }
.back { display: inline-block; margin: 4px 0 12px; }
section { scroll-margin-top: 20px; }
footer { border-top: 1px solid #608896; margin-top: 48px; padding-top: 18px; }
[hidden] { display: none !important; }
@media (max-width: 600px) {
  body { font-size: 16px; }
  main { padding: 24px 14px 40px; }
  .toolbar { padding: 12px 14px; }
  .cards, .facts { grid-template-columns: 1fr; }
  .facts, details { padding: 14px; }
  .instruction-card { gap: 8px; padding: 8px; font-size: 15px; }
  .nested-instructions { margin-left: 5px; padding-left: 5px; }
  h2 { font-size: 1.6rem; }
}
@media print {
  body { background: white; font-size: 11pt; }
  main { max-width: none; padding: 0; }
  .toolbar, nav, .back { display: none; }
  h2, h3, summary { break-after: avoid; }
  .instruction-list li, .facts { break-inside: avoid; }
  .instruction-card { break-inside: avoid; }
  * { print-color-adjust: exact; -webkit-print-color-adjust: exact; }
}
"""

SCRIPT = """
(() => {
  'use strict';
  const languages = ['en', 'es', 'ja'];
  const selector = document.getElementById('language');
  function chooseLanguage(lang) {
    if (!languages.includes(lang)) lang = 'en';
    document.querySelectorAll('[data-lang]').forEach(el => { el.hidden = el.dataset.lang !== lang; });
    document.documentElement.lang = lang;
    selector.value = lang;
    document.title = document.querySelector('h1 [data-lang="' + lang + '"]').textContent;
    document.querySelectorAll('[data-language-link]').forEach(el => {
      const url = new URL(el.href); url.searchParams.set('lang', lang); el.href = url.href;
    });
    try { localStorage.setItem('tlac-portal-language', lang); } catch (_) {}
    try { const url = new URL(location.href); url.searchParams.set('lang', lang); if (url.hash.includes('-function-')) url.hash = url.hash.replace(/-(en|es|ja)$/, '-' + lang); history.replaceState(null, '', url); } catch (_) {}
  }
  let saved;
  try { saved = localStorage.getItem('tlac-portal-language'); } catch (_) {}
  const query = new URLSearchParams(location.search).get('lang');
  const anchorLanguage = location.hash.match(/-function-.*-(en|es|ja)$/)?.[1];
  chooseLanguage(languages.includes(query) ? query : anchorLanguage || saved || 'en');
  selector.addEventListener('change', () => { chooseLanguage(selector.value); if (location.hash) revealAnchor(); });
  function revealAnchor() {
    const target = document.getElementById(location.hash.slice(1));
    if (!target) return;
    for (let parent = target.parentElement; parent; parent = parent.parentElement) {
      if (parent.tagName === 'DETAILS') parent.open = true;
    }
    target.scrollIntoView();
  }
  addEventListener('hashchange', revealAnchor);
  if (location.hash) revealAnchor();
  let closedForPrint = [];
  addEventListener('beforeprint', () => {
    closedForPrint = [...document.querySelectorAll('details:not([open])')];
    closedForPrint.forEach(el => { el.open = true; });
  });
  addEventListener('afterprint', () => { closedForPrint.forEach(el => { el.open = false; }); });
})();
"""


def build():
    actual = {p.name for p in ROOT.glob('*rulebook.py')}
    expected = {game['file'] for game in GAMES}
    if actual != expected:
        raise ValueError(f'Update the game catalog: missing={actual - expected}, extra={expected - actual}')
    title = t('Games in TLAC', 'Juegos en TLAC', 'TLACのゲーム')
    parts = ['<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">',
             '<meta name="viewport" content="width=device-width, initial-scale=1">',
             '<meta name="description" content="Seven complete game programs as plain-language TLAC instruction cards in English, Spanish, and Japanese.">',
             '<title>Games in TLAC</title><style>', CSS, '</style></head><body>',
             '<div class="toolbar"><label for="language">Language / Idioma / 言語</label><select id="language"><option value="en">English</option><option value="es">Español</option><option value="ja">日本語</option></select></div>',
             '<noscript><style>[data-lang][hidden]{display:block !important} .toolbar{display:none}</style></noscript>',
             '<main id="top"><header><p class="eyebrow">TLAC · Think Like A Computer</p>', heading(1, title),
             '<p class="subtitle">' + localized(t('Seven games, one instruction at a time. Read the rules, follow the game loop, and explore the complete programs.', 'Siete juegos, una instrucción a la vez. Lee las reglas, sigue el bucle del juego y explora los programas completos.', '7つのゲームを、1つずつ命令を追って学びましょう。ルールを読み、ゲームの繰り返しを追い、プログラム全体を確認できます。')) + '</p>',
             '<p><a data-language-link href="TLACPortal.html">' + localized(t('← Learn and play', '← Aprender y jugar', '← 学んで遊ぶ')) + '</a></p></header>',
             '<nav aria-label="Games"><ol class="cards">']
    for number, game in enumerate(GAMES, 1):
        parts.append(f'<li><a href="#{game["id"]}"><strong>{number:02} · {localized(game["title"])}</strong><small>{localized(game["concepts"])}</small></a></li>')
    parts += ['</ol></nav>', '<aside class="note"><p>' + localized(t(
        'Move a coin along the numbered cards. Yellow cards perform actions; darker yellow cards choose or repeat; green cards define functions or explain them. Skip a function’s enclosed cards until it is called, then return to the caller. The full cards include every program instruction and helper function.',
        'Mueve una moneda por las tarjetas numeradas. Las amarillas realizan acciones; las de amarillo más oscuro deciden o repiten; las verdes definen funciones o las explican. Salta las tarjetas internas de una función hasta que se llame y después vuelve al punto de llamada. Las tarjetas completas incluyen todas las instrucciones y funciones auxiliares.',
        '番号付きカードに沿ってコインを進めましょう。黄色は動作、濃い黄色は条件分岐や繰り返し、緑色は関数の定義や説明です。関数の中のカードは呼び出されるまで飛ばし、実行後は呼び出し元に戻ります。全ての命令と補助関数をカードにしています。')) + '</p></aside>',
        '<p>' + localized(t('Positions and list items start at 0. “Yes” and “no” are stored conditions. Parentheses group calculations or coordinate pairs; braces inside a message insert the current value. Short names such as x, y, nx, and ny are named storage spaces. Quoted display messages and symbols keep the game’s original wording.', 'Las posiciones y los elementos de las listas empiezan en 0. «Sí» y «no» son condiciones guardadas. Los paréntesis agrupan cálculos o coordenadas; las llaves dentro de un mensaje insertan el valor actual. Nombres cortos como x, y, nx y ny son espacios de almacenamiento. Los mensajes y símbolos entre comillas conservan el texto original del juego.', '位置とリストの番号は0から始まります。「はい」と「いいえ」は保存する条件の値です。丸括弧は計算や座標の組をまとめ、メッセージ内の波括弧には現在の値を入れます。x、y、nx、nyなどの短い名前は値を保存する場所です。引用符内のメッセージや記号はゲームの原文を使っています。')) + '</p>']
    for number, game in enumerate(GAMES, 1):
        parts += [f'<section id="{game["id"]}" class="game">',
                  f'<h2>{number:02} · {localized(game["title"])}</h2>',
                  '<p class="subtitle">' + localized(game['description']) + '</p>',
                  '<div class="facts"><div><strong>' + localized(t('Board & ideas', 'Tablero e ideas', '盤面と学ぶこと')) + f'</strong><p>{game["board"]}</p><p>' + localized(game['concepts']) + '</p></div>',
                  '<div><strong>' + localized(t('Controls', 'Controles', '操作')) + '</strong><p>' + localized(game['controls']) + '</p></div></div>',
                  heading(3, t('The game at a glance', 'El juego de un vistazo', 'ゲームの流れ')),
                  '<ol class="instruction-list">' + ''.join('<li>' + localized(step) + '</li>' for step in game['steps']) + '</ol>']
        for filename in game['assets']:
            parts += ['<details><summary>' + localized(t('Starting board', 'Tablero inicial', '初期盤面')) + '</summary><pre class="board-text" tabindex="0">' + escape((ROOT / filename).read_text()) + '</pre></details>']
        source = (ROOT / game['file']).read_text(encoding='utf-8')
        functions = [node.name for node in ast.parse(source).body if isinstance(node, ast.FunctionDef)]
        parts += ['<details class="program" open><summary>' + localized(t('Full TLAC instruction cards', 'Todas las tarjetas de instrucciones TLAC', 'TLAC命令カード全文')) + '</summary>']
        for lang in LANGS:
            chart, count = game_cards(source, game['id'], lang)
            parts.append(f'<div class="full-program" data-lang="{lang}" lang="{lang}" data-card-count="{count}" data-game="{game["id"]}"{" hidden" if lang != "en" else ""}>')
            parts.append('<nav class="function-links"><strong>' + t('Jump to a function', 'Ir a una función', '関数へ移動')[lang] + '</strong><ul>')
            for name in functions:
                parts.append(f'<li><a href="#{game["id"]}-function-{name}-{lang}">{escape(FUNCTIONS[name][lang])}</a></li>')
            parts.append('</ul></nav><div class="instruction-chart">' + chart + '</div></div>')
        parts.append('</details>')
        parts += ['<a class="back" href="#top">' + localized(t('↑ All games', '↑ Todos los juegos', '↑ ゲーム一覧')) + '</a></section>']
    parts += ['<footer><p>TLAC · Think Like A Computer</p><a data-language-link href="TLAC_advanced_concepts.html">' + localized(t('← Advanced programming concepts', '← Conceptos avanzados de programación', '← プログラミングの発展的な概念')) + '</a></footer></main>',
              '<script>', SCRIPT, '</script></body></html>']
    destination = ROOT / 'games.html'
    destination.write_text('\n'.join(parts), encoding='utf-8')
    print(f'Built {destination.name}: {len(GAMES)} complete game programs as TLAC instruction cards in three languages.')


if __name__ == '__main__':
    build()
