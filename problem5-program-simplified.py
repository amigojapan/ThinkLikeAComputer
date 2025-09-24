#problem 5
def P():
    if amILayingOnAnEgg():
        end()
    if not testIfICanProceed(2):
        rt()
    layEgg()
    fd(2)
    P()
lt()
P()
