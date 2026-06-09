#!/usr/bin/python3
import TLACsimulator as TLAC
import random

# 1. Setup Board Dimensions
TLAC.globals.W = 19
TLAC.globals.H = 14
TLAC.globals.slots = TLAC.initSlots(TLAC.globals)

# 2. Inject Game State Variables into Simulator memory
TLAC.globals.score = 0
TLAC.globals.lives = 3
TLAC.globals.powerModeCounter = 0

# 3. Load Board and Entities
TLAC.readBoardFromFile(TLAC.globals, "pacman-board1.txt")
TLAC.teleportTurtleTo(TLAC.globals, 1, 1)
TLAC.addGhost(TLAC.globals, "M", 1, 10) # Wanderer
TLAC.addGhost(TLAC.globals, "W", 1, 12) # Tracker

# 4. Helper Functions
def areThereCollectiblesLeft(globals):
    for slot in globals.slots:
        if slot.containsEgg or slot.diamond: return True
    return False

def getValidGhostMoves(globals, ghost):
    valid_moves = []
    X, Y = ghost.X, ghost.Y
    if Y - 1 >= 0 and not globals.slots[(Y - 1) * globals.W + X].wall: valid_moves.append(("UP", X, Y - 1))
    if Y + 1 < globals.H and not globals.slots[(Y + 1) * globals.W + X].wall: valid_moves.append(("DOWN", X, Y + 1))
    if X - 1 >= 0 and not globals.slots[Y * globals.W + (X - 1)].wall: valid_moves.append(("LEFT", X - 1, Y))
    if X + 1 < globals.W and not globals.slots[Y * globals.W + (X + 1)].wall: valid_moves.append(("RIGHT", X + 1, Y))
    return valid_moves

def executePlayerInput(globals):
    valid_move = False
    while not valid_move:
        move = input("Enter move (W=Up, S=Down, A=Left, D=Right): ").strip().upper()
        if move == 'W': globals.turtle.direction = "^"
        elif move == 'S': globals.turtle.direction = "V"
        elif move == 'A': globals.turtle.direction = "<"
        elif move == 'D': globals.turtle.direction = ">"
        else: continue
        
        if TLAC.testIfICanProceed(globals, 1):
            TLAC.fd(globals, 1)
            valid_move = True
        else:
            print("BONK! Wall ahead.")

def checkCollisions(globals):
    for ghost in globals.ghosts:
        if ghost.X == globals.turtle.X and ghost.Y == globals.turtle.Y:
            if globals.powerModeCounter > 0:
                print(f"POWER UP! Ate ghost {ghost.char}!")
                globals.score += 200
                ghost.X, ghost.Y = 1, 10
            else:
                globals.lives -= 1
                TLAC.teleportTurtleTo(globals, 1, 1)
                print(f"DIED! Lives remaining: {globals.lives}")
                return True # Reset triggered
    return False

def runGhostPlayerTurn(globals):
    # Handle Power Timer
    if globals.powerModeCounter > 0:
        globals.powerModeCounter -= 1
        if globals.powerModeCounter == 0:
            print("POWER MODE EXPIRED! Ghosts are back to ATTACK mode.")
    
    for ghost in globals.ghosts:
        valid_moves = getValidGhostMoves(globals, ghost)
        if not valid_moves: continue
        
        # Decide direction: Frightened (Escape) vs Attack
        if globals.powerModeCounter > 0:
            best_move = max(valid_moves, key=lambda m: abs(m[1]-globals.turtle.X) + abs(m[2]-globals.turtle.Y))
        else:
            best_move = random.choice(valid_moves) if ghost.char == "M" else \
                        min(valid_moves, key=lambda m: abs(m[1]-globals.turtle.X) + abs(m[2]-globals.turtle.Y))
        
        ghost.X, ghost.Y = best_move[1], best_move[2]

# 5. Main Game Loop
def playPacManInteractive(globals):
    print("Game Start! 3 Lives.")
    while areThereCollectiblesLeft(globals) and globals.lives > 0:
        print(f"\nSCORE: {globals.score} | LIVES: {globals.lives} | POWER: {globals.powerModeCounter}")
        TLAC.printBoard(globals)
        
        executePlayerInput(globals)
        if checkCollisions(globals): continue
        
        # Check collectibles
        if TLAC.amILayingOnAnEgg(globals):
            TLAC.eatEgg(globals)
            globals.score += 10
        if TLAC.amILayingOnADiamond(globals):
            TLAC.eatDiamond(globals)
            globals.score += 50
            globals.powerModeCounter = 10
            
        runGhostPlayerTurn(globals)
        if checkCollisions(globals): continue

    print(f"GAME OVER! Final Score: {globals.score}")

# Start the game
playPacManInteractive(TLAC.globals)