#!/usr/bin/python3
import TLACsimulator as TLAC

#board setup
TLAC.teleportTurtleTo(TLAC.globals,4,9)
print("initial board:")
TLAC.printBoard(TLAC.globals)

#program
def goToBeginningOfBoard():
    if TLAC.testIfICanProceed(TLAC.globals):
        TLAC.fd(TLAC.globals)
    else:
        return
    goToBeginningOfBoard()

def fillThisRowWithEggs():
    if TLAC.testIfICanProceed(TLAC.globals,2):
        TLAC.layEgg(TLAC.globals)
        TLAC.fd(TLAC.globals,2)
        fillThisRowWithEggs()
    else:
        TLAC.layEgg(TLAC.globals)
        return

def repeatThisUntilBoardFull():
    if TLAC.globals.turtle.direction=="^" :
        fillThisRowWithEggs()
        TLAC.rt(TLAC.globals)
        TLAC.fd(TLAC.globals)
        TLAC.rt(TLAC.globals)
        repeatThisUntilBoardFull()
    else:
        TLAC.fd(TLAC.globals,TLAC.globals.H-2)
        TLAC.lt(TLAC.globals)
        if TLAC.globals.turtle.direction==">" :
            if not TLAC.testIfICanProceed(TLAC.globals):
                TLAC.end(globals)
        TLAC.fd(TLAC.globals)
        TLAC.lt(TLAC.globals)

TLAC.lt(TLAC.globals)
goToBeginningOfBoard()
TLAC.rt(TLAC.globals)
fillThisRowWithEggs()
repeatThisUntilBoardFull()