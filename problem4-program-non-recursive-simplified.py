#problem 4 non-recursive solution
# Initial action before the loop starts
lt()

while True:
    # Exit condition
    if amILayingOnAnEgg():
        end()
        break  # Breaks out of the loop to end the script

    # Turtle actions
    if not testIfICanProceed():
        rt()
        
    layEgg()
    fd()