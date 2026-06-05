#!/usr/bin/python3
import TLACsimulator as TLAC

#board setup
TLAC.teleportTurtleTo(TLAC.globals, 4, 9)
print("initial board:")
TLAC.printBoard(TLAC.globals)

#problem 4 non-recursive solution
# Initial action before the loop starts
TLAC.lt(TLAC.globals)

while True:
    # Exit condition
    if TLAC.amILayingOnAnEgg(TLAC.globals):
        TLAC.end(TLAC.globals)
        break  # Breaks out of the loop to end the script

    # Turtle actions
    if not TLAC.testIfICanProceed(TLAC.globals):
        TLAC.rt(TLAC.globals)
        
    TLAC.layEgg(TLAC.globals)
    TLAC.fd(TLAC.globals)