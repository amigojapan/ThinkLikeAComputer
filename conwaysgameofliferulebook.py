#!/usr/bin/python3
import TLACsimulator as TLAC
import random
import time

# 1. Setup Board Dimensions
# A slightly larger board makes Game of Life patterns much more interesting.
TLAC.globals.W = 15
TLAC.globals.H = 15
TLAC.globals.slots = TLAC.initSlots(TLAC.globals)

# 2. Inject Life Variables into TLAC Cells
for slot in TLAC.globals.slots:
    slot.is_alive = False
    slot.next_alive = False

# 3. Game Initialization Logic
def seed_board(globals, fill_probability=0.25):
    """Randomly populates the board with initial live cells."""
    for slot in globals.slots:
        if random.random() < fill_probability:
            slot.is_alive = True

def calculate_next_generation(globals):
    """Applies Conway's rules to calculate the next state of the board."""
    for y in range(globals.H):
        for x in range(globals.W):
            index = y * globals.W + x
            alive_neighbors = 0
            
            # Check 8-way neighbors
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    if dx == 0 and dy == 0: 
                        continue
                    
                    nx, ny = x + dx, y + dy
                    
                    # Ensure we stay within board boundaries
                    if 0 <= nx < globals.W and 0 <= ny < globals.H:
                        n_index = ny * globals.W + nx
                        if globals.slots[n_index].is_alive:
                            alive_neighbors += 1
            
            # Apply the Rules of Life
            slot = globals.slots[index]
            if slot.is_alive:
                # Rule 1 & 3: Underpopulation (<2) or Overpopulation (>3) leads to death
                if alive_neighbors < 2 or alive_neighbors > 3:
                    slot.next_alive = False
                # Rule 2: 2 or 3 neighbors means the cell lives on
                else:
                    slot.next_alive = True
            else:
                # Rule 4: Exactly 3 neighbors causes reproduction
                if alive_neighbors == 3:
                    slot.next_alive = True
                else:
                    slot.next_alive = False

    # Apply the calculated next generation to the current board
    for slot in globals.slots:
        slot.is_alive = slot.next_alive

# 4. Rendering
def print_life_board(globals, generation):
    """A custom renderer to display the cellular automaton."""
    print(f"\n=== CONWAY'S GAME OF LIFE (Generation: {generation}) ===")
    board_str = ""
    for y in range(globals.H):
        for x in range(globals.W):
            index = y * globals.W + x
            slot = globals.slots[index]
            
            # Alive cells are solid blocks, dead cells are empty space
            if slot.is_alive:
                board_str += "[O]"
            else:
                board_str += "[ ]"
        board_str += "\n"
    print(board_str)

# 5. Main Loop
def play_life(globals):
    seed_board(globals)
    generation = 0
    
    while True:
        print_life_board(globals, generation)
        
        # Input handling
        move = input("Press [ENTER] for next step | (A)uto-play | (Q)uit: ").strip().upper()
        
        if move == 'Q':
            print("Halting simulation.")
            break
        elif move == 'A':
            print("Starting auto-play... (Press Ctrl+C to stop)")
            try:
                while True:
                    calculate_next_generation(globals)
                    generation += 1
                    print_life_board(globals, generation)
                    time.sleep(0.3) # Pause so the user can see the evolution
            except KeyboardInterrupt:
                print("\nAuto-play interrupted by user.")
        else:
            # Default action: Step forward one generation
            calculate_next_generation(globals)
            generation += 1

if __name__ == "__main__":
    play_life(TLAC.globals)