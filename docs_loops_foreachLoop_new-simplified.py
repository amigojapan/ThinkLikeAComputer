# Standard Python iteration (foreach)
my_commands_list = ['fd', 'fd', 'rt', 'fd', 'fd', 'lt', 'fd', 'fd']

# Loop directly through each command in the list
for command in my_commands_list:
    if command == "fd":
        fd(globals)
    elif command == "rt":
        rt(globals)
    elif command == "lt":
        lt(globals)