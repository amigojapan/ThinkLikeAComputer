#!/usr/bin/python3
import TLACsimulator as TLAC

# board setup
TLAC.setInitialTurtlePositionTo(TLAC.globals, 4, 9)

print("initial board:")
TLAC.printBoard(TLAC.globals)

#For loop counting from 5 to 9 (inclusive)
for i in range(5, 10):
    TLAC.teleportTurtleTo(TLAC.globals, i, i)

TLAC.promptUserToWriteDownOnPaper(TLAC.globals, "counted form 5 to 9")