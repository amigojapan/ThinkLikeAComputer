#!/usr/bin/python3
import TLACsimulator as TLAC

#board setup
#TLAC.teleportTurtleTo(TLAC.globals,4,9)
print("initial board:")
TLAC.printBoard(TLAC.globals)


#algo insertion sort
import TLACloopyLib as l

class SortGlobals:
    def __init__(self):
        #None values will be set later
        self.arr = None
        self.i = 0
        self.j = 0
        self.key = None

s_globals = SortGlobals()
s_globals.arr=["Pyramid3", "Pyramid1", "Pyramid4", "Pyramid5", "Pyramid2"]

def eq(n1, n2):
    return l.conditional(n1, l.op("=="), n2)

l.globals.condition = eq

def inner_body(current_j):
    s_globals.arr[current_j + 1] = s_globals.arr[current_j]
    s_globals.j = current_j - 1

def inner_condition(current_j, unused):
    next_j = current_j - 1
    if next_j >= 0 and s_globals.arr[next_j] > s_globals.key:
        # continue
        return False
    else:
        # stop
        return True

# Outer loop body
def outer_body(i):
    s_globals.i = i
    s_globals.key = s_globals.arr[i]
    s_globals.j = i - 1
    # Run inner loop if initial condition met
    if not inner_condition(s_globals.j + 1, None):
        l.globals.loop_body = inner_body
        l.globals.condition = inner_condition
        l.do_while(s_globals.j, 0, 1)
    # Insert key
    s_globals.arr[s_globals.j + 1] = s_globals.key

# Set outer loop_body
l.globals.loop_body = outer_body

# Run outer loop: i from 1 to length of array -1
l.forloop(1, len(s_globals.arr) - 1, 1)

# Output the sorted list
print(s_globals.arr)