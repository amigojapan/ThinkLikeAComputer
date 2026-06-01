#!/usr/bin/python3
import TLACsimulator as TLAC

# operations on lists example

fruits = ["banana", "apple", "peach", "pear"] # create a list

# print first element of list
TLAC.promptUserToWriteDownOnPaper(TLAC.globals, fruits[0])

# print last element
TLAC.promptUserToWriteDownOnPaper(TLAC.globals, fruits[3])

TLAC.promptUserToWriteDownOnPaper(TLAC.globals, "now re-writing all fruits:")
# Standard Python loop
for fruit in fruits:
    TLAC.promptUserToWriteDownOnPaper(TLAC.globals, fruit)

TLAC.promptUserToWriteDownOnPaper(TLAC.globals, "now re-writing all fruits in reverse:")
# reverses the list
fruits.reverse()
for fruit in fruits:
    TLAC.promptUserToWriteDownOnPaper(TLAC.globals, fruit)

TLAC.promptUserToWriteDownOnPaper(TLAC.globals, "now writing fruits in alphabetical order:")
# sorts the list in alphabetical order
fruits.sort()
for fruit in fruits:
    TLAC.promptUserToWriteDownOnPaper(TLAC.globals, fruit)

fruits.append("appricot")
# Inserts 'blueberry' at index 2
fruits.insert(2, "blueberry")
# deletes the third item of the list
del fruits[3]

TLAC.promptUserToWriteDownOnPaper(TLAC.globals, "now writing fruits in final order:")
for fruit in fruits:
    TLAC.promptUserToWriteDownOnPaper(TLAC.globals, fruit)