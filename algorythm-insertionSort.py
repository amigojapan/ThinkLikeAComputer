import TLACloopyLib as l

class SortGlobals:
    def __init__(self, arr):
        self.arr = arr
        self.i = 0
        self.j = 0
        self.key = 0

s_globals = SortGlobals(["C", "A", "D", "E", "B"])  # Replace with your list

# Outer loop condition
def eq(n1, n2):
    return l.conditional(n1, l.op("=="), n2)

l.globals.condition = eq

# Outer loop body
def outer_body(i):
    s_globals.i = i
    s_globals.key = s_globals.arr[i]
    s_globals.j = i - 1

    # Inner body
    def inner_body(current_j):
        s_globals.arr[current_j + 1] = s_globals.arr[current_j]
        s_globals.j = current_j - 1

    # Inner condition (stop if True)
    def inner_condition(current_j, unused):
        next_j = current_j - 1
        if next_j >= 0 and s_globals.arr[next_j] > s_globals.key:
            return False  # continue
        else:
            return True   # stop

    # Run inner loop if initial condition met
    if s_globals.j >= 0 and s_globals.arr[s_globals.j] > s_globals.key:
        # Set inner loop_body and condition
        l.globals.loop_body = inner_body
        l.globals.condition = inner_condition
        l.do_while(s_globals.j, 0, 1)

    # Insert key
    s_globals.arr[s_globals.j + 1] = s_globals.key

# Set outer loop_body
l.globals.loop_body = outer_body

# Run outer loop: i from 1 to len-1
l.forloop(1, len(s_globals.arr) - 1, 1)

# Output the sorted list
print(s_globals.arr)