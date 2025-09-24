def F1():
    print("this is printed by my 'first class function'")
def F2(f):
    f()
f=F1
F2(f)