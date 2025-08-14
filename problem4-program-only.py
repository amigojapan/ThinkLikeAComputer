#board setup
teleportTurtleTo(4,9)
print("initial board:")
printBoard(globals)

#proram
def P():
    if amILayingOnAnEgg(globals):
        end(globals)
    if not testIfICanProceed(globals):
        rt(globals)
    layEgg(globals)
    fd(globals)
    P()
lt(globals)
P()
