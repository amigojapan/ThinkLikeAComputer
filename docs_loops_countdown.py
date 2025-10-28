#!/usr/bin/python3
import TLACsimulator as TLAC

#board setup
TLAC.setInitialTurtlePositionTo(TLAC.globals,4,9)

print("initial board:")
TLAC.printBoard(TLAC.globals)

#countdown example
#loopy library import, name it l
import TLACloopyLib as l

def loop_body(n):
    TLAC.fd(TLAC.globals,n)

l.globals.loop_body = loop_body

l.countdown(3, 1)