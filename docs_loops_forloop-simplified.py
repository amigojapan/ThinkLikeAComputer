#loopy library import, name it l
import TLACloopyLib as l

#for loop example
def loop_body(n):
    teleportTurtleTo(n,n)
l.loop_body = loop_body

def condition(n1, n2):
    return l.conditional(n1, l.op("=="), n2)
l.condition = condition

l.forloop(5, 9, 1)
promptUserToWriteDownOnPaper("counted form 5 to 9")