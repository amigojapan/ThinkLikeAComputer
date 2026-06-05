#!/usr/bin/python3
import TLACsimulator as TLAC

#board setup
TLAC.teleportTurtleTo(TLAC.globals, 4, 9)
print("initial board:")
TLAC.printBoard(TLAC.globals)

#problem 5
# Initial action before the loop starts
TLAC.lt(TLAC.globals)

while True:
    # Exit condition
    if TLAC.amILayingOnAnEgg(TLAC.globals):
        TLAC.end(TLAC.globals)
        break  # Breaks out of the loop to end the script

    # Turtle actions
    # Note the second parameter (2) for checking and moving
    if not TLAC.testIfICanProceed(TLAC.globals, 2):
        TLAC.rt(TLAC.globals)
        
    TLAC.layEgg(TLAC.globals)
    TLAC.fd(TLAC.globals, 2)