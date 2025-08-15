#program
def goToBeginningOfBoard():
    if testIfICanProceed():
        fd()
    else:
        return
    goToBeginningOfBoard()

def fillThisRowWithEggs():
    if testIfICanProceed(2):
        layEgg()
        fd(2)
        fillThisRowWithEggs()
    else:
        layEgg()
        return

def repeatThisUntilBoardFull():
    if turtledirection=="^" :
        fillThisRowWithEggs()
        rt()
        fd()
        rt()
        repeatThisUntilBoardFull()
    else:
        fd(H-2)
        lt()
        if turtledirection==">" :
            if not testIfICanProceed():
                end()
        fd()
        lt()

lt()
goToBeginningOfBoard()
rt()
fillThisRowWithEggs()
repeatThisUntilBoardFull()