class IpClassError(Exception):
    pass

def validate(cidr_ranges):
    from termcolor import colored
    import ipaddress
    import netifaces

    gateways = netifaces.gateways()
    default_gateway = gateways['default'][netifaces.AF_INET][0]

    for range in cidr_ranges.split(", "):
        if ipaddress.ip_address(default_gateway) in ipaddress.ip_network(range):
            print(colored("ERROR!", "red"))
            print("")
            print("The AllowedIPs CIDR range of: " + colored(range, "cyan") + " conflicts with the IP address used the default IP address of your server.")
            print("")
            print("Applying this configuration could knock your server offline.")
            print("")
            print("Please real out to support@geeny.io for further information.")
            print("")
            raise(IpClassError)
