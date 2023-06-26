def print_header(message, color):
    from termcolor import colored

    print("")
    print(colored("==========================================", color))
    print(colored(message, color))
    print("")

def register(pub_key):
    from termcolor import colored

    print("You must email to register: sg-registration@geeny.io\n")
    print(colored("NOTE:", "yellow") + " you must register with the same email address used to purchase the SecureSIM cards.")
    print(colored("NOTE:", "yellow") + " that Geeny may ask further questions regarding network design and layout")
    print("")

    if pub_key:
        print("You must share your pubkey of: " + colored(pub_key, "yellow"))
        print("")

    print(colored("Geeny will NEVER ask you for your private key!", "red"))
