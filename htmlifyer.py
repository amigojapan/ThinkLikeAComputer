import sys

class initGlobals():
    def __init__(self):
        self.lineNumber=None
        self.slots=None
        self.buffer=None

class Line():
    def __init__(self):
        self.indentNumber = None # Instance attribute
        self.kindOfInstruction = None # Instance attribute
        self.parameters = None # Instance attribute

def initCodeInfo(globals):
    list=[]
    for X in range(0,globals.lineNumber):
        line=Line()
        linesInfo.append(line)
    return linesInfo

def printBuffer(globals):
    globals.buffer = ""
    for ln in range(0, globals.lineNumber):  # column
        print(globals.linesInfo[ln].indentNumber) #implement this when I have parsed it,globals.linesInfo[ln].kindOfInstruction
        globals.buffer += "\n"

def readPythonFile(globals,boardFilename):
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
                if char=="\n":
                    index=index+1
                    continue
                elif char==" ":
                    for indent in range(1,4):
                        char = f.read(1)
                        if not char == " ":
                            sys.exit("Error in number of spaces per indent, on line number "+str(index)+" remember to only use 4 spaces per indent.")
                    else:
                        pass #todo:parse lline here
    except FileNotFoundError:
        print("Error: The file was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

#main
globals=initGlobals()
globals.slots=initCodeInfo(globals)
fileName=sys.argv[1]
if fileName=="" or fileName=="--help":
    sys.exit("first parameter is the name of the python file to parse")
else:
    readPythonFile(globals,fileName)
