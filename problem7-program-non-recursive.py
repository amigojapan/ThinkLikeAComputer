#!/usr/bin/python3
import TLACsimulator as TLAC

#board setup
TLAC.teleportTurtleTo(TLAC.globals, 4, 9)
print("initial board:")
TLAC.printBoard(TLAC.globals)

#problem 7
TLAC.lt(TLAC.globals)

# 1. goToBeginningOfBoard
while TLAC.testIfICanProceed(TLAC.globals):
    TLAC.fd(TLAC.globals)

TLAC.rt(TLAC.globals)

# 2. fillThisRowWithEggs(Initial run)
while TLAC.testIfICanProceed(TLAC.globals):
    TLAC.layEgg(TLAC.globals)
    TLAC.fd(TLAC.globals)
TLAC.layEgg(TLAC.globals)

# 3. repeatThisUntilBoardFull
while True:
    if TLAC.globals.turtle.direction == "^":
        # fillThisRowWithEggs inline
        while TLAC.testIfICanProceed(TLAC.globals):
            TLAC.layEgg(TLAC.globals)
            TLAC.fd(TLAC.globals)
        TLAC.layEgg(TLAC.globals)
        
        # Turn logic for "^" direction
        TLAC.rt(TLAC.globals)
        TLAC.fd(TLAC.globals)
        TLAC.rt(TLAC.globals)
    else:
        # Move forward by height minus 1
        TLAC.fd(TLAC.globals, TLAC.globals.H - 1)
        TLAC.lt(TLAC.globals)
        
        # Exit condition check
        if TLAC.globals.turtle.direction == ">":
            if not TLAC.testIfICanProceed(TLAC.globals):
                TLAC.end(TLAC.globals) # Fixed from 'globals'
                break  # Breaks out of the loop to safely end the script
                
        TLAC.fd(TLAC.globals)
        TLAC.lt(TLAC.globals)