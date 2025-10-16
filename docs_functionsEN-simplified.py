#functions example
#the following is a function definition:
def Lay_Four_Eggs_In_Square_Pattern():
    layEgg()
    fd()
    layEgg()
    rt()
    fd()
    layEgg()
    rt()
    fd()
    layEgg()
    #the following two turns are
    #to assure the turtle ends up in
    #the up pusition
    rt()
    rt()
turtleX=0
print("printing board after teleport X")
printBoard()
Lay_Four_Eggs_In_Square_Pattern()
turtleX=5

print("printing board after teleport X")
printBoard()
Lay_Four_Eggs_In_Square_Pattern()
turtleX=8

print("printing board after teleport X")
printBoard()
Lay_Four_Eggs_In_Square_Pattern()