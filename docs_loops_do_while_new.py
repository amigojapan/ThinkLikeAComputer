#!/usr/bin/python3
import TLACsimulator as TLAC

# board setup
TLAC.setInitialTurtlePositionTo(TLAC.globals, 4, 9)

print("initial board:")
TLAC.printBoard(TLAC.globals)

# do_while example using standard Python
n1 = 1
n2 = 3
step = 1

# Python's equivalent of a do...while loop
while True:
    TLAC.promptUserToWriteDownOnPaper(TLAC.globals, "value of  n1 is "+str(n1))
    # 1. Execute the loop body
    TLAC.fd(TLAC.globals, n1)
    
    # 2. Apply the step decrement
    n1 += step
    
    # 3. Check the condition (Continue WHILE n1 > n2)
    # If the condition is False, break out of the loop
    if (n1 > n2): 
        break
TLAC.promptUserToWriteDownOnPaper(TLAC.globals, "n1 exceeds threshold")