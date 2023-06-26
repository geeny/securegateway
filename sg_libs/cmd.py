def print_std(std_type, output):
    from termcolor import colored
    if output != "":
        print(colored(std_type, "cyan"))
        print(output)

# stderr_bail means the function does an exit(1) if there is output in stderr
# returncode_bail means the function does an exit(1) if the command's return code is not 0
# print_output will print both stdout and stderr
# return_stdout will cause the function to return the value of stdout
def run(command_desc, command, input=False, stderr_bail=True, returncode_bail=True, print_output=True, return_stdout=False, handle_keyboard=False):
    import subprocess
    import sys
    from termcolor import colored

    bail = False
    color = "white"

    try:
        command_arr = command.split(" ")

        if input == False:
            cmd = subprocess.run(command_arr, capture_output=True, universal_newlines=True, text=True)
        else:
            cmd = subprocess.run(command_arr, input=input, capture_output=True, universal_newlines=True, text=True)

        if cmd.returncode != 0 and returncode_bail == True:
            color = "red"
            bail = True

        if cmd.stderr != "" and stderr_bail == True:
            color = "red"
            bail = True

        if bail == True:
            print(colored("The command `" + command_desc + "` had errors. Please check! Exiting", color))
            print("")
            print_std("stdout", cmd.stdout)
            print_std("stderr", cmd.stderr)
            sys.exit(1)
        else:
            if(print_output == True):
                print(colored("The command `" +  command_desc + "` produced the following output:\n", color))
                print_std("stdout", cmd.stdout)
                print_std("stderr", cmd.stderr)
    except KeyboardInterrupt as e:
        if handle_keyboard == True:
            print("Got a user interrupt!")
            print("Exiting the commands for " + command_desc)
        else:
            print("Got a user interrupt!")
            print("Exiting!")
            sys.exit(1)
    except Exception as e:
        print("Uncaught exception!")
        print(e)
        print(e.__class__)
        sys.exit(1)

    if (return_stdout == True):
        return cmd.stdout
