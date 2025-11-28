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
for col in range(0, 5):  # the number of pyramids
    print("column " + str(col))
    pyramidNumber, x, y = findNextElement(TLAC.globals)
    print("HERE pyr " + str(pyramidNumber))
    # No need for temp move to y+1; teleport directly to end of sorted prefix
    TLAC.simulateUserInputTeleportPyramidTo(TLAC.globals, pyramidNumber, col, 4)
    
    # Now bubble the new pyramid left until the prefix (0 to col) is sorted
    current = col
    while current > 0:
        # Peek left neighbor and current
        left_value, left_x, left_y = TLAC.peekPyramidThere(TLAC.globals, current - 1, 4)
        current_value, current_x, current_y = TLAC.peekPyramidThere(TLAC.globals, current, 4)
        
        if left_value == "not found" or current_value == "not found":
            print("Error: Missing pyramid during bubble")
            break
        
        if left_value <= current_value:
            break  # Sorted position found
        
        # Swap left and current using temp (0,0)
        print("SWAP pyramids " + str(left_value) + " and " + str(current_value))
        TLAC.simulateUserInputTeleportPyramidTo(TLAC.globals, current_value, 0, 0)  # Temp move current
        TLAC.simulateUserInputTeleportPyramidTo(TLAC.globals, left_value, current, 4)  # Move left to current pos
        TLAC.simulateUserInputTeleportPyramidTo(TLAC.globals, current_value, current - 1, 4)  # Move temp to left pos
        
        current -= 1

# Optional: Print final board after sorting
print("Final sorted board:")
TLAC.printBoard(TLAC.globals)