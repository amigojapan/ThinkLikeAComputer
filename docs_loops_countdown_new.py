#!/usr/bin/python3
import TLACsimulator as TLAC

# board setup
TLAC.setInitialTurtlePositionTo(TLAC.globals, 4, 9)

print("initial board:")
TLAC.printBoard(TLAC.globals)    

#Counting down  loop from 3 to 0
for i in range(3, -1, -1):
    TLAC.fd(TLAC.globals, i)