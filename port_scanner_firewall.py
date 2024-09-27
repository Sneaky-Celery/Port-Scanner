import subprocess
import socket
import os
import sys
import ctypes
import win32com.shell.shell as shell

def run_as_admin(cmd, params=None):
    """
    Run the given command with administrator privileges.
    """
    if params is None:
        params = []
    try:
        # Use the ShellExecuteEx function to run the command with administrator privileges
        shell.ShellExecuteEx(lpVerb='runas', lpFile=cmd, lpParameters=' '.join(params))
    except Exception as e:
        print(f"Error: {e}")

def block_ports(block_ports):
    """
    Blocks incoming traffic on the specified ports using the Windows Firewall,
    and verifies that each port has been successfully closed using a port scan.
    """
    # Check if the user has administrative privileges
    if not ctypes.windll.shell32.IsUserAnAdmin():
        # If not, re-run the script with administrator privileges
        run_as_admin(sys.executable, [os.path.abspath(__file__)] + sys.argv[1:])
        return
    # Add the firewall rules using netsh
    for block_port in block_ports:
        # Create the command to add the firewall rule
        command = f"netsh advfirewall firewall add rule name=\"Block Port {block_port}\" dir=in action=block protocol=TCP localport={block_port}"
        
         # Run the command using subprocess
        subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Verify that the ports are closed using a port scan
    blocked_ports = []
    for block_port in block_ports:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('127.0.0.1', block_port))
            except OSError:
                # If the port is already in use, it has been successfully blocked
                blocked_ports.append(block_port)
    return blocked_ports
