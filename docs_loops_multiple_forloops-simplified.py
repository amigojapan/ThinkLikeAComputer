#loopy library import, name it l
import TLACloopyLib as l

# The following makes a pyramid, it is an example of how to use several loopbodies for a forloop in the code
class initGlobals:
    def __init__(self):
        self.output = ""
        self.ch = "*"

globals = initGlobals()

def loop_body1(n):
    output = output + ' '

def loop_body2(n):
    output = output + ch

def condition_eq(n1, n2):
    return l.conditional(n1, l.op("=="), n2)
l.condition=condition_eq

def print_many_christmas(ch, times, triangle_width):
    output = ''
    ch = ch
    repeat_end = triangle_width - times
    # Save outer loop state and set inner loop state for spaces
    l.loop_body=loop_body1
    l.forloop(0, repeat_end, 1)
    # Set inner loop state for stars
    repeat_end2 = times * 2 - 2
    l.loop_body=loop_body2
    l.forloop(0, repeat_end2, 1)
    print(output)

def loop_body3(triangle_width):
    print_many_christmas('*', triangle_width, 5)

l.condition = condition_eq
l.loop_body = loop_body3
l.forloop(1, 5, 1)