"""
this example is supposed to explain first class functions
which are functions that are passed into another function
as parameters.
you just need to assign a varible to the function like in line 12
and then you can pass it to a function as a parameter
"""
def F1():
    print("this is printed by my 'first class function'")
def F2(f):
    f()
f=F1
F2(f)
"""
the output of this program is:
this is printed by my 'first class function'
"""