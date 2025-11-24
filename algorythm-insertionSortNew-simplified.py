#algo insertion sort
import TLACloopyLib as l

class SortGlobals:
    def __init__(self):
        #None values will be set later
        self.arr = None
        self.i = 0
        self.j = 0
        self.key = None

s_globals = SortGlobals()
s_arr=["Pyramid3", "Pyramid1", "Pyramid4", "Pyramid5", "Pyramid2"]

def eq(n1, n2):
    return l.conditional(n1, l.op("=="), n2)

l.condition = eq

def inner_body(current_j):
    s_arr[current_j + 1] = s_arr[current_j]
    s_j = current_j - 1

def inner_condition(current_j, unused):
    next_j = current_j - 1
    if next_j >= 0 and s_arr[next_j] > s_key:
        # continue
        return False
    else:
        # stop
        return True

# Outer loop body
def outer_body(i):
    s_i = i
    s_key = s_arr[i]
    s_j = i - 1
    # Run inner loop if initial condition met
    if not inner_condition(s_j + 1, None):
        l.loop_body = inner_body
        l.condition = inner_condition
        l.do_while(s_j, 0, 1)
    # Insert key
    s_arr[s_j + 1] = s_key

# Set outer loop_body
l.loop_body = outer_body

# Run outer loop: i from 1 to length of array -1
l.forloop(1, len(s_arr) - 1, 1)

# Output the sorted list
print(s_arr)