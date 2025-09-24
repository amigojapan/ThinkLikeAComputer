#!/usr/bin/python3
import loopy as l
import operator as op
"""
this module allows us to use functions like gt 'greater than' and lt 'less than'  and such operators as passable operators into a function
in the follwing way:
def perform_operation(operand1, op_func, operand2):
        return op_func(operand1, operand2)
"""
"""
the following is how ot implement a 'while loop' usinf primitive functions
python has its own while structure, but it is good to know how ot implement yoru own, here is how I implemented it
a while loop will repeat something until a condition is true
"""
# Example usage
def condition(n1,n2):
     return l.conditional(n1, op.le, n2)
l.recursive_countdown(5,1)
print("Blast off!")
l.recursive_countdown(10,2)
print("Blast off!")
"""
the output of these tow funciton calls is:
5
4
3
2
1
Blast off!
10
8
6
4
2
Blast off!
this is printed by my 'first class function'
"""

""" python does not have a do while stucture, but you can define one in the follwing way:
while True:
    # Code to be executed at least once
    # ...

    # Condition to check for exiting the loop
    if not condition_is_met:
        break

but we want to do if functionally which is done in the follwing way:
in loopy itis done the following way:
l.do_while(minimum,maximum,step)
"""
#example
def condition(n1,n2):#this will rewire over hte past condition
     return l.conditional(n1, op.gt, n2)
l.do_while(1,5,-1)
"""
the output of the last function is:
1
2
3
4
5
6
n is more than 5
"""

"""
for loops
forloop(initialvalue, maximum,condition, step,loopbody)
again python has it's own kind of for loops but we are going to implement a more standard kind of for loops but functional as follows:
"""
def condition(n1,n2):#this will rewire over hte past condition
     return l.conditional(n1, op.eq, n2)#eq is for equal
l.forloop(10, 15, 1)
print("counted form 10 to 15")
l.forloop(25, 20,  -1)
print("counted form 25 to 20")
"""
the output of this is:
10
11
12
13
14
15
counted form 10 to 15
25
24
23
22
21
20
counted form 25 to 20
"""
"""
foreach is a kind of loop that loops over the items of a list
"""
my_list = ['apple', 'banana', 'cherry']
loop_body=l.loop_body
l.foreach(my_list, loop_body)
"""
the output of this is:
apple
banana
cherry
"""

"""
with these functions you can basically just chnage the
condition and the loopbody to do almost anything
"""
"""
now lets see how to change the loop body.
we will revisit l.recursive_countdown for this
"""
def loop_body(n):
     print("seconds until lift-off:"+str(n))
l.loop_body=loop_body
l.recursive_countdown(5,1)