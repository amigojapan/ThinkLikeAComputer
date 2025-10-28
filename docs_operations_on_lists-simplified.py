#operations on lists example
#loopy library import, name it l
import TLACloopyLib as l

def loop_body(item):
    promptUserToWriteDownOnPaper( item)
l.loop_body = loop_body
fruits=["banana","apple","peach","pear"] # create a list
# print first element of list
promptUserToWriteDownOnPaper( fruits[0])
# print last element
promptUserToWriteDownOnPaper( fruits[3])
promptUserToWriteDownOnPaper( "now re-writing all fruits:")
l.foreach(fruits, l.loop_body)
promptUserToWriteDownOnPaper( "now re-writing all fruits in reverse:")
# reverses the list
fruits.reverse()
l.foreach(fruits, l.loop_body)
promptUserToWriteDownOnPaper( "now writing fruits in alphabetical order:")
# sorts the list in alphabetical order
fruits.sort()
l.foreach(fruits, l.loop_body)