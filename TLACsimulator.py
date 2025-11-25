#Think Like a Computer - simulator copyright 2025 Usmar A Padow
import sys
#increase recursion depth for the maze programs
sys.setrecursionlimit(5000)
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
        # Instance attributes
        self.containsEgg = False 
        self.diamond = False
        self.wall = False
        self.goal = False
        self.pyramidSize = False
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
                #print("globals.slots[index].containsEgg"+str(globals.slots[index].containsEgg))
                if globals.slots[index].containsEgg:
                    globals.board += "[o]"
                    continue
                elif globals.slots[index].diamond:
                    globals.board += "[X]"
                    continue
                elif globals.slots[index].wall:
                    globals.board += "[#]"
                    continue
                elif globals.slots[index].goal:
                    globals.board += "[G]"
                    continue
                elif (globals.slots[index].pyramidSize == 1):
                    #print("appending pyramid 1")
                    globals.board += "[1]"
                    continue
                elif globals.slots[index].pyramidSize == 2:
                    globals.board += "[2]"
                    continue
                elif globals.slots[index].pyramidSize == 3:
                    globals.board += "[3]"
                    continue
                elif globals.slots[index].pyramidSize == 4:
                    globals.board += "[4]"
                    continue
                elif globals.slots[index].pyramidSize == 5:
                    globals.board += "[5]"
                    continue
                #print(str(globals.slots[index].pyramidSize))
                globals.board += "[ ]"
        globals.board += "\n"
    #print(globals.board)

globals.slots = initSlots(globals)
globals.turtle = initTurtle()
#initBoard(globals)

def readBoardFromFile(globals,boardFilename):
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
                elif char=="1":
                    print("pyramid 1 found")
                    globals.slots[index].pyramidSize = 1
                elif char=="2":
                    print("pyramid 2 found")
                    globals.slots[index].pyramidSize = 2
                elif char=="3":
                    print("pyramid 3 found")
                    globals.slots[index].pyramidSize = 3
                elif char=="4":
                    print("pyramid 4 found")
                    globals.slots[index].pyramidSize = 4
                elif char=="5":
                    print("pyramid 5 found")
                    globals.slots[index].pyramidSize = 5
                elif char=="G":
                    globals.slots[index].goal = True
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
    #print("globals.slots[index].containsEgg:"+str(globals.slots[1].containsEgg))
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


def clearPyramidNumber(globals,pyramidNumber):
    #print("len(globals.slots):"+str(len(globals.slots)))
    pyramidFound=False
    for index in range(0,len(globals.slots)-1):
        if globals.slots[index].pyramidSize==pyramidNumber:
            globals.slots[index].pyramidSize = False
            pyramidFound=True
            break
    if pyramidFound==False:
        sys.exit("Error, tried to clear pyramid number " + str(pyramidNumber) + " but it does not exist on this board")
    
def simulateUserInputTeleportPyramidTo(globals,pyramidNumber,_x,_y):
    #globals.MoveNumber=globals.MoveNumber+1
    print("Simulating user move Pyramid "+str(pyramidNumber)+" to X:"+str(_x-1)+" Y:"+str(_y-1))
    clearPyramidNumber(globals,pyramidNumber)    
    #set pyramid on index
    X = _x
    Y = _y
    W = globals.W
    H = globals.H
    index = (Y) * W + (X)
    globals.slots[index].pyramidSize = pyramidNumber
    executeMove(globals)

def peekPyramidThere(globals,_x,_y):
    #globals.MoveNumber=globals.MoveNumber+1
    print("is X:"+str(_x)+" Y:"+str(_y)+" a pyramid?")
    #set pyramid on index
    X = _x+1
    Y = _y+1
    W = globals.W
    H = globals.H
    index = (Y-1) * W + (X-1)
    if globals.slots[index].pyramidSize:
        print(" Yes, it is pyramid size:"+str(globals.slots[index].pyramidSize))
        return globals.slots[index].pyramidSize, X-1, Y-1
    else:
        print("No, it is not")
        return "not found", X-1, Y-1
    executeMove(globals)
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


def amILayingOnTheGoalFlag(gloabls):
    index = globals.turtle.Y * globals.W + globals.turtle.X
    if globals.slots[index].goal==True:
        print("am I laying on the Goal flag?: Yes")
        executeMove(globals)
        return True
    else:
        print("am I laying on the Goal flag?: No")
        executeMove(globals)
        return False

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

def testIfICanProceed(globals, slots=1):
    X = globals.turtle.X
    Y = globals.turtle.Y
    W = globals.W
    H = globals.H

    # Calculate target position
    if globals.turtle.direction == "^":
        if Y - slots < 0:  # Check boundary first
            print("2Can I pass?: No (out of bounds)")
            executeMove(globals)
            return False
        index = (Y - slots) * W + X
    elif globals.turtle.direction == "<":
        if X - slots < 0:
            print("4Can I pass?: No (out of bounds)")
            executeMove(globals)
            return False
        index = Y * W + (X - slots)
    elif globals.turtle.direction == "V":
        if Y + slots > H - 1:
            print("6Can I pass?: No (out of bounds)")
            executeMove(globals)
            return False
        index = (Y + slots) * W + X
    elif globals.turtle.direction == ">":
        if X + slots > W - 1:
            print("8Can I pass?: No (out of bounds)")
            executeMove(globals)
            return False
        index = Y * W + (X + slots)
    else:
        print("Invalid direction")
        executeMove(globals)
        return False

    # Ensure index is within slots range
    if index < 0 or index >= W * H:
        print(f"Can I pass?: No (invalid index {index})")
        executeMove(globals)
        return False

    # Check for wall
    if globals.slots[index].wall:
        print(f"Can I pass?: No (wall at index {index})")
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