#!/usr/bin/python3
import TLACsimulator as TLAC

#board setup
TLAC.teleportTurtleTo(TLAC.globals,4,9)
print("initial board:")
TLAC.printBoard(TLAC.globals)

#problem 7
def goToBeginningOfBoard():
    if TLAC.testIfICanProceed(TLAC.globals):
        TLAC.fd(TLAC.globals)
        goToBeginningOfBoard()
    else:
        return
def fillThisRowWithEggs():
    if TLAC.testIfICanProceed(TLAC.globals):
        TLAC.layEgg(TLAC.globals)
        TLAC.fd(TLAC.globals)
        fillThisRowWithEggs()
        return
    else:
        TLAC.layEgg(TLAC.globals)
        return
def repeatThisUntilBoardFull():
    if TLAC.globals.turtle.direction=="^" :
        fillThisRowWithEggs()
        TLAC.rt(TLAC.globals)
        TLAC.fd(TLAC.globals)
        TLAC.rt(TLAC.globals)
    else:
        TLAC.fd(TLAC.globals,TLAC.globals.H-1)
        TLAC.lt(TLAC.globals)
        if TLAC.globals.turtle.direction==">" :
            if not TLAC.testIfICanProceed(TLAC.globals):
                TLAC.end(globals)
        TLAC.fd(TLAC.globals)
        TLAC.lt(TLAC.globals)
    repeatThisUntilBoardFull()
TLAC.lt(TLAC.globals)
goToBeginningOfBoard()
TLAC.rt(TLAC.globals)
fillThisRowWithEggs()
repeatThisUntilBoardFull()