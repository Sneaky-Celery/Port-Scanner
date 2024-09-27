import socket

# Define a function called checkUDPPortsSocket that takes an IP address and a range of ports to check as arguments
def checkUdpPortSocket(ip, min_port, max_port):
    openPorts = {}
    try:
        # Iterate over all the ports in the specified range
        for port in range(min_port, max_port + 1):
            # Create a new socket object
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # Set a timeout of 1 second
            sock.settimeout(1)
            # Try to send a blank message to the IP address and port
            sock.sendto(b' ', (ip, port))
            try:
                # Try to receive a response from the UDP socket
                data, addr = sock.recvfrom(1024)
                # If a response is received, the port is open and a service is likely running
                service = socket.getservbyport(port)
                openPorts[port] = service
                # Print the port and service information for open ports
                print("Port {}: \t Open ({})".format(port, service))
            except socket.timeout:
                # If no response is received, the port is closed
                print("Port {}: \t Closed".format(port))
            # Close the socket object
            sock.close()
    except socket.error as error:
        # If there is a socket error, print the error message
        print(str(error))
        print("Connection error")       
    return openPorts
