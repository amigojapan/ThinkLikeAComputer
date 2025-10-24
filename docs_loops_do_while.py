#!/usr/bin/python3
import TLACsimulator as TLAC

#board setup
TLAC.setInitialTurtlePositionTo(TLAC.globals,4,9)

print("initial board:")
TLAC.printBoard(TLAC.globals)

#loopy library import, name it l
import TLACloopyLib as l

# do_while example
def loop_body(n):
    TLAC.fd(TLAC.globals,n)
l.globals.loop_body = loop_body

def condition(n1, n2):
    return l.conditional(n1, l.op(">"), n2)
l.globals.condition = condition

l.do_while(1, 3, -1)
TLAC.promptUserToWriteDownOnPaper(TLAC.globals,"n1 exceeds threshold")