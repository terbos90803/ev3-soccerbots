import bluetooth
import threading
from Command import Command


_bt_port = 3

class RemoteRobot:
    def __init__(self, robot_mac_addr):
        self.robot_mac_addr = robot_mac_addr
        self._lock = threading.Lock()
        self.s = None
        self.connected = False

    def connect(self):
        if not self.s:
            with self._lock:
                if not self.s:
                    try:
                        self.s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
                        self.s.connect((self.robot_mac_addr, _bt_port))
                        print('Connected to robot', self.robot_mac_addr)
                        self.connected = True
                    except OSError as err:
                        self.s = None
                        self.connected = False
                        print(f'Failed to open BT connection to {self.robot_mac_addr}: {repr(err)}')

    def is_connected(self):
        return self.connected

    def close(self):
        with self._lock:
            if self.connected:
                self._send_command(Command(0, 0, 0))
            if self.s is not None:
                self.s.close()
            self.s = None
            self.connected = False

    def send_command(self, command):
        if self.connected:
            with self._lock:
                self._send_command(command)

    # Unsafe send_command.  Must lock before calling.
    def _send_command(self, command):
        if self.connected and self.s is not None:
            data = command.get_pickled()
            try:
                self.s.send(data)
            except OSError:
                self.s = None
                print('Robot disconnected', self.robot_mac_addr)

