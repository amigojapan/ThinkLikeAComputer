#loopy library import, name it l
import TLACloopyLib as l

# do_while example
def loop_body(n):
    fd(n)
l.loop_body = loop_body

def condition(n1, n2):
    return l.conditional(n1, l.op(">"), n2)
l.condition = condition

l.do_while(1, 3, -1)
promptUserToWriteDownOnPaper("n1 exceeds threshold")