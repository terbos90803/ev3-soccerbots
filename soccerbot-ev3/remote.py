import subprocess
import bluetooth
import socket
from Screen import debug_print


size = 1024 # size of receive buffer
_backlog = 1

# port numbers are arbitrary, but must match between server and client
_tcp_port = 32390
_ad_port = 32391
_bt_port = 3


# Check to see if the robot is connected to an IP network
_hostname = socket.gethostname()
host_address = socket.gethostbyname(_hostname)
debug_print('name:', _hostname)
debug_print('IP:', host_address)
# if the top octet of the IP address is 127, there is no active IP connection
_top_octet = host_address.split('.')[0].strip()
_use_tcp = _top_octet != '127' and _top_octet != '169'

if _use_tcp:
    _ad_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

    # Enable port reusage so we will be able to run multiple clients and servers on single (host, port).
    # Do not use socket.SO_REUSEADDR except you using linux(kernel<3.9): goto https://stackoverflow.com/questions/14388706/how-do-so-reuseaddr-and-so-reuseport-differ for more information.
    # For linux hosts all sockets that want to share the same address and port combination must belong to processes that share the same effective user ID!
    # So, on linux(kernel>=3.9) you have to run multiple servers and clients under one user to share the same (host, port).
    # Thanks to @stevenreddie
    _ad_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

    # Enable broadcasting mode
    _ad_server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    # Set a timeout so the socket does not block
    # indefinitely when trying to receive data.
    _ad_server.settimeout(0.2)
    _b_hostname = _hostname.encode('utf-8')


# Get a socket for accepting connections from the server
# returns: listener socket, robot's address (either IPv4 or BT-Mac)
def get_listener_socket():
    global host_address
    if _use_tcp:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('0.0.0.0', _tcp_port))
    else:
        # Fetch BT MAC address
        cmd = "hciconfig"
        device_id = "hci0"
        sp_result = subprocess.run(cmd, stdout=subprocess.PIPE, universal_newlines=True)
        host_address = sp_result.stdout.split("{}:".format(device_id))[1].split("BD Address: ")[1].split(" ")[0].strip()
        debug_print ('BT Mac:', host_address)

        s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        s.bind((host_address, _bt_port))

    s.listen(_backlog)

    return s, host_address


# Advertise the name and address of this robot
def advertise():
    if _use_tcp:
        _ad_server.sendto(_b_hostname, ("<broadcast>", _ad_port))
