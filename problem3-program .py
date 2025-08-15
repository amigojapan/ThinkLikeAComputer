#!/usr/bin/python3
import TLACsimulator as TLAC

#board setup
TLAC.readBoaedFromFile(TLAC.globals,"problem3-board.txt")
TLAC.teleportTurtleTo(4,9)
print("initial board:")
TLAC.printBoard(TLAC.globals)

#program
TLAC.fd(TLAC.globals)
TLAC.rt(TLAC.globals)
TLAC.fd(TLAC.globals,2)
TLAC.lt(TLAC.globals)
TLAC.fd(TLAC.globals,2)
TLAC.lt(TLAC.globals)
TLAC.fd(TLAC.globals,2)