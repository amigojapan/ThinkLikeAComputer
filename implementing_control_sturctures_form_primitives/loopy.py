import operator as op_

# State stack to manage condition and loop_body for nested loops
class initGlobls:
    def __init__(self):
        self.condition=None
        self.loop_body=None
        self.condition_stack = []
        self.loop_body_stack = []
globls=initGlobls()

def default_loop_body(n):
    print(n)  # Default loop body

def default_condition(n1, n2):
    return conditional(n1, op(">"), n2)  # Default for do_while

def push_state(g):
    """Push current condition and loop_body to stack and set new ones."""
    g.condition_stack.append(g.condition)
    g.loop_body_stack.append(g.loop_body)

def pop_state():
    """Restore previous condition and loop_body from stack."""
    globls.condition = globls.condition_stack.pop() if globls.condition_stack else default_condition
    globls.loop_body = globls.loop_body_stack.pop() if globls.loop_body_stack else default_loop_body

def op(operator):
    if operator == "==":
        return op_.eq
    elif operator == ">":
        return op_.gt
    elif operator == "<":
        return op_.lt
    elif operator == "<=" or operator == "=<":
        return op_.le
    elif operator == ">=" or operator == "=>":
        return op_.ge

def conditional(operand1, op_func, operand2):
    return op_func(operand1, operand2)

def countdown(n, countDownBy):
    if globls.condition(n, 0):
        return
    globls.loop_body(n)
    countdown(n - countDownBy, countDownBy)

def do_while(n1, n2, countDownBy):
    globls.loop_body(n1)
    if globls.condition(n1, n2-1):
        return
    do_while(n1 - countDownBy, n2, countDownBy)

def forloop(min_val, max_val, step, is_root=True):
    if is_root:
        push_state(globls)
    
    globls.loop_body_stack[-1](min_val)#get last item on list
    
    if globls.condition(min_val, max_val):
        if is_root:
            pop_state()
        return
    
    forloop(min_val + step, max_val, step, False)
    
    if is_root:
        pop_state()
    
def foreach(data, func):
    if not data:
        return
    func(data[0])
    foreach(data[1:], func)