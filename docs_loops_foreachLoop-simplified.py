#loopy library import, name it l
import TLACloopyLib as l

# foreach example
def loop_body(command):
    if command == "fd":
        fd(globals)
    if command == "rt":
        rt(globals)
    if command == "lt":
        lt(globals)
l.loop_body = loop_body

my_commands_list = ['fd', 'fd', 'rt','fd', 'fd','lt', 'fd', 'fd']
l.foreach(my_commands_list, l.loop_body)