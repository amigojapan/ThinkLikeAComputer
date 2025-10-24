#!/usr/bin/python3
import TLACsimulator as TLAC

#board setup
TLAC.setInitialTurtlePositionTo(TLAC.globals,4,9)

print("initial board:")
TLAC.printBoard(TLAC.globals)

#loopy library import, name it l
import TLACloopyLib as l

# foreach example
def loop_body(command):
    if command == "fd":
        TLAC.fd(TLAC.globals)
    if command == "rt":
        TLAC.rt(TLAC.globals)
    if command == "lt":
        TLAC.lt(TLAC.globals)
l.globals.loop_body = loop_body

my_commands_list = ['fd', 'fd', 'rt','fd', 'fd','lt', 'fd', 'fd']
l.foreach(my_commands_list, l.globals.loop_body)