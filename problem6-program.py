#!/usr/bin/python3
import TLACsimulator as TLAC

#board setup
TLAC.teleportTurtleTo(4,9)
print("initial board:")
TLAC.printBoard(TLAC.globals)

#problem 6
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
    else:
        TLAC.layEgg(TLAC.globals)
        return
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
TLAC.lt(TLAC.globals)
goToBeginningOfBoard()
TLAC.rt(TLAC.globals)
fillThisRowWithEggs()
repeatThisUntilBoardFull()
