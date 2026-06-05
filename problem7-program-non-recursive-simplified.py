#problem 7
lt()

# 1 goToBeginningOfBoard
while testIfICanProceed():
    fd()

rt()

# 2 fillThisRowWithEggs(Initial run)
while testIfICanProceed():
    layEgg()
    fd()
layEgg()

# 3 repeatThisUntilBoardFull
while True:
    if turtledirection == "^":
        # fillThisRowWithEggs inline
        while testIfICanProceed():
            layEgg()
            fd()
        layEgg()
        
        # Turn logic for "^" direction
        rt()
        fd()
        rt()
    else:
        # Move forward by height minus 1
        fd( H - 1)
        lt()
        
        # Exit condition check
        if turtledirection == ">":
            if not testIfICanProceed():
                end() # Fixed from ''
                break  # Breaks out of the loop to safely end the script
                
        fd()
        lt()