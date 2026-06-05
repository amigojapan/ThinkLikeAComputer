#!/usr/bin/python3
import TLACsimulator as TLAC

#board setup
TLAC.teleportTurtleTo(TLAC.globals, 4, 9)
print("initial board:")
TLAC.printBoard(TLAC.globals)

# --- Main Execution Sequence ---

# Step A: Move to the far left wall (Column 0)
TLAC.lt(TLAC.globals)
while TLAC.testIfICanProceed(TLAC.globals):
    TLAC.fd(TLAC.globals)

# Step B: Face UP and move to the very top wall (Row 0)
TLAC.rt(TLAC.globals)
while TLAC.testIfICanProceed(TLAC.globals):
    TLAC.fd(TLAC.globals)

# Step C: Turn completely around to face DOWN, and step down 1 space to Row 1
TLAC.rt(TLAC.globals)
TLAC.rt(TLAC.globals)
TLAC.fd(TLAC.globals)

# Step D: Begin the iterative snaking loop!
while True:
    # 1. Inline logic replacing fillThisColumnWithEggs()
    while TLAC.testIfICanProceed(TLAC.globals, 2):
        TLAC.layEgg(TLAC.globals)
        TLAC.fd(TLAC.globals, 2)
    TLAC.layEgg(TLAC.globals) # Lays the final egg in the column
    
    # 2. Inline logic replacing repeatThisUntilBoardFull()
    # If the turtle is at the top of the board facing UP (^)
    if TLAC.globals.turtle.direction == "^":
        TLAC.rt(TLAC.globals)
        # Check if we have hit the right edge of the board
        if not TLAC.testIfICanProceed(TLAC.globals, 2):
            if TLAC.testIfICanProceed(TLAC.globals):
                TLAC.fd(TLAC.globals)
                TLAC.rt(TLAC.globals)
            TLAC.end(TLAC.globals)
            break  # Break out of the loop to safely end the script
            
        TLAC.fd(TLAC.globals, 2)
        TLAC.rt(TLAC.globals)
        
    # If the turtle is at the bottom of the board facing DOWN
    else:
        TLAC.lt(TLAC.globals)
        # Check if we have hit the right edge of the board
        if not TLAC.testIfICanProceed(TLAC.globals, 2):
            # This neatly tucks the turtle into the final [v] corner position!
            if TLAC.testIfICanProceed(TLAC.globals):
                TLAC.fd(TLAC.globals)
                TLAC.rt(TLAC.globals) 
            TLAC.end(TLAC.globals)
            break  # Break out of the loop to safely end the script
            
        TLAC.fd(TLAC.globals, 2)
        TLAC.lt(TLAC.globals)