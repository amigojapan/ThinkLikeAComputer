#!/usr/bin/python3
import TLACsimulator as TLAC

#board setup
#TLAC.setInitialTurtlePositionTo(TLAC.globals,4,9)

#print("initial board:")
#TLAC.printBoard(TLAC.globals)

#loopy library import, name it l
import TLACloopyLib as l

# ------------------------------------------------------------------
# Global container used by the loop bodies
# ------------------------------------------------------------------
class TableGlobals:
    def __init__(self):
        self.i = 0          # current outer-loop value
        self.j = 0          # current inner-loop value
        self.line = ""      # accumulated text for one row

globals = TableGlobals()

# ------------------------------------------------------------------
# Helper: equality condition (used by both loops)
# ------------------------------------------------------------------
def eq(n1, n2):
    return l.conditional(n1, l.op("=="), n2)
l.globals.condition = eq                   # termination condition

# ------------------------------------------------------------------
# Inner-loop body – compute i*j and append to the current line
# ------------------------------------------------------------------
def inner_body(j):
    product = globals.i * j
    globals.line += "\t" + str(globals.i) + " * " + str(j) + " = " + str(product)

# ------------------------------------------------------------------
# Outer-loop body – run the *inner* loop and then print the line
# ------------------------------------------------------------------
def outer_body(i):
    globals.i = i
    globals.line = ""

    # ---- inner loop (j from 1 to 3) --------------------------------
    l.globals.loop_body = inner_body       # body that fills the line
    l.forloop(1, 3, 1)                     # 1 … 3                         # restore outer state
    # ----------------------------------------------------------------

    print(globals.line)                    # row finished
    print()                                # newline after row

# ------------------------------------------------------------------
# Run the outer loop (i from 1 to 3)
# ------------------------------------------------------------------
l.globals.loop_body = outer_body           # body that runs inner loop
l.forloop(1, 3, 1)                         # 1 … 3