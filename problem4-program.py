#!/usr/bin/python3
import TLACsimulator as TLAC

#board setup
TLAC.teleportTurtleTo(4,9)
print("initial board:")
TLAC.printBoard(TLAC.globals)

#problem 4
def P():
    if TLAC.amILayingOnAnEgg(TLAC.globals):
        TLAC.end(TLAC.globals)
    if not TLAC.testIfICanProceed(TLAC.globals):
        TLAC.rt(TLAC.globals)
    TLAC.layEgg(TLAC.globals)
    TLAC.fd(TLAC.globals)
    P()
TLAC.lt(TLAC.globals)
P()