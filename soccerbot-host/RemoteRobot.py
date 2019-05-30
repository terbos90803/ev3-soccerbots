import bluetooth
import pickle


class RemoteRobot:
    def __init__(self, robot_mac_addr):
        self.robot_mac_addr = robot_mac_addr
        self.port = 3
        self.s = 0

    def connect(self):
        self.s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.s.connect((self.robot_mac_addr, self.port))

    def send_command(self, command):
        data = pickle.dumps(command)
        self.s.send(data)
