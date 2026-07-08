#!/usr/bin/python3
import TLACsimulator as TLAC

# 1. Setup Board Dimensions
TLAC.globals.W = 8
TLAC.globals.H = 8
TLAC.globals.slots = TLAC.initSlots(TLAC.globals)

# 2. Inject Game State Variables into Simulator memory
TLAC.globals.playing = True
TLAC.globals.boxes = [] # List of (X, Y) tuples for the boxes
TLAC.globals.moves = 0

# 3. Level Design (Map out your levels here!)
# '#' = Wall, 'G' = Goal, '1' = Box, '^' = Player Start
level_1 = [
    "  ####  ",
    "###  #  ",
    "# G1 #  ",
    "### 1G# ",
    "# G1  # ",
    "##  ^## ",
    " ####   ",
    "        "
]

def load_level(globals, layout):
    globals.boxes = []
    for y, row in enumerate(layout):
        for x, char in enumerate(row):
            idx = y * globals.W + x
            if char == '#':
                globals.slots[idx].wall = True
            elif char == 'G':
                globals.slots[idx].goal = True
            elif char == '1':
                globals.boxes.append((x, y))
            elif char == '^':
                TLAC.teleportTurtleTo(globals, x, y)
                globals.turtle.direction = "^"

def syncEntitiesForRender(globals):
    # Clear out previous frame's entities
    globals.ghosts = []
    
    # Add all boxes as '1' ghosts so the board renders them
    for box_x, box_y in globals.boxes:
        TLAC.addGhost(globals, "1", box_x, box_y)

def executePlayerInput(globals):
    move = input("Enter move (W=Up, S=Down, A=Left, D=Right, Q=Quit): ").strip().upper()
    
    dx, dy = 0, 0
    if move == 'W':
        dx, dy = 0, -1
        globals.turtle.direction = "^"
    elif move == 'S':
        dx, dy = 0, 1
        globals.turtle.direction = "V"
    elif move == 'A':
        dx, dy = -1, 0
        globals.turtle.direction = "<"
    elif move == 'D':
        dx, dy = 1, 0
        globals.turtle.direction = ">"
    elif move == 'Q':
        globals.playing = False
        return
    else:
        print("Invalid input.")
        return

    # Calculate where the player is trying to go
    tx, ty = globals.turtle.X, globals.turtle.Y
    nx, ny = tx + dx, ty + dy
    n_idx = ny * globals.W + nx

    # 1. Check Wall Collision
    if globals.slots[n_idx].wall:
        print("BONK! You hit a wall.")
        return

    # 2. Check Box Collision (Pushing logic)
    if (nx, ny) in globals.boxes:
        # Calculate the space BEHIND the box
        nnx, nny = nx + dx, ny + dy
        nn_idx = nny * globals.W + nnx
        
        # Can the box move? (Is it blocked by a wall or another box?)
        if globals.slots[nn_idx].wall or (nnx, nny) in globals.boxes:
            print("BONK! The box is blocked and too heavy to push.")
            return
        
        # Success! Move the box
        box_index = globals.boxes.index((nx, ny))
        globals.boxes[box_index] = (nnx, nny)
        print("Pushed a box!")

    # 3. Move Player
    globals.moves += 1
    TLAC.teleportTurtleTo(globals, nx, ny)

def check_win(globals):
    # The game is won if every box is sitting on top of a Goal slot
    for box_x, box_y in globals.boxes:
        idx = box_y * globals.W + box_x
        if not globals.slots[idx].goal:
            return False # Found a box that is NOT on a goal
    return True

# 4. Main Game Loop
def playSokoban(globals):
    load_level(globals, level_1)
    print("=== SOKOBAN START ===")
    print("Push the boxes [1] onto the Goals [G]!")
    
    while globals.playing:
        syncEntitiesForRender(globals)
        print(f"\nMoves: {globals.moves}")
        
        # Force a redraw of the board so boxes update
        TLAC.updateBoard(globals) 
        
        if check_win(globals):
            print("\n!!! YOU WIN !!!")
            print(f"All boxes secured in {globals.moves} moves!")
            break
            
        executePlayerInput(globals)

# Start the game
playSokoban(TLAC.globals)