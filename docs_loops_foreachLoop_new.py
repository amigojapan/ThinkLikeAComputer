#!/usr/bin/python3
import TLACsimulator as TLAC

# board setup
TLAC.setInitialTurtlePositionTo(TLAC.globals, 4, 9)

print("initial board:")
TLAC.printBoard(TLAC.globals)

# Standard Python iteration (foreach)
my_commands_list = ['fd', 'fd', 'rt', 'fd', 'fd', 'lt', 'fd', 'fd']

# Loop directly through each command in the list
for command in my_commands_list:
    if command == "fd":
        TLAC.fd(TLAC.globals)
    elif command == "rt":
        TLAC.rt(TLAC.globals)
    elif command == "lt":
        TLAC.lt(TLAC.globals)