#!/usr/bin/python3
import TLACsimulator as TLAC

#board setup
TLAC.teleportTurtleTo(4,9)
print("initial board:")
TLAC.printBoard(TLAC.globals)

#proram
def goToBeginningOfBoard():
    if TLAC.testIfICanProceed(TLAC.globals):
        TLAC.fd(TLAC.globals)
    else:
        return
    goToBeginningOfBoard()

def fillThisRowWithEggs():
    if TLAC.testIfICanProceed(TLAC.globals):
        TLAC.layEgg(TLAC.globals)
        TLAC.fd(TLAC.globals)
    else:
        TLAC.layEgg(TLAC.globals)
        return
    fillThisRowWithEggs()
def repeatThisUntilBoardFull():
    fillThisRowWithEggs()
    if TLAC.globals.turtle.direction=="^" :
        TLAC.rt(TLAC.globals)
        TLAC.fd(TLAC.globals)
        TLAC.rt(TLAC.globals)
    else:
        TLAC.lt(TLAC.globals)
        if TLAC.globals.turtle.direction==">" :
            if not TLAC.testIfICanProceed(TLAC.globals):
                TLAC.end(globals)
        TLAC.fd(TLAC.globals)
        TLAC.lt(TLAC.globals)
    repeatThisUntilBoardFull()
    return 
TLAC.lt(TLAC.globals)
goToBeginningOfBoard()
TLAC.rt(TLAC.globals)
fillThisRowWithEggs()
repeatThisUntilBoardFull()