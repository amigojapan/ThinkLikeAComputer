#problem 7
def goToBeginningOfBoard():
    if testIfICanProceed():
        fd()
        goToBeginningOfBoard()
    else:
        return
def fillThisRowWithEggs():
    if testIfICanProceed():
        layEgg()
        fd()
        fillThisRowWithEggs()
        return
    else:
        layEgg()
        return
def repeatThisUntilBoardFull():
    if turtledirection=="^" :
        fillThisRowWithEggs()
        rt()
        fd()
        rt()
    else:
        fd(H-1)
        lt()
        if turtledirection==">" :
            if not testIfICanProceed():
                end()
        fd()
        lt()
    repeatThisUntilBoardFull()
lt()
goToBeginningOfBoard()
rt()
fillThisRowWithEggs()
repeatThisUntilBoardFull()
