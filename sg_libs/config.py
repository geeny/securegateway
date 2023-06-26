def get_input(option, text):
    from termcolor import colored

    color = "cyan"

    print("")
    print(colored("--------------------------------", color))
    print(colored(option.upper(), color))
    print("")
    print(text)
    print("")

    return(input(option + ": "))

def write_file(priv_key, pub_key):
    import datetime
    import os
    import shutil
    from jinja2 import Environment, FileSystemLoader
    from sg_libs import ipaddr
    from termcolor import colored

    overwrite = True
    backup = False

    if not priv_key and not pub_key:
        print("ERROR: Please generate or input a wireguard keypair!")
        return

    try:
        if os.path.exists("/etc/wireguard/sg.conf"):
            backup = True
            print(
            """
    You have an existing configuration at: /etc/wireguard/sg.conf
    Would you like to overwrite your existing configuration?

    1: keep configuration
    2: overwrite configuration
            """)

            user_input = input("Please make a selection: ")

            match user_input:
                case "1":
                    overwrite = False
                case "2":
                    overwrite = True
                case _:
                    print("Invalid selection! Keeping existing configuration file!")
                    overwrite = False
    except Exception as e:
        print("We had an error accessing /etc/wireguard/sg.conf!")
        print(e)
        print(e.__class__)
        print("We keep the existing file for now!")
        return

    if overwrite == True:
        inputs = {}
        inputs["priv_key"] = priv_key
        inputs["pub_key"]  = pub_key

        try:
            print("Please note that at any time, you can hit control-c, and the configuration will NOT be written!")

            listen_port_text = """This is the local port wireguard listens to connections for.
This configuration parameter is required, but currently unused by Geeny."""
            inputs["listen_port"] = get_input("Listen Port", listen_port_text)

            address_text = """This is the address of the IP of the wireguard interface.
This is provided by Geeny as part of the registration process.

Please copy and paste exactly as given to you."""
            inputs["address"] = get_input("Address", address_text)

            endpoint_text="""This is the Geeny IP and port that wireguard will connect to.
This is provided by Geeny as part of the registration process.

Please copy and paste exactly as given to you."""
            inputs["endpoint"] = get_input("Endpoint", endpoint_text)

            peer_pubkey_text = """This is Geeny's public key.
This is provided by Geeny as part of the registration process.

Please copy and paste exactly as given to you."""
            inputs["peer_pubkey"] = get_input("Peer public key", peer_pubkey_text)
            
            allowedips_text = """These are the IPs blocks that are allowed to communicate to this
wireguard peer.

This is provided by Geeny as part of the registration process.

Please copy and paste exactly as given to you."""
            inputs["allowedips"] = get_input("Allowed IPs", allowedips_text)

            print("")

            ipaddr.validate(inputs["allowedips"])
        except ipaddr.IpClassError as e:
            print(colored("Got an error with AllowedIPs", "yellow"))
            print(colored("NOT saving the config!", "yellow"))
            return
        except KeyboardInterrupt as e:
            print(colored("Got a user interrupt!", "yellow"))
            print(colored("NOT saving the config!", "yellow"))
            return

        try:
            if os.path.exists("./templates/"):
                templates_dir = "./templates/"
            else:
                templates_dir = "/opt/sg/templates/"

            environment = Environment(loader=FileSystemLoader(templates_dir))
            template = environment.get_template("sg.conf.jinja2")

            file_contents = template.render(inputs=inputs)

            # If needed, back up the existing config AFTER the render, but before
            # writing the new config

            if backup == True:
                backup_filename = "/etc/wireguard/sg.conf-backup-" + datetime.datetime.today().strftime("%Y-%m-%d-%H-%M")
                print("Backing up existing /etc/wireguard/sg.conf to:")
                print(backup_filename)

                shutil.copy2("/etc/wireguard/sg.conf", backup_filename)
                os.chmod(backup_filename, 0o600)
                os.chown(backup_filename, 0, 0)

                with open(backup_filename, "a") as old_config:
                    old_config.write("# wg config backed up by /opt/sg/sg")

                print("")

            with open("/etc/wireguard/sg.conf", mode="w") as wg_file:
                wg_file.write(file_contents)

            os.chmod("/etc/wireguard/sg.conf", 0o600)
            os.chown("/etc/wireguard/sg.conf", 0, 0)

            print(colored("New configuration has been written to /etc/wireguard/sg.conf!", "cyan"))

        except Exception as e:
            print("We had an issue somewhere")
            print("Please check the configurations manually")
            print(e)
            print(e.__class__)

def print_file():
    from termcolor import colored

    try:
        with open("/etc/wireguard/sg.conf", 'r') as f:
            print(f.read())
    except FileNotFoundError as e:
        print(colored("Config /etc/wireguard/sg.conf does not exist", "yellow"))
        print(colored("Please create a conf first!", "yellow"))
    except Exception as e:
        print(e)
        print(e.__class__)
