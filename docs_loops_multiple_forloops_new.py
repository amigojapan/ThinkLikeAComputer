#!/usr/bin/python3
import TLACsimulator as TLAC

# board setup (commented out as in original)
# TLAC.setInitialTurtlePositionTo(TLAC.globals,4,9)

# print("initial board:")
# TLAC.printBoard(TLAC.globals)

# The following makes a pyramid, it is an example of how to use 
# several for loops (outer and inner) in the same program.

def print_many_christmas(ch, times, triangle_width):
    output = ""
    
    # 1. First inner loop: Add the spaces
    # loopy's forloop was inclusive, so we add +1 to the range stop condition
    repeat_end = triangle_width - times
    for _ in range(0, repeat_end + 1):
        output += " "
        
    # 2. Second inner loop: Add the characters (stars)
    repeat_end2 = times * 2 - 2
    for _ in range(0, repeat_end2 + 1):
        output += ch
        
    print(output)

# 3. Outer loop: Run the pyramid builder for rows 1 through 5
# range(1, 6) counts exactly 1, 2, 3, 4, 5
for i in range(1, 6):
    print_many_christmas('*', i, 5)