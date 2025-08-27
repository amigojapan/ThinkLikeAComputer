#!/usr/bin/python3
import sys

def count_lines(filepath):
    try:
        with open(filepath, 'r') as file:
            line_count = 0
            for line in file:
                line_count += 1
            return line_count
    except FileNotFoundError:
        print(f"Error: The file '{filepath}' was not found.")
        return -1  # Or raise an exception, depending on desired error handling
    except Exception as e:
        print(f"An error occurred: {e}")
        return -1

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

def initCodeInfo(globals,fileName):
    globals.lineNumber=count_lines(fileName)
    linesInfo=[]
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

def error1quit():
    sys.exit("first parameter is the name of the python file to parse")

#main
globals=initGlobals()
if (len(sys.argv)<2):
    error1quit()    
else:
    if sys.argv[1]=="--help":
        error1quit()
    fileName=sys.argv[1]
    globals.slots=initCodeInfo(globals,fileName)
    readPythonFile(globals,fileName)
