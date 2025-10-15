#!/usr/bin/python3
import TLACsimulator as TLAC

#board setup
TLAC.teleportTurtleTo(4,9)
print("initial board:")
TLAC.printBoard(TLAC.globals)

#functions example
#the following is a function definition:
def Lay_Four_Eggs_In_Square_Pattern():
    TLAC.layEgg(TLAC.globals)
    TLAC.fd(TLAC.globals)
    TLAC.layEgg(TLAC.globals)
    TLAC.rt(TLAC.globals)
    TLAC.fd(TLAC.globals)
    TLAC.layEgg(TLAC.globals)
    TLAC.rt(TLAC.globals)
    TLAC.fd(TLAC.globals)
    TLAC.layEgg(TLAC.globals)
    #the following two turns are
    #to assure the turtle ends up in
    #the up pusition
    TLAC.rt(TLAC.globals)
    TLAC.rt(TLAC.globals)
TLAC.globals.turtle.X=0
print("printing board after teleport X")
TLAC.printBoard(TLAC.globals)
Lay_Four_Eggs_In_Square_Pattern()
TLAC.globals.turtle.X=5

print("printing board after teleport X")
TLAC.printBoard(TLAC.globals)
Lay_Four_Eggs_In_Square_Pattern()
TLAC.globals.turtle.X=8

print("printing board after teleport X")
TLAC.printBoard(TLAC.globals)
Lay_Four_Eggs_In_Square_Pattern()