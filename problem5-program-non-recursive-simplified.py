#problem 5
# Initial action before the loop starts
lt()

while True:
    # Exit condition
    if amILayingOnAnEgg():
        end()
        break  # Breaks out of the loop to end the script

    # Turtle actions
    # Note the second parameter (2) for checking and moving
    if not testIfICanProceed( 2):
        rt()
        
    layEgg()
    fd( 2)