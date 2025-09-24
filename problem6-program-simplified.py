#problem 6
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
    else:
        layEgg()
        return
def repeatThisUntilBoardFull():
    fillThisRowWithEggs()
    if turtledirection=="^" :
        rt()
        fd()
        rt()
    else:
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
