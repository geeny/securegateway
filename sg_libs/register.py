def register(pub_key):
        from termcolor import colored

        print("You must email to register: sg-registration@geeny.io\n")
        if pub_key:
            print("You must share your pubkey of: " + pub_key + "\n")
        print(colored("Geeny will NEVER ask you for your private key!", "red"))
