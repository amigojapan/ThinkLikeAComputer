#!/usr/bin/python3
import TLACsimulator as TLAC

#board setup
TLAC.teleportTurtleTo(TLAC.globals, 4, 9)
print("initial board:")
TLAC.printBoard(TLAC.globals)

#problem 6
# 1. Turn left and go to the beginning of the board
TLAC.lt(TLAC.globals)
while TLAC.testIfICanProceed(TLAC.globals):
    TLAC.fd(TLAC.globals)
TLAC.rt(TLAC.globals)

# 2. Initial row fill (Executes before the repeating main loop)
while TLAC.testIfICanProceed(TLAC.globals):
    TLAC.layEgg(TLAC.globals)
    TLAC.fd(TLAC.globals)
TLAC.layEgg(TLAC.globals)

# 3. Main repeating loop for the rest of the board
while True:
    # Inner loop replacing fillThisRowWithEggs()
    while TLAC.testIfICanProceed(TLAC.globals):
        TLAC.layEgg(TLAC.globals)
        TLAC.fd(TLAC.globals)
    TLAC.layEgg(TLAC.globals)
    
    # Turning and proceeding logic
    if TLAC.globals.turtle.direction == "^":
        TLAC.rt(TLAC.globals)
        TLAC.fd(TLAC.globals)
        TLAC.rt(TLAC.globals)
    else:
        TLAC.lt(TLAC.globals)
        # Check if we've reached the end of the board
        if TLAC.globals.turtle.direction == ">":
            if not TLAC.testIfICanProceed(TLAC.globals):
                TLAC.end(TLAC.globals)
                break  # Break out of the loop to end the script
                
        TLAC.fd(TLAC.globals)
        TLAC.lt(TLAC.globals)