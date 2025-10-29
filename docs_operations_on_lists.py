#!/usr/bin/python3
import TLACsimulator as TLAC







#operations on lists example
#loopy library import, name it l
import TLACloopyLib as l

def loop_body(item):
    TLAC.promptUserToWriteDownOnPaper(TLAC.globals, item)
l.globals.loop_body = loop_body
fruits=["banana","apple","peach","pear"] # create a list
# print first element of list
TLAC.promptUserToWriteDownOnPaper(TLAC.globals, fruits[0])
# print last element
TLAC.promptUserToWriteDownOnPaper(TLAC.globals, fruits[3])
TLAC.promptUserToWriteDownOnPaper(TLAC.globals, "now re-writing all fruits:")
l.foreach(fruits, l.globals.loop_body)
TLAC.promptUserToWriteDownOnPaper(TLAC.globals, "now re-writing all fruits in reverse:")
# reverses the list
fruits.reverse()
l.foreach(fruits, l.globals.loop_body)
TLAC.promptUserToWriteDownOnPaper(TLAC.globals, "now writing fruits in alphabetical order:")
# sorts the list in alphabetical order
fruits.sort()
l.foreach(fruits, l.globals.loop_body)
fruits.append("appricot")
# Inserts 'blueberry' at index 2
fruits.insert(2, "blueberry")
#deletes the third item of the list
del fruits[3]
TLAC.promptUserToWriteDownOnPaper(TLAC.globals, "now writing fruits in final order:")
l.foreach(fruits, l.globals.loop_body)