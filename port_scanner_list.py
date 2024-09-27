import socket

# Define a function called checkPortsSocket that takes an IP address and a list of ports to check as arguments
def checkPortsSocket(ip, portlist):
    openPorts = {}
    try:
        # Iterate over the list of ports to check
        for port in portlist:
            # Create a new socket object
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Set a timeout of 10 milliseconds
            sock.settimeout(.01)
            # Try to connect to the IP address and port
            result = sock.connect_ex((ip, port))
            # If the connection was successful, add the port and its associated service to the openPorts dictionary
            if result == 0:
                # Try to get the service name associated with the port
                try:
                    service = socket.getservbyport(port)
                except socket.error:
                    # If the service name cannot be found, set it to "unknown"
                    service = "unknown"
                openPorts[port] = service
                # Print the port and service information for open ports
                print("Port {}: \t Open ({})".format(port, service))
            # If the connection was not successful, print a message indicating that the port is closed
            else:
                print("Port {}: \t Closed".format(port))
            # Close the socket object
            sock.close()
    except socket.error as error:
        # If there is a socket error, print the error message
        print(str(error))
        print("Connection error")
    return openPorts
