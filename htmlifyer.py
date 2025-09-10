#!/usr/bin/python3
import sys

def count_lines(filepath):
    try:
        with open(filepath, 'r') as file:
            return sum(1 for line in file) + 2  # +2 to avoid EOF issues
    except FileNotFoundError:
        print(f"Error: The file '{filepath}' was not found.")
        return -1
    except Exception as e:
        print(f"An error occurred: {e}")
        return -1

class initGlobals:
    def __init__(self):
        self.fileLineCount = None
        self.slots = None
        self.buffer = None

class Line:
    def __init__(self):
        self.indentNumber = 0
        self.instruction = None
        self.parameters = None

def initCodeInfo(globals, fileName):
    globals.fileLineCount = count_lines(fileName)
    linesInfo = [Line() for _ in range(globals.fileLineCount)]
    return linesInfo

def readPythonFile(globals, boardFilename):
    currentLine = 1
    print("reading python file...")
    try:
        with open(boardFilename, 'r', encoding='utf-8') as f:
            for line in f:
                if currentLine >= globals.fileLineCount:
                    break
                # Count leading spaces to determine indent level (4 spaces = 1 indent)
                indent_count = 0
                for char in line:
                    if char == " ":
                        indent_count += 1
                    else:
                        break
                globals.slots[currentLine].indentNumber = indent_count // 4
                globals.slots[currentLine].instruction = line.strip()
                print(f"Line {currentLine}, indent: {globals.slots[currentLine].indentNumber}, instruction: {globals.slots[currentLine].instruction}")
                currentLine += 1
            print("EOF reached.")
    except FileNotFoundError:
        print("Error: The file was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def createHTML(globals):
    HTML = ""
    print("creating HTML...")
    for currentLine in range(1, globals.fileLineCount):
        if not globals.slots[currentLine].instruction:
            continue  # Skip empty lines
        # Add ----> for each indent level
        HTML += "---->" * globals.slots[currentLine].indentNumber
        HTML += globals.slots[currentLine].instruction
        HTML += "<BR>\n"
        print(f"Line {currentLine}, indent: {globals.slots[currentLine].indentNumber}, instruction: {globals.slots[currentLine].instruction}")
    print(HTML)

def error1quit():
    sys.exit("first parameter is the name of the python file to parse")

# main
globals = initGlobals()
if len(sys.argv) < 2:
    error1quit()
else:
    if sys.argv[1] == "--help":
        error1quit()
    fileName = sys.argv[1]
    globals.slots = initCodeInfo(globals, fileName)
    readPythonFile(globals, fileName)
    createHTML(globals)