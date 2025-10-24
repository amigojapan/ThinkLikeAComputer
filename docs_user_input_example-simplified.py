#user input example

#initialize turtle position
teleportTurtleTo(,4,9)
orderUser(,"put turtle at top left of the board")
simulateUserInputTeleportTurtleTo(,0,0)
savedX=turtleX
savedY=turtleY
orderUser(,"put turtle at top bottom right of the board")
simulateUserInputTeleportTurtleTo(,9,9)
teleportTurtleTo(, savedX, savedY)
