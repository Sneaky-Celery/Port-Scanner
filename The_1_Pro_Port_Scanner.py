# Written by Scott Proctor and Uri Wortberg
import port_scanner_range
import port_scanner_list
import port_scanner_udp
import center_tables
import ipaddress
import textwrap
import pandas
import time
import re

# This function handles user input for 'port_scanner_range.py' and 'port_scanner_udp.py'
def user_range_input(ip, min_port, max_port):
    # Prompt the user to enter the IP address, minimum port number, and maximum port number
    while True:
        try:
            ip = input("Enter the target IP address: ")
            ipaddress.IPv4Address(ip)
            break
        except ipaddress.AddressValueError:
            print("Invalid IP address. Please enter a valid IPv4 address.")
    while True:
        try:
            min_port = int(input("Enter the minimum port number (1-65535): "))
            if not (1 <= min_port <= 65535):
                raise ValueError()
            while True:
                try:
                    max_port = int(input("Enter the maximum port number ({}-65535): ".format(min_port)))
                    if not (min_port <= max_port <= 65535):
                        raise ValueError()
                    break
                except ValueError:
                    print("Invalid input: please enter a valid maximum port number.")
            break
        except ValueError:
            print("Invalid input: please enter a valid minimum port number.")
    return (ip, min_port, max_port)

# This function creates a table containing all open port numbers and associated services and waits for the user to prompt
# the program to continue running.
def create_table ():
    if openPorts:
        port_table = {'Open Ports': [], 'Services': []}
        for port, status in openPorts.items():
            port_table['Open Ports'].append(port)
            port_table['Services'].append(status)
        port_df = pandas.DataFrame(port_table)
        print('-' * 42)
        print(center_tables.center_table(port_df,42))
        print('-' * 42)
        # Pause for input so the user can read prior results
        input('Press Enter to continue...')
        print('-' * 42)
            
    # Displays None if there are no open ports
    else:
        port_table = {'Open Ports': ['None'], 'Services': ['None']}
        port_df = pandas.DataFrame(port_table)
        print('-' * 42)
        print(center_tables.center_table(port_df,42))
        print('-' * 42)
        # Pause for input so the user can read prior results
        input('Press Enter to continue...')
        print('-' * 42)

def sudoLoad():     # For fun #1!
    print('-' * 42)
    print(f"Pseudo Load Time Initiated...")
    print('-' * 42)
    time.sleep(3)

def sudoSleep():    # For fun #2!
    print('-' * 42)
    print('Creating open ports and services table...')
    time.sleep(1.5)

# Required global variables for user input
ip = ''
min_port = 0
max_port = 0

print('-' * 42)
print('The #1 Pro Recommended Port Scanner'.center(42))    # Main Program Starts Here
print('-' * 42)

# Create a menu dictionary with options for the user to choose from
menu = {'Input': ['1','2','3','Q'], 'Scanner Options': ['Specific Ports', 'Port Range', 'UDP Probe', 'Quit']}
the_pretties = pandas.DataFrame(menu)

# Prompt the user to specify whether they want to check a port range or specific ports
while True:
    print(center_tables.center_table(menu,42))
    port_input = input('Please input an option: ')
    if port_input == '4' or port_input.lower() == 'q':
        break

    elif port_input == '3':
        sudoLoad()
        # Display note regarding security around UDP probes
        udpNote = 'Note: Most firewalls will block the UDP probes that this utility uses. This program will never disable nor alter any of your security configurations.  If you want to run the UDP Probe, you could create a firewall rule allowing inbound UDP packets for this program.'
        # Format the string to fit in line with the program
        udpNote = textwrap.wrap(udpNote, width=42)
        for words in udpNote:
            print(words)
        print('-' * 42)
        # Prompt the user to enter the IP address, minimum port number, and maximum port number
        ip, min_port, max_port = user_range_input(ip, min_port, max_port)
        # Call the checkPortsSocket function with the specified IP address and port range
        openPorts = port_scanner_udp.checkUdpPortSocket(ip, min_port, max_port)
        sudoSleep()
        create_table()
            
    elif port_input == '2':
        # Let the user know what is about to happen
        sudoLoad()
        # Prompt the user to enter the IP address, minimum port number, and maximum port number
        ip, min_port, max_port = user_range_input(ip, min_port, max_port)        
        # Call the checkPortsSocket function with the specified IP address and port range
        openPorts = port_scanner_range.checkPortsSocket(ip, min_port, max_port)
        sudoSleep()
        create_table()

    elif port_input == '1':
        # Let the user know what is about to happen
        sudoLoad()
        # Prompt the user to enter the IP address and a list of specific ports to scan
        while True:
            try:
                ip = input("Enter the target IP address: ")
                ipaddress.IPv4Address(ip)
                break
            except ipaddress.AddressValueError:
                print("Invalid IP address. Please enter a valid IPv4 address.")
        while True:
            portListTest = re.compile(r'^(?:[1-9]\d{0,3}|[1-5][0-9]{0,4}|6[0-4][0-9]{0,3}|65[0-4][0-9]{0,2}|655[0-2][0-9]?|6553[0-5]?)(?:,\s?(?:[1-9]\d{0,3}|[1-5][0-9]{0,4}|6[0-4][0-9]{0,3}|65[0-4][0-9]{0,2}|655[0-2][0-9]?|6553[0-5]?))*$')
            ports_str = input("Enter a comma-separated list of ports to scan: ")
            if portListTest.match(ports_str):
                break
            else: print('Invalid input. You must use valid port numbers (1-65535) where each value is separated by a comma(,).')
        # Parse the list of ports as integers
        ports = [int(port) for port in ports_str.split(",")]

        # Call the checkPortsSocket function with the specified IP address and list of ports
        openPorts = port_scanner_list.checkPortsSocket(ip, ports)
        sudoSleep()
        create_table()

    # Re-prompt the user for valid menu choices
    else:
        oops = "Invalid input. Please enter: '1' for specific ports, '2' for port range, '3' to probe udp services, or 'Q' to quit."
        oops = textwrap.wrap(oops, width=42)
        print('-' * 42)
        for oop in oops:
            print(oop)
        print('-' * 42)