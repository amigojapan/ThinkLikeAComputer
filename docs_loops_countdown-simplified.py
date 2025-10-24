#loopy library import, name it l
import TLACloopyLib as l

def loop_body(n):
    fd(n)

l.loop_body = loop_body

l.countdown(3, 1)