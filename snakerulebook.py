#!/usr/bin/python3
import TLACsimulator as TLAC
import random

# 1. Setup Board Dimensions (15x15)
TLAC.globals.W = 15
TLAC.globals.H = 15
TLAC.globals.slots = TLAC.initSlots(TLAC.globals)

# 2. Load Board and Entities (FIXED FILENAME)
TLAC.readBoardFromFile(TLAC.globals, "snakefield.txt")

# 3. Inject Game State Variables into Simulator memory
TLAC.globals.score = 0
TLAC.globals.playing = True
TLAC.globals.snake_body = [] # List of (X, Y) tuples
TLAC.globals.food = (0, 0)
TLAC.globals.dx = 1
TLAC.globals.dy = 0

# 4. Helper Functions
def spawn_food(globals):
    while True:
        # Spawn within the inner play area (avoiding walls at 0 and W-1 / H-1)
        fx = random.randint(1, globals.W - 2)
        fy = random.randint(1, globals.H - 2)
        
        # Ensure food doesn't spawn on top of the snake
        if (fx, fy) not in globals.snake_body:
            globals.food = (fx, fy)
            break

def init_game(globals):
    globals.score = 0
    globals.playing = True
    globals.dx = 1
    globals.dy = 0
    
    # Initialize snake with length 4 (Centered for 15x15 grid: Y=7, X=7,6,5,4)
    globals.snake_body = [(7 - i, 7) for i in range(4)]
    TLAC.teleportTurtleTo(globals, globals.snake_body[0][0], globals.snake_body[0][1])
    globals.turtle.direction = ">"
    
    spawn_food(globals)

def syncEntitiesForRender(globals):
    # Clear out previous frame's entities
    globals.ghosts = []
    
    # Add food as an '@' ghost so the board renders it
    TLAC.addGhost(globals, "@", globals.food[0], globals.food[1])
    
    # Add snake body segments (excluding head) as 'O' ghosts
    for segment in globals.snake_body[1:]:
        TLAC.addGhost(globals, "O", segment[0], segment[1])

def executePlayerInput(globals):
    move = input("Enter move (W=Up, S=Down, A=Left, D=Right, Q=Quit): ").strip().upper()
    
    # Update movement vectors, preventing reversing into itself
    if move == 'W' and globals.dy == 0:
        globals.dx, globals.dy = 0, -1
        globals.turtle.direction = "^"
    elif move == 'S' and globals.dy == 0:
        globals.dx, globals.dy = 0, 1
        globals.turtle.direction = "V"
    elif move == 'A' and globals.dx == 0:
        globals.dx, globals.dy = -1, 0
        globals.turtle.direction = "<"
    elif move == 'D' and globals.dx == 0:
        globals.dx, globals.dy = 1, 0
        globals.turtle.direction = ">"
    elif move == 'Q':
        globals.playing = False

def updateSnakeLogic(globals):
    head_x, head_y = globals.snake_body[0]
    new_x = head_x + globals.dx
    new_y = head_y + globals.dy

    # Check Wall Collision
    if new_x <= 0 or new_x >= globals.W - 1 or new_y <= 0 or new_y >= globals.H - 1:
        print("BONK! You hit the wall!")
        globals.playing = False
        return

    # Check Self Collision
    if (new_x, new_y) in globals.snake_body[:-1]:
        print("OUCH! You bit yourself!")
        globals.playing = False
        return

    # Move head forward
    globals.snake_body.insert(0, (new_x, new_y))
    TLAC.teleportTurtleTo(globals, new_x, new_y)

    # Check Food Collision
    if (new_x, new_y) == globals.food:
        globals.score += 10
        print("Ate food! +10 points. YUM!")
        spawn_food(globals)
    else:
        # If no food was eaten, pop the tail
        globals.snake_body.pop()

# 5. Main Game Loop
def playSnakeInteractive(globals):
    init_game(globals)
    print("Snake Game Start! (Turn-based mode, 15x15 Grid)")
    
    while globals.playing:
        syncEntitiesForRender(globals)
        print(f"\nSCORE: {globals.score}")
        
        # FIXED: Call updateBoard instead of printBoard to force walls/ghosts to redraw
        TLAC.updateBoard(globals)
        
        executePlayerInput(globals)
        
        if globals.playing:
            updateSnakeLogic(globals)

    print(f"GAME OVER! Final Score: {globals.score}")

# Start the game
playSnakeInteractive(TLAC.globals)