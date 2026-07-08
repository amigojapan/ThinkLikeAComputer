#!/usr/bin/python3
import TLACsimulator as TLAC
import random

# 1. Setup Board Dimensions
TLAC.globals.W = 10
TLAC.globals.H = 10
TLAC.globals.slots = TLAC.initSlots(TLAC.globals)

NUM_MINES = 12

# 2. Inject Minesweeper Variables into TLAC Cells
for slot in TLAC.globals.slots:
    slot.is_mine = False
    slot.revealed = False
    slot.flagged = False
    slot.neighbor_mines = 0

# 3. Game Initialization Logic
def place_mines_and_calculate(globals):
    """Randomly distributes mines and pre-calculates neighbor numbers."""
    placed = 0
    while placed < NUM_MINES:
        rx = random.randint(0, globals.W - 1)
        ry = random.randint(0, globals.H - 1)
        index = ry * globals.W + rx
        
        if not globals.slots[index].is_mine:
            globals.slots[index].is_mine = True
            placed += 1
            
    # Calculate 8-way neighbors for every cell
    for y in range(globals.H):
        for x in range(globals.W):
            index = y * globals.W + x
            if globals.slots[index].is_mine:
                continue
                
            count = 0
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    if dx == 0 and dy == 0: continue
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < globals.W and 0 <= ny < globals.H:
                        n_index = ny * globals.W + nx
                        if globals.slots[n_index].is_mine:
                            count += 1
            globals.slots[index].neighbor_mines = count

# 4. Rendering and Mechanics
def print_ms_board(globals):
    """A custom renderer that overrides TLAC's native graphics to show numbers."""
    print(f"\n=== MINESWEEPER ({NUM_MINES} Mines) ===")
    board_str = ""
    for y in range(globals.H):
        for x in range(globals.W):
            index = y * globals.W + x
            slot = globals.slots[index]
            
            # Cursor takes precedence
            if x == globals.turtle.X and y == globals.turtle.Y:
                board_str += "[@]"
            elif slot.flagged:
                board_str += "[F]"
            elif not slot.revealed:
                board_str += "[#]"
            elif slot.is_mine:
                board_str += "[*]"
            elif slot.neighbor_mines > 0:
                board_str += f"[{slot.neighbor_mines}]"
            else:
                board_str += "[ ]"
        board_str += "\n"
    print(board_str)

def reveal_cell(globals, x, y):
    """Recursive flood-fill to reveal empty spaces (TLAC has a high recursion depth)."""
    if x < 0 or x >= globals.W or y < 0 or y >= globals.H:
        return
    index = y * globals.W + x
    slot = globals.slots[index]
    
    if slot.revealed or slot.flagged:
        return
        
    slot.revealed = True
    
    if slot.is_mine:
        return
        
    # If it's a blank space, reveal all surrounding spaces
    if slot.neighbor_mines == 0:
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dx != 0 or dy != 0:
                    reveal_cell(globals, x + dx, y + dy)

def check_win(globals):
    """Player wins when all non-mine cells are revealed."""
    for slot in globals.slots:
        if not slot.is_mine and not slot.revealed:
            return False
    return True

def executeMSInput(globals):
    """Processes Turtle movement and Minesweeper actions."""
    valid_input = False
    while not valid_input:
        move = input("Move (W,A,S,D) | Reveal (R) | Flag (F) | Quit (Q): ").strip().upper()
        x, y = globals.turtle.X, globals.turtle.Y
        
        if move == 'W' and y > 0:
            globals.turtle.Y -= 1
            valid_input = True
        elif move == 'S' and y < globals.H - 1:
            globals.turtle.Y += 1
            valid_input = True
        elif move == 'A' and x > 0:
            globals.turtle.X -= 1
            valid_input = True
        elif move == 'D' and x < globals.W - 1:
            globals.turtle.X += 1
            valid_input = True
        elif move == 'R':
            index = y * globals.W + x
            slot = globals.slots[index]
            if not slot.flagged:
                reveal_cell(globals, x, y)
                if slot.is_mine:
                    return "LOSS"
            valid_input = True
        elif move == 'F':
            index = y * globals.W + x
            slot = globals.slots[index]
            if not slot.revealed:
                slot.flagged = not slot.flagged # Toggle flag on/off
            valid_input = True
        elif move == 'Q':
            print("Quitting game...")
            exit(0)
            
    return "CONTINUE"

# 5. Main Loop
def play_minesweeper(globals):
    TLAC.setInitialTurtlePositionTo(globals, 0, 0)
    place_mines_and_calculate(globals)
    
    game_state = "CONTINUE"
    while game_state == "CONTINUE":
        print_ms_board(globals)
        game_state = executeMSInput(globals)
        
        if game_state == "LOSS":
            # Reveal all mines on game over
            for slot in globals.slots:
                if slot.is_mine:
                    slot.revealed = True
            print_ms_board(globals)
            print("BOOM! You stepped on a mine. GAME OVER.")
            break
            
        if check_win(globals):
            print_ms_board(globals)
            print("Congratulations! You flagged all the mines and cleared the safe zones!")
            break

if __name__ == "__main__":
    play_minesweeper(TLAC.globals)