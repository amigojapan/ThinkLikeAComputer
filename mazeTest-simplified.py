#maze Test 1
import TLACloopyLib as l

def notDone():
    return not amILayingOnTheGoalFlag()
def isPathForward():
    return testIfICanProceed()
def isPathLeft():
    lt()
    result=isPathForward()
    rt()
    return result
def turnLeft():
    lt()
def turnRight():
    rt()
def moveForward():
    fd()

def loop_body(current):
    if isPathLeft():
        turnLeft()
    elif not isPathForward():
        turnRight()
    if isPathForward():
        moveForward()

def loop_condition(current, unused):
    if notDone():
        # continue
        return False
    else:
        # stop
        return True

l.loop_body = loop_body
l.condition = loop_condition
l.do_while(0, 0, 1)