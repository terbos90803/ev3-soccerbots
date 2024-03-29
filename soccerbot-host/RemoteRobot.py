import bluetooth
import pickle
from Command import Command


_bt_port = 3

class RemoteRobot:
    def __init__(self, robot_mac_addr):
        self.robot_mac_addr = robot_mac_addr
        self.s = None

    def connect(self):
        if not self.s:
            try:
                self.s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
                self.s.connect((self.robot_mac_addr, _bt_port))
                print('Connected to robot', self.robot_mac_addr)
            except OSError as err:
                self.s = None
                print(f'Failed to open BT connection to {self.robot_mac_addr}: {repr(err)}')

    def is_connected(self):
        return self.s is not None

    def close(self):
        if self.s is not None:
            self.send_command(Command(0, 0, 0))
            if self.s is not None:
                self.s.close()
            self.s = None

    def send_command(self, command):
        if self.s is not None:
            data = pickle.dumps(command, protocol=4)
            try:
                self.s.send(data)
            except OSError:
                self.s = None
                print('Robot disconnected', self.robot_mac_addr)

