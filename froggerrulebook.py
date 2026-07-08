#!/usr/bin/python3
import TLACsimulator as TLAC

# 1. Setup Board Dimensions (15 wide, 11 high is perfect for Frogger)
TLAC.globals.W = 15
TLAC.globals.H = 11
TLAC.globals.slots = TLAC.initSlots(TLAC.globals)

# 2. Inject Game State Variables into Simulator memory
TLAC.globals.playing = True
TLAC.globals.lives = 3
TLAC.globals.cars = [] # List of dictionaries tracking traffic

# 3. Level Design and Traffic Spawner
def init_level(globals):
    # Set the top row (Y=0) as the GOAL flags
    for x in range(globals.W):
        globals.slots[x].goal = True

def spawn_traffic(globals):
    globals.cars = []
    # TOP ROAD (Harder, some fast cars)
    # Lane Y=2: Slow cars moving Left
    globals.cars.append({"x": 2, "y": 2, "dx": -1, "char": "c"})
    globals.cars.append({"x": 8, "y": 2, "dx": -1, "char": "c"})
    # Lane Y=3: Fast trucks moving Right (dx=2)
    globals.cars.append({"x": 0, "y": 3, "dx": 2, "char": "T"})
    globals.cars.append({"x": 7, "y": 3, "dx": 2, "char": "T"})
    # Lane Y=4: Slow cars moving Left
    globals.cars.append({"x": 5, "y": 4, "dx": -1, "char": "c"})
    globals.cars.append({"x": 12, "y": 4, "dx": -1, "char": "c"})

    # Y=5 is a Safe Median

    # BOTTOM ROAD (Easier, slower traffic)
    # Lane Y=6: Slow trucks moving Right
    globals.cars.append({"x": 1, "y": 6, "dx": 1, "char": "t"})
    globals.cars.append({"x": 6, "y": 6, "dx": 1, "char": "t"})
    globals.cars.append({"x": 11, "y": 6, "dx": 1, "char": "t"})
    # Lane Y=7: Slow cars moving Left
    globals.cars.append({"x": 4, "y": 7, "dx": -1, "char": "c"})
    globals.cars.append({"x": 10, "y": 7, "dx": -1, "char": "c"})
    # Lane Y=8: Slow trucks moving Right
    globals.cars.append({"x": 2, "y": 8, "dx": 1, "char": "t"})
    globals.cars.append({"x": 9, "y": 8, "dx": 1, "char": "t"})

def reset_player(globals):
    # Spawn player safely at the bottom middle
    TLAC.teleportTurtleTo(globals, 7, 10)
    globals.turtle.direction = "^"

# 4. Helper Functions
def syncEntitiesForRender(globals):
    # Clear out previous frame's entities
    globals.ghosts = []
    
    # Render all traffic as Ghosts
    for car in globals.cars:
        TLAC.addGhost(globals, car["char"], car["x"], car["y"])

def move_traffic(globals):
    for car in globals.cars:
        # Move the car by its speed (dx)
        car["x"] += car["dx"]
        
        # Screen wrap logic (if they drive off the edge, loop back around)
        if car["x"] >= globals.W:
            car["x"] -= globals.W
        elif car["x"] < 0:
            car["x"] += globals.W

def check_collisions(globals):
    px, py = globals.turtle.X, globals.turtle.Y
    
    # Check if the player is standing on the same spot as ANY car
    for car in globals.cars:
        if car["x"] == px and car["y"] == py:
            return True
            
        # Extra check for FAST trucks (dx=2) jumping *over* the frog
        if car["dx"] == 2 and (car["x"] - 1 == px or car["x"] - 1 + globals.W == px) and car["y"] == py:
            return True
            
    return False

def executePlayerInput(globals):
    # Space allows the player to "wait" while traffic moves
    move = input("Enter move (W=Up, S=Down, A=Left, D=Right, Space=Wait, Q=Quit): ").strip().upper()
    
    nx, ny = globals.turtle.X, globals.turtle.Y
    
    if move == 'W':
        ny -= 1
        globals.turtle.direction = "^"
    elif move == 'S':
        ny += 1
        globals.turtle.direction = "V"
    elif move == 'A':
        nx -= 1
        globals.turtle.direction = "<"
    elif move == 'D':
        nx += 1
        globals.turtle.direction = ">"
    elif move == '' or move == ' ':
        print("Frog waits...") # Player chose not to move this turn
    elif move == 'Q':
        globals.playing = False
        return
    else:
        print("Invalid input.")
        return

    # Enforce board boundaries
    if nx < 0: nx = 0
    if nx >= globals.W: nx = globals.W - 1
    if ny < 0: ny = 0
    if ny >= globals.H: ny = globals.H - 1

    # Move Player
    TLAC.teleportTurtleTo(globals, nx, ny)

# 5. Main Game Loop
def playFrogger(globals):
    init_level(globals)
    spawn_traffic(globals)
    reset_player(globals)
    
    print("=== FROGGER START ===")
    print("Cross the roads! Watch out for fast trucks [T] and cars [c]!")
    
    while globals.playing and globals.lives > 0:
        syncEntitiesForRender(globals)
        
        print(f"\nLIVES: {globals.lives}")
        TLAC.updateBoard(globals)
        
        executePlayerInput(globals)
        if not globals.playing: break
        
        # 1. Did the player walk directly into a car?
        if check_collisions(globals):
            print("SPLAT! You walked into traffic!")
            globals.lives -= 1
            reset_player(globals)
            continue
            
        # 2. Advance the traffic
        move_traffic(globals)
        
        # 3. Did the traffic run over the player while they were standing there?
        if check_collisions(globals):
            print("HONK! SPLAT! A car ran you over!")
            globals.lives -= 1
            reset_player(globals)
            continue
            
        # 4. Did the player reach the goal?
        if globals.turtle.Y == 0:
            syncEntitiesForRender(globals)
            TLAC.updateBoard(globals)
            print("\n!!! YOU WIN !!!")
            print("The frog has reached the safe riverbank!")
            break

    if globals.lives <= 0:
        print("\nGAME OVER! Out of frogs!")

# Start the game
playFrogger(TLAC.globals)