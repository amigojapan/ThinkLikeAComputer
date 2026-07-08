#!/usr/bin/python3
import TLACsimulator as TLAC
import random

# 1. Setup Board Dimensions (11x11 is a classic Bomberman arena size)
TLAC.globals.W = 11
TLAC.globals.H = 11
TLAC.globals.slots = TLAC.initSlots(TLAC.globals)

# 2. Inject Game State Variables into Simulator memory
TLAC.globals.playing = True
TLAC.globals.bombs = []   # List of dictionaries tracking bombs: {'x': X, 'y': Y, 'timer': 3}
TLAC.globals.enemies = [] # List of dictionaries tracking enemies: {'x': X, 'y': Y, 'char': 'M'}

# 3. Level Generation
def init_level(globals):
    for y in range(globals.H):
        for x in range(globals.W):
            idx = y * globals.W + x
            
            # Create the unbreakable border walls
            if x == 0 or x == globals.W - 1 or y == 0 or y == globals.H - 1:
                globals.slots[idx].wall = True
                
            # Create the unbreakable grid pillars (even coordinates)
            elif x % 2 == 0 and y % 2 == 0:
                globals.slots[idx].wall = True
                
            # Randomly place breakable crates (Eggs), keeping the top-left safe for the player
            else:
                if (x > 2 or y > 2) and random.random() < 0.4:
                    globals.slots[idx].containsEgg = True

    # Spawn Player at top left
    TLAC.teleportTurtleTo(globals, 1, 1)
    globals.turtle.direction = ">"

    # Spawn Enemies in the other corners
    globals.enemies.append({'x': 9, 'y': 9, 'char': 'M'})
    globals.enemies.append({'x': 1, 'y': 9, 'char': 'M'})
    globals.enemies.append({'x': 9, 'y': 1, 'char': 'M'})

# 4. Helper Functions
def syncEntitiesForRender(globals):
    globals.ghosts = []
    
    # Render bombs as ghosts displaying their timer
    for b in globals.bombs:
        TLAC.addGhost(globals, str(b['timer']), b['x'], b['y'])
        
    # Render enemies
    for e in globals.enemies:
        TLAC.addGhost(globals, e['char'], e['x'], e['y'])

def process_explosions(globals):
    # Tick down bombs
    for b in globals.bombs[:]:
        b['timer'] -= 1
        
        # If the bomb hits 0, EXPLODE!
        if b['timer'] <= 0:
            print(f"\n*** BOOM at {b['x']},{b['y']}! ***")
            
            # The cross blast radius: center, up, down, left, right
            blast_zones = [(0,0), (1,0), (-1,0), (0,1), (0,-1)]
            
            for dx, dy in blast_zones:
                tx, ty = b['x'] + dx, b['y'] + dy
                idx = ty * globals.W + tx
                
                # Check for unbreakable walls (stops the blast)
                if globals.slots[idx].wall:
                    continue 
                
                # Destroy breakable crates (Eggs)
                if globals.slots[idx].containsEgg:
                    globals.slots[idx].containsEgg = False
                    print(f"-> Destroyed crate at {tx},{ty}")
                
                # Check if it hit an enemy
                for e in globals.enemies[:]:
                    if e['x'] == tx and e['y'] == ty:
                        globals.enemies.remove(e)
                        print(f"-> Blew up an enemy at {tx},{ty}!")
                
                # Check if it hit the player
                if globals.turtle.X == tx and globals.turtle.Y == ty:
                    print("-> OH NO! You blew yourself up!")
                    globals.playing = False
                    
            # Remove the exploded bomb
            globals.bombs.remove(b)

def move_enemies(globals):
    for e in globals.enemies:
        valid_moves = []
        # Check all 4 directions
        for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
            nx, ny = e['x'] + dx, e['y'] + dy
            idx = ny * globals.W + nx
            
            # Ensure no walls or crates are there
            if not globals.slots[idx].wall and not globals.slots[idx].containsEgg:
                # Ensure no bomb is sitting there
                if not any(b['x'] == nx and b['y'] == ny for b in globals.bombs):
                    valid_moves.append((nx, ny))
                    
        # Pick a random valid move and step there
        if valid_moves:
            e['x'], e['y'] = random.choice(valid_moves)
            
            # Did the enemy just walk into the player?
            if e['x'] == globals.turtle.X and e['y'] == globals.turtle.Y:
                print("An enemy bumped into you!")
                globals.playing = False

def executePlayerInput(globals):
    move = input("Enter move (W=Up, S=Down, A=Left, D=Right, B=Drop Bomb, Space=Wait, Q=Quit): ").strip().upper()
    
    nx, ny = globals.turtle.X, globals.turtle.Y
    
    if move == 'W': ny -= 1; globals.turtle.direction = "^"
    elif move == 'S': ny += 1; globals.turtle.direction = "V"
    elif move == 'A': nx -= 1; globals.turtle.direction = "<"
    elif move == 'D': nx += 1; globals.turtle.direction = ">"
    elif move == 'B':
        # Drop a bomb with a 3-turn fuse
        globals.bombs.append({'x': nx, 'y': ny, 'timer': 4}) # Set to 4 because it immediately ticks down to 3
        print("Bomb planted!")
        return
    elif move == '' or move == ' ':
        print("Waiting...")
        return
    elif move == 'Q':
        globals.playing = False
        return
    else:
        print("Invalid input.")
        return

    # Look at the tile the player is trying to step on
    idx = ny * globals.W + nx
    
    # 1. Check if it's a wall or crate
    if globals.slots[idx].wall or globals.slots[idx].containsEgg:
        print("BONK! Blocked by an object.")
        return
        
    # 2. Check if a bomb is sitting there
    if any(b['x'] == nx and b['y'] == ny for b in globals.bombs):
        print("BONK! You can't walk through a bomb.")
        return
        
    # 3. Move the player
    TLAC.teleportTurtleTo(globals, nx, ny)
    
    # 4. Did the player walk directly into an enemy?
    for e in globals.enemies:
        if e['x'] == globals.turtle.X and e['y'] == globals.turtle.Y:
            print("You walked right into an enemy!")
            globals.playing = False

# 5. Main Game Loop
def playBomberman(globals):
    init_level(globals)
    
    print("=== BOMBERMAN START ===")
    print("Destroy the [o] crates and the [M] monsters!")
    print("Use B to drop a bomb. Stay out of the blast zone!")
    
    while globals.playing:
        syncEntitiesForRender(globals)
        TLAC.updateBoard(globals)
        
        # Win condition check
        if len(globals.enemies) == 0:
            print("\n!!! YOU WIN !!!")
            print("All monsters have been destroyed!")
            break
            
        executePlayerInput(globals)
        if not globals.playing: break
        
        # Advance the world states
        process_explosions(globals)
        if not globals.playing: break
        
        move_enemies(globals)

    if not globals.playing and len(globals.enemies) > 0:
        syncEntitiesForRender(globals)
        TLAC.updateBoard(globals)
        print("\nGAME OVER!")

# Start the game
playBomberman(TLAC.globals)