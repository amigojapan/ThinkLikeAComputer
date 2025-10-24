#!/usr/bin/python3
import TLACsimulator as TLAC






#user input example

#initialize turtle position
TLAC.teleportTurtleTo(TLAC.globals,4,9)
TLAC.orderUser(TLAC.globals,"put turtle at top left of the board")
TLAC.simulateUserInputTeleportTurtleTo(TLAC.globals,0,0)
savedX=TLAC.globals.turtle.X
savedY=TLAC.globals.turtle.Y
TLAC.orderUser(TLAC.globals,"put turtle at top bottom right of the board")
TLAC.simulateUserInputTeleportTurtleTo(TLAC.globals,9,9)
TLAC.teleportTurtleTo(TLAC.globals, savedX, savedY)
