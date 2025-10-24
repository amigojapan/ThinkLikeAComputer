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

# Initialize globals at module level
globals = initGlobals()
globals.W = 10
globals.H = 10

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

def initBoard(globals):
    globals.board = ""
    for y in range(0, globals.H):  # row
        for x in range(0, globals.W):  # column
            if x == globals.turtle.X and y == globals.turtle.Y:
                globals.board += "[" + globals.turtle.direction + "]"
            else:
                index = y * globals.W + x
                if globals.slots[index].containsEgg:
                    globals.board += "[o]"
                    continue
                elif globals.slots[index].diamond:
                    globals.board += "[X]"
                    continue
                elif globals.slots[index].wall:
                    globals.board += "[#]"
                    continue
                globals.board += "[ ]"
        globals.board += "\n"
    #print(globals.board)

globals.slots = initSlots(globals)
globals.turtle = initTurtle()
initBoard(globals)

def readBoaedFromFile(globals,boardFilename):
    index=0
    print("reading board file")
    try:
        with open(boardFilename, 'r', encoding='utf-8') as f:
            while True:
                char = f.read(1)
                if not char:
                    # End of file reached
                    print("")
                    break
                print(".", end='') # Process or print the character
                if char=="[" or char=="]" or char=="\n":
                    #index=index+1
                    continue
                elif char=="o":
                    globals.slots[index].containsEgg = True
                elif char=="X":
                    globals.slots[index].diamond = True
                elif char=="#":
                    globals.slots[index].wall = True
                index=index+1
    except FileNotFoundError:
        print("Error: The file was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def exitIfTurtleOutOfBounds(globals):
    if(globals.turtle.X>globals.W or globals.turtle.X<0 or globals.turtle.Y>globals.H or globals.turtle.Y<0):
        sys.exit("Error, turtle went outside of board, program terminated.")
def printBoard(globals):
    print(globals.board)

def updateBoard(globals):
    initBoard(globals)
    exitIfTurtleOutOfBounds(globals)
    "Updating board"
    #print("Move Number:"+str(globals.MoveNumber))
    #printBoard(globals)

def executeMove(globals):
    updateBoard(globals)
    exitIfTurtleOutOfBounds(globals)
    print("Move Number:"+str(globals.MoveNumber))
    printBoard(globals)

def executeMoveDontPrintBoard(globals):
    updateBoard(globals)
    exitIfTurtleOutOfBounds(globals)
    print("Move Number:"+str(globals.MoveNumber))


def teleportTurtleTo(globals,_x,_y):
    globals.MoveNumber=globals.MoveNumber+1
    print("Teleporting to X:"+str(_x)+" Y:"+str(_y))
    globals.turtle.X=_x
    globals.turtle.Y=_y
    executeMove(globals)

def setInitialTurtlePositionTo(globals,_x,_y):
    print("setting initial turtle position to X:"+str(_x)+" Y:"+str(_y))
    globals.turtle.X=_x
    globals.turtle.Y=_y
    updateBoard(globals)
    #executeMove(globals)

def simulateUserInputTeleportTurtleTo(globals,_x,_y):
    #globals.MoveNumber=globals.MoveNumber+1
    print("Simulating user move Teleporting to X:"+str(_x)+" Y:"+str(_y))
    globals.turtle.X=_x
    globals.turtle.Y=_y
    executeMove(globals)

def promptUserToWriteDownOnPaper(globals,prompt):
    globals.MoveNumber=globals.MoveNumber+1
    executeMoveDontPrintBoard(globals)
    print("USER!, WRITE DOWN THE FOLLOWING ON PAPER!:\n\""+prompt+"\"")

#move functions
def fd(globals,slots=1):
    print("moved foward "+str(slots)+" slots")
    globals.MoveNumber+=1
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

def orderUser(gloabls,prompt):
    print("USER DO THIS!:"+prompt)
    globals.MoveNumber=globals.MoveNumber+1
    #executeMove(globals)

if __name__ == "__main__":
    globals=initGlobals()
    globals.W=10
    globals.H=10
    globals.slots=initSlots(globals)
    globals.turtle=initTurtle()
    initBoard(globals)
#-(done)add a function to read a board form a text file
#   should be easier to design boards this way
#-add collision detection for walls and diamonds, including stuff like fd(5)
#-(done,very bad results)try pip3 install pyflowchart
#-(done with sed, made a bash file that converts all the programs)try pcpp, C preprocessor  for python 
#   https://pypi.org/project/pcpp/
#   I think I can symplify the code with stuff like hiding calls to the TLAC. library and also all the globals sending
#   possibly can be used to make html flocharts fo the code?