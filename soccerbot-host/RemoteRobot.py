import bluetooth
import pickle
from Command import Command


class RemoteRobot:
    def __init__(self, robot_mac_addr):
        self.robot_mac_addr = robot_mac_addr
        self.port = 3
        self.s = None

    def connect(self):
        try:
            self.s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            self.s.connect((self.robot_mac_addr, self.port))
            print('Connected to robot', self.robot_mac_addr)
        except OSError:
            self.s = None
            print('Failed to open BT connection to', self.robot_mac_addr)

    def is_connected(self):
        return self.s is not None

    def close(self):
        if self.s is not None:
            self.send_command(0, 0, 0)
            self.s.close()
            self.s = None

    def send_command(self, left_stick, right_stick, pressed):
        if self.s is not None:
            data = pickle.dumps(Command(left_stick, right_stick, pressed))
            try:
                self.s.send(data)
            except OSError:
                self.s = None
                print('Robot disconnected', self.robot_mac_addr)

    @staticmethod
    def deadzone(val):
        return val if abs(val) > 3 else 0

    def use_joystick(self, joystick):
        left_stick = self.deadzone(joystick.get_axis(1) * -100)
        right_stick = self.deadzone(joystick.get_axis(3) * -100)

        hat = joystick.get_hat(0)
        if hat[0] != 0 or hat[1] != 0:
            left_stick = (hat[1] + hat[0]) * 50
            right_stick = (hat[1] - hat[0]) * 50

        buttons = joystick.get_numbuttons()
        pressed = 0
        for i in range(buttons):
            pressed += joystick.get_button(i)

        self.send_command(left_stick, right_stick, pressed)
