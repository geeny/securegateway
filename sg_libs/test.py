def endpoint_connectivity():
    import configparser
    import os
    import subprocess
    from sg_libs import cmd
    from termcolor import colored

    print("""This script uses `nmap` to do the testing.
If the connectivity to the endpoint is good, the results may say ether of the following:

STATE open

Anything else and there may be a problem with the endpoint itself,
or your outbound internet/firewall rules to the endpoint.

If the `nmap` scan seems stuck, you can safely Control+C out of it without exiting this program.
    """)

    try:
        wg_config = configparser.ConfigParser()
        wg_config.read_file(open('/etc/wireguard/sg.conf'))

        ip, port = wg_config["Peer"]["Endpoint"].split(":")

        cmd.run("nmap", "/usr/bin/nmap -sU -p " + port + " " + ip, returncode_bail=False, print_output=True, return_stdout=False, handle_keyboard=True)
    except FileNotFoundError as e:
        print(colored("Config /etc/wireguard/sg.conf does not exist", "yellow"))
        print(colored("Please create a conf first!", "yellow"))
    except KeyError as e:
        print(colored("There seems to be an issue with /etc/wireguard/sg.conf", "yellow"))
        print(colored("Please check the file for any errors", "yellow"))
    except Exception as e:
        print(e)
        print(e.__class__)

def other():
    from sg_libs import cmd

    print("This test will use the wireguard 'sg' interface to attempt to ping another host.")
    print("If you have a connected SecureSIM device, you can try pinging that.")
    target = input("Please enter an IP or hostname to ping test: ")

    print("Please note output will print when ping command is complete.\n")
    print("If the `ping` test seems stuck, you can safely Control+C out of it without exiting this program.")
    print("This `ping` test will take a maximum of 25 seconds")
    print("")

    cmd.run("ping test", "/usr/bin/ping -I sg -W 5 -c 5 " + target, returncode_bail=False, print_output=True, stderr_bail = False, handle_keyboard=True)
