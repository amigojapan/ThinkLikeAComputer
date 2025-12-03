#board setup
readBoardFromFile("algorithm-pyramids1.txt")
#seems you need teleport turtle to fill the board for some reason I dont understand?
teleportTurtleTo(4,9)
print("initial board:")
#simulateUserInputTeleportPyramidTo(3,1,1)
printBoard()

#insertion sort pyramids 1
#import TLACloopyLib as l
import sys
def findNextElement(globals):
    for x in range(0,9+1,1):
        print("Ax:"+str(x))
        value, _x, _y=peekPyramidThere(x,2)
        if value!="not found":
            return  value, _x, _y
    return None
def findNextBottom(globals):
    for x in range(9, 0-1, -1):
        print("Bx:"+str(x))            #  value:+str(value))
        value, _x, _y=peekPyramidThere(x,4)
        if value!="not found":
            return  value, _x, _y
    return None
# the number of pyramids is 5
for col in range(0, 5):
    print("column " + str(col))
    pyramidNumber, x, y = findNextElement()
    print("HERE pyr " + str(pyramidNumber))
    # No need for temp move to y+1; teleport directly to end of sorted prefix
    simulateUserInputTeleportPyramidTo( pyramidNumber, col, 4)
    
    # Now bubble the new pyramid left until the prefix (0 to col) is sorted
    current = col
    while current > 0:
        # Peek left neighbor and current
        left_value, left_x, left_y = peekPyramidThere( current - 1, 4)
        current_value, current_x, current_y = peekPyramidThere( current, 4)
        
        if left_value == "not found" or current_value == "not found":
            print("Error: Missing pyramid during bubble")
            break
        
        if left_value <= current_value:
            break  # Sorted position found
        
        # Swap left and current using temp (0,0)
        print("SWAP pyramids " + str(left_value) + " and " + str(current_value))
        simulateUserInputTeleportPyramidTo( current_value, 0, 0)  # Temp move current
        simulateUserInputTeleportPyramidTo( left_value, current, 4)  # Move left to current pos
        simulateUserInputTeleportPyramidTo( current_value, current - 1, 4)  # Move temp to left pos
        
        current -= 1

# Optional: Print final board after sorting
print("Final sorted board:")
printBoard()