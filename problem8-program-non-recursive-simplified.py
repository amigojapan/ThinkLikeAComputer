# --- Main Execution Sequence ---

# Step A: Move to the far left wall (Column 0)
lt()
while testIfICanProceed():
    fd()

# Step B: Face UP and move to the very top wall (Row 0)
rt()
while testIfICanProceed():
    fd()

# Step C: Turn completely around to face DOWN and step down 1 space to Row 1
rt()
rt()
fd()

# Step D: Begin the iterative snaking loop!
while True:
    # 1 Inline logic replacing fillThisColumnWithEggs()
    while testIfICanProceed( 2):
        layEgg()
        fd( 2)
    layEgg() # Lays the final egg in the column
    
    # 2 Inline logic replacing repeatThisUntilBoardFull()
    # If the turtle is at the top of the board facing UP (^)
    if turtledirection == "^":
        rt()
        # Check if we have hit the right edge of the board
        if not testIfICanProceed( 2):
            if testIfICanProceed():
                fd()
                rt()
            end()
            break  # Break out of the loop to safely end the script
            
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
            break  # Break out of the loop to safely end the script
            
        fd( 2)
        lt()