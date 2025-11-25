#!/usr/bin/python3
import TLACsimulator as TLAC

#board setup
#TLAC.readBoardFromFile(TLAC.globals,"algorithm-pyramids1.txt")
#TLAC.teleportTurtleTo(TLAC.globals,4,9)
#print("initial board:")
#TLAC.printBoard(TLAC.globals)

#board setup
TLAC.readBoardFromFile(TLAC.globals,"algorithm-pyramids1.txt")
#seems you need teleport turtle to fill the board for some reason I dont understand?
TLAC.teleportTurtleTo(TLAC.globals,4,9)
print("initial board:")
#TLAC.simulateUserInputTeleportPyramidTo(TLAC.globals,3,1,1)
TLAC.printBoard(TLAC.globals)

#insertion sort pyramids 1
#import TLACloopyLib as l
import sys
def findNextElement(globals):
    for x in range(0,9+1,1):
        print("Ax:"+str(x))
        value, _x, _y=TLAC.peekPyramidThere(globals,x,2)
        if value!="not found":
            return  value, _x, _y
    return None
def findNextBottom(globals):
    for x in range(9, 0-1, -1):
        print("Bx:"+str(x))            #  value:+str(value))
        value, _x, _y=TLAC.peekPyramidThere(TLAC.globals,x,4)
        if value!="not found":
            return  value, _x, _y
    return None
for col in range(0,5):#the number of pyramids
    print("columb"+str(col))
    pyramidNumber, x, y = findNextElement(TLAC.globals)
    #lower next elemen
    print("HERE pyr "+str(pyramidNumber))
    TLAC.simulateUserInputTeleportPyramidTo(TLAC.globals,pyramidNumber,x,y+1)
    TLAC.simulateUserInputTeleportPyramidTo(TLAC.globals,pyramidNumber,col,4)
    pyramidNumberBottom, x, y = findNextBottom(TLAC.globals)
    #    if pyramidNumberBottom<pyramidNumber:
    #        pass
            #SWAP pyramids
            #TLAC.simulateUserInputTeleportPyramidTo(TLAC.globals,pyramidNumber,9,4)
            #TLAC.simulateUserInputTeleportPyramidTo(TLAC.globals,pyramidNumber,0,3)
            #TLAC.simulateUserInputTeleportPyramidTo(TLAC.globals,pyramidNumber,x2,4)
 