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
def loop_body(n):
    print(n)#default loop body
def conditional(operand1, op_func, operand2):
        return op_func(operand1, operand2)     
def recursive_countdown(n,countDownBy):
    # Base case: Stop when n becomes 0 or less
    if condition(n,0):#op.le means less than or equal to, simillar to <= but in a function that can be sent as a parameter in this case it is like writing n <= 0
        return
    # "Loop" body: Print the current number
    loop_body(n)
    # Recursive call: Call the function with a decremented n
    recursive_countdown(n - countDownBy,countDownBy)
# Example usage
# def condition(n1,n2):
#     return conditional(n1, op.le, n2)
#lb=loop_body
#recursive_countdown(5,1)
#print("Blast off!")
#recursive_countdown(10,2)
#print("Blast off!")
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
"""
def condition(n1,n2):#this will rewire over hte past condition
     return conditional(n1, op.gt, n2)
def do_while(n1,n2,countDownBy):
    #put the bopdy of the do while loop here:
    loop_body(n1)
    if condition(n1,n2):#op.gt means greater than or equal to, simillar to > but in a function that can be sent as a parameter in this case it is like writing not n > 0
        print("n1 is more than 5")
        return
    # Recursive call: Call the function with a decremented n
    do_while(n1 - countDownBy,n2,countDownBy)
#example
#do_while(1,-1)
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
     return conditional(n1, op.eq, n2)#eq is for equal
def forloop(counter, max, step):
    loop_body(counter)
    if condition(counter,max):
         return
    forloop(counter+step,max, step)
#forloop(10, 15, 1)
#print("counted form 10 to 15")
#forloop(25, 20,  -1)
#print("counted form 25 to 20")
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
def foreach(data, func):
    if not data:
        return
    func(data[0])
    foreach(data[1:], func)
#my_list = ['apple', 'banana', 'cherry']
#foreach(my_list, loop_body)
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