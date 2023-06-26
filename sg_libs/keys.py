def check_existing(priv_key, pub_key, message):
    from termcolor import colored

    if priv_key:
        print("You already have an existing keypair of:")
        print("")
        print("        Private key: " + colored(priv_key, "yellow"))
        print("        Public key: " + colored(pub_key, "yellow"))
        print("")
        print("Do you want to keep the existing keypair, or generate a new key pair?")
        print("")
        print("1: Keep existing key pair")
        print("2: " + message)
        print("")

        user_input = input("Please make a selection: ")
        print("")

        match user_input:
            case "1":
                print("Keeping existing key pair")
                return(False)
            case "2":
                return(True)
            case _:
                print("Invalid selection! Keeping existing keys!")
                return(False)

    else:
        return(True)

def gen(priv_key, pub_key):
    from sg_libs import cmd
    from termcolor import colored
    import subprocess

    if check_existing(priv_key, pub_key, "Generate new keypair"):
        pass
    else:
        return(priv_key, pub_key)

    priv_key = cmd.run("/usr/bin/wg genkey", "/usr/bin/wg genkey", print_output=False, return_stdout=True).rstrip()
    pub_key = cmd.run("/usr/bin/wg pubkey", "/usr/bin/wg pubkey", input=priv_key, print_output=False, return_stdout=True).rstrip()

    print("Private key: " + colored(priv_key, "yellow"))
    print("")
    print("Public key: " + colored(pub_key, "yellow"))
    print("")
    print(colored("Never share your private key! Geeny will NEVER ask for your private key!", "red"))

    return [priv_key, pub_key]

def get_input(priv_key, pub_key):
    if check_existing(priv_key, pub_key, "Input existing keypair"):
        pass
    else:
        return(priv_key, pub_key)

    user_priv_key = input("Please input private key: ")
    user_pub_key = input("Please input public key: ")

    #TODO: Validate keys

    return [user_priv_key, user_pub_key]
