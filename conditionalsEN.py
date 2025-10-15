#!/usr/bin/python3
import TLACsimulator as TLAC

#board setup
TLAC.teleportTurtleTo(4,9)
print("initial board:")
TLAC.printBoard(TLAC.globals)

#conditionals example
#green lines like these are called 'comments'
#and do not affect the execution of the program
#but I want you to read them for now
if X>3:
    #since X is more than 3,
    #this block(the block surrounded by the
    #pink rectangle) of code will be executed 
    fd()
if X<3:
    #since X is not less than,
    #this block of code won't be executed
    fd()
X=2
TLAC.printBoard(TLAC.globals)
#this assignment statement teleports
#the turtle to X slot 2(two slots
#from the left of the board)
if X<3:
    #now after the last assignment statement
    #X is less than 3, so the following block
    #of code gets executed.
    fd()