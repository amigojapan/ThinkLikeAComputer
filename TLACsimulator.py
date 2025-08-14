#Think Like a Computer - simulator copyright 2025 Usmar A Padow
import sys

class initGlobals:
    def __init__(self):
        self.MoveNumber = 0 # Instruction Pointer
        self.board=""
        self.W=None
        self.H=None
        self.slots=None
        self.turtle=None

class Cell:
    def __init__(self):
        self.containsEgg = False # Instance attribute
        self.diamond = False # Instance attribute
        self.wall = False # Instance attribute

class initTurtle:
    def __init__(self):
        self.X = 0 # Instance attribute
        self.Y = 0 # Instance attribute
        self.direction = "^" #UP Instance attribute

def initSlots(globals):
    slots=[]
    for Y in range(0,globals.H):
        for X in range(0,globals.W):
            cell=Cell()
            slots.append(cell)
    return slots

def printBoard(globals):
    globals.board = ""
    for y in range(0, globals.H):  # row
        for x in range(0, globals.W):  # column
            if x == globals.turtle.X and y == globals.turtle.Y:
                globals.board += "[" + globals.turtle.direction + "]"
            else:
                index = y * globals.W + x
                if globals.slots[index].containsEgg:
                    globals.board += "[o]"
                else:
                    globals.board += "[ ]"
        globals.board += "\n"
    print(globals.board)

def executeMove(globals):
    if(globals.turtle.X>globals.W or globals.turtle.X<0 or globals.turtle.Y>globals.H or globals.turtle.Y<0):
        sys.exit("Error, turtle went outside of board, program terminated.")
    print("Move Number:"+str(globals.MoveNumber))
    printBoard(globals)

def teleportTurtleTo(x,y):
    globals.turtle.X=4
    globals.turtle.Y=9

#move functions
def fd(globals,slots=1):
    print("moved foward "+str(slots)+" slots")
    globals.MoveNumber=globals.MoveNumber+1
    if globals.turtle.direction == "^":   # up
        globals.turtle.Y -= slots
    elif globals.turtle.direction == "V": # down
        globals.turtle.Y += slots
    elif globals.turtle.direction == "<": # left
        globals.turtle.X -= slots
    elif globals.turtle.direction == ">": # right
        globals.turtle.X += slots
    executeMove(globals)

def lt(globals):
    print("turned left")
    globals.MoveNumber=globals.MoveNumber+1
    if globals.turtle.direction=="^":
        globals.turtle.direction="<"
    elif globals.turtle.direction=="<":
        globals.turtle.direction="V"
    elif globals.turtle.direction=="V":
        globals.turtle.direction=">"
    elif globals.turtle.direction==">":
        globals.turtle.direction="^"
    executeMove(globals)

def rt(globals):
    print("turned right")
    globals.MoveNumber=globals.MoveNumber+1
    if globals.turtle.direction=="^":
        globals.turtle.direction=">"
    elif globals.turtle.direction==">":
        globals.turtle.direction="V"
    elif globals.turtle.direction=="V":
        globals.turtle.direction="<"
    elif globals.turtle.direction=="<":
        globals.turtle.direction="^"
    executeMove(globals)

def layEgg(gloabls):
    print("layed egg")
    index = globals.turtle.Y * globals.W + globals.turtle.X
    globals.slots[index].containsEgg=True
    executeMove(globals)

def amILayingOnAnEgg(gloabls):
    index = globals.turtle.Y * globals.W + globals.turtle.X
    if globals.slots[index].containsEgg==True:
        print("am I laying on an egg?: Yes")
        executeMove(globals)
        return True
    else:
        print("am I laying on an egg?: No")
        executeMove(globals)
        return False

def testIfICanProceed(gloabls,slots=1):
    if globals.turtle.direction=="^":
        if globals.turtle.Y-slots<0:
            print("Can I pass?: No")
            executeMove(globals)
            return False
    elif globals.turtle.direction=="<":
        if globals.turtle.X-slots<0:
            print("Can I pass?: No")
            executeMove(globals)
            return False
    elif globals.turtle.direction=="V":
        if globals.turtle.Y+slots>globals.H-1:
            print("Can I pass?: No")
            executeMove(globals)
            return False
    elif globals.turtle.direction==">":
        if globals.turtle.X+slots>globals.W-1:
            print("Can I pass?: No")
            executeMove(globals)
            return False
    print("Can I pass?: Yes")
    executeMove(globals)
    return True

def end(gloabls):
    print("Program edned withought errors.")
    print("Final state board:")
    printBoard(globals)
    sys.exit()

globals=initGlobals()
globals.W=10
globals.H=10
globals.slots=initSlots(globals)
globals.turtle=initTurtle()
#add a function to read a board form a text file
#   should be easier to design boards this way