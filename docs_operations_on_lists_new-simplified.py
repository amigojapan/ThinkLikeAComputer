
# print last element
promptUserToWriteDownOnPaper( fruits[3])

promptUserToWriteDownOnPaper( "now re-writing all fruits:")
# Standard Python loop
for fruit in fruits:
    promptUserToWriteDownOnPaper( fruit)

promptUserToWriteDownOnPaper( "now re-writing all fruits in reverse:")
# reverses the list
fruits.reverse()
for fruit in fruits:
    promptUserToWriteDownOnPaper( fruit)

promptUserToWriteDownOnPaper( "now writing fruits in alphabetical order:")
# sorts the list in alphabetical order
fruits.sort()
for fruit in fruits:
    promptUserToWriteDownOnPaper( fruit)

fruits.append("appricot")
# Inserts 'blueberry' at index 2
fruits.insert(2, "blueberry")
# deletes the third item of the list
del fruits[3]

promptUserToWriteDownOnPaper( "now writing fruits in final order:")
for fruit in fruits:
    promptUserToWriteDownOnPaper( fruit)