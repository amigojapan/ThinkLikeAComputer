#!/usr/bin/python3
import loopy as l

# Example usage for countdown
def condition(n1, n2):
    return l.conditional(n1, l.op("<="), n2)
l.globls.condition = condition
def loop_body(n):
    print(n)
l.globls.loop_body = loop_body
l.countdown(5, 1)
print("Blast off!")
l.countdown(10, 2)
print("Blast off!")

# do_while example
def condition(n1, n2):
    return l.conditional(n1, l.op(">"), n2)
l.globls.condition = condition
l.do_while(1, 5, -1)

# forloop example
def condition(n1, n2):
    return l.conditional(n1, l.op("=="), n2)
l.globls.condition = condition
l.forloop(10, 15, 1)
print("counted form 10 to 15")
l.forloop(25, 20, -1)
print("counted form 25 to 20")

# foreach example
my_list = ['apple', 'banana', 'cherry']
l.foreach(my_list, l.globls.loop_body)

# Custom loop body for countdown
def loop_body(n):
    print("seconds until lift-off:" + str(n))
l.globls.loop_body = loop_body
l.countdown(5, 1)
print("Blast off!")

# The following makes a pyramid, it is an example of how to use several loopbodies for a forloop in the code
class initGlobals:
    def __init__(self):
        self.output = ""
        self.ch = "*"

globals = initGlobals()

def loop_body1(n):
    globals.output = globals.output + ' '

def loop_body2(n):
    globals.output = globals.output + globals.ch

def condition_eq(n1, n2):
    return l.conditional(n1, l.op("=="), n2)
l.globls.condition=condition_eq
def print_many_christmas(ch, times, triangle_width):
    globals.output = ''
    globals.ch = ch
    repeat_end = triangle_width - times
    # Save outer loop state and set inner loop state for spaces
    l.globls.loop_body=loop_body1
    l.forloop(0, repeat_end, 1)
    # Set inner loop state for stars
    repeat_end2 = times * 2 - 2
    l.globls.loop_body=loop_body2
    l.forloop(0, repeat_end2, 1)
    print(globals.output)

def loop_body3(triangle_width):
    print_many_christmas('*', triangle_width, 5)

l.globls.condition = condition_eq
l.globls.loop_body = loop_body3
l.forloop(1, 5, 1)
#todo:try to see if I can put the push state and pop state into the forloop function itself
"""
the output from this program is:
     *
    ***
   *****
  *******
 *********
"""