# 1 Moves turtle to the wall it's facing
def goToBeginningOfBoard():
    if testIfICanProceed():
        fd()
        goToBeginningOfBoard()
    else:
        return

# 2 Lays an egg and jumps 2 spaces recursively 
def fillThisColumnWithEggs():
    if testIfICanProceed( 2):
        layEgg()
        fd( 2)
        fillThisColumnWithEggs()
    else:
        layEgg()
        return

# 3 Turns the turtle jumps 2 columns and repeats
def repeatThisUntilBoardFull():
    fillThisColumnWithEggs()
    
    # If the turtle is at the top of the board facing UP (^)
    if turtledirection == "^":
        rt()
        # Check if we have hit the right edge of the board
        if not testIfICanProceed( 2):
            if testIfICanProceed():
                fd()
                rt()
            end()
            return
            
        fd( 2)
        rt()
        
    # If the turtle is at the bottom of the board facing DOWN
    else:
        lt()
        # Check if we have hit the right edge of the board
        if not testIfICanProceed( 2):
            # This neatly tucks the turtle into the final [v] corner position!
            if testIfICanProceed():
                fd()
                rt() 
            end()
            return
            
        fd( 2)
        lt()
        
    # Recursively repeat for the newly positioned column
    repeatThisUntilBoardFull()


# --- Main Execution Sequence ---

# Step A: Move to the far left wall (Column 0)
lt()
goToBeginningOfBoard()

# Step B: Face UP and move to the very top wall (Row 0)
rt()
goToBeginningOfBoard()

# Step C: Turn completely around to face DOWN and step down 1 space to Row 1
rt()
rt()
fd()

# Step D: Begin the recursive snaking!
repeatThisUntilBoardFull()