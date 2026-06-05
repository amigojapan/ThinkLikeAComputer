#problem 6
# 1 Turn left and go to the beginning of the board
lt()
while testIfICanProceed():
    fd()
rt()

# 2 Initial row fill (Executes before the repeating main loop)
while testIfICanProceed():
    layEgg()
    fd()
layEgg()

# 3 Main repeating loop for the rest of the board
while True:
    # Inner loop replacing fillThisRowWithEggs()
    while testIfICanProceed():
        layEgg()
        fd()
    layEgg()
    
    # Turning and proceeding logic
    if turtledirection == "^":
        rt()
        fd()
        rt()
    else:
        lt()
        # Check if we've reached the end of the board
        if turtledirection == ">":
            if not testIfICanProceed():
                end()
                break  # Break out of the loop to end the script
                
        fd()
        lt()