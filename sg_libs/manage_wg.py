def activate():
    from sg_libs import cmd
    from termcolor import colored
    import netifaces

    if "sg" in netifaces.interfaces():
        print(colored("Wireguard interface 'sg' is already up!", "yellow"))
    else:
        cmd.run("/usr/bin/wg-quick up /etc/wireguard/sg.conf", "/usr/bin/wg-quick up /etc/wireguard/sg.conf", stderr_bail=False, print_output=True, return_stdout=False)

def display_status():
    from sg_libs import cmd

    cmd.run("wg", "wg")
    print("""-----------------------------------------------
END OF OUTPUT

A working Wireguard connection will have two key outputs:

1: A `latest handshake:` of two minutes or less.

2: A `transfer` of more than 0 bytes.

Without both of these outputs, there maybe a connection problem.""")

def deactivate():
    from sg_libs import cmd
    from termcolor import colored
    import netifaces

    if "sg" in netifaces.interfaces():
        cmd.run("/usr/bin/wg-quick down /etc/wireguard/sg.conf", "/usr/bin/wg-quick down /etc/wireguard/sg.conf", stderr_bail=False, print_output=True, return_stdout=False)
    else:
        print(colored("Wireguard interface 'sg' not found! Maybe it is already down?", "yellow"))
