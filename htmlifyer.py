#!/usr/bin/python3
import sys
#sudo apt install  python3-wcwidth
import wcwidth
#wcwidth.wcswidth(text)
#constants
language="jp"
if language=="en":
    constFunctCall="Function call "
    constFunctCallFull=" Function call "
    constFunctDef="Function definition"
    constFunctDefFull=" Function definition "
    constFd="fd"
    constFdSimple="Turtle Move Foward"
    constRt="rt"
    constRtSimple="Trun Turtle Right"
    constLt="lt"
    constLtSimple="Trun Turtle Left"
    constLayEgg="layEgg"
    constLayEggSimple="Turtle lays egg underneeth itself"
    constEnd="end"
    constEndSimple="End Program"
    constIf="if"
    constIfSimple="if"
    constNot="not"
    constNotSimple="not"
    constThen="then"
    constThenSimple="then"

elif language=="jp":
    constFunctCall="関数を呼び出す: "
    constFunctCallFull=" 関数を呼び出す: "
    constFunctDef="関数定義:"
    constFunctDefFull=" 関数定義: "
    constFd="fd"
    constFdSimple="亀さんが前に進む"
    constRt="rt"
    constRtSimple="亀さんが右に曲がる"
    constLt="lt"
    constLtSimple="亀さんが右に左がる"
    constLayEgg="layEgg"
    constLayEggSimple="亀さんが自分の下に卵を生む"
    constEnd="end"
    constEndSimple="プログラム終了"
    constIf="if"
    constIfSimple="もし"
    constNot="not"
    constNotSimple="でなければ"
    constThen="then"
    constThenSimple="、次に"
    constTurtleDir="turtledirection"
    constTurtleDirSimplified="亀さんの向き"
    constEQ="=="
    constEQSimplified="＝"
    constTurtleUp='"^"'
    constTurtleUpSimplified="上"
    constTurtleRight='">"'
    constTurtleRightSimplified="右"
    constTurtleLeft='"<"'
    constTurtleLeftSimplified="左"
    constTurtleDown='"V"'
    constTurtleDownSimplified="下"
    constTurtleCanProceedFoward="testIfICanProceed()"
    constTurtleCanProceedFowardSimplified="亀さんが前に進められる"
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
                globals.slots[currentLine].indentNumber = int(indent_count // 4)
                globals.slots[currentLine].instruction = line.strip()
                print(f"Line {currentLine}, indent: {globals.slots[currentLine].indentNumber}, instruction: {globals.slots[currentLine].instruction}")
                currentLine += 1
            print("EOF reached.")
    except FileNotFoundError:
        print("Error: The file was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def createoutput(globals): 
    output =""
    #output +='<output lang="jp">\n'
    #output +='<head>\n'
    #output +='    <meta charset="UTF-8">\n'
    #output +='</head>\n'
    #output +='<body style="background-color:powderblue;">\n'
    print("creating output...")
    for currentLine in range(1, globals.fileLineCount):
        if not globals.slots[currentLine].instruction:
            continue  # Skip empty lines
        first_character = globals.slots[currentLine].instruction[0]
        if first_character=="#":#this instruction is a comment
            rest_of_string = globals.slots[currentLine].instruction[1:]
            comment = rest_of_string
            output += " "+"_" * wcwidth.wcswidth(comment)
            output += "<BR>\n"
            output += "/"+comment+"/"
            output += "<BR>\n"
            output += " "+"-" * wcwidth.wcswidth(comment)
            output += "<BR>\n"
            continue 
        # Get the first three characters
        first_three_chars = globals.slots[currentLine].instruction[:3]
        if first_three_chars=="def":#this instruction is a comment
            # Get the rest of the string
            rest_of_string = globals.slots[currentLine].instruction[3:]
            index_of_paren = rest_of_string.find('(')
            if index_of_paren != -1:
                functionName = rest_of_string[:index_of_paren]
                from_paren_onwards = rest_of_string[index_of_paren:]  # Fix: Use rest_of_string
                index_of_closing_paren = from_paren_onwards.find(')')
                if index_of_closing_paren == -1:
                    # If no parenthesis is found, the entire string is "before_paren"
                    sys.exit("Uneven parenthesys on line: " + str(currentLine))                
                else:
                    parameters = from_paren_onwards[1:index_of_closing_paren]
                if not parameters == "":
                    output += " "+"_" * wcwidth.wcswidth(constFunctDefFull + functionName + " parameters: " + parameters)
                    output += "<BR>\n"
                    output += "| "
                    output += constFunctDef+functionName
                    output += " parameters: " + parameters
                    output += " |"
                    output += "<BR>\n"
                    output += " "+"-" * wcwidth.wcswidth(constFunctDefFull + functionName + " parameters: " + parameters)
                    output += "<BR>\n"
                    continue
                else:
                    output += " "+"_" * wcwidth.wcswidth(constFunctDefFull + functionName)
                    output += "<BR>\n"
                    output += "| "
                    output += constFunctDef+functionName
                    output += " |"
                    output += "<BR>\n"
                    output += " "+"-" * wcwidth.wcswidth(constFunctDefFull + functionName)
                    output += "<BR>\n"
                    continue
            else:
                # If no parenthesis is found, the entire string is "before_paren"
                sys.exit("error while parsing python file, open parenthesis not found after function name on line: " + str(currentLine))
        first_three_chars = globals.slots[currentLine].instruction[:3]
        if first_three_chars=="if ":#this instruction is a comment
            #rest_of_string = globals.slots[currentLine].instruction[3:]
            simplifiedAndTrsanlsated = globals.slots[currentLine].instruction.replace(":", " then ")
            simplifiedAndTrsanlsated = simplifiedAndTrsanlsated.replace(constIf, constIfSimple)
            simplifiedAndTrsanlsated = simplifiedAndTrsanlsated.replace(constThen, "")
            if language=="jp":
                if constNot in simplifiedAndTrsanlsated:#if it contains "not"
                    simplifiedAndTrsanlsated = simplifiedAndTrsanlsated.replace(constNot, "")
                    simplifiedAndTrsanlsated = simplifiedAndTrsanlsated+constNotSimple
                    simplifiedAndTrsanlsated = simplifiedAndTrsanlsated.replace(constThen, constThenSimple)
            simplifiedAndTrsanlsated = simplifiedAndTrsanlsated.replace(constTurtleDir, constTurtleDirSimplified)
            simplifiedAndTrsanlsated = simplifiedAndTrsanlsated.replace(constEQ, constEQSimplified)
            simplifiedAndTrsanlsated = simplifiedAndTrsanlsated.replace(constTurtleUp, constTurtleUpSimplified)
            simplifiedAndTrsanlsated = simplifiedAndTrsanlsated.replace(constTurtleLeft, constTurtleLeftSimplified)
            simplifiedAndTrsanlsated = simplifiedAndTrsanlsated.replace(constTurtleRight, constTurtleRightSimplified)
            simplifiedAndTrsanlsated = simplifiedAndTrsanlsated.replace(constTurtleDown, constTurtleDownSimplified)
            simplifiedAndTrsanlsated = simplifiedAndTrsanlsated.replace(constTurtleCanProceedFoward, constTurtleCanProceedFowardSimplified)
            if language=="jp":
                simplifiedAndTrsanlsated = simplifiedAndTrsanlsated+constThenSimple
            else:
                simplifiedAndTrsanlsated = simplifiedAndTrsanlsated+" "+constThenSimple                 
            output += "     " * globals.slots[currentLine].indentNumber
            output += " "+"_" * wcwidth.wcswidth(simplifiedAndTrsanlsated)
            output += "<BR>\n"
            output += "---->" * globals.slots[currentLine].indentNumber
            output += "| "
            output += simplifiedAndTrsanlsated
            output += " |"
            output += "<BR>\n"
            output += "     " * globals.slots[currentLine].indentNumber
            output += " "+"-" * wcwidth.wcswidth(simplifiedAndTrsanlsated)
            output += "<BR>\n"
            continue
        if globals.slots[currentLine].instruction.endswith(")"):
            # Get the rest of the string
            rest_of_string = globals.slots[currentLine].instruction
            index_of_paren = rest_of_string.find('(')
            if index_of_paren != -1:
                functionName = rest_of_string[:index_of_paren]
                if functionName==constFd:
                    functionName=constFdSimple
                if functionName==constRt:
                    functionName=constRtSimple
                if functionName==constLt:
                    functionName=constLtSimple
                if functionName==constLayEgg:
                    functionName=constLayEggSimple
                if functionName==constEnd:
                    functionName=constEndSimple
                from_paren_onwards = rest_of_string[index_of_paren:]  # Fix: Use rest_of_string
                index_of_closing_paren = from_paren_onwards.find(')')
                if index_of_closing_paren == -1:
                    # If no parenthesis is found, the entire string is "before_paren"
                    sys.exit("Uneven parenthesys on line: " + str(currentLine))                
                else:
                    index_of_closing_paren = globals.slots[currentLine].instruction.find(')')
                    parameters = globals.slots[currentLine].instruction[index_of_paren+1:index_of_closing_paren]
                if not parameters == "":
                    output += "     " * globals.slots[currentLine].indentNumber
                    output += " "+"_" * wcwidth.wcswidth(constFunctCallFull + functionName + " parameters: " + parameters)
                    output += "<BR>\n"
                    output += "---->" * globals.slots[currentLine].indentNumber
                    output += "| "
                    output += constFunctCall+functionName
                    output += " parameters: " + parameters
                    output += " |"
                    output += "<BR>\n"
                    output += "     " * globals.slots[currentLine].indentNumber
                    output += " "+"-" * wcwidth.wcswidth(constFunctCallFull + functionName + " parameters: " + parameters)
                    output += "<BR>\n"
                    continue
                else:
                    output += "     " * globals.slots[currentLine].indentNumber
                    output += " "+"_" * wcwidth.wcswidth(constFunctCallFull + functionName)
                    output += "<BR>\n"
                    output += "---->" * globals.slots[currentLine].indentNumber
                    output += "| "
                    output += constFunctCall+functionName
                    output += " |"
                    output += "<BR>\n"
                    output += "     " * globals.slots[currentLine].indentNumber
                    output += " "+"-" * wcwidth.wcswidth(constFunctCallFull + functionName)
                    output += "<BR>\n"
                    continue
    #output +='</body></output>\n'
    print(output)

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
    createoutput(globals)